"""
Market Depth Checker.
Checks liquidity depth via Kafka telemetry.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DepthChecker:
    """Checks market depth for liquidity risk."""
    
    MIN_BID_ASK_VOLUME = 1000000 # $1M depth min
    
    def check_depth(self, ticker: str, current_depth: Dict[str, Any]) -> Dict[str, Any]:
        bid_vol = current_depth.get("bids_vol", 0)
        ask_vol = current_depth.get("asks_vol", 0)
        
        is_thin = (bid_vol + ask_vol) < self.MIN_BID_ASK_VOLUME
        
        if is_thin:
            logger.warning(f"LIQUIDITY_RISK: {ticker} is thin. Vol: {bid_vol+ask_vol}")
            
        return {
            "ticker": ticker,
            "is_thin": is_thin,
            "total_depth": bid_vol + ask_vol
        }
