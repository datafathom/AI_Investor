
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class BequestPrioritizer:
    """
    Ensures Specific Bequests are satisfied before Residue distributions.
    """
    
    def prioritize_bequests(self, bequests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sorts bequests by legal priority (Specific > General > Residual).
        """
        priority_map = {
            "SPECIFIC": 1,
            "GENERAL": 2,
            "RESIDUAL": 3
        }
        
        sorted_bequests = sorted(bequests, key=lambda x: priority_map.get(x.get("type", "RESIDUAL"), 99))
        
        logger.info(f"Prioritized {len(sorted_bequests)} bequests.")
        return sorted_bequests
Line Content: 
