"""
Tests for Ethereum API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.ethereum_api import router, get_eth_client_provider


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_eth_client(api_app):
    """Mock EthereumClient."""
    client = AsyncMock()
    client.get_eth_balance.return_value = 1.5
    client.get_all_token_balances.return_value = [
        {'token': 'USDC', 'balance': 1000.0, 'decimals': 6}
    ]
    client.get_gas_price.return_value = 50.0
    # validate_address is synchronous, use regular return value
    client.validate_address = MagicMock(return_value=True)
    api_app.dependency_overrides[get_eth_client_provider] = lambda: client
    return client



def test_get_balance_success(client, mock_eth_client):
    """Test successful ETH balance retrieval."""
    response = client.get('/api/v1/ethereum/balance/0x1234567890abcdef')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['address'] == '0x1234567890abcdef'
    assert data['data']['balance_eth'] == 1.5


def test_get_tokens_success(client, mock_eth_client):
    """Test successful token balances retrieval."""
    response = client.get('/api/v1/ethereum/tokens/0x1234567890abcdef')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'tokens' in data['data']


def test_get_gas_price_success(client, mock_eth_client):
    """Test successful gas price retrieval."""
    response = client.get('/api/v1/ethereum/gas-price')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['gas_price_gwei'] == 50.0


def test_validate_address_success(client, mock_eth_client):
    """Test successful address validation."""
    response = client.post('/api/v1/ethereum/validate-address',
                          json={'address': '0x1234567890abcdef'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['valid'] is True
