import logging
import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid

logger = logging.getLogger(__name__)

class NewsAggregator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NewsAggregator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.sources = [
            {"id": "reuters", "name": "Reuters", "type": "Tier 1"},
            {"id": "bloomberg", "name": "Bloomberg", "type": "Tier 1"},
            {"id": "wsj", "name": "Wall Street Journal", "type": "Tier 1"},
            {"id": "seeking_alpha", "name": "Seeking Alpha", "type": "Contributor"},
            {"id": "twitter_fintwit", "name": "FinTwit", "type": "Social"},
        ]
        
        self.cached_articles = self._seed_articles()
        self.saved_searches = []
        self._initialized = True

    def _seed_articles(self) -> List[Dict]:
        articles = []
        tickers = ["AAPL", "TSLA", "NVDA", "AMD", "MSFT", "GOOGL", "AMZN"]
        tags = ["Earnings", "M&A", "Regulatory", "Macro", "Product Launch", "Analyst Rating"]
        
        for i in range(50):
            ticker = random.choice(tickers)
            source = random.choice(self.sources)
            tag = random.choice(tags)
            
            # Simple mock sentiment based on tag
            sentiment_score = random.uniform(-0.8, 0.8)
            if tag == "Earnings": sentiment_score = random.uniform(-0.9, 0.9)
            elif tag == "Product Launch": sentiment_score = random.uniform(0.2, 0.9)
            
            articles.append({
                "id": str(uuid.uuid4()),
                "title": f"{ticker}: {tag} update regarding recent market movements",
                "summary": f"Breaking news for {ticker} from {source['name']}. Analysts are watching closely as...",
                "source": source["name"],
                "source_id": source["id"],
                "tickers": [ticker],
                "tags": [tag],
                "sentiment_score": round(sentiment_score, 2),
                "sentiment_label": "Positive" if sentiment_score > 0.3 else "Negative" if sentiment_score < -0.3 else "Neutral",
                "published_at": (datetime.now() - timedelta(minutes=random.randint(1, 4000))).isoformat(),
                "url": "#"
            })
            
        return sorted(articles, key=lambda x: x['published_at'], reverse=True)

    async def get_articles(self, 
                           limit: int = 20, 
                           cursor: Optional[str] = None,
                           source: Optional[str] = None,
                           ticker: Optional[str] = None,
                           tag: Optional[str] = None) -> Dict:
        
        filtered = self.cached_articles
        
        if source:
            filtered = [a for a in filtered if a['source_id'] == source]
        if ticker:
            filtered = [a for a in filtered if ticker in a['tickers']]
        if tag:
            filtered = [a for a in filtered if tag in a['tags']]
            
        # Cursor pagination (simple slice)
        start_idx = 0
        if cursor:
            try:
                start_idx = int(cursor)
            except:
                pass
                
        end_idx = start_idx + limit
        results = filtered[start_idx:end_idx]
        
        next_cursor = str(end_idx) if end_idx < len(filtered) else None
        
        return {
            "articles": results,
            "next_cursor": next_cursor,
            "total": len(filtered)
        }

    async def get_article_details(self, id: str) -> Optional[Dict]:
        return next((a for a in self.cached_articles if a['id'] == id), None)

    async def get_sources(self) -> List[Dict]:
        return self.sources

    async def create_saved_search(self, name: str, filters: Dict) -> Dict:
        search = {
            "id": str(uuid.uuid4()),
            "name": name,
            "filters": filters,
            "created_at": datetime.now().isoformat()
        }
        self.saved_searches.append(search)
        return search

    async def list_saved_searches(self) -> List[Dict]:
        return self.saved_searches
