import logging
import random
import uuid
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RumorClassifier:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RumorClassifier, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.rumors = self._seed_rumors()
        self._initialized = True

    def _seed_rumors(self) -> List[Dict]:
        rumors = []
        types = ["M&A", "Earnings Leak", "FDA Approval", "Executive Departure", "Product Delay"]
        statuses = ["UNVERIFIED", "CONFIRMED", "DEBUNKED"]
        tickers = ["AAPL", "TSLA", "PFE", "MRNA", "AMD", "INTC"]
        
        for i in range(15):
            r_type = random.choice(types)
            ticker = random.choice(tickers)
            status = random.choice(statuses)
            
            # Weighted confidence based on status
            confidence = random.uniform(0.1, 0.4)
            if status == "CONFIRMED": confidence = random.uniform(0.8, 0.99)
            elif status == "DEBUNKED": confidence = random.uniform(0.0, 0.1)
            elif status == "UNVERIFIED": confidence = random.uniform(0.3, 0.7)

            rumors.append({
                "id": str(uuid.uuid4()),
                "type": r_type,
                "ticker": ticker,
                "title": f"Potential {r_type} involving {ticker}",
                "description": f"Sources suggest {ticker} is involved in {r_type.lower()} activity. Unconfirmed reports from social channels.",
                "status": status,
                "confidence": round(confidence, 2),
                "source": "Blind Item",
                "upvotes": random.randint(0, 500),
                "downvotes": random.randint(0, 100),
                "created_at": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat()
            })
        return sorted(rumors, key=lambda x: x['created_at'], reverse=True)

    async def list_rumors(self) -> List[Dict]:
        return self.rumors

    async def get_rumor(self, id: str) -> Optional[Dict]:
        return next((r for r in self.rumors if r['id'] == id), None)

    async def vote(self, id: str, vote_type: str) -> Dict:
        rumor = await self.get_rumor(id)
        if rumor:
            if vote_type == "up":
                rumor['upvotes'] += 1
            elif vote_type == "down":
                rumor['downvotes'] += 1
            
            # Recalculate mock confidence based on votes
            total = rumor['upvotes'] + rumor['downvotes']
            if total > 0:
                rumor['confidence'] = round(rumor['upvotes'] / total, 2)
                
            return rumor
        return None
