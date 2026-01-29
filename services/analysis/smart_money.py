"""
Smart Money Analyzer.
Tracks institutional order flow.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SmartMoneyAnalyzer:
    """Analyzes smart money flow."""
    
    LARGE_ORDER_THRESHOLD = 100000 # volume or dollars
    
    def analyze_flow(self, trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        large_buys = 0
        large_sells = 0
        
        for t in trades:
            if t.get("size", 0) >= self.LARGE_ORDER_THRESHOLD:
                if t.get("side") == "buy":
                    large_buys += 1
                else:
                    large_sells += 1
                    
        sentiment = "NEUTRAL"
        if large_buys > large_sells * 1.5:
            sentiment = "BULLISH_INSTITUTIONAL"
        elif large_sells > large_buys * 1.5:
            sentiment = "BEARISH_INSTITUTIONAL"
            
        return {
            "large_buys": large_buys,
            "large_sells": large_sells,
            "sentiment": sentiment
        }
