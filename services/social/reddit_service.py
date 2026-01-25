"""
==============================================================================
FILE: services/social/reddit_service.py
ROLE: Social Data Provider
PURPOSE: Interfaces with Reddit API (or Mock) for social sentiment tracking 
         and "hype" detection on key subreddits.
         
INTEGRATION POINTS:
    - APIGovernor: Manages Reddit rate limits (if live).
    - SocialStore: Frontend state for hype scores.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class RedditPost(BaseModel):
    """Pydantic model for a Reddit post."""
    id: str
    title: str
    score: int
    num_comments: int
    url: str
    created_utc: float
    author: str
    subreddit: str
    sentiment_score: float = 0.0  # -1.0 to 1.0

class RedditClient:
    """
    Client for Reddit API interaction.
    Currently defaults to MOCK MODE as per Phase 8 requirements.
    """
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None,
                 mock: bool = True):
        self.mock = mock
        self.client_id = client_id
        self.client_secret = client_secret
        # Dictionary of "Hype" tickers for mock generation
        self._hype_tickers = ["NVDA", "TSLA", "GME", "AMC", "AAPL", "AMD", "PLTR", "HOOD",
                              "COIN", "MSFT"]

    async def get_subreddit_posts(self, subreddit: str = "wallstreetbets",
                                  limit: int = 10) -> List[RedditPost]:
        """
        Get top posts from a subreddit.
        """
        if self.mock:
            return self._generate_mock_posts(subreddit, limit)
        # Placeholder for real API implementation
        logger.warning("Live Reddit API not implemented yet. Returning empty list.")
        return []

    async def analyze_sentiment(self, ticker: str) -> Dict[str, Any]:
        """
        Returns sentiment analysis for a specific ticker.
        """
        if self.mock:
            score = random.uniform(-0.5, 0.9)
            return {
                "ticker": ticker.upper(),
                "sentiment_score": round(score, 2),
                "sentiment_label": "BULLISH" if score > 0.2 else (
                    "BEARISH" if score < -0.2 else "NEUTRAL"),
                "mention_count": random.randint(50, 5000),
                "hype_score": random.randint(10, 100)
            }
        return {}

    def _generate_mock_posts(self, subreddit: str, limit: int) -> List[RedditPost]:
        posts = []
        templates = [
            "YOLO on {ticker} calls expiring Friday!",
            "{ticker} is going to the moon 🚀",
            "Why {ticker} is a trap, stay away",
            "Just bought the dip on {ticker}",
            "{ticker} earnings are going to be insane",
            "Loss porn: Down 99% on {ticker}",
            "{ticker} technical analysis inside",
        ]
        for i in range(limit):
            ticker = random.choice(self._hype_tickers)
            title = random.choice(templates).format(ticker=ticker)
            # Simple heuristic for mock sentiment
            sentiment = (0.8 if "moon" in title or "YOLO" in title 
                         else (-0.6 if "trap" in title or "Loss" in title else 0.1))
            
            posts.append(RedditPost(
                id=f"mock_{i}",
                title=title,
                score=random.randint(10, 50000),
                num_comments=random.randint(5, 5000),
                url=f"https://reddit.com/r/{subreddit}/comments/mock_{i}",
                created_utc=(datetime.now() - timedelta(hours=random.randint(0, 24))).timestamp(),
                author=f"user_{random.randint(1000, 9999)}",
                subreddit=subreddit,
                sentiment_score=sentiment
            ))
        return posts

class RedditClientSingleton:
    """Singleton wrapper for RedditClient."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> RedditClient:
        """Returns the singleton instance of RedditClient."""
        if cls._instance is None:
            cls._instance = RedditClient(mock=mock)
        return cls._instance

def get_reddit_client(mock: bool = True) -> RedditClient:
    """Legacy helper to get the reddit client instance."""
    return RedditClientSingleton.get_instance(mock=mock)
