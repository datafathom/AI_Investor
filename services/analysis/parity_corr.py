"""
Correlation Adjuster.
Adjusts risk parity weights based on cross-asset correlation.
"""
import logging
import numpy as np
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CorrelationAdjuster:
    """Adjusts leverage based on correlation regime."""
    
    def adjust_leverage(self, corr_matrix: np.ndarray, base_leverage: float) -> float:
        # If correlation median is high (risk diversification fails), reduce leverage
        median_corr = np.median(corr_matrix)
        if median_corr > 0.6:
            return base_leverage * 0.5
        return base_leverage
