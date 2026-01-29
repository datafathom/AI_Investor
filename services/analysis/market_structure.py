import logging
from typing import List, Dict, Any, Optional
from decimal import Decimal

logger = logging.getLogger(__name__)

class MarketStructureService:
    """
    Detects market structure patterns: Higher Highs, Lower Lows, BOS, CHoCH.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MarketStructureService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("MarketStructureService initialized")

    def detect_swing_points(self, prices: List[float], lookback: int = 5) -> Dict[str, List[int]]:
        """
        Identify swing highs and swing lows in price data.
        Returns indices of detected swing points.
        """
        highs = []
        lows = []
        
        for i in range(lookback, len(prices) - lookback):
            window = prices[i - lookback:i + lookback + 1]
            if prices[i] == max(window):
                highs.append(i)
            if prices[i] == min(window):
                lows.append(i)
                
        return {"swing_highs": highs, "swing_lows": lows}

    def identify_trend(self, swing_highs: List[float], swing_lows: List[float]) -> str:
        """
        Classify trend based on swing point progression.
        HH + HL = UPTREND, LH + LL = DOWNTREND
        """
        if len(swing_highs) < 2 or len(swing_lows) < 2:
            return "UNKNOWN"
            
        hh = swing_highs[-1] > swing_highs[-2]  # Higher High
        hl = swing_lows[-1] > swing_lows[-2]    # Higher Low
        
        if hh and hl:
            return "UPTREND"
        elif not hh and not hl:
            return "DOWNTREND"
        else:
            return "RANGING"

    def detect_break_of_structure(self, prices: List[float], swing_points: Dict) -> Optional[str]:
        """
        Detect Break of Structure (BOS) or Change of Character (CHoCH).
        """
        # Simplified detection logic
        if len(prices) < 10:
            return None
            
        recent_high = max(prices[-5:])
        recent_low = min(prices[-5:])
        
        # Check if price broke previous structure
        if swing_points.get("swing_highs") and prices[-1] > max(swing_points["swing_highs"][-3:] if len(swing_points["swing_highs"]) >= 3 else swing_points["swing_highs"]):
            return "BOS_BULLISH"
        if swing_points.get("swing_lows") and prices[-1] < min(swing_points["swing_lows"][-3:] if len(swing_points["swing_lows"]) >= 3 else swing_points["swing_lows"]):
            return "BOS_BEARISH"
            
        return None
