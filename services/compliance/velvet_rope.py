import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class VelvetRopeGate:
    """
    Phase 173.2: Retail 'Velvet Rope' Blocking Service.
    Enforces access thresholds for top-tier private deals.
    """
    
    def can_access_deal(self, client_tier: str, deal_min_tier: str = "TIER_2_UHNW") -> bool:
        """
        Policy: Only TIER_1 and TIER_2 (Qualified Purchasers) can see institutional deals.
        """
        tier_map = {"TIER_1_SFO": 1, "TIER_2_UHNW": 2, "TIER_3_RETAIL": 3}
        
        client_rank = tier_map.get(client_tier, 99)
        deal_rank = tier_map.get(deal_min_tier, 1)
        
        is_allowed = client_rank <= deal_rank
        
        if not is_allowed:
            logger.warning(f"COMPLIANCE_LOG: Access DENIED to deal (Min: {deal_min_tier}, Client: {client_tier})")
            
        return is_allowed
