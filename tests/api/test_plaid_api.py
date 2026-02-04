"""
Tests for Plaid API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.plaid_api import router, get_plaid_provider


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
def mock_plaid_service(api_app):
    """Mock Plaid Service."""
    service = AsyncMock()
    service.create_link_token.return_value = "link-token-123"
    service.exchange_public_token.return_value = {
        "item_id": "item_123",
        "accounts": ["acc_1"],
        "access_token": "access_123"
    }
    service.get_accounts.return_value = [{"id": "acc_1", "name": "Checking"}]
    service.get_balance.return_value = {"acc_1": 5000.0}
    service.check_overdraft_protection.return_value = {"safe": True}
    
    api_app.dependency_overrides[get_plaid_provider] = lambda: service
    return service


def test_create_link_token_success(client, mock_plaid_service):
    """Test creating link token."""
    response = client.post('/api/v1/plaid/link-token', json={"client_name": "Test"})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['link_token'] == "link-token-123"


def test_exchange_token_success(client, mock_plaid_service):
    """Test exchanging token."""
    response = client.post('/api/v1/plaid/exchange-token', json={"public_token": "public_123"})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['access_token'] == "access_123"


def test_get_accounts_success(client, mock_plaid_service):
    """Test getting accounts."""
    headers = {"Authorization": "Bearer access_123"}
    response = client.get('/api/v1/plaid/accounts', headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['accounts']) == 1


def test_get_balance_success(client, mock_plaid_service):
    """Test getting balance."""
    headers = {"Authorization": "Bearer access_123"}
    response = client.get('/api/v1/plaid/balance', headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['acc_1'] == 5000.0


def test_check_overdraft_success(client, mock_plaid_service):
    """Test checking overdraft."""
    headers = {"Authorization": "Bearer access_123"}
    payload = {"account_id": "acc_1", "deposit_amount": 100.0}
    response = client.post('/api/v1/plaid/check-overdraft', json=payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['safe'] is True


def test_get_accounts_invalid_header(client, mock_plaid_service):
    """Test with invalid auth header."""
    headers = {"Authorization": "Invalid access_123"}
    response = client.get('/api/v1/plaid/accounts', headers=headers)
    
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False
