"""
Tests for Public API Endpoints
Phase 29: Public API & Developer Platform
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.public_api_endpoints import public_api_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(public_api_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_public_api_service():
    """Mock PublicAPIService."""
    with patch('web.api.public_api_endpoints.get_public_api_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_developer_portal_service():
    """Mock DeveloperPortalService."""
    with patch('web.api.public_api_endpoints.get_developer_portal_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_api_key_success(client, mock_public_api_service):
    """Test successful API key creation."""
    from models.public_api import APIKey
    
    mock_api_key = APIKey(
        api_key_id='key_1',
        user_id='user_1',
        api_key='test_key_12345',
        tier='free',
        rate_limit=100,
        created_date=None
    )
    mock_public_api_service.create_api_key.return_value = mock_api_key
    
    response = client.post('/api/public/api-key/create',
                          json={
                              'user_id': 'user_1',
                              'tier': 'free'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['tier'] == 'free'


@pytest.mark.asyncio
async def test_create_api_key_missing_user_id(client):
    """Test API key creation without user_id."""
    response = client.post('/api/public/api-key/create', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_get_api_key_success(client, mock_public_api_service):
    """Test successful API key retrieval."""
    from models.public_api import APIKey
    
    mock_api_key = APIKey(
        api_key_id='key_1',
        user_id='user_1',
        api_key='test_key_12345',
        tier='free',
        rate_limit=100,
        created_date=None
    )
    mock_public_api_service._get_api_key.return_value = mock_api_key
    
    response = client.get('/api/public/api-key/key_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_get_documentation_success(client, mock_developer_portal_service):
    """Test successful documentation retrieval."""
    mock_docs = {
        'version': 'v1.0',
        'endpoints': [],
        'authentication': {}
    }
    mock_developer_portal_service.get_documentation.return_value = mock_docs
    
    response = client.get('/api/public/documentation')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
