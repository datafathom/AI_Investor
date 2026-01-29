import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RollingCorrelationEngine:
    """Calculates rolling correlation coefficients across multiple periods."""
    
    def calculate_correlation(self, returns_a: List[float], returns_b: List[float]) -> float:
        """
        Calculates Pearson correlation between two series.
        """
        if len(returns_a) != len(returns_b) or len(returns_a) < 2:
            return 0.0
            
        corr = np.corrcoef(returns_a, returns_b)[0, 1]
        
        logger.debug(f"QUANT_LOG: Calculated correlation: {corr:.4f}")
        return round(float(corr), 4)

    def identify_crisis_spike(self, prev_corr: float, curr_corr: float) -> bool:
        """Detects if correlation is approaching 1.0 (Integration failure during crisis)."""
        is_spike = curr_corr > 0.85 and (curr_corr - prev_corr) > 0.3
        if is_spike:
            logger.warning(f"MARKET_ALERT: Correlation spike detected! {prev_corr} -> {curr_corr}")
        return is_spike
