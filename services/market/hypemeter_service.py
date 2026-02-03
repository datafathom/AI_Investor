"""
==============================================================================
FILE: services/market/hypemeter_service.py
ROLE: Social Sentiment Analysis Service
PURPOSE: Aggregates and analyzes social sentiment ("Hype") from various 
         sources (Reddit, Twitter/X, News) to provide the HypeMeter feed.
         
ARCHITECTURE:
    - Service Layer: Ingests text data, performs sentiment analysis (mock for MVP).
    - Data Access: Designed to interface with Postgres (History) and Neo4j (Graph).
    
DEPENDENCIES:
    - Standard Lib (random, datetime)
==============================================================================
"""
import random
from typing import List, Dict
from datetime import datetime, timedelta
from services.social.reddit_service import get_reddit_client
from services.social.discord_bot import get_discord_bot
from services.social.inertia_cache import get_inertia_cache

class HypeMeterService:
    """
    Service for managing Social Sentiment (HypeMeter) data.
    """
    
    def __init__(self):
        self.reddit = get_reddit_client()
        self.discord = get_discord_bot()
        self.cache = get_inertia_cache()

    async def get_hype_feed(self, limit: int = 50) -> List[Dict]:
        """
        Get the latest social sentiment messages stream.
        
        Args:
            limit (int): Number of messages to retrieve.
            
        Returns:
            List[Dict]: List of sentiment objects.
        """
        # Simulated feed for MVP
        symbols = ["AAPL", "TSLA", "GME", "NVDA", "BTC", "SPY", "AMC", "PLTR"]
        sources = ["Reddit", "Twitter", "Bloomberg", "CNBC"]
        keywords_map = {
            "TSLA": ["Robotaxi", "Musk", "Calls"],
            "GME": ["Squeeze", "HODL", "Diamond Hands"],
            "BTC": ["Halving", "ETF", "Moon"],
            "NVDA": ["AI", "Chips", "Jensen"],
            "PLTR": ["Defense", "AI", "Contract"]
        }
        
        feed = []
        base_time = datetime.utcnow()
        
        for i in range(limit):
            symbol = random.choice(symbols)
            sentiment = random.uniform(-1, 1)
            source = random.choice(sources)
            magnitude = round(abs(sentiment) * random.uniform(1, 15), 1) # Range 0-15
            is_viral = magnitude > 8.0
            
            # Extract Keywords (Mock logic for MVP)
            item_keywords = []
            if symbol in keywords_map:
                # Randomly pick 0-2 keywords
                item_keywords = random.sample(keywords_map[symbol], k=random.randint(0, min(2, len(keywords_map[symbol]))))
            
            # Add general keywords based on sentiment
            if sentiment > 0.8: item_keywords.append("Breakout")
            if sentiment < -0.8: item_keywords.append("Crash")

            feed.append({
                "id": f"msg-{i}-{int(base_time.timestamp())}",
                "timestamp": (base_time - timedelta(seconds=i*5)).isoformat(),
                "symbol": symbol,
                "source": source,
                "sentiment": round(sentiment, 2),
                "text": self._generate_fake_text(symbol, sentiment, is_viral),
                "magnitude": magnitude,
                "viral": is_viral,
                "keywords": item_keywords
            })
            
        return feed

    def _generate_fake_text(self, symbol: str, sentiment: float, viral: bool = False) -> str:
        """Helper to generate realistic fake sentiment text."""
        viral_prefix = "🚨 BREAKING: " if viral else ""
        
        if sentiment > 0.6:
            return f"{viral_prefix}{symbol} to the moon! 🚀 Structure looking extremely bullish on 4H."
        elif sentiment > 0.2:
            return f"Accumulating more {symbol} here. Good risk/reward."
        elif sentiment < -0.6:
            return f"{viral_prefix}{symbol} breaking support levels, heavy sell volume coming in."
        elif sentiment < -0.2:
            return f"Taking profits on {symbol}, looks extended."
        else:
            return f"{symbol} chopping around in range, waiting for catalyst."

    async def get_top_hyped_assets(self) -> List[Dict]:
        """
        Get assets ranked by social volume/sentiment magnitude based on inertia cache.
        """
        trending = self.cache.get_trending_tickers(limit=5)
        results = []
        for ticker in trending:
            inertia = self.cache.get_inertia(ticker)
            results.append({
                "symbol": ticker,
                "score": int(abs(inertia) * 100),
                "volume": "Extreme" if self.cache.inertia_data[ticker]["velocity"] > 500 else "High"
            })
        
        # Fallback to defaults if cache is empty
        if not results:
            return [
                {"symbol": "NVDA", "score": 95, "volume": "Extreme"},
                {"symbol": "TSLA", "score": 82, "volume": "High"},
            ]
        return results

# Singleton Instance
hypemeter_service = HypeMeterService()
