import logging
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SentimentAnalyzer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.tickers = ["AAPL", "TSLA", "NVDA", "AMD", "MSFT", "GOOGL", "AMZN", "PLTR", "GME", "AMC"]
        self._initialized = True

    async def get_ticker_sentiment(self, ticker: str) -> Dict:
        # Simulate sentiment analysis
        base_score = random.uniform(-0.5, 0.5)
        
        # Add some randomness based on ticker hash or time to make it seemingly dynamic but stable for demo
        seed = sum(ord(c) for c in ticker) + int(datetime.now().timestamp() / 300) # Changes every 5 mins
        random.seed(seed)
        
        score = base_score + random.uniform(-0.3, 0.3)
        score = max(-1.0, min(1.0, score))
        
        volume = random.randint(100, 50000)
        
        return {
            "ticker": ticker,
            "overall_score": round(score * 100, 1), # -100 to 100
            "sentiment_label": "Bullish" if score > 0.2 else "Bearish" if score < -0.2 else "Neutral",
            "volume": volume,
            "platforms": {
                "twitter": {
                    "score": round(min(100, max(-100, (score + random.uniform(-0.2, 0.2)) * 100)), 1),
                    "mentions": int(volume * 0.45)
                },
                "reddit": {
                    "score": round(min(100, max(-100, (score + random.uniform(-0.4, 0.1)) * 100)), 1),
                    "mentions": int(volume * 0.35)
                },
                "stocktwits": {
                    "score": round(min(100, max(-100, (score + random.uniform(-0.1, 0.3)) * 100)), 1),
                    "mentions": int(volume * 0.20)
                }
            },
            "last_updated": datetime.now().isoformat()
        }

    async def get_top_sentiment_movers(self, limit: int = 5) -> List[Dict]:
        results = []
        for t in random.sample(self.tickers, limit):
             results.append(await self.get_ticker_sentiment(t))
        return sorted(results, key=lambda x: abs(x['overall_score']), reverse=True)

    async def get_sentiment_history(self, ticker: str, days: int = 7) -> List[Dict]:
        history = []
        current = datetime.now()
        base_val = random.uniform(-50, 50)
        
        for i in range(days * 24): # Hourly granularity
            dt = current - timedelta(hours=i)
            val = base_val + random.uniform(-10, 10)
            base_val = val * 0.95 # Mean reversion
            
            history.append({
                "timestamp": dt.isoformat(),
                "score": round(max(-100, min(100, val)), 1),
                "price_chg": round(random.uniform(-0.5, 0.5) + (val * 0.01), 2) # Correlate price slightly
            })
            
        return sorted(history, key=lambda x: x['timestamp'])

    async def get_correlation(self, ticker: str) -> Dict:
        return {
            "ticker": ticker,
            "correlation_coef": round(random.uniform(0.6, 0.95), 2),
            "lead_lag_hours": random.randint(-4, 12),
            "significance": "High"
        }
