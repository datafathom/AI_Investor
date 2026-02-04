"""
Tests for Settlement API Endpoints
"""

import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.settlement_api import router, get_settlement_provider, get_cache_provider


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
def mock_service(api_app):
    """Mock Settlement Service."""
    service = MagicMock()
    service.get_balance_summary.return_value = {"USD": 10000.0, "EUR": 5000.0}
    service.get_rates.return_value = {"USD_EUR": 0.92, "EUR_USD": 1.08}
    service.convert_currency.return_value = {"status": "SUCCESS", "from": "USD", "to": "EUR", "amount": 100, "result": 92}
    
    api_app.dependency_overrides[get_settlement_provider] = lambda: service
    return service


@pytest.fixture
def mock_cache(api_app):
    """Mock Cache Service."""
    service = MagicMock()
    service.get.return_value = None
    
    api_app.dependency_overrides[get_cache_provider] = lambda: service
    return service


def test_get_balances_success(client, mock_service):
    """Test getting balances."""
    response = client.get('/api/v1/settlement/balances')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['USD'] == 10000.0


def test_get_rates_success(client, mock_service, mock_cache):
    """Test getting rates."""
    response = client.get('/api/v1/settlement/rates')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['USD_EUR'] == 0.92


def test_convert_currency_success(client, mock_service):
    """Test converting currency."""
    payload = {"from": "USD", "to": "EUR", "amount": 100.0}
    response = client.post('/api/v1/settlement/convert', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['result'] == 92


def test_convert_currency_missing_params(client):
    """Test missing parameters."""
    payload = {"from": "USD"}
    response = client.post('/api/v1/settlement/convert', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
