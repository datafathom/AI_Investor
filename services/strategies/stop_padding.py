"""
Stop Padding Logic.
Adds buffer to raw stop loss levels.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class StopPadding:
    """Calculates padded stop loss levels."""
    
    @staticmethod
    def apply_padding(raw_stop: float, atr: float, direction: str, padding_multiplier: float = 1.5) -> float:
        padding = atr * padding_multiplier
        if direction.upper() == "LONG":
            return raw_stop - padding
        else:
            return raw_stop + padding
