"""
Tests for Binance API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.binance_api import binance_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(binance_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_binance_client():
    """Mock BinanceClient."""
    with patch('web.api.binance_api.get_binance_client') as mock:
        client = AsyncMock()
        client.get_ticker.return_value = {
            'symbol': 'BTCUSDT',
            'price': '50000.00',
            'priceChangePercent': '2.5'
        }
        client.get_order_book.return_value = {
            'bids': [[50000, 1.0]],
            'asks': [[50001, 1.0]]
        }
        client.place_order.return_value = {'orderId': 12345, 'status': 'NEW'}
        mock.return_value = client
        yield client


def test_get_ticker_success(client, mock_binance_client):
    """Test successful ticker retrieval."""
    response = client.get('/binance/ticker/BTCUSDT')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'symbol' in data or 'price' in data


def test_get_order_book_success(client, mock_binance_client):
    """Test successful order book retrieval."""
    response = client.get('/binance/depth/BTCUSDT?limit=5')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'bids' in data or 'asks' in data


def test_place_order_success(client, mock_binance_client):
    """Test successful order placement."""
    response = client.post('/binance/order',
                          json={
                              'symbol': 'BTCUSDT',
                              'side': 'BUY',
                              'quantity': 0.001
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'orderId' in data or 'status' in data
