"""
News & Sentiment Services Package

Provides news aggregation and sentiment analysis capabilities.
"""

from services.news.news_aggregation_service import NewsAggregationService
from services.news.sentiment_analysis_service import SentimentAnalysisService

__all__ = [
    "NewsAggregationService",
    "SentimentAnalysisService",
]
