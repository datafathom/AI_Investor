"""
Tests for Mobile API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.mobile_api import router, get_mobile_provider


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
def mock_mobile_service(api_app):
    """Mock Mobile Service."""
    service = AsyncMock()
    
    service.activate_kill_switch.return_value = True
    
    auth = MagicMock()
    auth.model_dump.return_value = {"id": "auth_123", "symbol": "AAPL", "action": "BUY"}
    service.get_pending_authorizations.return_value = [auth]
    
    service.authorize_trade.return_value = True
    
    api_app.dependency_overrides[get_mobile_provider] = lambda: service
    return service


def test_activate_kill_switch_success(client, mock_mobile_service):
    """Test activating kill switch."""
    response = client.post('/api/v1/mobile/kill-switch', json={'biometric_token': 'token_123'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['message'] == "Kill switch activated"


def test_activate_kill_switch_failure(client, mock_mobile_service):
    """Test activating kill switch with invalid token."""
    mock_mobile_service.activate_kill_switch.return_value = False
    response = client.post('/api/v1/mobile/kill-switch', json={'biometric_token': 'invalid'})
    
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False


def test_list_pending_authorizations_success(client, mock_mobile_service):
    """Test listing authorizations."""
    response = client.get('/api/v1/mobile/authorize')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_decide_authorization_success(client, mock_mobile_service):
    """Test authorizing trade."""
    response = client.post('/api/v1/mobile/authorize/auth_123', json={'approve': True})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_decide_authorization_not_found(client, mock_mobile_service):
    """Test authorizing non-existent trade."""
    mock_mobile_service.authorize_trade.return_value = False
    response = client.post('/api/v1/mobile/authorize/invalid', json={'approve': True})
    
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
