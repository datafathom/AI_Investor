"""
Tests for Banking API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.banking_api import router, get_banking_service


@pytest.fixture
def api_app(mock_banking_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_banking_service] = lambda: mock_banking_service
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_banking_service():
    """Mock BankingService."""
    service = MagicMock()
    service.create_link_token.return_value = 'link_token_123'
    service.exchange_public_token.return_value = 'access_token_456'
    service.get_accounts.return_value = [{'account_id': 'acc_1', 'balance': 1000.0}]
    return service


def test_create_link_token_success(client, mock_banking_service):
    """Test successful link token creation."""
    response = client.post('/api/v1/banking/plaid/create-link-token')
    
    assert response.status_code == 200
    data = response.json()
    assert 'link_token' in data


def test_exchange_public_token_success(client, mock_banking_service):
    """Test successful public token exchange."""
    response = client.post('/api/v1/banking/plaid/exchange-public-token',
                          json={'public_token': 'public_token_123'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'


def test_get_accounts_success(client, mock_banking_service):
    """Test successful accounts retrieval."""
    response = client.get('/api/v1/banking/accounts')
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_sync_transactions_success(client):
    """Test successful transaction sync."""
    response = client.post('/api/v1/banking/sync')
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
