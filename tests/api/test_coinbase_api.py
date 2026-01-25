"""
Tests for Coinbase API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.coinbase_api import coinbase_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(coinbase_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_coinbase_client():
    """Mock Coinbase client."""
    with patch('web.api.coinbase_api.get_coinbase_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_connect_wallet_success(client, mock_coinbase_client):
    """Test successful wallet connection."""
    mock_result = {'status': 'connected', 'wallet_id': 'wallet_1'}
    
    async def mock_connect(user_id):
        return mock_result
    
    mock_coinbase_client.connect_wallet = mock_connect
    
    response = client.post('/wallet/coinbase/connect?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'connected'


def test_get_balance_success(client, mock_coinbase_client):
    """Test successful balance retrieval."""
    mock_balance = {'BTC': 1.5, 'ETH': 10.0, 'USD': 5000.0}
    
    async def mock_get_balance():
        return mock_balance
    
    mock_coinbase_client.get_wallet_balance = mock_get_balance
    
    response = client.get('/wallet/coinbase/balance?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'BTC' in data


def test_get_transactions_success(client, mock_coinbase_client):
    """Test successful transactions retrieval."""
    mock_transactions = [
        {'id': 'tx_1', 'type': 'buy', 'amount': 1000.0}
    ]
    
    async def mock_get_transactions():
        return mock_transactions
    
    mock_coinbase_client.get_transactions = mock_get_transactions
    
    response = client.get('/wallet/coinbase/transactions?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
