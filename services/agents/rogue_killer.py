"""
Rogue Agent Kill Switch.
Automatically disables swarms showing outlier behavior.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RogueKiller:
    """Detects and stops rogue agents."""
    
    MAX_TRADES_PER_MIN = 100
    
    def monitor_agent(self, agent_id: str, current_tpm: int):
        if current_tpm > self.MAX_TRADES_PER_MIN:
            logger.critical(f"ROGUE_AGENT_DETECTED: {agent_id} at {current_tpm} TPM. KILLING PROCESS.")
            return {"action": "KILL", "reason": "Trade rate anomaly"}
        return {"action": "MONITOR"}
