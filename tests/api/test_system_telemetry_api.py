"""
Tests for System Telemetry API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.system_telemetry_api import router


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


def test_get_quota_success(client):
    """Test getting quota."""
    response = client.get('/api/v1/system/quota')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'used' in data['data']


def test_get_health_telemetry_success(client):
    """Test getting health telemetry."""
    response = client.get('/api/v1/system/health')
    
    # NOTE: system_api.py and system_telemetry_api.py both use /health.
    # In this isolated test, it should work fine.
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "nominal"


def test_get_load_success(client):
    """Test getting load."""
    response = client.get('/api/v1/system/load')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 20
