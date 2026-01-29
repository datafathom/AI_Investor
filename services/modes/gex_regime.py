"""
Volatility Regime Setter.
Switches backend logic based on Gamma Exposure levels.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GEXRegimeSetter:
    """Sets system volatility regime."""
    
    def determine_regime(self, total_gex: float) -> str:
        if total_gex > 0:
            return "LOW_VOL_MEAN_REVERTING"
        elif total_gex < -1000000: # Threshold
            return "HIGH_VOL_CRASH_ACCELERATION"
        else:
            return "NEUTRAL_TRANSITION"
