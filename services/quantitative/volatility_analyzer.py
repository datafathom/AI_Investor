import logging
import numpy as np
from typing import List

logger = logging.getLogger(__name__)

class VolatilityAnalyzer:
    """Calculates various types of portfolio volatility (Standard and Downside)."""
    
    def calculate_standard_vol(self, returns: List[float], annualize: bool = True) -> float:
        if len(returns) < 2: return 0.0
        std = np.std(returns)
        if annualize:
            std *= np.sqrt(252)
        return float(std)

    def calculate_downside_deviation(self, returns: List[float], target: float = 0.0) -> float:
        """Denominator for Sortino Ratio (only penalizes returns below target)."""
        downside = [r for r in returns if r < target]
        if not downside: return 0.0
        
        # Calculate deviation relative to whole periods
        sum_sq = sum((r - target)**2 for r in downside)
        dev = np.sqrt(sum_sq / len(returns)) * np.sqrt(252)
        
        logger.info(f"QUANT_LOG: Downside Deviation: {dev:.4f}")
        return float(dev)
