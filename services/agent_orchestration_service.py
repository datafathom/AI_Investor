import json
import os
import logging
import asyncio
import hashlib
from typing import Dict, Any, List, Optional

import redis.asyncio as redis

from agents.department_agent import DepartmentAgent
from services.infrastructure.event_bus import EventBusService
from services.risk.circuit_breaker import get_circuit_breaker
from config.environment_manager import get_settings
from web.socket_gateway import broadcaster

logger = logging.getLogger(__name__)

class AgentOrchestrationService:
    """
    Singleton service to manage the lifecycle of 108 specialized agents.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AgentOrchestrationService, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        
        self.settings = get_settings()
        self.definitions_path = os.path.join("config", "agent_definitions.json")
        self.agents: Dict[str, DepartmentAgent] = {}
        self.definitions: List[Dict[str, Any]] = []
        self.event_bus = EventBusService()
        self.circuit_breaker = get_circuit_breaker()
        self.broadcaster = broadcaster
        self.semaphore = asyncio.Semaphore(10)  # Cap LLM concurrency
        
        # Redis Caching (L2)
        self.redis: Optional[redis.Redis] = None
        self.cache_enabled = False
        self._init_redis()
        
        # In-Memory Cache (L1)
        self.local_cache: Dict[str, Dict[str, Any]] = {}  # key -> {"result": dict, "expiry": timestamp}
        
        self._load_definitions()
        logger.info("AgentOrchestrationService initialized (Concurrency Limit: 10)")

    def _init_redis(self) -> None:
        """Initialize Redis connection for caching."""
        try:
            self.redis = redis.from_url(
                self.settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=1.0,
                socket_timeout=1.0
            )
            self.cache_enabled = True
            logger.info(f"Agent Cache (Redis) initialized: {self.settings.REDIS_URL}")
        except Exception as e:
            self.cache_enabled = False
            logger.warning(f"Agent Cache fallback: Redis is offline. L2 Caching disabled. Error: {e}")

    def _load_definitions(self) -> None:
        """Load agent definitions from JSON config."""
        try:
            if os.path.exists(self.definitions_path):
                with open(self.definitions_path, "r") as f:
                    self.definitions = json.load(f)
                logger.info(f"Loaded {len(self.definitions)} agent definitions")
            else:
                logger.error(f"Agent definitions file not found at {self.definitions_path}")
        except Exception as e:
            logger.error(f"Error loading agent definitions: {e}")

    def _get_cache_key(self, agent_id: str, payload: Dict[str, Any]) -> str:
        """Generate a stable cache key from agent_id and payload."""
        payload_str = json.dumps(payload, sort_keys=True)
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        return f"agent_cache:{agent_id}:{payload_hash}"

    def get_agent(self, agent_id: str) -> Optional[DepartmentAgent]:
        """Lazy-load and return an agent instance."""
        if agent_id in self.agents:
            return self.agents[agent_id]
        
        # Find definition
        defn = next((d for d in self.definitions if d["id"] == agent_id), None)
        if not defn:
            logger.error(f"No definition found for agent: {agent_id}")
            return None
            
        # Create instance
        agent = DepartmentAgent(
            name=defn["id"],
            dept_id=defn["dept_id"],
            role=defn["role"]
        )
        self.agents[agent_id] = agent
        agent.start()
        return agent

    async def invoke_agent(self, agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a specific agent with a payload.
        Wrapped in circuit breaker logic, L1 (Memory) and L2 (Redis) caching.
        """
        import time

        if self.circuit_breaker.is_halted():
            return {"error": "System Halted", "reason": self.circuit_breaker.freeze_reason}
            
        cache_key = self._get_cache_key(agent_id, payload)
        
        # 1. Check L1 Cache (In-Memory)
        if cache_key in self.local_cache:
            entry = self.local_cache[cache_key]
            if entry["expiry"] > time.time():
                logger.info(f"L1 Cache HIT for agent {agent_id}")
                return entry["result"]
            else:
                del self.local_cache[cache_key]

        # 2. Check L2 Cache (Redis)
        if self.cache_enabled:
            try:
                cached_val = await self.redis.get(cache_key)
                if cached_val:
                    logger.info(f"L2 Cache HIT for agent {agent_id}")
                    result = json.loads(cached_val)
                    # Backfill L1
                    self.local_cache[cache_key] = {"result": result, "expiry": time.time() + 300}
                    return result
            except Exception as e:
                logger.warning(f"Cache read error: {e}")

        agent = self.get_agent(agent_id)
        if not agent:
            return {"error": "Agent Not Found", "agent_id": agent_id}
            
        async with self.semaphore:
            logger.info(f"Invoking agent {agent_id} (Cache MISS)")
            
            # Broadcast BUSY status
            await self.broadcaster.broadcast_agent_status(agent_id, "BUSY", True)
            
            try:
                # Real invocation
                result = await agent.invoke(payload)
                
                # 3. Store in Caches (if success)
                if result.get("status") == "success":
                    expiry = time.time() + 300
                    # Store in L1
                    self.local_cache[cache_key] = {"result": result, "expiry": expiry}
                    
                    # Store in L2 (Redis)
                    if self.cache_enabled:
                        try:
                            await self.redis.setex(cache_key, 300, json.dumps(result))
                        except Exception as e:
                            logger.warning(f"Cache write error: {e}")

                # Broadcast SUCCESS status
                await self.broadcaster.broadcast_agent_status(agent_id, "SUCCESS", False, details=result)
                return result
                
            except Exception as e:
                logger.exception(f"Error invoking agent {agent_id}: {e}")
                # Broadcast ERROR status
                await self.broadcaster.broadcast_agent_status(agent_id, "ERROR", False, details={"error": str(e)})
                return {"error": str(e), "agent_id": agent_id}

    def broadcast_to_department(self, dept_id: int, event: Dict[str, Any]) -> None:
        """Broadcast an event to all agents in a department."""
        self.event_bus.publish(f"dept.{dept_id}.events", event)
        logger.info(f"Broadcasted to Dept {dept_id}: {event.get('type')}")

    def broadcast_event(self, event: Dict[str, Any]):
        """Broadcast event to all interested agents."""
        # implementation...
        pass

    def get_all_agents_status(self) -> List[Dict[str, Any]]:
        """Return status for all currently active agents."""
        return [agent.health_check() for agent in self.agents.values()]

def get_orchestration_service() -> AgentOrchestrationService:
    """Helper to get the singleton service."""
    return AgentOrchestrationService()
