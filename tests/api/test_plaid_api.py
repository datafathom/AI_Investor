"""
Tests for Plaid API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.plaid_api import plaid_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(plaid_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_plaid_service():
    """Mock PlaidService."""
    with patch('web.api.plaid_api.get_plaid_service') as mock:
        service = AsyncMock()
        service.create_link_token.return_value = 'link_token_123'
        service.exchange_public_token.return_value = 'access_token_456'
        service.get_accounts.return_value = [{'account_id': 'acc_1'}]
        service.get_balance.return_value = {'available': 1000.0, 'current': 1000.0}
        mock.return_value = service
        yield service


def test_create_link_token_success(client, mock_plaid_service):
    """Test successful link token creation."""
    response = client.post('/api/v1/plaid/link-token',
                          json={'client_name': 'AI Investor'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'link_token' in data


def test_exchange_token_success(client, mock_plaid_service):
    """Test successful public token exchange."""
    response = client.post('/api/v1/plaid/exchange-token',
                          json={'public_token': 'public_token_123'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data


def test_get_accounts_success(client, mock_plaid_service):
    """Test successful accounts retrieval."""
    response = client.get('/api/v1/plaid/accounts')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_balance_success(client, mock_plaid_service):
    """Test successful balance retrieval."""
    response = client.get('/api/v1/plaid/balance?account_id=acc_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'available' in data or 'current' in data
