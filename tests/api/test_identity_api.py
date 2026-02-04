"""
Tests for Identity API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.identity_api import router
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: {
        "id": "user_1",
        "username": "testuser",
        "role": "user"
    }
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_identity_service():
    """Mock IdentityService."""
    with patch('web.api.identity_api._identity_service') as mock:
        mock.get_identity_profile.return_value = {
            'user_id': 'user_1',
            'trust_score': 0.95,
            'verified': True
        }
        mock.reconcile_identity.return_value = {
            'user_id': 'user_1',
            'trust_score': 0.95
        }
        yield mock


def test_get_profile_success(client, mock_identity_service):
    """Test successful profile retrieval."""
    response = client.get('/api/v1/identity/profile')
    
    assert response.status_code == 200
    data = response.json()
    assert 'user_id' in data or 'trust_score' in data


def test_reconcile_success(client, mock_identity_service):
    """Test successful identity reconciliation."""
    response = client.post('/api/v1/identity/reconcile')
    
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data or 'data' in data


def test_manual_verify_success(client):
    """Test successful manual verification."""
    response = client.post('/api/v1/identity/manual-verify')
    
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
