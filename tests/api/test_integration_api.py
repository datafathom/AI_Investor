"""
Tests for Integration API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.integration_api import router, get_integration_framework_provider, get_integration_service_provider


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
def mock_integration_framework(api_app):
    """Mock Integration Framework."""
    framework = AsyncMock()
    integration = MagicMock()
    integration.model_dump.return_value = {'id': 'int_123', 'app_name': 'Slack'}
    framework.create_integration.return_value = integration
    api_app.dependency_overrides[get_integration_framework_provider] = lambda: framework
    return framework


@pytest.fixture
def mock_integration_service(api_app):
    """Mock Integration Service."""
    service = AsyncMock()
    job = MagicMock()
    job.model_dump.return_value = {'job_id': 'job_123', 'status': 'PENDING'}
    service.sync_data.return_value = job
    api_app.dependency_overrides[get_integration_service_provider] = lambda: service
    return service


def test_create_integration_success(client, mock_integration_framework):
    """Test creating an integration."""
    response = client.post('/api/v1/integration/create',
                           json={'user_id': 'user_1', 'app_name': 'Slack'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['app_name'] == 'Slack'


def test_get_user_integrations_success(client):
    """Test getting user integrations."""
    response = client.get('/api/v1/integration/user/user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)


def test_sync_integration_success(client, mock_integration_service):
    """Test syncing an integration."""
    response = client.post('/api/v1/integration/int_123/sync',
                           json={'sync_type': 'full'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['job_id'] == 'job_123'
