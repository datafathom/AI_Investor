"""
Tests for Integrations API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.integrations_api import router, get_integrations_provider
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
def mock_integrations_service(api_app):
    """Mock Integrations Service."""
    service = AsyncMock()
    
    # Mock connector objects
    c1 = MagicMock()
    c1.id = 'conn_1'
    c1.name = 'Slack'
    c1.type = 'messenger'
    c1.status = 'active'
    c1.last_sync = '2026-01-01T00:00:00'
    service.get_connectors.return_value = [c1]
    
    service.get_available_integrations.return_value = [{'id': 'slack', 'name': 'Slack'}]
    service.get_connected_integrations.return_value = [{'id': 'conn_1', 'name': 'Slack'}]
    service.test_connector.return_value = {'status': 'success'}
    
    # Mock key objects
    k1 = MagicMock()
    k1.id = 'key_1'
    k1.label = 'Production'
    k1.prefix = 'ak_'
    k1.created_at = '2026-01-01T00:00:00'
    service.get_api_keys.return_value = [k1]
    
    service.create_api_key.return_value = {'id': 'key_2', 'key': 'secret_key'}
    
    # Mock webhook objects
    w1 = MagicMock()
    w1.model_dump.return_value = {'url': 'http://example.com/webhook', 'events': ['order.filled']}
    service.get_webhooks.return_value = [w1]
    
    service.add_webhook.return_value = {'id': 'wh_1', 'status': 'active'}
    
    api_app.dependency_overrides[get_integrations_provider] = lambda: service
    return service


def test_list_connectors_success(client, mock_integrations_service):
    """Test listing connectors."""
    response = client.get('/api/v1/integrations/connectors')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'][0]['name'] == 'Slack'


def test_list_available_integrations_success(client, mock_integrations_service):
    """Test listing available integrations."""
    response = client.get('/api/v1/integrations/available')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'][0]['id'] == 'slack'


def test_test_connector_success(client, mock_integrations_service):
    """Test testing a connector."""
    response = client.post('/api/v1/integrations/connectors/conn_1/test')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'success'


def test_list_keys_success(client, mock_integrations_service):
    """Test listing API keys."""
    response = client.get('/api/v1/integrations/keys')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'][0]['label'] == 'Production'


def test_add_webhook_success(client, mock_integrations_service):
    """Test adding a webhook."""
    response = client.post('/api/v1/integrations/webhooks',
                           json={'url': 'http://example.com/webhook', 'events': ['trade.executed']})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'active'
