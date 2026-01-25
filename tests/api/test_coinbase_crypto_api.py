"""
Tests for Coinbase Crypto API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.coinbase_crypto_api import coinbase_crypto_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(coinbase_crypto_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_coinbase_client():
    """Mock CoinbaseClient."""
    with patch('web.api.coinbase_crypto_api.get_coinbase_client') as mock:
        client = AsyncMock()
        client.get_accounts.return_value = [{'id': 'acc_1', 'balance': 1.5, 'currency': 'BTC'}]
        client.get_trading_pairs.return_value = ['BTC-USD', 'ETH-USD']
        client.place_order.return_value = {'order_id': 'order_1', 'status': 'pending'}
        client.get_orders.return_value = [{'id': 'order_1', 'status': 'filled'}]
        client.get_vaults.return_value = [{'id': 'vault_1', 'balance': 10.0}]
        client.request_withdrawal.return_value = {'withdrawal_id': 'wd_1', 'status': 'pending'}
        mock.return_value = client
        yield client


def test_get_accounts_success(client, mock_coinbase_client):
    """Test successful accounts retrieval."""
    response = client.get('/api/v1/coinbase/accounts')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'accounts' in data


def test_get_trading_pairs_success(client, mock_coinbase_client):
    """Test successful trading pairs retrieval."""
    response = client.get('/api/v1/coinbase/trading-pairs')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'pairs' in data


def test_place_order_success(client, mock_coinbase_client):
    """Test successful order placement."""
    response = client.post('/api/v1/coinbase/orders',
                          json={
                              'product_id': 'BTC-USD',
                              'side': 'buy',
                              'size': '0.001'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'order_id' in data or 'status' in data


def test_get_vaults_success(client, mock_coinbase_client):
    """Test successful vaults retrieval."""
    response = client.get('/api/v1/coinbase/vaults')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'vaults' in data
