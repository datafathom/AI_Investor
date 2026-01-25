"""
Tests for Spatial API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from flask import Flask
from web.api.spatial_api import spatial_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(spatial_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_get_spatial_portfolio_success(client):
    """Test successful spatial portfolio retrieval."""
    response = client.get('/api/v1/spatial/portfolio')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'nodes' in data
    assert 'links' in data
    assert isinstance(data['nodes'], list)
    assert isinstance(data['links'], list)


def test_get_xr_status_success(client):
    """Test successful XR status retrieval."""
    response = client.get('/api/v1/spatial/status')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert 'mode' in data
    assert 'engine' in data
