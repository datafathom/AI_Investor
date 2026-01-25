"""
Tests for Marketplace API Endpoints
Phase 30: Extension Marketplace & Custom Tools
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.marketplace_api import marketplace_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(marketplace_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_extension_framework():
    """Mock ExtensionFramework."""
    with patch('web.api.marketplace_api.get_extension_framework') as mock:
        framework = AsyncMock()
        mock.return_value = framework
        yield framework


@pytest.fixture
def mock_marketplace_service():
    """Mock MarketplaceService."""
    with patch('web.api.marketplace_api.get_marketplace_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_extension_success(client, mock_extension_framework):
    """Test successful extension creation."""
    from models.marketplace import Extension
    
    mock_extension = Extension(
        extension_id='ext_1',
        developer_id='dev_1',
        extension_name='Test Extension',
        description='Test description',
        version='1.0.0',
        category='analytics',
        status='pending'
    )
    mock_extension_framework.create_extension.return_value = mock_extension
    
    response = client.post('/api/marketplace/extension/create',
                          json={
                              'developer_id': 'dev_1',
                              'extension_name': 'Test Extension',
                              'description': 'Test description',
                              'version': '1.0.0',
                              'category': 'analytics'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['extension_name'] == 'Test Extension'


@pytest.mark.asyncio
async def test_create_extension_missing_params(client):
    """Test extension creation with missing parameters."""
    response = client.post('/api/marketplace/extension/create',
                          json={'developer_id': 'dev_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_get_extensions_success(client, mock_marketplace_service):
    """Test successful extensions retrieval."""
    from models.marketplace import Extension
    
    mock_extensions = [
        Extension(
            extension_id='ext_1',
            developer_id='dev_1',
            extension_name='Test Extension',
            description='Test description',
            version='1.0.0',
            category='analytics',
            status='approved'
        )
    ]
    mock_marketplace_service.get_extensions.return_value = mock_extensions
    
    response = client.get('/api/marketplace/extensions?category=analytics')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1


@pytest.mark.asyncio
async def test_install_extension_success(client, mock_marketplace_service):
    """Test successful extension installation."""
    response = client.post('/api/marketplace/extension/ext_1/install',
                          json={'user_id': 'user_1'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
