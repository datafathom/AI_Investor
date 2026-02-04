"""
Tests for News & Sentiment API Endpoints
Phase 16: News & Sentiment Analysis
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.news_api import router, get_news_aggregation_service, get_sentiment_analysis_service
from web.auth_utils import get_current_user


@pytest.fixture
def api_app(mock_news_aggregation_service, mock_sentiment_analysis_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_news_aggregation_service] = lambda: mock_news_aggregation_service
    app.dependency_overrides[get_sentiment_analysis_service] = lambda: mock_sentiment_analysis_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_news_aggregation_service():
    """Mock NewsAggregationService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_sentiment_analysis_service():
    """Mock SentimentAnalysisService."""
    service = AsyncMock()
    return service


def test_get_news_articles_success(client, mock_news_aggregation_service):
    """Test successful news articles retrieval."""
    from schemas.news import NewsArticle
    from datetime import datetime, timezone
    
    mock_articles = [
        NewsArticle(
            article_id='article_1',
            title='Test Article',
            content='Test content',
            source='Test Source',
            published_date=datetime.now(timezone.utc),
            symbols=['AAPL'],
            relevance_score=0.9
        )
    ]
    mock_news_aggregation_service.fetch_news.return_value = mock_articles
    
    response = client.get('/api/v1/news/articles?symbols=AAPL&limit=50')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_get_news_for_symbol_success(client, mock_news_aggregation_service):
    """Test successful symbol-specific news retrieval."""
    from schemas.news import NewsArticle
    from datetime import datetime, timezone
    
    mock_articles = [
        NewsArticle(
            article_id='article_1',
            title='Test Article',
            content='Test content',
            source='Test Source',
            published_date=datetime.now(timezone.utc),
            symbols=['AAPL'],
            relevance_score=0.9
        )
    ]
    mock_news_aggregation_service.get_news_for_symbol.return_value = mock_articles
    
    response = client.get('/api/v1/news/symbol/AAPL?limit=20')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_sentiment_success(client, mock_sentiment_analysis_service):
    """Test successful sentiment analysis."""
    from schemas.news import NewsSentiment, SentimentScore
    from datetime import datetime, timezone
    
    mock_sentiment = NewsSentiment(
        symbol='AAPL',
        overall_sentiment=0.65,
        sentiment_label=SentimentScore.BULLISH,
        article_count=10,
        bullish_count=7,
        bearish_count=1,
        neutral_count=2,
        confidence=0.8,
        last_updated=datetime.now(timezone.utc)
    )
    mock_sentiment_analysis_service.get_symbol_sentiment.return_value = mock_sentiment
    
    response = client.get('/api/v1/news/sentiment/AAPL')
    
    assert response.status_code == 200
    data = response.json()
    print(f"DEBUG SENTIMENT RESPONSE: {data}")
    assert data['success'] is True
    assert data['data']['symbol'] == 'AAPL'
    assert data['data']['overall_sentiment'] == 0.65
