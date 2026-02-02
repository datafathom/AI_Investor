"""
Tests for Banking API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.banking_api import banking_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(banking_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_banking_service():
    """Mock BankingService."""
    with patch('web.api.banking_api.get_banking_service') as mock:
        service = MagicMock()
        service.create_link_token.return_value = 'link_token_123'
        service.exchange_public_token.return_value = 'access_token_456'
        service.get_accounts.return_value = [{'account_id': 'acc_1', 'balance': 1000.0}]
        mock.return_value = service
        yield service


def test_create_link_token_success(client, mock_banking_service):
    """Test successful link token creation."""
    # Rely on dev environment login_required bypass (g.user_id = 'demo-admin')
    response = client.post('/api/v1/banking/plaid/create-link-token')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'link_token' in data


def test_exchange_public_token_success(client, mock_banking_service):
    """Test successful public token exchange."""
    response = client.post('/api/v1/banking/plaid/exchange-public-token',
                          json={'public_token': 'public_token_123'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'


def test_get_accounts_success(client, mock_banking_service):
    """Test successful accounts retrieval."""
    response = client.get('/api/v1/banking/accounts')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_sync_transactions_success(client):
    """Test successful transaction sync."""
    # Requires 'trader' role, handled by auth_utils dev bypass
    response = client.post('/api/v1/banking/sync')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
