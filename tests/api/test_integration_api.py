"""
Tests for Integration API Endpoints (Flask version)
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.integration_api import integration_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(integration_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_integration_framework():
    """Mock IntegrationFramework."""
    with patch('web.api.integration_api.get_integration_framework') as mock:
        framework = AsyncMock()
        from models.integration import Integration, IntegrationStatus
        from datetime import datetime
        mock_integration = Integration(
            integration_id='int_1',
            user_id='user_1',
            app_name='mint',
            status=IntegrationStatus.CONNECTED,
            oauth_token='token_123',
            last_sync_date=datetime.now(),
            sync_frequency='daily',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        framework.create_integration.return_value = mock_integration
        mock.return_value = framework
        yield framework


@pytest.fixture
def mock_integration_service():
    """Mock IntegrationService."""
    with patch('web.api.integration_api.get_integration_service') as mock:
        service = AsyncMock()
        from models.integration import Integration, IntegrationStatus
        from datetime import datetime
        mock_integrations = [
            Integration(
                integration_id='int_1',
                user_id='user_1',
                app_name='mint',
                status=IntegrationStatus.CONNECTED,
                created_date=datetime.now(),
                updated_date=datetime.now()
            )
        ]
        service.get_user_integrations.return_value = mock_integrations
        service.sync_data.return_value = {'status': 'success', 'records_synced': 100}
        mock.return_value = service
        yield service


def test_create_integration_success(client, mock_integration_framework):
    """Test successful integration creation."""
    response = client.post('/api/integration/create',
                          json={
                              'user_id': 'user_1',
                              'app_name': 'mint',
                              'oauth_token': 'token_123'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_create_integration_missing_params(client):
    """Test integration creation with missing parameters."""
    response = client.post('/api/integration/create',
                          json={'user_id': 'user_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_get_user_integrations_success(client, mock_integration_service):
    """Test successful user integrations retrieval."""
    response = client.get('/api/integration/user/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'success' in data or isinstance(data, list)


def test_sync_integration_success(client, mock_integration_service):
    """Test successful integration sync."""
    response = client.post('/api/integration/int_1/sync', json={})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data or 'success' in data
