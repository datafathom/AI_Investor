"""
Tests for IBKR API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.ibkr_api import router, get_ibkr_client_provider, get_ibkr_gateway_provider


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
def mock_ibkr_client(api_app):
    """Mock IBKR Client."""
    client = AsyncMock()
    client.connected = True
    client.get_account_summary.return_value = {'NetLiquidation': 100000}
    client.get_positions.return_value = [{'symbol': 'AAPL', 'quantity': 10}]
    client.get_orders.return_value = [{'order_id': 1, 'status': 'Filled'}]
    client.place_order.return_value = {'order_id': 2, 'status': 'Submitted'}
    client.cancel_order.return_value = True
    client.get_margin_requirements.return_value = {'equity_with_loan': 50000}
    client.get_currency_exposure.return_value = {'USD': 1.0}
    api_app.dependency_overrides[get_ibkr_client_provider] = lambda: client
    return client


@pytest.fixture
def mock_ibkr_gateway(api_app):
    """Mock IBKR Gateway."""
    gateway = AsyncMock()
    gateway.get_session_status.return_value = {'status': 'Connected'}
    api_app.dependency_overrides[get_ibkr_gateway_provider] = lambda: gateway
    return gateway


def test_get_account_summary_success(client, mock_ibkr_client):
    """Test getting account summary."""
    response = client.get('/api/v1/ibkr/account-summary')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['NetLiquidation'] == 100000


def test_get_positions_success(client, mock_ibkr_client):
    """Test getting positions."""
    response = client.get('/api/v1/ibkr/positions')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['count'] == 1


def test_place_order_success(client, mock_ibkr_client):
    """Test placing an order."""
    response = client.post('/api/v1/ibkr/orders',
                           json={'contract': 'AAPL', 'action': 'BUY', 'quantity': 10})
    
    assert response.status_code == 201
    data = response.json()
    assert data['success'] is True
    assert data['data']['order']['order_id'] == 2


def test_cancel_order_success(client, mock_ibkr_client):
    """Test cancelling an order."""
    response = client.delete('/api/v1/ibkr/orders/1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'cancelled' in data['data']['message']


def test_get_gateway_status_success(client, mock_ibkr_gateway):
    """Test getting gateway status."""
    response = client.get('/api/v1/ibkr/gateway/status')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'Connected'
