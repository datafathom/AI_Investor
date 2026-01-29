import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class CorrelationCalculator:
    """Calculates Pearson correlation between asset price series."""
    
    def calculate_pearson(self, series_a: List[float], series_b: List[float]) -> float:
        if len(series_a) != len(series_b) or len(series_a) < 2:
            return 0.0
            
        corr_matrix = np.corrcoef(series_a, series_b)
        correlation = corr_matrix[0, 1]
        
        logger.info(f"QUANT_LOG: Calculated correlation: {correlation:.4f}")
        return round(float(correlation), 4)

    def calculate_rolling_correlation(self, series_a: List[float], series_b: List[float], window: int = 20) -> List[float]:
        # rolling windows for breakdown detection
        correlations = []
        for i in range(window, len(series_a) + 1):
            correlations.append(self.calculate_pearson(series_a[i-window:i], series_b[i-window:i]))
        return correlations
