"""
Integration Tests: Legal Document Acceptance Flow
Tests the complete flow of legal document acceptance
"""

import pytest
from unittest.mock import Mock, patch
from flask import Flask
from web.api.legal_api import legal_bp


@pytest.fixture
def app():
    """Create test Flask app."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.register_blueprint(legal_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(autouse=True)
def app_context(app):
    """Push application context."""
    with app.app_context():
        yield


@pytest.fixture
def mock_user():
    """Mock user for testing."""
    user = Mock()
    user.id = 1
    user.email = 'test@example.com'
    return user


class TestLegalDocumentFlow:
    """Test legal document acceptance flow."""
    
    def test_list_documents(self, client):
        """Test listing all legal documents."""
        response = client.get('/api/v1/legal/documents')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert len(data['data']) > 0
    
    def test_get_document(self, client):
        """Test getting a specific document."""
        response = client.get('/api/v1/legal/documents/terms_of_service')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert data['data']['id'] == 'terms_of_service'
    
    def test_get_nonexistent_document(self, client):
        """Test getting a non-existent document."""
        response = client.get('/api/v1/legal/documents/nonexistent')
        assert response.status_code == 404
    
    @patch('web.api.legal_api.g')
    def test_accept_documents(self, mock_g, client, mock_user):
        """Test accepting legal documents."""
        mock_g.user_id = mock_user.id
        
        response = client.post('/api/v1/legal/accept', json={
            'documents': ['terms_of_service', 'privacy_policy']
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert len(data['data']['acceptances']) == 2
    
    @patch('web.api.legal_api.g')
    def test_accept_documents_unauthorized(self, mock_g, client):
        """Test accepting documents without authentication."""
        mock_g.user_id = None
        
        response = client.post('/api/v1/legal/accept', json={
            'documents': ['terms_of_service']
        })
        assert response.status_code == 401
    
    @patch('web.api.legal_api.g')
    def test_get_acceptance_status(self, mock_g, client, mock_user):
        """Test getting user acceptance status."""
        mock_g.user_id = mock_user.id
        
        response = client.get('/api/v1/legal/acceptance-status')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'user_id' in data['data']
    
    @patch('web.api.legal_api.g')
    def test_get_acceptance_history(self, mock_g, client, mock_user):
        """Test getting acceptance history."""
        mock_g.user_id = mock_user.id
        
        response = client.get('/api/v1/legal/acceptance-history')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
    
    @patch('web.api.legal_api.g')
    def test_check_document_updates(self, mock_g, client, mock_user):
        """Test checking for document updates."""
        mock_g.user_id = mock_user.id
        
        response = client.get('/api/v1/legal/check-updates')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
