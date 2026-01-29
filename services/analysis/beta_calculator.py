"""
Beta Exposure Calculator.
Calculates portfolio beta relative to benchmark.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class BetaCalculator:
    """Calculates portfolio beta exposure."""
    
    def calculate_portfolio_beta(self, holdings: List[Dict[str, Any]]) -> float:
        total_value = sum(h["value"] for h in holdings)
        if total_value == 0:
            return 0.0
            
        weighted_beta = 0
        for h in holdings:
            weight = h["value"] / total_value
            beta = h.get("beta", 1.0) # Default to 1.0 if unknown
            weighted_beta += weight * beta
            
        logger.info(f"PORTFOLIO_BETA: {weighted_beta:.2f}")
        return weighted_beta
