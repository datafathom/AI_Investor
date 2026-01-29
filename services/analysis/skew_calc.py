"""
Skew Detector.
Measures Put/Call Skew on the volatility surface.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SkewCalculator:
    """Calculates volatility skew."""
    
    def calculate_skew(self, put_iv: float, call_iv: float) -> float:
        """Standard Skew = Put IV - Call IV"""
        skew = put_iv - call_iv
        logger.info(f"SKEW_DETECTED: {skew:.2f}")
        return skew
