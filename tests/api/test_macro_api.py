"""
Tests for Macro API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.macro_api import router, get_macro_provider, get_futures_provider


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
def mock_macro_service(api_app):
    """Mock Macro Service."""
    service = AsyncMock()
    
    # Mock insider trade
    trade = MagicMock()
    trade.politician = "Alice Smith"
    trade.party = "Blue"
    trade.country = "US"
    trade.ticker = "AAPL"
    trade.action = "BUY"
    trade.amount = 50000
    trade.trade_date = "2026-01-01"
    trade.disclosure_date = "2026-01-15"
    trade.delay_days = 14
    service.get_political_insider_trades.return_value = [trade]
    
    # Mock CPI
    cpi = MagicMock()
    cpi.country_code = "US"
    cpi.country_name = "United States"
    cpi.current_cpi = 310.5
    cpi.yoy_change = 3.2
    cpi.core_cpi = 3.8
    cpi.updated_at = "2026-01-01T00:00:00"
    service.get_regional_cpi.return_value = cpi
    
    # Mock Correlations
    matrix = MagicMock()
    matrix.assets = ["Gold", "BTC"]
    matrix.correlations = [[1.0, 0.5], [0.5, 1.0]]
    matrix.best_hedge = "Gold"
    matrix.worst_hedge = "Silver"
    service.get_inflation_hedge_correlations.return_value = matrix
    
    service.get_world_map_data.return_value = {"US": 1.0}
    service.get_economic_calendar.return_value = [{"event": "FOMC"}]
    
    # Mock regime
    regime = MagicMock()
    regime.status = "Expansion"
    regime.signals = ["High Yield Narrowing"]
    regime.metrics = {"GDP": 2.5}
    regime.health_score = 75
    regime.timestamp.isoformat.return_value = "2026-01-01T00:00:00"
    service._fred.get_macro_regime = AsyncMock(return_value=regime)
    
    api_app.dependency_overrides[get_macro_provider] = lambda: service
    return service


@pytest.fixture
def mock_futures_service(api_app):
    """Mock Futures Service."""
    service = AsyncMock()
    
    # Mock Curve
    curve = MagicMock()
    curve.commodity = "CL"
    curve.commodity_name = "Crude Oil"
    curve.spot_price = 75.0
    curve.curve_shape = "Backwardation"
    curve.updated_at = "2026-01-01T00:00:00"
    
    contract = MagicMock()
    contract.symbol = "CLH6"
    contract.expiry_date = "2026-03-20"
    contract.price = 74.0
    contract.volume = 100000
    contract.open_interest = 500000
    curve.contracts = [contract]
    
    service.get_futures_curve.return_value = curve
    service.calculate_roll_yield.return_value = 5.2
    service.get_all_curves.return_value = [curve]
    
    # Mock Spread
    spread = MagicMock()
    spread.name = "3:2:1 Crack Spread"
    spread.value = 25.4
    spread.historical_mean = 20.0
    spread.z_score = 1.2
    spread.components = {"WTI": 75.0, "Gasoline": 100.0, "Heating Oil": 95.0}
    service.calculate_crack_spread.return_value = spread
    
    api_app.dependency_overrides[get_futures_provider] = lambda: service
    return service


def test_get_insider_trades_success(client, mock_macro_service):
    """Test getting insider trades."""
    response = client.get('/api/v1/macro/insider-trades')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'][0]['politician'] == "Alice Smith"


def test_get_cpi_success(client, mock_macro_service):
    """Test getting CPI."""
    response = client.get('/api/v1/macro/cpi/US')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['country_name'] == "United States"


def test_get_futures_curve_success(client, mock_futures_service):
    """Test getting futures curve."""
    response = client.get('/api/v1/macro/futures/CL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['commodity'] == "CL"


def test_get_crack_spread_success(client, mock_futures_service):
    """Test getting crack spread."""
    response = client.get('/api/v1/macro/crack-spread')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['value'] == 25.4


def test_get_macro_dashboard_success(client, mock_macro_service):
    """Test getting macro dashboard."""
    response = client.get('/api/v1/macro/dashboard')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'world_map_data' in data['data']
    assert 'political_signals' in data['data']


def test_get_macro_regime_success(client, mock_macro_service):
    """Test getting macro regime."""
    response = client.get('/api/v1/macro/regime')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "Expansion"
