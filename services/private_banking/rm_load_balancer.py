import logging
from typing import List, Dict, Any, Optional
from uuid import UUID

logger = logging.getLogger(__name__)

class RMLoadBalancer:
    """Balances client assignments to Relationship Managers."""
    
    def __init__(self):
        # Mock capacity data
        self.rm_capacity = {} # {rm_id: current_count}

    def assign_next_available_rm(self, client_tier: str, managers: List[Dict[str, Any]]) -> Optional[UUID]:
        max_limit = 50 if client_tier == "ULTRA" else 100
        
        # Sort by current load
        sorted_rms = sorted(managers, key=lambda m: m["current_count"])
        
        for rm in sorted_rms:
            if rm["current_count"] < max_limit:
                logger.info(f"RM_LOG: Assigned client to RM {rm['id']} (Current count: {rm['current_count']})")
                return rm["id"]
                
        logger.error("RM_LOG: All suitable relationship managers are at capacity!")
        return None
