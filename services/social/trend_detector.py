import logging
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class TrendDetector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TrendDetector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.trends = self._seed_trends()
        self._initialized = True

    def _seed_trends(self) -> List[Dict]:
        topics = [
            {"topic": "AI Regulation", "tickers": ["NVDA", "MSFT", "GOOGL"]},
            {"topic": "EV Battery Tech", "tickers": ["TSLA", "F", "GM"]},
            {"topic": "Semiconductor Shortage", "tickers": ["AMD", "INTC", "TSM"]},
            {"topic": "Crypto ETF", "tickers": ["COIN", "BLK"]},
            {"topic": "Consumer Spending", "tickers": ["AMZN", "WMT", "TGT"]},
            {"topic": "GLP-1 Drugs", "tickers": ["LLY", "NVO"]},
        ]
        
        results = []
        for t in topics:
            velocity = random.uniform(1.2, 5.0) # Multiplier of normal volume
            mentions_1h = random.randint(500, 10000)
            
            results.append({
                "id": str(uuid.uuid4()),
                "topic": t['topic'],
                "related_tickers": t['tickers'],
                "velocity": round(velocity, 2),
                "mentions_1h": mentions_1h,
                "mentions_24h": int(mentions_1h * random.uniform(10, 20)),
                "sentiment_score": round(random.uniform(-0.8, 0.8), 2),
                "first_detected": (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat()
            })
            
        return sorted(results, key=lambda x: x['velocity'], reverse=True)

    async def get_trends(self) -> List[Dict]:
        # Regenerate velocity randomly to simulate live changes
        for t in self.trends:
            t['velocity'] = round(t['velocity'] * random.uniform(0.95, 1.05), 2)
        return sorted(self.trends, key=lambda x: x['velocity'], reverse=True)

    async def get_trend_details(self, topic_id: str) -> Optional[Dict]:
        return next((t for t in self.trends if t['id'] == topic_id or t['topic'] == topic_id), None)
