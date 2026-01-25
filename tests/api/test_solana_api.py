"""
Tests for Solana API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.solana_api import solana_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(solana_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_solana_client():
    """Mock SolanaClient."""
    with patch('web.api.solana_api.get_solana_client') as mock:
        client = AsyncMock()
        client.get_sol_balance.return_value = 10.5
        client.get_token_balances.return_value = [
            {'mint': 'USDC', 'balance': 500.0, 'decimals': 6}
        ]
        client.get_transactions.return_value = [
            {'signature': 'sig_123', 'type': 'transfer', 'amount': 1.0}
        ]
        client.get_token_info.return_value = {'name': 'USDC', 'symbol': 'USDC', 'decimals': 6}
        mock.return_value = client
        yield client


def test_get_balance_success(client, mock_solana_client):
    """Test successful SOL balance retrieval."""
    response = client.get('/api/v1/solana/balance/9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'address' in data
    assert 'balance' in data


def test_get_tokens_success(client, mock_solana_client):
    """Test successful token balances retrieval."""
    response = client.get('/api/v1/solana/tokens/9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'tokens' in data


def test_get_transactions_success(client, mock_solana_client):
    """Test successful transactions retrieval."""
    response = client.get('/api/v1/solana/transactions/9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'transactions' in data


def test_get_token_info_success(client, mock_solana_client):
    """Test successful token info retrieval."""
    response = client.get('/api/v1/solana/token-info/EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'name' in data or 'symbol' in data
