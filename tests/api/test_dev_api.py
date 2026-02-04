"""
Tests for Developer/Dev API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.dev_api import router


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


def test_get_dev_status_success(client):
    """Test successful dev status retrieval."""
    response = client.get('/api/v1/dev/status')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'autocoder_active' in data['data']


def test_get_dev_sessions_success(client):
    """Test successful dev sessions retrieval."""
    response = client.get('/api/v1/dev/sessions')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)


def test_get_dev_logs_success(client):
    """Test successful dev logs retrieval."""
    response = client.get('/api/v1/dev/logs')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) > 0


def test_execute_command_success(client):
    """Test successful dev command execution mock."""
    response = client.post('/api/v1/dev/execute?command=ls')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['command'] == 'ls'
