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
def app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_fx_service():
    """Mock FXService."""
    with patch('web.api.cash_api.get_fx_service') as mock:
        service = AsyncMock()
        from services.trading.fx_service import FXRate, CurrencyBalance, SweepSuggestion, RepoRate
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
        service.convert_currency.return_value = ConversionResult(
            from_currency='USD',
            to_currency='EUR',
            amount=1000.0,
            converted_amount=909.09,
            rate=1.10
        )
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
        service.execute_sweep.return_value = {'status': 'success', 'sweep_id': 'sweep_1'}
        mock_repo = RepoRate(
            region='US',
            name='SOFR',
            rate=0.05,
            change=0.001
        )
        service.get_repo_rates.return_value = [mock_repo]
        mock.return_value = service
        yield service


def test_get_dashboard_success(client, mock_fx_service):
    """Test successful dashboard retrieval."""
    response = client.get('/api/v1/cash/dashboard')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'balances' in data or 'dashboard' in data


def test_get_fx_rates_success(client, mock_fx_service):
    """Test successful FX rates retrieval."""
    response = client.get('/api/v1/cash/fx/rates')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'rates' in data


def test_convert_currency_success(client, mock_fx_service):
    """Test successful currency conversion."""
    response = client.post('/api/v1/cash/fx/convert',
                          json={
                              'from_currency': 'USD',
                              'to_currency': 'EUR',
                              'amount': 1000.0
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'converted_amount' in data or 'result' in data


def test_get_sweep_suggestions_success(client, mock_fx_service):
    """Test successful sweep suggestions retrieval."""
    response = client.get('/api/v1/cash/sweep/suggestions')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'suggestions' in data
