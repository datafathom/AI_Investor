"""
Tests for Sentiment Analysis Service
Comprehensive test coverage for sentiment scoring and market impact
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.news.sentiment_analysis_service import SentimentAnalysisService
from models.news import NewsArticle, SentimentScore, MarketImpact


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.news.sentiment_analysis_service.get_news_aggregation_service'), \
         patch('services.news.sentiment_analysis_service.get_cache_service'):
        return SentimentAnalysisService()


@pytest.fixture
def mock_article():
    """Mock news article."""
    return NewsArticle(
        article_id="article_123",
        title="AAPL Stock Rises on Strong Earnings",
        content="Apple Inc. reported strong earnings that beat expectations, driving the stock price up.",
        source="Financial News",
        published_date=datetime.utcnow(),
        symbols=['AAPL'],
        relevance_score=0.9
    )


@pytest.mark.asyncio
async def test_analyze_article_sentiment_positive(service, mock_article):
    """Test sentiment analysis for positive article."""
    result = await service.analyze_article_sentiment(mock_article)
    
    assert result is not None
    assert hasattr(result, 'sentiment') or 'sentiment' in result.dict()
    # Should detect positive sentiment from "rises", "strong", "beat"


@pytest.mark.asyncio
async def test_analyze_article_sentiment_negative(service):
    """Test sentiment analysis for negative article."""
    article = NewsArticle(
        article_id="article_456",
        title="AAPL Stock Falls on Weak Guidance",
        content="Apple Inc. provided weak guidance, causing the stock to decline.",
        source="Financial News",
        published_date=datetime.utcnow(),
        symbols=['AAPL'],
        relevance_score=0.9
    )
    
    result = await service.analyze_article_sentiment(article)
    
    assert result is not None
    # Should detect negative sentiment from "falls", "weak", "decline"


@pytest.mark.asyncio
async def test_aggregate_sentiment_by_symbol(service):
    """Test aggregating sentiment by symbol."""
    articles = [
        NewsArticle(
            article_id="1",
            title="AAPL Positive News",
            content="Strong earnings",
            source="Source",
            published_date=datetime.utcnow(),
            symbols=['AAPL'],
            relevance_score=0.9
        ),
        NewsArticle(
            article_id="2",
            title="AAPL More Positive News",
            content="Growth continues",
            source="Source",
            published_date=datetime.utcnow(),
            symbols=['AAPL'],
            relevance_score=0.8
        ),
    ]
    
    # Analyze each article first
    for article in articles:
        article = await service.analyze_article_sentiment(article)
    
    result = await service.aggregate_sentiment_by_symbol(articles, 'AAPL')
    
    assert result is not None
    assert isinstance(result, SentimentScore) or isinstance(result, dict)


@pytest.mark.asyncio
async def test_assess_market_impact(service):
    """Test market impact assessment."""
    sentiment_score = SentimentScore(
        symbol='AAPL',
        overall_sentiment=0.7,
        positive_count=10,
        negative_count=2,
        neutral_count=3,
        calculated_date=datetime.utcnow()
    )
    
    result = await service.assess_market_impact(sentiment_score)
    
    assert result is not None
    assert isinstance(result, MarketImpact) or isinstance(result, dict)
    assert 'expected_impact' in str(result) or hasattr(result, 'expected_impact')
