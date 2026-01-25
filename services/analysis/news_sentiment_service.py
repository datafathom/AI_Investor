"""
==============================================================================
FILE: services/analysis/news_sentiment_service.py
ROLE: Analysis Engine
PURPOSE: Processes news articles to calculate sentiment scores and detect
         market-moving events.
         
INTEGRATION POINTS:
    - NewsAPIClient: Source of news articles.
    - HypeTracker: Consumes sentiment signals (future).
    - FearGreedService: Uses sentiment for fear/greed calculation (future).

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from services.data.news_api_service import get_news_client, NewsArticle

logger = logging.getLogger(__name__)

class SentimentResult(BaseModel):
    article: NewsArticle
    score: float  # -1.0 to 1.0
    label: str  # BULLISH, BEARISH, NEUTRAL
    indicators: List[str]

class SectorSentiment(BaseModel):
    sector: str
    average_score: float
    article_count: int
    top_indicators: List[str]

class NewsSentimentService:
    """
    Service for analyzing news sentiment.
    """

    # Heuristic keywords for financial sentiment
    POSITIVE_KEYWORDS = [
        "surge", "rally", "growth", "beat", "outperform", "bullish", 
        "optimistic", "record", "dividend", "acquisition", "buyback",
        "expansion", "successful", "positive", "upgrade"
    ]
    
    NEGATIVE_KEYWORDS = [
        "plunge", "crash", "miss", "underperform", "bearish", 
        "pessimistic", "lawsuit", "investigation", "bankruptcy",
        "restructuring", "loss", "negative", "downgrade", "debt",
        "inflation", "recession"
    ]

    def __init__(self, news_client=None):
        self.news = news_client or get_news_client()

    async def analyze_topic(self, topic: str) -> List[SentimentResult]:
        """Fetch and analyze news for a specific topic/ticker."""
        articles = await self.news.everything_search(topic)
        results = []
        for article in articles:
            results.append(self._calculate_sentiment(article))
        return results

    async def get_market_sentiment(self) -> Dict[str, Any]:
        """Analyze top headlines for overall market sentiment."""
        articles = await self.news.get_top_headlines()
        results = [self._calculate_sentiment(a) for a in articles]
        
        if not results:
            return {"average_score": 0, "label": "NEUTRAL", "count": 0}
            
        avg_score = sum(r.score for r in results) / len(results)
        
        label = "NEUTRAL"
        if avg_score > 0.2: label = "BULLISH"
        elif avg_score < -0.2: label = "BEARISH"
        
        return {
            "average_score": avg_score,
            "label": label,
            "count": len(results),
            "top_news": results[:5]
        }

    def _calculate_sentiment(self, article: NewsArticle) -> SentimentResult:
        """
        Simple heuristic-based sentiment analysis.
        In a real app, this would use a transformer model (BERT/RoBERTa).
        """
        text = f"{article.title} {article.description or ''}".lower()
        score = 0.0
        indicators = []

        # Simple keyword weight mapping
        for word in self.POSITIVE_KEYWORDS:
            if re.search(rf"\b{word}\b", text):
                score += 0.2
                indicators.append(word)
        
        for word in self.NEGATIVE_KEYWORDS:
            if re.search(rf"\b{word}\b", text):
                score -= 0.2
                indicators.append(word)

        # Cap score between -1 and 1
        score = max(-1.0, min(1.0, score))
        
        label = "NEUTRAL"
        if score > 0.1: label = "BULLISH"
        elif score < -0.1: label = "BEARISH"

        return SentimentResult(
            article=article,
            score=score,
            label=label,
            indicators=list(set(indicators))
        )

_instance = None

def get_news_sentiment_service() -> NewsSentimentService:
    global _instance
    if _instance is None:
        _instance = NewsSentimentService()
    return _instance
