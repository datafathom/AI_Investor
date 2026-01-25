"""
Tests for StockTwits API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.stocktwits_api import stocktwits_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(stocktwits_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_stocktwits_client():
    """Mock StockTwitsClient."""
    with patch('web.api.stocktwits_api.get_stocktwits_client') as mock:
        client = AsyncMock()
        client.get_symbol_stream.return_value = [
            {'id': 'msg_1', 'body': 'Test message', 'sentiment': 'bullish'}
        ]
        client.get_trending.return_value = ['AAPL', 'MSFT', 'GOOGL']
        client.analyze_sentiment.return_value = {'sentiment': 'bullish', 'score': 0.75}
        mock.return_value = client
        yield client


def test_get_stream_success(client, mock_stocktwits_client):
    """Test successful stream retrieval."""
    response = client.get('/api/v1/stocktwits/stream/AAPL')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'symbol' in data
    assert 'messages' in data


def test_get_trending_success(client, mock_stocktwits_client):
    """Test successful trending symbols retrieval."""
    response = client.get('/api/v1/stocktwits/trending')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'trending' in data or isinstance(data, list)


def test_get_sentiment_success(client, mock_stocktwits_client):
    """Test successful sentiment analysis."""
    response = client.get('/api/v1/stocktwits/sentiment/AAPL')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'sentiment' in data or 'score' in data
