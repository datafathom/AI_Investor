
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.documents_api import router, get_s3_provider

@pytest.fixture
def api_app(mock_s3_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_s3_provider] = lambda: mock_s3_service
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_s3_service():
    """Mock S3Service."""
    service = AsyncMock()
    service.upload_file.return_value = MagicMock(
        document_id='doc_1', 
        s3_key='key', 
        bucket='bucket',
        size_bytes=1024,
        checksum='sum',
        timestamp='2024-01-01'
    )
    service.generate_presigned_url = MagicMock(return_value='https://s3.../presigned')
    service.delete_file.return_value = True
    return service
        
@pytest.fixture
def mock_metadata_store():
    """Mock the in-memory metadata store."""
    with patch('web.api.documents_api._document_metadata_store', {}) as store:
        # Pre-populate for retrieval tests
        store['doc_1'] = {
            "document_id": "doc_1",
            "user_id": "demo-user",
            "s3_key": "key",
            "bucket": "bucket",
            "filename": "test.pdf",
            "content_type": "application/pdf",
            "size_bytes": 1024,
            "checksum": "sum",
            "category": "tax",
            "description": "test",
            "uploaded_at": "2024-01-01"
        }
        yield store

def test_upload_document_success(client, mock_s3_service):
    """Test successful document upload."""
    
    # Needs multipart/form-data
    response = client.post('/api/v1/documents',
                          files={'file': ('test.pdf', b'test content', 'application/pdf')},
                          data={'category': 'tax'})
    
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['category'] == 'tax'

def test_list_documents_success(client, mock_metadata_store):
    """Test successful documents listing."""
    response = client.get('/api/v1/documents')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'documents' in data['data']
    assert len(data['data']['documents']) > 0

def test_get_download_url_success(client, mock_metadata_store, mock_s3_service):
    """Test successful download URL retrieval."""
    response = client.get('/api/v1/documents/doc_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'download_url' in data['data']

def test_delete_document_success(client, mock_metadata_store, mock_s3_service):
    """Test successful document deletion."""
    response = client.delete('/api/v1/documents/doc_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['deleted'] is True
