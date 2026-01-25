"""
Tests for Assets API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.assets_api import assets_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(assets_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_assets_service():
    """Mock AssetsService."""
    with patch('web.api.assets_api.assets_service') as mock:
        service = MagicMock()
        service.get_all_assets.return_value = [
            {'id': 'asset_1', 'name': 'House', 'value': 500000.0}
        ]
        service.add_asset.return_value = {'id': 'asset_2', 'name': 'Car', 'value': 30000.0}
        service.update_asset.return_value = {'id': 'asset_1', 'name': 'House', 'value': 550000.0}
        service.delete_asset.return_value = True
        service.get_total_valuation.return_value = 530000.0
        mock.return_value = service
        yield service


def test_get_assets_success(client, mock_assets_service):
    """Test successful assets retrieval."""
    response = client.get('/')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_create_asset_success(client, mock_assets_service):
    """Test successful asset creation."""
    response = client.post('/',
                          json={'name': 'Car', 'value': 30000.0})
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['name'] == 'Car'


def test_create_asset_missing_params(client):
    """Test asset creation with missing parameters."""
    response = client.post('/', json={'name': 'Car'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_update_asset_success(client, mock_assets_service):
    """Test successful asset update."""
    response = client.put('/asset_1',
                         json={'name': 'House', 'value': 550000.0})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['value'] == 550000.0


def test_delete_asset_success(client, mock_assets_service):
    """Test successful asset deletion."""
    response = client.delete('/asset_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data


def test_get_valuation_success(client, mock_assets_service):
    """Test successful valuation retrieval."""
    response = client.get('/valuation')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_valuation' in data
