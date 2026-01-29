import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class EqualWeightRebalancer:
    """Calculates alternate portfolio weights using an equal-weighted strategy."""
    
    def calculate_equal_weights(self, tickers: List[str]) -> List[Dict[str, Any]]:
        if not tickers: return []
        
        target_weight = 1.0 / len(tickers)
        logger.info(f"PORTFOLIO_LOG: Equal weighting {len(tickers)} assets at {target_weight:.2%}")
        
        return [{"ticker": t, "target_weight": round(target_weight, 6)} for t in tickers]

    def estimate_drift(self, current_holdings: List[Dict[str, Any]]) -> float:
        """Sum of absolute differences between current and equal weights."""
        if not current_holdings: return 0.0
        
        equal_w = 1.0 / len(current_holdings)
        drift = sum(abs(h.get("weight", 0) - equal_w) for h in current_holdings)
        return round(float(drift), 4)
