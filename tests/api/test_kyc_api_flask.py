"""
Tests for KYC API Flask Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.kyc_api_flask import kyc_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(kyc_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_kyc_service():
    """Mock KYCService."""
    with patch('web.api.kyc_api_flask.get_kyc_service') as mock:
        service = AsyncMock()
        from services.security.kyc_service import VerificationResult, DocumentType
        mock_result = VerificationResult(
            is_verified=True,
            verification_level='tier2',
            missing_documents=[],
            expires_at=None
        )
        service.get_verification_status.return_value = mock_result
        from services.security.kyc_service import Document
        mock_docs = [
            Document(
                id='doc_1',
                document_type=DocumentType.PASSPORT,
                filename='passport.pdf',
                status='verified',
                uploaded_at='2024-01-01',
                expires_at=None
            )
        ]
        service.get_user_documents.return_value = mock_docs
        service.upload_document.return_value = {'document_id': 'doc_2', 'status': 'pending'}
        mock.return_value = service
        yield service


def test_get_verification_status_success(client, mock_kyc_service):
    """Test successful verification status retrieval."""
    response = client.get('/status?user_id=user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'is_verified' in data
    assert 'level' in data


def test_list_documents_success(client, mock_kyc_service):
    """Test successful documents listing."""
    response = client.get('/documents?user_id=user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'documents' in data
    assert 'total' in data


def test_upload_document_success(client, mock_kyc_service):
    """Test successful document upload."""
    response = client.post('/documents/upload',
                          json={
                              'user_id': 'user_1',
                              'document_type': 'passport',
                              'filename': 'passport.pdf'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'document_id' in data or 'status' in data
