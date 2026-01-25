"""
Tests for Documents API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.documents_api import documents_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(documents_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_s3_service():
    """Mock S3Service."""
    with patch('web.api.documents_api._get_s3_service') as mock:
        service = AsyncMock()
        service.upload_document.return_value = {'document_id': 'doc_1', 'url': 'https://s3...'}
        service.list_documents.return_value = [
            {'id': 'doc_1', 'filename': 'test.pdf', 'uploaded_at': '2024-01-01'}
        ]
        service.get_download_url.return_value = {'url': 'https://s3.../presigned', 'expires_in': 3600}
        service.delete_document.return_value = True
        mock.return_value = service
        yield service


def test_upload_document_success(client, mock_s3_service):
    """Test successful document upload."""
    response = client.post('/api/v1/documents',
                          json={
                              'filename': 'test.pdf',
                              'document_type': 'tax',
                              'content_type': 'application/pdf'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'document_id' in data or 'url' in data


def test_list_documents_success(client, mock_s3_service):
    """Test successful documents listing."""
    response = client.get('/api/v1/documents')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'documents' in data


def test_get_download_url_success(client, mock_s3_service):
    """Test successful download URL retrieval."""
    response = client.get('/api/v1/documents/doc_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'url' in data or 'download_url' in data


def test_delete_document_success(client, mock_s3_service):
    """Test successful document deletion."""
    response = client.delete('/api/v1/documents/doc_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data or 'status' in data
