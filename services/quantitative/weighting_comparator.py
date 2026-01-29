import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class WeightingComparator:
    """Compares returns of equal-weighted vs market-cap weighted indexes."""
    
    def compare_performance(self, cap_weighted_rets: List[float], equal_weighted_rets: List[float]) -> Dict[str, Any]:
        if not cap_weighted_rets or not equal_weighted_rets: return {}
        
        total_cw = sum(cap_weighted_rets)
        total_ew = sum(equal_weighted_rets)
        
        spread = total_ew - total_cw
        
        logger.info(f"QUANT_LOG: Weighting Spread: {spread*100:.2f}% (EW - CW)")
        
        return {
            "cw_return": round(total_cw, 4),
            "ew_return": round(total_ew, 4),
            "spread": round(spread, 4),
            "market_breadth": "HEALTHY" if spread > 0 else "NARROW_LEADERSHIP"
        }
