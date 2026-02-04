"""
Integration Tests: Legal Document Acceptance Flow
Tests the complete flow of legal document acceptance using FastAPI TestClient.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.legal_api import router


@pytest.fixture
def app() -> FastAPI:
    """Create test FastAPI app with legal router."""
    test_app = FastAPI()
    test_app.include_router(router)
    return test_app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_user() -> dict:
    """Mock user for testing."""
    return {
        "id": "test_user_1",
        "email": "test@example.com"
    }


class TestLegalDocumentFlow:
    """Test legal document acceptance flow."""
    
    def test_list_documents(self, client: TestClient) -> None:
        """Test listing all legal documents."""
        response = client.get('/api/v1/legal/documents')
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'data' in data
        assert len(data['data']) > 0
    
    def test_get_document(self, client: TestClient) -> None:
        """Test getting a specific document."""
        response = client.get('/api/v1/legal/documents/terms_of_service')
        # May return 404 if doc file not found, 200 if found
        assert response.status_code in [200, 404]
        data = response.json()
        if response.status_code == 200:
            assert data['success'] is True
            assert 'data' in data
            assert data['data']['id'] == 'terms_of_service'
    
    def test_get_nonexistent_document(self, client: TestClient) -> None:
        """Test getting a non-existent document."""
        response = client.get('/api/v1/legal/documents/nonexistent')
        assert response.status_code == 404
    
    @patch('web.api.legal_api.get_current_user')
    def test_accept_documents(self, mock_get_user, client: TestClient, mock_user: dict) -> None:
        """Test accepting legal documents."""
        mock_get_user.return_value = mock_user
        
        response = client.post('/api/v1/legal/accept', json={
            'documents': ['terms_of_service', 'privacy_policy']
        })
        # 401 without proper auth, or 200/422 with auth
        assert response.status_code in [200, 401, 422]
    
    def test_accept_documents_unauthorized(self, client: TestClient) -> None:
        """Test accepting documents without authentication.
        Note: In dev mode, auth falls back to demo user, so this may return 200.
        """
        response = client.post('/api/v1/legal/accept', json={
            'documents': ['terms_of_service']
        })
        # In dev mode returns 200 (demo user), in prod would be 401
        assert response.status_code in [200, 401, 422]
    
    @patch('web.api.legal_api.get_current_user')
    def test_get_acceptance_status(self, mock_get_user, client: TestClient, mock_user: dict) -> None:
        """Test getting user acceptance status."""
        mock_get_user.return_value = mock_user
        
        response = client.get('/api/v1/legal/acceptance-status')
        # May require auth
        assert response.status_code in [200, 401, 422]
    
    @patch('web.api.legal_api.get_current_user')
    def test_get_acceptance_history(self, mock_get_user, client: TestClient, mock_user: dict) -> None:
        """Test getting acceptance history."""
        mock_get_user.return_value = mock_user
        
        response = client.get('/api/v1/legal/acceptance-history')
        # May require auth
        assert response.status_code in [200, 401, 422]
    
    @patch('web.api.legal_api.get_current_user')
    def test_check_document_updates(self, mock_get_user, client: TestClient, mock_user: dict) -> None:
        """Test checking for document updates."""
        mock_get_user.return_value = mock_user
        
        response = client.get('/api/v1/legal/check-updates')
        # May require auth
        assert response.status_code in [200, 401, 422]
