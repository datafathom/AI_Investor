"""
IV Rank Filter.
Ensures we only sell premium when it is expensive.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class IVRankFilter:
    """Filters based on Implied Volatility Rank."""
    
    def check_rank(self, ticker: str, current_iv: float, iv_high: float, iv_low: float) -> Dict[str, Any]:
        rank = (current_iv - iv_low) / (iv_high - iv_low)
        
        is_expensive = rank > 0.50
        
        return {
            "iv_rank": round(rank * 100, 2),
            "is_expensive": is_expensive,
            "action": "SELL_PREMIUM" if is_expensive else "WAIT"
        }
