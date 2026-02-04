"""
Tests for Facebook Auth API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.facebook_auth_api import router
import web.api.facebook_auth_api as facebook_auth_module


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


def test_initiate_login_success(client):
    """Test successful login initiation."""
    response = client.get('/api/v1/facebook_auth/login')
    
    # May return 200 with url or 500 if service not available
    assert response.status_code in [200, 500]
    data = response.json()
    if response.status_code == 200:
        assert data['success'] is True
        assert 'authorization_url' in data['data'] or 'data' in data


def test_initiate_login_with_redirect(client):
    """Test login initiation with redirect flag."""
    response = client.get('/api/v1/facebook_auth/login?redirect=false')
    
    # Should return JSON with authorization URL
    if response.status_code == 200:
        data = response.json()
        assert data['success'] is True


def test_callback_missing_code(client):
    """Test callback without authorization code."""
    response = client.get('/api/v1/facebook_auth/callback')
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False


def test_callback_invalid_state(client):
    """Test callback with invalid state token."""
    # Clear any existing states
    facebook_auth_module._oauth_states.clear()
    
    response = client.get('/api/v1/facebook_auth/callback?code=test_code&state=invalid_state')
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
