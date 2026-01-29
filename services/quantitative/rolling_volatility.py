import logging
import numpy as np
from typing import List

logger = logging.getLogger(__name__)

class RollingVolatilityEngine:
    """Calculates standard deviation across rolling windows."""
    
    def calculate_rolling_vol(self, returns: List[float], window: int = 21) -> List[float]:
        """
        Policy: Returns a list of annualized volatility values.
        Default 21 trading days (approx 1 month).
        """
        if len(returns) < window:
            return []
            
        results = []
        for i in range(len(returns) - window + 1):
            subset = returns[i : i + window]
            vol = np.std(subset) * np.sqrt(252)
            results.append(round(float(vol), 4))
            
        logger.info(f"QUANT_LOG: Calculated {len(results)} rolling vol points (Window: {window})")
        return results
