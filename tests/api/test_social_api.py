"""
Tests for Social API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.social_api import social_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(social_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_reddit_client():
    """Mock RedditClient."""
    with patch('web.api.social_api.get_reddit_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_get_reddit_posts_success(client, mock_reddit_client):
    """Test successful Reddit posts retrieval."""
    from models.social import RedditPost
    
    mock_posts = [
        RedditPost(
            post_id='post_1',
            title='Test Post',
            subreddit='wallstreetbets',
            score=100,
            upvote_ratio=0.95
        )
    ]
    
    async def mock_get_posts(subreddit, limit):
        return mock_posts
    
    mock_reddit_client.get_subreddit_posts = mock_get_posts
    
    response = client.get('/reddit/posts?subreddit=wallstreetbets&limit=10&mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_analyze_ticker_sentiment_success(client, mock_reddit_client):
    """Test successful ticker sentiment analysis."""
    mock_result = {'sentiment': 'bullish', 'score': 0.75, 'mentions': 50}
    
    async def mock_analyze(ticker):
        return mock_result
    
    mock_reddit_client.analyze_sentiment = mock_analyze
    
    response = client.get('/reddit/analyze/AAPL?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'sentiment' in data or 'score' in data
