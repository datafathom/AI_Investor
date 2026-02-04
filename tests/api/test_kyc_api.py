"""
Tests for KYC API Endpoints
"""

import pytest
import io
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI, UploadFile
from fastapi.testclient import TestClient
from web.api.kyc_api import router, get_kyc_service


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


@pytest.fixture
def mock_kyc_service(api_app):
    """Mock KYC Service."""
    service = AsyncMock()
    
    # Mock Document objects
    d1 = MagicMock()
    d1.id = 'doc_1'
    d1.document_type.value = 'passport'
    d1.filename = 'passport.jpg'
    d1.status.value = 'verified'
    d1.uploaded_at = '2026-01-01T00:00:00'
    d1.expires_at = '2031-01-01T00:00:00'
    service.get_user_documents.return_value = [d1]
    
    # Mock VerificationResult
    v_res = MagicMock()
    v_res.is_verified = True
    v_res.verification_level = 'basic'
    v_res.missing_documents = []
    v_res.expires_at = '2027-01-01T00:00:00'
    service.get_verification_status.return_value = v_res
    service.verify_identity.return_value = v_res
    
    # Mock FilingDeadline
    fd1 = MagicMock()
    fd1.filing_type = '13F'
    fd1.due_date = '2026-02-15'
    fd1.description = 'Quarterly Holdings'
    fd1.status = 'pending'
    fd1.days_remaining = 12
    service.get_filing_calendar.return_value = [fd1]
    
    service.upload_document.return_value = d1
    service.generate_13f_xml.return_value = b"<xml>13F Data</xml>"
    service.get_required_documents = MagicMock(return_value=[{'type': 'passport', 'required': True}])
    
    api_app.dependency_overrides[get_kyc_service] = lambda: service
    return service


def test_get_verification_status_success(client, mock_kyc_service):
    """Test getting verification status."""
    response = client.get('/api/v1/kyc/status?user_id=user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['is_verified'] is True


def test_list_documents_success(client, mock_kyc_service):
    """Test listing documents."""
    response = client.get('/api/v1/kyc/documents?user_id=user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['total'] == 1


def test_upload_document_success(client, mock_kyc_service):
    """Test uploading a document."""
    file_content = b"fake image content"
    files = {'file': ('passport.jpg', io.BytesIO(file_content), 'image/jpeg')}
    data = {'document_type': 'passport', 'user_id': 'user_1'}
    
    response = client.post('/api/v1/kyc/documents/upload', files=files, data=data)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['filename'] == 'passport.jpg'


def test_get_filing_calendar_success(client, mock_kyc_service):
    """Test getting filing calendar."""
    response = client.get('/api/v1/kyc/filings/calendar')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['deadlines'][0]['filing_type'] == '13F'


def test_export_13f_xml_success(client, mock_kyc_service):
    """Test exporting 13F XML."""
    response = client.get('/api/v1/kyc/filings/13f/p_1/export')
    
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/xml'
    assert b"13F Data" in response.content


def test_get_required_documents_success(client, mock_kyc_service):
    """Test getting required documents."""
    response = client.get('/api/v1/kyc/requirements/basic')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['level'] == 'basic'
