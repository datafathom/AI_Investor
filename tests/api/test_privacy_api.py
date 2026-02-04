"""
Tests for Privacy API Endpoints
"""

import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.privacy_api import router, get_privacy_provider
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
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
def mock_privacy_service(api_app):
    """Mock Privacy Service."""
    service = MagicMock()
    service.export_user_data.return_value = {"email": "test@example.com", "trades": []}
    service.delete_user_account.return_value = True
    
    api_app.dependency_overrides[get_privacy_provider] = lambda: service
    return service


def test_export_data_success(client, mock_privacy_service):
    """Test exporting data."""
    response = client.get('/api/v1/privacy/export')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['email'] == "test@example.com"
    assert response.headers['Content-Disposition'] == 'attachment;filename=my_data.json'


def test_delete_account_success(client, mock_privacy_service):
    """Test deleting account."""
    response = client.delete('/api/v1/privacy/forget-me')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert "deleted successfully" in data['data']['message']


def test_delete_account_failure(client, mock_privacy_service):
    """Test deleting account failure."""
    mock_privacy_service.delete_user_account.return_value = False
    response = client.delete('/api/v1/privacy/forget-me')
    
    assert response.status_code == 500
    data = response.json()
    assert data['success'] is False
