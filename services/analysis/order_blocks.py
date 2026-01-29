"""
Order Block Detection Algorithm.
Identifies institutional supply and demand zones based on impulsive price rejection.
"""
import logging
from typing import List, Dict, Any, Optional
from decimal import Decimal

logger = logging.getLogger(__name__)

class OrderBlockDetector:
    """
    Logic for detecting high-probability institutional zones.
    """

    @staticmethod
    def detect_zones(candles: List[Dict[str, Any]], atr_multiplier: float = 3.0) -> List[Dict[str, Any]]:
        """
        Identify Order Blocks in a sequence of candles.
        
        Logic:
        1. Find a candle with a body size > (ATR * multiplier) -> Impulse Candle.
        2. The candle immediately preceding the impulse is the "Order Block".
        
        :param candles: List of candle dicts {open, high, low, close, volume}
        :param atr_multiplier: Sensitivity for impulse detection
        :return: List of identified zones
        """
        zones = []
        if len(candles) < 2:
            return zones

        for i in range(1, len(candles)):
            # Use all candles before the current one to establish 'Normal' range
            prior_candles = candles[:i]
            ranges = [abs(c['high'] - c['low']) for c in prior_candles]
            avg_range = sum(ranges) / len(ranges)
            impulse_threshold = avg_range * atr_multiplier

            curr_candle = candles[i]
            prev_candle = candles[i-1]
            
            body_size = abs(curr_candle['close'] - curr_candle['open'])
            
            if body_size >= impulse_threshold:
                # Impulse Detected
                is_bullish = curr_candle['close'] > curr_candle['open']
                
                zone = {
                    "type": "DEMAND" if is_bullish else "SUPPLY",
                    "price_low": prev_candle['low'],
                    "price_high": prev_candle['high'],
                    "impulse_candle_idx": i,
                    "strength": 1, # Initial strength
                    "is_mitigated": False
                }
                
                logger.info(f"ORDER_BLOCK_DETECTED: {zone['type']} at [{zone['price_low']}, {zone['price_high']}]")
                zones.append(zone)

        return zones
