"""
Tests for Legal API Endpoints
"""

import pytest
from unittest.mock import MagicMock, patch, mock_open
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.legal_api import router
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    # Mock current user
    app.dependency_overrides[get_current_user] = lambda: {'id': 'user_1', 'email': 'test@example.com'}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_list_documents_success(client):
    """Test listing legal documents."""
    response = client.get('/api/v1/legal/documents')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) > 0
    assert data['data'][0]['id'] == 'terms_of_service'


def test_get_document_success(client):
    """Test getting a specific document content."""
    with patch("builtins.open", mock_open(read_data="# Terms of Service")):
        with patch("web.api.legal_api.Path.exists", return_value=True):
            response = client.get('/api/v1/legal/documents/terms_of_service')
            
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert "# Terms of Service" in data['data']['content']


def test_get_document_not_found(client):
    """Test getting a non-existent document."""
    response = client.get('/api/v1/legal/documents/invalid_doc')
    
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False


def test_accept_documents_success(client):
    """Test accepting documents."""
    response = client.post('/api/v1/legal/accept',
                           json={'documents': ['terms_of_service', 'privacy_policy']})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['acceptances']) == 2


def test_get_acceptance_status_success(client):
    """Test getting acceptance status."""
    response = client.get('/api/v1/legal/acceptance-status')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'required_documents' in data['data']


def test_check_updates_success(client):
    """Test checking for updates."""
    response = client.get('/api/v1/legal/check-updates')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'updates_available' in data['data']
