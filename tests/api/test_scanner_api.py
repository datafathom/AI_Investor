"""
Tests for Scanner API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.scanner_api import router


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


def test_get_scanner_matches_success(client):
    """Test getting scanner matches."""
    response = client.get('/api/v1/scanner/matches')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 10


def test_get_galaxy_data_success(client):
    """Test getting galaxy data."""
    response = client.get('/api/v1/scanner/galaxy')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 100


def test_get_market_pulse_success(client):
    """Test getting market pulse."""
    response = client.get('/api/v1/scanner/pulse')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 6
