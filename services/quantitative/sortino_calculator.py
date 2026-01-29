import logging
import numpy as np
from typing import List

logger = logging.getLogger(__name__)

class SortinoCalculator:
    """
    Calculates the Sortino Ratio: (Rp - Rf) / DownsideDeviation.
    Only penalizes volatility below a target return (usually 0).
    """
    
    def calculate_downside_deviation(self, returns: List[float], target: float = 0.0) -> float:
        """
        Returns annualized downside deviation.
        Matches the logic implemented in VolatilityAnalyzer.
        """
        downside_returns = [min(0, r - target) for r in returns]
        if not returns: return 0.0
        
        sum_sq = sum(r**2 for r in downside_returns)
        dev = np.sqrt(sum_sq / len(returns)) * np.sqrt(252)
        return float(dev)

    def calculate_sortino(self, returns: List[float], risk_free_rate: float, target: float = 0.0) -> float:
        if len(returns) < 2: return 0.0
        
        # Annualized Mean Return
        mean_ret = np.mean(returns) * 252
        
        # Downside Deviation
        downside_dev = self.calculate_downside_deviation(returns, target)
        
        if downside_dev == 0:
            # If no downside, Sortino is technically infinite/high. 
            # Industry practice often caps or returns high value.
            return 99.9 if mean_ret > risk_free_rate else 0.0
            
        sortino = (mean_ret - risk_free_rate) / downside_dev
        
        logger.info(f"QUANT_LOG: Sortino Calculated: {sortino:.4f}")
        return round(float(sortino), 4)
