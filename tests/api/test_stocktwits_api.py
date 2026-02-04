"""
Tests for StockTwits API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.stocktwits_api import router, get_stocktwits_provider, get_sentiment_provider


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
    """Mock StockTwits Client."""
    service = AsyncMock()
    service.get_symbol_stream.return_value = [{"id": 1, "body": "Bullish on AAPL"}]
    service.get_trending_symbols.return_value = [{"symbol": "TSLA", "watchlist_count": 1000}]
    
    api_app.dependency_overrides[get_stocktwits_provider] = lambda: service
    return service


@pytest.fixture
def mock_analyzer(api_app):
    """Mock StockTwits Sentiment."""
    service = AsyncMock()
    service.analyze_symbol.return_value = {"symbol": "AAPL", "sentiment": 0.5}
    service.detect_volume_spikes.return_value = {"symbol": "AAPL", "spike": True}
    
    api_app.dependency_overrides[get_sentiment_provider] = lambda: service
    return service


def test_get_stream_success(client, mock_client):
    """Test getting stream."""
    response = client.get('/api/v1/stocktwits/stream/AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['symbol'] == "AAPL"


def test_get_trending_success(client, mock_client):
    """Test getting trending."""
    response = client.get('/api/v1/stocktwits/trending')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['trending']) == 1


def test_analyze_sentiment_success(client, mock_analyzer):
    """Test analyzing sentiment."""
    response = client.get('/api/v1/stocktwits/sentiment/AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['sentiment'] == 0.5


def test_detect_volume_spike_success(client, mock_analyzer):
    """Test detecting volume spike."""
    response = client.get('/api/v1/stocktwits/volume-spike/AAPL?threshold=50')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['spike'] is True
