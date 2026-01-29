"""
Regime Switcher.
Switches entre Risk Parity potentially and Growth Mode.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RegimeSwitcher:
    """Switches portfolio modes."""
    
    def determine_mode(self, vix: float, inflation_moving_avg: float) -> str:
        if vix > 30 or inflation_moving_avg > 0.05:
             return "ALL_WEATHER_PARITY"
        return "GROWTH_CONCENTRATED"
