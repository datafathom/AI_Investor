"""
Market Data API Tests
"""

from datetime import datetime
from unittest.mock import patch, MagicMock, AsyncMock

import pytest
from flask import Flask

from web.api.market_data_api import market_data_bp
from models.market_data import Quote, OHLCV


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(market_data_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(name="alpha_client_mock")
def fixture_alpha_client_mock():
    """Mock Alpha Vantage client with AsyncMock for async methods."""
    with patch('web.api.market_data_api._get_alpha_client') as mock:
        mock_client = MagicMock()
        # Use AsyncMock for async methods
        mock_client.get_quote = AsyncMock()
        mock_client.get_daily = AsyncMock()
        mock_client.get_intraday = AsyncMock()
        mock.return_value = mock_client
        yield mock_client


def test_get_quote_success(client, alpha_client_mock):
    """Test successful quote retrieval."""
    mock_quote = Quote(
        symbol='AAPL',
        price=150.0,
        open=149.0,
        high=151.0,
        low=148.0,
        volume=1000000,
        previous_close=149.5,
        change=0.5,
        change_percent="0.33%",
        latest_trading_day=datetime.now().date().isoformat(),
        timestamp=datetime.now(),
        source="alpha_vantage"
    )

    alpha_client_mock.get_quote.return_value = mock_quote

    response = client.get('/quote/AAPL')

    assert response.status_code == 200
    data = response.get_json()
    assert data['data']['symbol'] == 'AAPL'
    assert data['data']['price'] == 150.0


def test_get_quote_invalid_symbol(client):
    """Test quote retrieval with invalid symbol."""
    response = client.get('/quote/')

    assert response.status_code == 404


def test_get_history_success(client, alpha_client_mock):
    """Test successful historical data retrieval."""
    mock_ohclv = OHLCV(
        timestamp=datetime.now(), 
        open=150.0, 
        high=152.0, 
        low=149.0,
        close=151.0, 
        volume=1000000
    )
    mock_data = [
        mock_ohclv,
        OHLCV(
            timestamp=datetime.now(), 
            open=151.0, 
            high=153.0, 
            low=150.0,
            close=152.0, 
            volume=1100000
        )
    ]

    alpha_client_mock.get_daily.return_value = mock_data

    response = client.get('/history/AAPL?period=compact&adjusted=true')

    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data


def test_get_intraday_success(client, alpha_client_mock):
    """Test successful intraday data retrieval."""
    mock_data = [
        OHLCV(
            timestamp=datetime.now(), 
            open=150.0, 
            high=151.0, 
            low=149.0, 
            close=150.5,
            volume=500000
        )
    ]

    alpha_client_mock.get_intraday.return_value = mock_data

    response = client.get('/intraday/AAPL?interval=5min')

    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
