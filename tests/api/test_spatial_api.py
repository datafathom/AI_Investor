"""
Tests for Spatial API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.spatial_api import router


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_get_spatial_portfolio_success(client):
    """Test getting spatial portfolio."""
    response = client.get('/api/v1/spatial/portfolio')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['nodes']) == 8
    assert len(data['data']['links']) == 7


def test_get_xr_status_success(client):
    """Test getting XR status."""
    response = client.get('/api/v1/spatial/status')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "ready"
