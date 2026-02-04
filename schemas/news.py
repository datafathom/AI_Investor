"""
==============================================================================
FILE: models/news.py
ROLE: News & Sentiment Data Models
PURPOSE: Pydantic models for news aggregation, sentiment analysis, and
         market impact assessment.

INTEGRATION POINTS:
    - NewsAggregationService: News collection
    - SentimentAnalysisService: Sentiment scoring
    - NewsAPI: News endpoints
    - FrontendNews: News dashboard widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class SentimentScore(str, Enum):
    """Sentiment score levels."""
    VERY_BEARISH = "very_bearish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    BULLISH = "bullish"
    VERY_BULLISH = "very_bullish"


class NewsArticle(BaseModel):
    """News article model."""
    article_id: str
    title: str
    content: str
    source: str
    author: Optional[str] = None
    published_date: datetime
    url: Optional[str] = None
    symbols: List[str] = []  # Related stock symbols
    sentiment_score: Optional[float] = None  # -1 to 1
    sentiment_label: Optional[SentimentScore] = None
    relevance_score: float = 0.0  # 0 to 1


class NewsSentiment(BaseModel):
    """Aggregated sentiment analysis."""
    symbol: str
    overall_sentiment: float  # -1 to 1
    sentiment_label: SentimentScore
    article_count: int
    bullish_count: int
    bearish_count: int
    neutral_count: int
    confidence: float  # 0 to 1
    last_updated: datetime


class MarketImpact(BaseModel):
    """Market impact assessment from news."""
    symbol: str
    impact_score: float  # 0 to 1
    expected_direction: str  # "up", "down", "neutral"
    expected_magnitude: float  # Percentage change
    confidence: float
    time_horizon: str  # "short", "medium", "long"


class SectorSentiment(BaseModel):
    """Aggregated sentiment analysis by sector."""
    sector: str
    overall_sentiment: float  # -1 to 1
    sentiment_label: SentimentScore
    article_count: int
    bullish_count: int
    bearish_count: int
    neutral_count: int
    confidence: float  # 0 to 1
    velocity: float  # -1 to 1 (rate of change)
    last_updated: datetime
