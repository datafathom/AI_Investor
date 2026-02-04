"""
Tests for Market Data API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.market_data_api import router, get_alpha_provider
from unittest.mock import patch


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_alpha_client(api_app):
    """Mock Alpha Vantage Client."""
    service = MagicMock()
    
    # Mock quote
    quote = MagicMock()
    quote.symbol = "AAPL"
    quote.price = 150.0
    quote.open = 149.0
    quote.high = 151.0
    quote.low = 148.0
    quote.volume = 1000000
    quote.previous_close = 149.5
    quote.change = 0.5
    quote.change_percent = 0.33
    quote.latest_trading_day = "2026-01-01"
    quote.timestamp.isoformat.return_value = "2026-01-01T16:00:00"
    service.get_quote.return_value = quote
    
    # Mock bars
    bar = MagicMock()
    bar.timestamp.isoformat.return_value = "2026-01-01T09:30:00"
    bar.open = 150.0
    bar.high = 151.0
    bar.low = 149.0
    bar.close = 150.5
    bar.adjusted_close = 150.5
    bar.volume = 100000
    bar.dividend = 0.0
    bar.split_coefficient = 1.0
    
    service.get_daily.return_value = [bar]
    service.get_intraday.return_value = [bar]
    
    # Mock earnings
    earning = MagicMock()
    earning.symbol = "AAPL"
    earning.name = "Apple Inc."
    earning.report_date = "2026-01-28"
    earning.fiscal_date_ending = "2025-12-31"
    earning.estimate = 1.25
    earning.currency = "USD"
    service.get_earnings_calendar.return_value = [earning]
    
    api_app.dependency_overrides[get_alpha_provider] = lambda: service
    return service


def test_get_quote_success(client, mock_alpha_client):
    """Test getting real-time quote."""
    response = client.get('/api/v1/market/quote/AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['content']['symbol'] == "AAPL"


def test_get_fear_greed_success(client):
    """Test getting fear & greed index."""
    response = client.get('/api/v1/market/fear-greed')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'score' in data['data']['content']


def test_get_history_success(client, mock_alpha_client):
    """Test getting historical data."""
    response = client.get('/api/v1/market/history/AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['content']['symbol'] == "AAPL"
    assert len(data['data']['content']['bars']) == 1


def test_get_intraday_success(client, mock_alpha_client):
    """Test getting intraday data."""
    response = client.get('/api/v1/market/intraday/AAPL?interval=5min')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['content']['interval'] == "5min"


def test_get_earnings_success(client, mock_alpha_client):
    """Test getting earnings calendar."""
    response = client.get('/api/v1/market/earnings')
    
    _data = response.json()
    assert response.status_code == 200
    assert _data['success'] is True
    assert _data['data']['content']['count'] == 1


def test_get_market_health_success(client):
    """Test market health check."""
    mock_governor = MagicMock()
    mock_governor._usage = {"ALPHA_VANTAGE": {"day_count": 10, "minute_count": 1}}
    mock_governor.LIMITS = {"ALPHA_VANTAGE": {"per_day": 500, "per_minute": 5}}
    
    with patch("services.system.api_governance.get_governor", return_value=mock_governor):
        response = client.get('/api/v1/market/health')
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'overall_status' in data['data']['content']
