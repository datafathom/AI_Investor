"""
Tests for Robinhood API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.robinhood_api import router, get_robinhood_provider


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
    """Mock Robinhood Service."""
    service = AsyncMock()
    service.login.return_value = True
    service.get_holdings.return_value = [{"symbol": "AAPL", "quantity": 10}]
    service.get_orders.return_value = [{"id": "ord_1", "symbol": "AAPL", "side": "buy"}]
    service.get_historical_transactions.return_value = [{"id": "tx_1", "symbol": "AAPL", "amount": 1000}]
    service.calculate_cost_basis.return_value = {"symbol": "AAPL", "cost_basis": 150.0}
    
    api_app.dependency_overrides[get_robinhood_provider] = lambda: service
    return service


def test_connect_account_success(client, mock_service):
    """Test connecting account."""
    payload = {"username": "testuser", "password": "password123"}
    response = client.post('/api/v1/robinhood/connect', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert "Robinhood account connected successfully" in data['data']['message']


def test_connect_account_failure(client, mock_service):
    """Test connection failure."""
    mock_service.login.return_value = False
    payload = {"username": "testuser", "password": "wrongpassword"}
    response = client.post('/api/v1/robinhood/connect', json=payload)
    
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False


def test_get_holdings_success(client, mock_service):
    """Test getting holdings."""
    response = client.get('/api/v1/robinhood/holdings')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['holdings']) == 1


def test_get_orders_success(client, mock_service):
    """Test getting orders."""
    response = client.get('/api/v1/robinhood/orders?limit=10')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['orders']) == 1


def test_get_transactions_success(client, mock_service):
    """Test getting transactions."""
    response = client.get('/api/v1/robinhood/transactions')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_calculate_cost_basis_success(client, mock_service):
    """Test calculating cost basis."""
    response = client.get('/api/v1/robinhood/cost-basis?symbol=AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['cost_basis'] == 150.0
