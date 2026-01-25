"""
Tests for Integrations API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.integrations_api import router


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
def mock_integrations_service():
    """Mock IntegrationsService."""
    with patch('web.api.integrations_api.get_integrations_service') as mock:
        service = AsyncMock()
        from services.trading.integrations_service import APIConnector, APIKey, Webhook
        mock_connector = APIConnector(
            id='conn_1',
            name='Test Connector',
            type='brokerage',
            status='active',
            last_sync='2024-01-01'
        )
        service.get_connectors.return_value = [mock_connector]
        service.test_connector.return_value = {'status': 'success', 'latency_ms': 50}
        mock_key = APIKey(
            id='key_1',
            label='Test Key',
            prefix='sk_test_',
            created_at='2024-01-01'
        )
        service.get_api_keys.return_value = [mock_key]
        mock_webhook = Webhook(
            id='webhook_1',
            url='https://example.com/webhook',
            events=['trade.executed'],
            status='active'
        )
        service.create_webhook.return_value = mock_webhook
        service.list_webhooks.return_value = [mock_webhook]
        mock.return_value = service
        yield service


def test_list_connectors_success(client, mock_integrations_service):
    """Test successful connectors listing."""
    response = client.get('/api/v1/integrations/connectors')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_test_connector_success(client, mock_integrations_service):
    """Test successful connector testing."""
    response = client.post('/api/v1/integrations/connectors/conn_1/test')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data or 'latency_ms' in data


def test_list_api_keys_success(client, mock_integrations_service):
    """Test successful API keys listing."""
    response = client.get('/api/v1/integrations/keys')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_create_webhook_success(client, mock_integrations_service):
    """Test successful webhook creation."""
    response = client.post('/api/v1/integrations/webhooks',
                          json={
                              'url': 'https://example.com/webhook',
                              'events': ['trade.executed']
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data or 'webhook_id' in data
