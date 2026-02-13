"""
Rogue Agent Kill Switch.
Automatically disables swarms showing outlier behavior.
"""
import logging
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class RogueKiller:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RogueKiller, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.kill_history: List[Dict] = []
        self._generate_mock_history()
        self._initialized = True
        
    def _generate_mock_history(self):
        """Generate some mock kill events for the UI."""
        reasons = ["TPM Surge > 200", "Memory Leap", "Recursive Loop", "Unauthorized Access"]
        agents = ["AGENT-007", "AGENT-042", "AGENT-013", "AGENT-099"]
        
        for _ in range(3):
            self.kill_history.append({
                "timestamp": datetime.now().isoformat(),
                "agent_id": random.choice(agents),
                "reason": random.choice(reasons),
                "initiated_by": "SYSTEM"
            })

    def monitor_agent(self, agent_id: str, current_tpm: int) -> Dict:
        MAX_TRADES_PER_MIN = 100
        if current_tpm > MAX_TRADES_PER_MIN:
            kill_event = {
                "timestamp": datetime.now().isoformat(),
                "agent_id": agent_id,
                "reason": f"TPM Surge: {current_tpm}",
                "initiated_by": "SYSTEM"
            }
            self.kill_history.insert(0, kill_event)
            logger.critical(f"ROGUE_AGENT_DETECTED: {agent_id} at {current_tpm} TPM. KILLING PROCESS.")
            return {"action": "KILL", "reason": "Trade rate anomaly"}
        return {"action": "MONITOR"}

    def kill_agent(self, agent_id: str, reason: str = "Manual Override") -> Dict:
        """Manually kill an agent."""
        kill_event = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "reason": reason,
            "initiated_by": "USER"
        }
        self.kill_history.insert(0, kill_event)
        return {"success": True, "message": f"Agent {agent_id} terminated."}

    def get_history(self) -> List[Dict]:
        return self.kill_history
