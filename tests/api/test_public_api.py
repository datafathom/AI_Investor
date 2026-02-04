"""
Tests for Public API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.public_api import router, get_public_api_provider, get_developer_portal_provider
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
def mock_public_service(api_app):
    """Mock Public API Service."""
    service = AsyncMock()
    
    api_key = MagicMock()
    api_key.model_dump.return_value = {"id": "key_123", "key": "sk_test_123"}
    
    service.create_api_key.return_value = api_key
    service._get_api_key.return_value = api_key
    
    api_app.dependency_overrides[get_public_api_provider] = lambda: service
    return service


@pytest.fixture
def mock_portal_service(api_app):
    """Mock Developer Portal Service."""
    service = AsyncMock()
    service.get_api_documentation.return_value = {"version": "v1"}
    service.get_sdks.return_value = ["python", "nodejs"]
    
    api_app.dependency_overrides[get_developer_portal_provider] = lambda: service
    return service


def test_create_api_key_success(client, mock_public_service):
    """Test creating API key."""
    payload = {"user_id": "user_1", "tier": "free"}
    response = client.post('/api/v1/public/api-key/create', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['id'] == "key_123"


def test_get_api_key_success(client, mock_public_service):
    """Test getting API key."""
    response = client.get('/api/v1/public/api-key/key_123')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_api_key_not_found(client, mock_public_service):
    """Test getting unknown API key."""
    mock_public_service._get_api_key.return_value = None
    response = client.get('/api/v1/public/api-key/unknown')
    
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False


def test_get_documentation_success(client, mock_portal_service):
    """Test getting documentation."""
    response = client.get('/api/v1/public/documentation')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_sdks_success(client, mock_portal_service):
    """Test getting SDKs."""
    response = client.get('/api/v1/public/sdks')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert "python" in data['data']
