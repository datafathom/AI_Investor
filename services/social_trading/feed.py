import logging
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class SocialTradingFeed:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SocialTradingFeed, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.posts = self._seed_feed()
        self._initialized = True

    def _seed_feed(self) -> List[Dict]:
        influencers = [
            {"id": "user1", "name": "CryptoKing", "avatar": "👑"},
            {"id": "user2", "name": "ValueInv", "avatar": "📈"},
            {"id": "user3", "name": "DeepValue", "avatar": "🧠"},
            {"id": "user4", "name": "ChartWizard", "avatar": "🧙‍♂️"},
        ]
        
        tickers = ["BTC", "ETH", "SOL", "AAPL", "TSLA", "GME"]
        actions = ["BUY", "SELL", "HOLD"]
        
        feed = []
        for i in range(20):
            inf = random.choice(influencers)
            ticker = random.choice(tickers)
            action = random.choice(actions)
            price = random.uniform(10, 3000)
            
            feed.append({
                "id": str(uuid.uuid4()),
                "influencer_id": inf['id'],
                "influencer_name": inf['name'],
                "influencer_avatar": inf['avatar'],
                "ticker": ticker,
                "action": action,
                "confidence": random.randint(60, 99),
                "price": round(price, 2),
                "comment": f"Entering {action} position on {ticker} at ${round(price, 2)}. Key levels holding.",
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 120))).isoformat(),
                "likes": random.randint(0, 500)
            })
            
        return sorted(feed, key=lambda x: x['timestamp'], reverse=True)

    async def get_feed(self, limit: int = 20) -> List[Dict]:
        return self.posts[:limit]
