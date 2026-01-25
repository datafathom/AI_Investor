"""
Tests for TaxBit API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.taxbit_api import taxbit_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(taxbit_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_ingest_transactions_success(client):
    """Test successful transaction ingestion."""
    response = client.post('/api/v1/taxbit/ingest-transactions',
                          json={'source': 'alpaca'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'source' in data


def test_generate_document_success(client):
    """Test successful document generation."""
    response = client.post('/api/v1/taxbit/generate-document',
                          json={'year': 2024, 'document_type': '8949'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'success' in data or 'document_id' in data


def test_list_documents_success(client):
    """Test successful documents listing."""
    response = client.get('/api/v1/taxbit/documents')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'documents' in data


def test_get_document_by_year_success(client):
    """Test successful document retrieval by year."""
    response = client.get('/api/v1/taxbit/documents/2024')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'year' in data or 'document' in data
