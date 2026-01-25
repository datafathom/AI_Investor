"""
Tests for Square API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.square_api import square_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(square_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_square_client():
    """Mock Square client."""
    with patch('web.api.square_api.get_square_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_get_stats_success(client, mock_square_client):
    """Test successful stats retrieval."""
    mock_stats = {'revenue': 10000.0, 'transactions': 100}
    
    async def mock_get_stats():
        return mock_stats
    
    mock_square_client.get_merchant_stats = mock_get_stats
    
    response = client.get('/merchant/square/stats?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'revenue' in data


def test_get_catalog_success(client, mock_square_client):
    """Test successful catalog retrieval."""
    mock_catalog = {'items': [{'id': 'item_1', 'name': 'Test Item'}]}
    
    async def mock_get_catalog():
        return mock_catalog
    
    mock_square_client.get_catalog = mock_get_catalog
    
    response = client.get('/merchant/square/catalog?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
