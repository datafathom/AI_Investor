"""
Tests for News Aggregation Service
Comprehensive test coverage for news fetching, filtering, and aggregation
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from services.news.news_aggregation_service import NewsAggregationService
from models.news import NewsArticle


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.news.news_aggregation_service.get_cache_service'):
        return NewsAggregationService()


@pytest.mark.asyncio
async def test_fetch_news_with_symbols(service):
    """Test fetching news for specific symbols."""
    result = await service.fetch_news(
        symbols=['AAPL', 'MSFT'],
        limit=50,
        hours_back=24
    )
    
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(article, NewsArticle) for article in result)


@pytest.mark.asyncio
async def test_fetch_news_no_symbols(service):
    """Test fetching general news without symbols."""
    result = await service.fetch_news(
        symbols=None,
        limit=50,
        hours_back=24
    )
    
    assert result is not None
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_fetch_news_with_limit(service):
    """Test fetching news with limit."""
    result = await service.fetch_news(
        symbols=['AAPL'],
        limit=10,
        hours_back=24
    )
    
    assert result is not None
    assert len(result) <= 10


@pytest.mark.asyncio
async def test_get_news_by_symbol(service):
    """Test getting news for a specific symbol."""
    result = await service.get_news_by_symbol(
        symbol='AAPL',
        limit=20
    )
    
    assert result is not None
    assert isinstance(result, list)
    if len(result) > 0:
        assert all('AAPL' in article.symbols for article in result)


@pytest.mark.asyncio
async def test_filter_news_by_relevance(service):
    """Test filtering news by relevance score."""
    articles = [
        NewsArticle(
            article_id="1",
            title="Test Article 1",
            content="Content",
            source="Source",
            published_date=datetime.utcnow(),
            symbols=['AAPL'],
            relevance_score=0.9
        ),
        NewsArticle(
            article_id="2",
            title="Test Article 2",
            content="Content",
            source="Source",
            published_date=datetime.utcnow(),
            symbols=['AAPL'],
            relevance_score=0.3
        ),
    ]
    
    result = await service.filter_news_by_relevance(articles, min_relevance=0.5)
    
    assert result is not None
    assert len(result) == 1
    assert result[0].relevance_score >= 0.5
