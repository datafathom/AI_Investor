"""
Fear & Greed Index Calculator.
Aggregates multiple signals into a single sentiment metric.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FearGreedIndex:
    """Calculates the fear & greed score (0-100)."""
    
    def calculate_index(self, vix: float, put_call_ratio: float, rs_momentum: float) -> int:
        score = 50 # Baseline
        if vix > 30: score -= 20
        if put_call_ratio > 1.2: score -= 15
        if rs_momentum > 0.8: score += 20
        
        return max(0, min(100, int(score)))
