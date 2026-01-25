"""
Market Data API Tests
"""

from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest
from flask import Flask

from web.api.market_data_api import market_data_bp
from models.market_data import Quote, OHLCV


@pytest.fixture(name="app_instance")
def fixture_app_instance():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(market_data_bp)
    return app


@pytest.fixture(name="test_client")
def fixture_test_client(app_instance):
    """Create test client."""
    return app_instance.test_client()


@pytest.fixture(name="alpha_client_mock")
def fixture_alpha_client_mock():
    """Mock Alpha Vantage client."""
    with patch('web.api.market_data_api._get_alpha_client') as mock:
        mock_client = MagicMock()
        mock.return_value = mock_client
        yield mock_client


def test_get_quote_success(test_client, alpha_client_mock):
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
        timestamp=datetime.now()
    )

    async def mock_get_quote(_symbol):
        return mock_quote

    alpha_client_mock.get_quote = mock_get_quote

    response = test_client.get('/quote/AAPL')

    assert response.status_code == 200
    data = response.get_json()
    assert data['data']['symbol'] == 'AAPL'
    assert data['data']['price'] == 150.0


def test_get_quote_invalid_symbol(test_client):
    """Test quote retrieval with invalid symbol."""
    response = test_client.get('/quote/')

    assert response.status_code == 404


def test_get_history_success(test_client, alpha_client_mock):
    """Test successful historical data retrieval."""
    mock_ohclv = OHLCV(timestamp=datetime.now(), open=150.0, high=152.0, low=149.0,
                       close=151.0, volume=1000000)
    mock_data = [
        mock_ohclv,
        OHLCV(timestamp=datetime.now(), open=151.0, high=153.0, low=150.0,
              close=152.0, volume=1100000)
    ]

    async def mock_get_daily(_symbol, **_kwargs):
        return mock_data

    alpha_client_mock.get_daily = mock_get_daily

    response = test_client.get('/history/AAPL?period=compact&adjusted=true')

    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data


def test_get_intraday_success(test_client, alpha_client_mock):
    """Test successful intraday data retrieval."""
    mock_data = [
        OHLCV(timestamp=datetime.now(), open=150.0, high=151.0, low=149.0, close=150.5,
              volume=500000)
    ]

    async def mock_get_intraday(_symbol, **_kwargs):
        return mock_data

    alpha_client_mock.get_intraday = mock_get_intraday

    response = test_client.get('/intraday/AAPL?interval=5min')

    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
