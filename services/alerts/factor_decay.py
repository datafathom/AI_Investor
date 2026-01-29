"""
Factor Decay Monitor.
Detects if historical factor premia are disappearing.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FactorDecayMonitor:
    """Alerts on factor underperformance."""
    
    def check_decay(self, factor_name: str, rolling_10y_return: float) -> bool:
        if rolling_10y_return < 0:
             logger.warning(f"FACTOR_DECAY: {factor_name} has negative 10-year return. Structural break?")
             return True
        return False
