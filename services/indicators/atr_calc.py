"""
ATR Calculator Service.
Computes Average True Range for volatility-adjusted stop loss padding.
"""
import logging
from typing import List, Dict, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class ATRCalculator:
    """
    Volatility measurement for institutional stop placement.
    """

    @staticmethod
    def calculate_atr(candles: List[Dict[str, Any]], period: int = 14) -> float:
        """
        Calculate Average True Range over a given period.
        """
        if len(candles) < period + 1:
            return 0.0

        true_ranges = []
        for i in range(1, len(candles)):
            high = candles[i]['high']
            low = candles[i]['low']
            prev_close = candles[i-1]['close']
            
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            true_ranges.append(tr)

        recent_trs = true_ranges[-period:]
        return sum(recent_trs) / len(recent_trs)

    @staticmethod
    def get_padded_stop(swing_level: float, atr: float, direction: str, padding_mult: float = 1.5) -> float:
        """
        Apply ATR padding to a structural stop level.
        """
        padding = atr * padding_mult
        
        if direction.upper() == "LONG":
            return round(swing_level - padding, 5) # Below swing low
        else:
            return round(swing_level + padding, 5) # Above swing high
