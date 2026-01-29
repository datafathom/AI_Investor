import logging
from typing import Dict, Any
from uuid import UUID

logger = logging.getLogger(__name__)

class PrivateBankingQualifier:
    """Qualifies clients for private banking tiers based on net worth."""
    
    TIERS = {
        "PRIVATE": 10000000,        # $10M
        "ULTRA": 50000000,          # $50M
        "FAMILY_OFFICE": 100000000  # $100M
    }

    def qualify_client(self, user_id: UUID, net_worth: float) -> Dict[str, Any]:
        tier = "NONE"
        if net_worth >= self.TIERS["FAMILY_OFFICE"]:
            tier = "FAMILY_OFFICE"
        elif net_worth >= self.TIERS["ULTRA"]:
            tier = "ULTRA"
        elif net_worth >= self.TIERS["PRIVATE"]:
            tier = "PRIVATE"
            
        is_qualified = tier != "NONE"
        
        logger.info(f"PB_LOG: User {user_id} qualified for {tier} (NW: ${net_worth:,.2f})")
        
        return {
            "user_id": user_id,
            "qualified": is_qualified,
            "tier": tier,
            "minimum_nw_required": self.TIERS["PRIVATE"] if not is_qualified else 0
        }
