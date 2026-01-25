"""
Tests for News & Sentiment API Endpoints
Phase 16: News & Sentiment Analysis
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.news_api import news_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(news_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_news_aggregation_service():
    """Mock NewsAggregationService."""
    with patch('web.api.news_api.get_news_aggregation_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_sentiment_analysis_service():
    """Mock SentimentAnalysisService."""
    with patch('web.api.news_api.get_sentiment_analysis_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_get_news_articles_success(client, mock_news_aggregation_service):
    """Test successful news articles retrieval."""
    from models.news import NewsArticle
    
    mock_articles = [
        NewsArticle(
            article_id='article_1',
            title='Test Article',
            content='Test content',
            source='Test Source',
            published_at=None,
            symbols=['AAPL']
        )
    ]
    mock_news_aggregation_service.fetch_news.return_value = mock_articles
    
    response = client.get('/api/news/articles?symbols=AAPL,MSFT&limit=50')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1


@pytest.mark.asyncio
async def test_get_news_for_symbol_success(client, mock_news_aggregation_service):
    """Test successful symbol-specific news retrieval."""
    from models.news import NewsArticle
    
    mock_articles = [
        NewsArticle(
            article_id='article_1',
            title='Test Article',
            content='Test content',
            source='Test Source',
            published_at=None,
            symbols=['AAPL']
        )
    ]
    mock_news_aggregation_service.fetch_news_for_symbol.return_value = mock_articles
    
    response = client.get('/api/news/symbol/AAPL?limit=20')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_get_sentiment_success(client, mock_sentiment_analysis_service):
    """Test successful sentiment analysis."""
    from models.news import SentimentAnalysis
    
    mock_sentiment = SentimentAnalysis(
        symbol='AAPL',
        overall_sentiment=0.65,
        sentiment_score=0.7,
        article_count=10
    )
    mock_sentiment_analysis_service.analyze_sentiment.return_value = mock_sentiment
    
    response = client.get('/api/news/sentiment/AAPL')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['symbol'] == 'AAPL'
    assert data['data']['sentiment_score'] == 0.7
