"""
==============================================================================
FILE: services/social/stocktwits_client.py
ROLE: StockTwits Retail Sentiment Client
PURPOSE: Fetches real-time message streams and trending symbols from StockTwits.
         Provides highest signal-to-noise source for meme stock activity and
         retail momentum tracking.

INTEGRATION POINTS:
    - StockTwitsSentimentAnalyzer: Sentiment analysis
    - HypeTracker: Volume spike detection
    - StockTwitsFeed: Frontend widget

AUTHOR: AI Investor Team
CREATED: 2026-01-22
UPDATED: 2026-01-21 (Enhanced for Phase 27)
==============================================================================
"""

import logging
import asyncio
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class StockTwitsClient:
    """
    Client for StockTwits API.
    Defaults to MOCK MODE for Phase 27.
    """
    
    def __init__(self, access_token: Optional[str] = None, mock: bool = True):
        self.mock = mock
        sm = get_secret_manager()
        self.access_token = access_token or sm.get_secret('STOCKTWITS_ACCESS_TOKEN')
        self.base_url = sm.get_secret('STOCKTWITS_BASE_URL', 'https://api.stocktwits.com/api/2')

    async def get_symbol_stream(self, symbol: str) -> List[Dict[str, Any]]:
        """Get message stream for a specific ticker."""
        if self.mock:
            await asyncio.sleep(0.4)
            # Mix of bullish/bearish for "Retail" feel
            sentiments = ["Bullish", "Bearish", None]
            messages = [
                "Buying the dip on $BTC! 🚀",
                "Earnings were weak, selling my $AAPL position.",
                "Shorting $TSLA here, look at that wedge.",
                "Anyone seeing the volume on $NVDA?",
                "Total bloodbath today. Holding my $SPY puts."
            ]
            
            stream = []
            for i in range(10):
                msg = random.choice(messages)
                sent = random.choice(sentiments)
                stream.append({
                    "id": 1000 + i,
                    "body": msg,
                    "created_at": datetime.utcnow().isoformat(),
                    "user": {
                        "username": f"trader_{random.randint(1,99)}",
                        "identity": "Retail"
                    },
                    "entities": {"sentiment": {"basic": sent} if sent else None}
                })
            return stream
        return []

    async def get_trending_symbols(self) -> List[Dict[str, Any]]:
        """
        Get current trending symbols on StockTwits.
        
        Returns:
            List of trending symbol dicts with scores
        """
        if self.mock:
            await asyncio.sleep(0.3)
            return [
                {"symbol": "BTC.X", "name": "Bitcoin", "trending_score": 98, "watchlist_count": 12500},
                {"symbol": "NVDA", "name": "NVIDIA", "trending_score": 92, "watchlist_count": 8900},
                {"symbol": "TSLA", "name": "Tesla", "trending_score": 85, "watchlist_count": 7200},
                {"symbol": "SPY", "name": "SPDR S&P 500 ETF", "trending_score": 80, "watchlist_count": 5600}
            ]
        return []
    
    async def get_watchlist_stream(self, watchlist_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get personalized watchlist stream.
        
        Args:
            watchlist_id: Optional watchlist ID
            
        Returns:
            List of messages from watchlist
        """
        if self.mock:
            await asyncio.sleep(0.4)
            return await self.get_symbol_stream("AAPL")  # Mock watchlist
        return []
    
    async def get_user_stream(self, username: str) -> List[Dict[str, Any]]:
        """
        Get messages from a specific user.
        
        Args:
            username: StockTwits username
            
        Returns:
            List of user messages
        """
        if self.mock:
            await asyncio.sleep(0.3)
            return [
                {
                    "id": 2000,
                    "body": f"Latest analysis from @{username}",
                    "created_at": datetime.utcnow().isoformat(),
                    "user": {"username": username, "identity": "Retail"},
                    "entities": {"sentiment": {"basic": "Bullish"}}
                }
            ]
        return []

_instance = None

def get_stocktwits_client(mock: bool = True) -> StockTwitsClient:
    global _instance
    if _instance is None:
        _instance = StockTwitsClient(mock=mock)
    return _instance
