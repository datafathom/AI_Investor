"""
Tests for Payment Transfer API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.payment_transfer_api import router, get_social_auth_provider
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    # Mock current user
    app.dependency_overrides[get_current_user] = lambda: {'id': 'user_1', 'email': 'test@example.com'}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_social_service(api_app):
    """Mock Social Auth Service."""
    service = MagicMock()
    service.users = {"test@example.com": {"id": "user_1"}}
    service.get_linked_finance_vendors.return_value = ["paypal", "venmo"]
    service.transfer_funds.return_value = {"success": True, "transaction_id": "tx_123"}
    
    api_app.dependency_overrides[get_social_auth_provider] = lambda: service
    return service


def test_get_linked_vendors_success(client, mock_social_service):
    """Test getting linked vendors."""
    response = client.get('/api/v1/payment_transfer/linked-vendors')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert "paypal" in data['data']['linked_vendors']


def test_get_linked_vendors_user_not_found(client, mock_social_service):
    """Test getting vendors for unknown user."""
    mock_social_service.users = {}
    response = client.get('/api/v1/payment_transfer/linked-vendors')
    
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False


def test_transfer_funds_success(client, mock_social_service):
    """Test transferring funds."""
    payload = {"vendor": "paypal", "amount": 100.0, "direction": "deposit"}
    response = client.post('/api/v1/payment_transfer/transfer', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['transaction_id'] == "tx_123"


def test_transfer_funds_missing_data(client, mock_social_service):
    """Test transfer with missing data."""
    payload = {"vendor": "", "amount": 0}
    response = client.post('/api/v1/payment_transfer/transfer', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False


def test_transfer_funds_failure(client, mock_social_service):
    """Test transfer failure from service."""
    mock_social_service.transfer_funds.return_value = {"success": False, "error": "Insufficient funds"}
    payload = {"vendor": "paypal", "amount": 100.0}
    response = client.post('/api/v1/payment_transfer/transfer', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert "Insufficient funds" in data['detail']
