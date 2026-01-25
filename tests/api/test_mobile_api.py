"""
Tests for Mobile API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.mobile_api import router


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
def mock_mobile_service():
    """Mock MobileService."""
    with patch('web.api.mobile_api.get_mobile_service') as mock:
        service = AsyncMock()
        service.activate_kill_switch.return_value = True
        service.get_pending_authorizations.return_value = []
        service.authorize_trade.return_value = True
        mock.return_value = service
        yield service


def test_activate_kill_switch_success(client, mock_mobile_service):
    """Test successful kill switch activation."""
    response = client.post('/api/v1/mobile/kill-switch',
                          json={'biometric_token': 'token_123'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'


def test_list_pending_authorizations_success(client, mock_mobile_service):
    """Test successful authorizations listing."""
    response = client.get('/api/v1/mobile/authorize')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_decide_authorization_success(client, mock_mobile_service):
    """Test successful authorization decision."""
    response = client.post('/api/v1/mobile/authorize/auth_1',
                          json={'approve': True})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
