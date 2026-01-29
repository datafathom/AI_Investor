import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class COISCalculator:
    """
    Calculates the Conflict of Interest Score (COIS).
    Factors:
    - Commission Revenue (40%)
    - Product Kickbacks (30%)
    - Trading Volume (15%)
    - Fee Transparency (15%)
    """
    
    def calculate_score(self, data: Dict[str, Any]) -> float:
        """Calculates a score from 0 to 100, where 0 is high conflict."""
        comm_rev_pct = data.get("commission_revenue_pct", 0.0) # 0.0 to 1.0 (higher is worse)
        kickback_pct = data.get("kickback_revenue_pct", 0.0)
        trading_vol_excess = data.get("trading_volume_excess", 0.0) # 0.0 to 1.0
        fee_transparency = data.get("fee_transparency_score", 1.0) # 0.0 to 1.0 (higher is better)

        # Higher weight on revenue factors
        comm_penalty = comm_rev_pct * 40
        kickback_penalty = kickback_pct * 30
        vol_penalty = trading_vol_excess * 15
        transparency_bonus = fee_transparency * 15

        base_score = 85 - (comm_penalty + kickback_penalty + vol_penalty)
        final_score = base_score + transparency_bonus

        score = max(0, min(100, final_score))
        logger.info(f"COIS_LOG: Calculated COIS={score} for advisor_id={data.get('advisor_id')}")
        return round(score, 2)
