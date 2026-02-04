"""
Tests for Social API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.social_api import router, get_reddit_provider


class MockPost:
    def __init__(self, id, title):
        self.id = id
        self.title = title
    def model_dump(self):
        return {"id": self.id, "title": self.title}


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_client(api_app):
    """Mock Reddit Client."""
    service = AsyncMock()
    service.get_subreddit_posts.return_value = [MockPost("p1", "GME to the moon")]
    service.analyze_sentiment.return_value = {"ticker": "GME", "sentiment": 0.8}
    
    api_app.dependency_overrides[get_reddit_provider] = lambda: service
    return service


def test_get_reddit_posts_success(client, mock_client):
    """Test getting reddit posts."""
    response = client.get('/api/v1/social/reddit/posts?subreddit=wallstreetbets')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'][0]['title'] == "GME to the moon"


def test_analyze_ticker_sentiment_success(client, mock_client):
    """Test analyzing ticker sentiment."""
    response = client.get('/api/v1/social/reddit/analyze/GME')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['sentiment'] == 0.8


def test_get_sentiment_heatmap_success(client):
    """Test getting sentiment heatmap."""
    response = client.get('/api/v1/social/sentiment/heatmap')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 6
