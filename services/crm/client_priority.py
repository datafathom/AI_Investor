import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PriorityScorer:
    """
    Phase 173.1: Priority Scorer.
    Determines client tier and allocation priority based on AUM and strategic value.
    """
    
    def calculate_priority(self, aum: float, is_sfo: bool) -> Dict[str, Any]:
        """
        Policy: 
        - SFOs ($50M+) = TIER_1_SFO (Priority 1)
        - UHNW ($5M+) = TIER_2_UHNW (Priority 2)
        - Others = TIER_3_RETAIL (Priority 3)
        """
        if is_sfo or aum >= 50_000_000:
            tier = "TIER_1_SFO"
            priority = 1
        elif aum >= 5_000_000:
            tier = "TIER_2_UHNW"
            priority = 2
        else:
            tier = "TIER_3_RETAIL"
            priority = 3
            
        logger.info(f"CRM_LOG: Client priority determined: {tier} (Priority {priority})")
        
        return {
            "tier": tier,
            "priority": priority,
            "is_qualified_purchaser": aum >= 5_000_000
        }
