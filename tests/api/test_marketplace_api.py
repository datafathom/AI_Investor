"""
Tests for Marketplace API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.marketplace_api import router


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_get_extensions_success(client):
    """Test getting extensions list."""
    response = client.get('/api/v1/marketplace/extensions')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 3


def test_get_extensions_filter_success(client):
    """Test filtering extensions by category."""
    response = client.get('/api/v1/marketplace/extensions?category=charting')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['category'] == 'charting'


def test_get_installed_extensions_success(client):
    """Test getting installed extensions."""
    response = client.get('/api/v1/marketplace/installed?user_id=user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 2


def test_get_extension_details_success(client):
    """Test getting extension details."""
    response = client.get('/api/v1/marketplace/extension/ext_001')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['id'] == 'ext_001'


def test_get_extension_details_not_found(client):
    """Test getting non-existent extension details."""
    response = client.get('/api/v1/marketplace/extension/invalid')
    
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False


def test_create_extension_success(client):
    """Test creating an extension."""
    payload = {
        "developer_id": "dev_123",
        "extension_name": "New Tool",
        "description": "Desc",
        "version": "1.0.0",
        "category": "utility"
    }
    response = client.post('/api/v1/marketplace/extension/create', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['name'] == "New Tool"


def test_install_extension_success(client):
    """Test installing an extension."""
    payload = {"user_id": "user_1"}
    response = client.post('/api/v1/marketplace/extension/ext_001/install', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['extension_id'] == "ext_001"


def test_uninstall_extension_success(client):
    """Test uninstalling an extension."""
    payload = {"user_id": "user_1"}
    response = client.post('/api/v1/marketplace/extension/ext_001/uninstall', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['extension_id'] == "ext_001"


def test_add_review_success(client):
    """Test adding a review."""
    payload = {
        "user_id": "user_1",
        "rating": 5,
        "comment": "Great!"
    }
    response = client.post('/api/v1/marketplace/extension/ext_001/review', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['rating'] == 5


def test_add_review_invalid_rating(client):
    """Test adding a review with invalid rating."""
    payload = {
        "user_id": "user_1",
        "rating": 6,
        "comment": "Too good!"
    }
    response = client.post('/api/v1/marketplace/extension/ext_001/review', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
