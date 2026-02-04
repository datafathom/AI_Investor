"""
Tests for TaxBit API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.taxbit_api import router


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_ingest_transactions_success(client):
    """Test ingesting transactions."""
    payload = {"source": "Coinbase"}
    response = client.post('/api/v1/taxbit/ingest-transactions', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['source'] == "Coinbase"


def test_generate_document_success(client):
    """Test generating document."""
    payload = {"tax_year": 2025}
    response = client.post('/api/v1/taxbit/generate-document', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['tax_year'] == 2025


def test_list_documents_success(client):
    """Test listing documents."""
    response = client.get('/api/v1/taxbit/documents')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['documents']) == 2


def test_get_document_success(client):
    """Test getting a specific document."""
    response = client.get('/api/v1/taxbit/documents/2025')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['tax_year'] == 2025
