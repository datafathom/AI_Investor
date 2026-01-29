import logging
import numpy as np
from typing import List

logger = logging.getLogger(__name__)

class InflationHedgeScorer:
    """Calculates sensitivity of assets to inflation (Inflation Beta)."""
    
    def calculate_inflation_beta(self, asset_returns: List[float], inflation_changes: List[float]) -> float:
        """
        Calculates the regression coefficient of asset returns against inflation changes.
        """
        if len(asset_returns) != len(inflation_changes) or len(asset_returns) < 2:
            return 0.0
            
        # Linear regression: return = alpha + beta * inflation_change
        beta = np.polyfit(inflation_changes, asset_returns, 1)[0]
        
        logger.info(f"QUANT_LOG: Inflation Beta: {beta:.4f}")
        return round(float(beta), 4)

    def score_effectiveness(self, beta: float) -> str:
        if beta > 1.0: return "SUPER_HEDGER"
        if beta > 0.5: return "STRONG_HEDGER"
        if beta > 0.0: return "WEAK_HEDGER"
        return "VULNERABLE"
