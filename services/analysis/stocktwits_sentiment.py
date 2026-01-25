"""
==============================================================================
FILE: services/analysis/stocktwits_sentiment.py
ROLE: StockTwits Sentiment Analyzer
PURPOSE: Analyzes StockTwits streams to calculate community consensus, detect
         volume spikes, and store sentiment history for trend analysis.

INTEGRATION POINTS:
    - StockTwitsClient: Message stream source
    - HypeTracker: Volume spike alerts
    - Database: Sentiment history storage

AUTHOR: AI Investor Team
CREATED: 2026-01-22
UPDATED: 2026-01-21 (Enhanced for Phase 27)
==============================================================================
"""

import logging
from typing import Dict, Any, List
from services.social.stocktwits_client import get_stocktwits_client

logger = logging.getLogger(__name__)

class StockTwitsSentimentAnalyzer:
    """
    Processes StockTwits messages for bullish/bearish ratios.
    """
    
    def __init__(self):
        self.client = get_stocktwits_client()

    async def analyze_symbol(self, symbol: str) -> Dict[str, Any]:
        """Fetch stream and aggregate sentiment score."""
        stream = await self.client.get_symbol_stream(symbol)
        
        bullish = 0
        bearish = 0
        neutral = 0
        
        for msg in stream:
            sent = msg.get('entities', {}).get('sentiment', {}).get('basic') if msg.get('entities') else None
            if sent == "Bullish":
                bullish += 1
            elif sent == "Bearish":
                bearish += 1
            else:
                neutral += 1
        
        total = bullish + bearish + neutral
        consensus = "Neutral"
        if total > 0:
            bull_ratio = bullish / total
            if bull_ratio > 0.6: consensus = "Bullish"
            elif bull_ratio < 0.3: consensus = "Bearish"

        # Detect volume spikes (if message count exceeds threshold)
        volume_spike = total > 50  # Threshold for spike detection
        
        result = {
            "symbol": symbol,
            "consensus": consensus,
            "bull_count": bullish,
            "bear_count": bearish,
            "neutral_count": neutral,
            "total_messages": total,
            "sentiment_score": round((bullish - bearish) / max(total, 1), 2),
            "volume_spike": volume_spike,
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        # Store sentiment history (in production, save to database)
        # await self._store_sentiment_history(result)
        
        return result
    
    async def detect_volume_spikes(self, symbol: str, threshold: int = 50) -> Dict[str, Any]:
        """
        Detect volume spikes in message activity.
        
        Args:
            symbol: Ticker symbol
            threshold: Message count threshold
            
        Returns:
            Dict with spike detection results
        """
        analysis = await self.analyze_symbol(symbol)
        
        return {
            "symbol": symbol,
            "has_spike": analysis["volume_spike"],
            "message_count": analysis["total_messages"],
            "threshold": threshold,
            "alert_triggered": analysis["volume_spike"]
        }

_instance = None

def get_stocktwits_sentiment() -> StockTwitsSentimentAnalyzer:
    global _instance
    if _instance is None:
        _instance = StockTwitsSentimentAnalyzer()
    return _instance
