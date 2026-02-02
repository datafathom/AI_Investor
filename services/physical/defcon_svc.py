import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DefconService:
    """
    Phase 202.4: Threat Level Defcon Aggregator.
    Aggregates signals from CCTV, Drone, and Access sensors to determine the Defcon level.
    """

    def __init__(self):
        self.current_level = 5 # 5 = Normal, 1 = Critical
        self.active_threats = []

    def assess_threat_level(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates the Defcon level based on incoming signals.
        """
        new_threats = []
        level = 5
        
        for signal in signals:
            if signal.get("type") == "INTRUSION":
                level = min(level, 2)
                new_threats.append(signal)
            elif signal.get("type") == "FAILED_ACCESS":
                level = min(level, 3)
                new_threats.append(signal)
            elif signal.get("type") == "CYBER_ATTACK":
                level = min(level, 1) # Max Alert
                new_threats.append(signal)
                
        self.current_level = level
        self.active_threats = new_threats
        
        status_map = {
            5: "GREEN (Normal)",
            4: "BLUE (Guarded)",
            3: "YELLOW (Elevated)",
            2: "ORANGE (High)",
            1: "RED (Severe)"
        }
        
        return {
            "defcon": self.current_level,
            "status": status_map.get(self.current_level, "UNKNOWN"),
            "threats": len(self.active_threats),
            "lockdown_active": self.current_level <= 2
        }
