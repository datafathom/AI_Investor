"""Agent heartbeat monitoring service."""
from typing import List, Dict, Optional
from datetime import timezone, datetime, timedelta
from enum import Enum
import asyncio
import logging

class AgentStatus(Enum):
    ALIVE = "alive"
    DEAD = "dead"
    STARTING = "starting"
    STOPPING = "stopping"

class HeartbeatService:
    """Tracks agent heartbeats via Kafka topic 'agent-heartbeat'."""
    
    HEARTBEAT_TIMEOUT_SECONDS = 5
    
    def __init__(self):
        self._heartbeats: Dict[str, datetime] = {}
        self._statuses: Dict[str, AgentStatus] = {}
        self.logger = logging.getLogger("HeartbeatService")

    async def record_heartbeat(self, agent_id: str, status_str: str = "alive") -> None:
        """Record heartbeat from agent."""
        try:
            status = AgentStatus(status_str.lower())
        except ValueError:
            status = AgentStatus.ALIVE
            
        self._heartbeats[agent_id] = datetime.now(timezone.utc)
        self._statuses[agent_id] = status
        # self.logger.debug(f"Heartbeat: {agent_id} -> {status}")

    def is_agent_alive(self, agent_id: str) -> bool:
        """Check if agent heartbeat is within threshold."""
        last = self._heartbeats.get(agent_id)
        if not last:
            return False
            
        # If explicitly marked as dead or stopping
        if self._statuses.get(agent_id) in [AgentStatus.DEAD, AgentStatus.STOPPING]:
            return False
            
        return datetime.now(timezone.utc) - last < timedelta(seconds=self.HEARTBEAT_TIMEOUT_SECONDS)

    async def get_all_agents(self) -> List[Dict]:
        """Get status of all registered agents."""
        agents = []
        now = datetime.now(timezone.utc)
        
        # Snapshot keys to avoid runtime modification issues
        for agent_id, last_beat in list(self._heartbeats.items()):
            time_diff = (now - last_beat).total_seconds()
            is_alive = self.is_agent_alive(agent_id)
            
            # Auto-mark as dead if timeout
            if time_diff > self.HEARTBEAT_TIMEOUT_SECONDS:
                self._statuses[agent_id] = AgentStatus.DEAD
                is_alive = False
                
            agents.append({
                "agent_id": agent_id,
                "status": self._statuses.get(agent_id, AgentStatus.DEAD).value,
                "is_alive": is_alive,
                "last_heartbeat": last_beat.isoformat(),
                "latency_ms": int(time_diff * 1000)
            })
        return agents

# Global Singleton
heartbeat_service = HeartbeatService()
