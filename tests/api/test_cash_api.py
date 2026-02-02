"""
Tests for Cash API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.cash_api import router


@pytest.fixture
def mock_fx_service_obj():
    """Create Mock FXService object."""
    service = AsyncMock()
    from services.trading.fx_service import FXRate, CurrencyBalance, SweepSuggestion, RepoRate, ConversionResult
    
    # Mock Models
    mock_rate = FXRate(
        pair='EUR/USD',
        base='EUR',
        quote='USD',
        rate=1.10,
        bid=1.0995,
        ask=1.1005,
        spread_bps=10.0,
        change_24h=0.01
    )
    service.get_fx_rates.return_value = [mock_rate]
    
    mock_balance = CurrencyBalance(
        currency='USD',
        amount=100000.0,
        amount_usd=100000.0,
        interest_rate=0.05
    )
    service.get_balances.return_value = [mock_balance]
    service.get_total_value_usd.return_value = 100000.0
    
    service.convert_currency.return_value = ConversionResult(
        from_currency='USD',
        to_currency='EUR',
        from_amount=1000.0,
        to_amount=909.09,
        rate_used=1.10,
        spread_cost=0.05,
        timestamp='2023-01-01T12:00:00Z'
    )
    
    service.execute_conversion.return_value = ConversionResult(
        from_currency='USD',
        to_currency='EUR',
        from_amount=1000.0,
        to_amount=909.09,
        rate_used=1.10,
        spread_cost=0.05,
        timestamp='2023-01-01T12:00:00Z'
    )
    service.check_exposure_limit.return_value = False
    
    mock_suggestion = SweepSuggestion(
        id='sweep_1',
        from_currency='USD',
        to_vehicle='MMF',
        amount=50000.0,
        projected_yield=0.05,
        risk='low',
        description='Money Market Fund'
    )
    service.get_sweep_suggestions.return_value = [mock_suggestion]
    service.execute_sweep.return_value = True
    
    mock_repo = RepoRate(
        region='US',
        name='SOFR',
        rate=0.05,
        change=0.001
    )
    service.get_repo_rates.return_value = [mock_repo]
    
    return service


@pytest.fixture
def app(mock_fx_service_obj):
    """Create FastAPI app for testing with overrides."""
    app = FastAPI()
    app.include_router(router)
    
    # Override Dependency
    from services.trading.fx_service import get_fx_service
    app.dependency_overrides[get_fx_service] = lambda: mock_fx_service_obj
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


def test_get_dashboard_success(client, mock_fx_service_obj):
    """Test successful dashboard retrieval."""
    response = client.get('/api/v1/cash/dashboard')
    
    assert response.status_code == 200
    data = response.json()
    assert 'balances' in data or 'dashboard' in data


def test_get_fx_rates_success(client, mock_fx_service_obj):
    """Test successful FX rates retrieval."""
    response = client.get('/api/v1/cash/fx/rates')
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert 'rates' in data


def test_convert_currency_success(client, mock_fx_service_obj):
    """Test successful currency conversion."""
    response = client.post('/api/v1/cash/fx/convert',
                          json={
                              'from_currency': 'USD',
                              'to_currency': 'EUR',
                              'amount': 1000.0
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert 'to_amount' in data


def test_get_sweep_suggestions_success(client, mock_fx_service_obj):
    """Test successful sweep suggestions retrieval."""
    response = client.get('/api/v1/cash/sweep/suggestions')
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
