
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.brokerage_api import router, get_brokerage_service

@pytest.fixture
def api_app(mock_brokerage_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_brokerage_service] = lambda: mock_brokerage_service
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_brokerage_service():
    """Mock BrokerageService."""
    service = MagicMock()
    service.get_status.return_value = {
        'connected': True,
        'provider': 'test_provider',
        'account_id': 'account_1'
    }
    service.get_supported_providers.return_value = [
        'test_provider',
        'another_provider'
    ]
    service.get_positions.return_value = [
        {'symbol': 'AAPL', 'quantity': 100, 'price': 150.0}
    ]
    service.connect_with_keys.return_value = True
    return service

def test_get_brokerage_status_success(client, mock_brokerage_service):
    """Test successful brokerage status retrieval."""
    response = client.get('/api/v1/brokerage/status')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['connected'] is True
    assert 'provider' in data['data']

def test_get_supported_providers_success(client, mock_brokerage_service):
    """Test successful providers list retrieval."""
    response = client.get('/api/v1/brokerage/providers')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)
    assert len(data['data']) > 0

def test_get_brokerage_positions_success(client, mock_brokerage_service):
    """Test successful positions retrieval."""
    response = client.get('/api/v1/brokerage/positions')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)
    assert len(data['data']) > 0

def test_connect_brokerage_success(client, mock_brokerage_service):
    """Test successful brokerage connection."""
    response = client.post('/api/v1/brokerage/connect',
                          json={
                              'api_key': 'test_key',
                              'secret_key': 'test_secret',
                              'base_url': 'https://api.test.com'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['message'] == 'Brokerage connected successfully'

def test_connect_brokerage_missing_credentials(client):
    """Test brokerage connection with missing credentials."""
    response = client.post('/api/v1/brokerage/connect',
                          json={'api_key': 'test_key'})
                          
    assert response.status_code in [400, 422]
