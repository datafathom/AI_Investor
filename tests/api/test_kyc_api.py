"""
Tests for KYC API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.kyc_api import router


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_kyc_service():
    """Mock KYCService."""
    with patch('web.api.kyc_api.get_kyc_service') as mock:
        service = AsyncMock()
        from services.security.kyc_service import VerificationResult
        mock_status = VerificationResult(
            verified=True,
            trust_score=0.95,
            documents_required=[],
            next_steps=[]
        )
        service.get_verification_status.return_value = mock_status
        service.list_documents.return_value = []
        service.upload_document.return_value = {'id': 'doc_1', 'status': 'pending'}
        service.get_filing_deadlines.return_value = []
        service.export_13f.return_value = b'<xml>...</xml>'
        mock.return_value = service
        yield service


def test_get_verification_status_success(client, mock_kyc_service):
    """Test successful verification status retrieval."""
    response = client.get('/api/v1/kyc/status?user_id=user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'verified' in data or 'trust_score' in data


def test_list_documents_success(client, mock_kyc_service):
    """Test successful documents listing."""
    response = client.get('/api/v1/kyc/documents?user_id=user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'documents' in data


def test_get_filing_calendar_success(client, mock_kyc_service):
    """Test successful filing calendar retrieval."""
    response = client.get('/api/v1/kyc/filings/calendar?user_id=user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'deadlines' in data
