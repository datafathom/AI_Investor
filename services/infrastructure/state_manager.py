import os
import redis
import json
import logging
from typing import Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class AgentState(Enum):
    INIT = "INIT"
    SCANNING = "SCANNING"
    ANALYZING = "ANALYZING"
    EXECUTING = "EXECUTING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    SECURITY_HALT = "SECURITY_HALT"

class FSMManager:
    """
    Manages agent state transitions and persistence using Redis.
    """
    VALID_TRANSITIONS = {
        AgentState.INIT: [AgentState.SCANNING, AgentState.ANALYZING, AgentState.SECURITY_HALT],
        AgentState.SCANNING: [AgentState.ANALYZING, AgentState.ERROR, AgentState.SECURITY_HALT],
        AgentState.ANALYZING: [AgentState.EXECUTING, AgentState.ERROR, AgentState.SECURITY_HALT],
        AgentState.EXECUTING: [AgentState.VERIFYING, AgentState.ERROR, AgentState.SECURITY_HALT],
        AgentState.VERIFYING: [AgentState.COMPLETED, AgentState.ANALYZING, AgentState.ERROR, AgentState.SECURITY_HALT],
        AgentState.COMPLETED: [AgentState.INIT, AgentState.ANALYZING],
        AgentState.ERROR: [AgentState.INIT, AgentState.ANALYZING, AgentState.SECURITY_HALT],
        AgentState.SECURITY_HALT: [] # Terminal state for safety
    }

    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD", "84zMsasS0WfXGGVFU6t7vLd9"),
            decode_responses=True
        )

    def validate_transition(self, old_state: AgentState, new_state: AgentState) -> bool:
        """Enforces deterministic state transitions."""
        allowed = self.VALID_TRANSITIONS.get(old_state, [])
        return new_state in allowed

    def save_state(self, agent_id: str, state: AgentState, context: Optional[Dict[str, Any]] = None) -> None:
        """Persists agent state and context to Redis."""
        key = f"agent_state:{agent_id}"
        data = {
            "state": state.value,
            "context": context or {},
            "updated_at": datetime.now().isoformat()
        }
        self.redis_client.set(key, json.dumps(data))
        logger.debug(f"Saved state for {agent_id}: {state.value}")

    def load_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Loads agent state from Redis."""
        key = f"agent_state:{agent_id}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

# Singleton
from datetime import datetime
fsm_manager = FSMManager()

def get_fsm_manager() -> FSMManager:
    return fsm_manager
