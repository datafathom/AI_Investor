"""
Tests for Ethereum API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.ethereum_api import ethereum_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(ethereum_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_eth_client():
    """Mock EthereumClient."""
    with patch('web.api.ethereum_api.get_eth_client') as mock:
        client = AsyncMock()
        client.get_eth_balance.return_value = 1.5
        client.get_token_balances.return_value = [
            {'token': 'USDC', 'balance': 1000.0, 'decimals': 6}
        ]
        client.get_gas_price.return_value = {'fast': 50, 'standard': 30, 'slow': 20}
        client.validate_address.return_value = True
        mock.return_value = client
        yield client


def test_get_balance_success(client, mock_eth_client):
    """Test successful ETH balance retrieval."""
    response = client.get('/api/v1/ethereum/balance/0x1234567890abcdef')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'address' in data
    assert 'balance' in data


def test_get_tokens_success(client, mock_eth_client):
    """Test successful token balances retrieval."""
    response = client.get('/api/v1/ethereum/tokens/0x1234567890abcdef')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'tokens' in data


def test_get_gas_price_success(client, mock_eth_client):
    """Test successful gas price retrieval."""
    response = client.get('/api/v1/ethereum/gas-price')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'fast' in data or 'gas_price' in data


def test_validate_address_success(client, mock_eth_client):
    """Test successful address validation."""
    response = client.post('/api/v1/ethereum/validate-address',
                          json={'address': '0x1234567890abcdef'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'valid' in data or 'is_valid' in data
