"""
Structure Scanner Service.
Finds valid swing highs/lows for institutional stop loss placement.
"""
import logging
from typing import List, Dict, Any, Optional
from decimal import Decimal

logger = logging.getLogger(__name__)

class StructureScanner:
    """
    Market structure analyzer for optimal SL levels.
    """

    @staticmethod
    def find_swing_low(candles: List[Dict[str, Any]], lookback: int = 20) -> Optional[float]:
        """
        Find the lowest low in the last N candles.
        """
        if not candles or len(candles) < 3:
            return None
        
        recent = candles[-lookback:] if len(candles) >= lookback else candles
        return min(c['low'] for c in recent)

    @staticmethod
    def find_swing_high(candles: List[Dict[str, Any]], lookback: int = 20) -> Optional[float]:
        """
        Find the highest high in the last N candles.
        """
        if not candles or len(candles) < 3:
            return None
        
        recent = candles[-lookback:] if len(candles) >= lookback else candles
        return max(c['high'] for c in recent)

    @staticmethod
    def get_stop_level(direction: str, candles: List[Dict[str, Any]], lookback: int = 20) -> Optional[float]:
        """
        Get the optimal SL anchor based on trade direction.
        """
        if direction.upper() == "LONG":
            return StructureScanner.find_swing_low(candles, lookback)
        else:
            return StructureScanner.find_swing_high(candles, lookback)
