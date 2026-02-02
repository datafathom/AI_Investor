import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SecondaryMarketService:
    """
    Phase 172.5: Secondary Market Valuation Discount Estimator.
    Estimates the 'Haircut' needed for immediate liquidity in secondary markets.
    """
    
    def estimate_discount(self, asset_type: str, lock_remaining_months: int) -> Dict[str, Any]:
        """
        Base discount: 0.10.
        Adds 0.02 for every 12 months remaining.
        """
        base_discount = 0.10
        time_penalty = (lock_remaining_months / 12) * 0.02
        total_discount = base_discount + time_penalty
        
        logger.info(f"VALUATION_LOG: Estimated secondary discount for {asset_type}: {total_discount:.2%}")
        
        return {
            "asset_type": asset_type,
            "lock_months": lock_remaining_months,
            "estimated_discount_pct": round(total_discount * 100, 2),
            "secondary_nav": round(1.0 - total_discount, 4)
        }
