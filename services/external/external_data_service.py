import logging
from typing import List, Dict
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class ExternalDataSource:
    def __init__(self, id: str, name: str, category: str, status: str, quota_limit: int, quota_used: int):
        self.id = id
        self.name = name
        self.category = category
        self.status = status
        self.quota_limit = quota_limit
        self.quota_used = quota_used
        self.last_updated = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "status": self.status,
            "quota_limit": self.quota_limit,
            "quota_used": self.quota_used,
            "usage_pct": round((self.quota_used / self.quota_limit) * 100, 1) if self.quota_limit > 0 else 0,
            "last_updated": self.last_updated.isoformat()
        }

class ExternalDataService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExternalDataService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.sources = [
            ExternalDataSource("src_1", "Bloomberg Terminal Data", "Market Data", "active", 100000, 45200),
            ExternalDataSource("src_2", "Reuters News Feed", "News", "active", 50000, 12050),
            ExternalDataSource("src_3", "Alternative Data: Satellite", "Alt Data", "active", 1000, 850),
            ExternalDataSource("src_4", "Social Sentiment Firehose", "Social", "warning", 1000000, 980000),
            ExternalDataSource("src_5", "Fed Reserve Economic Data", "Macro", "active", 0, 0), # Unlimited
            ExternalDataSource("src_6", "Custom Scraper: Real Estate", "Alt Data", "error", 500, 0),
        ]
        self._initialized = True

    async def list_sources(self) -> List[Dict]:
        # Simulate dynamic usage updates
        for src in self.sources:
            if src.quota_limit > 0 and src.status == "active":
                change = random.randint(0, 50)
                src.quota_used = min(src.quota_limit, src.quota_used + change)
        
        return [s.to_dict() for s in self.sources]

    async def toggle_source(self, source_id: str) -> Dict:
        forsrc = next((s for s in self.sources if s.id == source_id), None)
        if forsrc:
            forsrc.status = "inactive" if forsrc.status == "active" else "active"
            return forsrc.to_dict()
        return None

    async def get_usage_stats(self) -> Dict:
        total_sources = len(self.sources)
        active = len([s for s in self.sources if s.status == "active"])
        errors = len([s for s in self.sources if s.status == "error"])
        
        return {
            "total_sources": total_sources,
            "active_sources": active,
            "error_sources": errors,
            "overall_health": 92.5
        }
