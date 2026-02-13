import logging
import random
import uuid
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class InfluencerTracker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InfluencerTracker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.influencers = self._seed_influencers()
        self.following = set()
        self._initialized = True

    def _seed_influencers(self) -> List[Dict]:
        return [
            {
                "id": "user1", 
                "name": "CryptoKing", 
                "avatar": "👑", 
                "followers": 15400, 
                "win_rate": 68.5, 
                "avg_return_pct": 12.4,
                "bio": "Crypto OG. DCA into adoption."
            },
            {
                "id": "user2", 
                "name": "ValueInv", 
                "avatar": "📈", 
                "followers": 8200, 
                "win_rate": 55.2, 
                "avg_return_pct": 8.1,
                "bio": "Searching for undervalued gems."
            },
            {
                "id": "user3", 
                "name": "DeepValue", 
                "avatar": "🧠", 
                "followers": 2100, 
                "win_rate": 42.0, 
                "avg_return_pct": 25.6,
                "bio": "High risk, high reward."
            },
            {
                "id": "user4", 
                "name": "ChartWizard", 
                "avatar": "🧙‍♂️", 
                "followers": 32000, 
                "win_rate": 71.2, 
                "avg_return_pct": 5.3,
                "bio": "Technical Analysis is all that matters."
            },
        ]

    async def list_influencers(self) -> List[Dict]:
        # dynamic Following status
        return [{**i, "is_following": i['id'] in self.following} for i in self.influencers]

    async def follow(self, id: str) -> bool:
        if id in [i['id'] for i in self.influencers]:
            if id in self.following:
                self.following.remove(id) # Toggle
                return False
            else:
                self.following.add(id)
                return True
        return False
