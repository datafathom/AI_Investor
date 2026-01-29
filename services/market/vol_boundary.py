"""
Volatility Boundary Monitor.
Checks if VIX/ATR exceeds safe limits.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class VolatilityBoundary:
    """Monitors volatility limits."""
    
    VIX_SHIELD_THRESHOLD = 40.0
    
    def check_boundaries(self, current_vix: float) -> str:
        if current_vix > self.VIX_SHIELD_THRESHOLD:
            logger.critical(f"VOLATILITY_SPIKE: VIX {current_vix} > {self.VIX_SHIELD_THRESHOLD}")
            return "DEFENSIVE_SHIELD_ACTIVE"
        return "NORMAL"
