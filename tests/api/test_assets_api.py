
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.assets_api import router, get_assets_service
from web.auth_utils import get_current_user

@pytest.fixture
def api_app(mock_assets_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_assets_service] = lambda: mock_assets_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app

@pytest.fixture
def mock_assets_service():
    """Mock AssetsService."""
    service = MagicMock()
    service.get_all_assets.return_value = [
        {'id': 'asset_1', 'name': 'House', 'value': 500000.0}
    ]
    service.add_asset.return_value = {'id': 'asset_2', 'name': 'Car', 'value': 30000.0}
    service.update_asset.return_value = {'id': 'asset_1', 'name': 'House', 'value': 550000.0}
    service.delete_asset.return_value = True
    service.get_total_valuation.return_value = 530000.0
    return service

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

def test_get_assets_success(client, mock_assets_service):
    """Test successful assets retrieval."""
    response = client.get('/api/v1/assets/')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)

def test_create_asset_success(client, mock_assets_service):
    """Test successful asset creation."""
    response = client.post('/api/v1/assets/',
                          json={'name': 'Car', 'value': 30000.0})
    
    assert response.status_code == 201
    data = response.json()
    assert data['success'] is True
    assert 'id' in data['data']
    assert data['data']['name'] == 'Car'

def test_create_asset_missing_params(client):
    """Test asset creation with missing parameters."""
    response = client.post('/api/v1/assets/', json={'name': 'Car'})
    
    assert response.status_code in [400, 422]

def test_update_asset_success(client, mock_assets_service):
    """Test successful asset update."""
    response = client.put('/api/v1/assets/asset_1',
                         json={'name': 'House', 'value': 550000.0})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['value'] == 550000.0

def test_delete_asset_success(client, mock_assets_service):
    """Test successful asset deletion."""
    response = client.delete('/api/v1/assets/asset_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'message' in data['data']

def test_get_valuation_success(client, mock_assets_service):
    """Test successful valuation retrieval."""
    response = client.get('/api/v1/assets/valuation')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'total_valuation' in data['data']
