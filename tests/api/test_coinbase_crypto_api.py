
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.coinbase_crypto_api import router, get_coinbase_service, get_coinbase_custody_service

@pytest.fixture
def api_app(mock_coinbase_client, mock_custody_client):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_coinbase_service] = lambda: mock_coinbase_client
    app.dependency_overrides[get_coinbase_custody_service] = lambda: mock_custody_client
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_coinbase_client():
    """Mock CoinbaseClient."""
    client = AsyncMock()
    client.get_accounts.return_value = [{'id': 'acc_1', 'balance': 1.5, 'currency': 'BTC'}]
    client.get_trading_pairs.return_value = ['BTC-USD', 'ETH-USD']
    client.place_order.return_value = {'order_id': 'order_1', 'status': 'pending'}
    client.get_orders.return_value = [{'id': 'order_1', 'status': 'filled'}]
    return client
        
@pytest.fixture
def mock_custody_client():
    """Mock CoinbaseCustody (for vaults)."""
    custody = AsyncMock()
    custody.get_vault_balances.return_value = [{'id': 'vault_1', 'balance': 10.0}]
    custody.request_withdrawal.return_value = {'withdrawal_id': 'wd_1', 'status': 'pending'}
    return custody

def test_get_accounts_success(client, mock_coinbase_client):
    """Test successful accounts retrieval."""
    response = client.get('/api/v1/coinbase_crypto/accounts')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data']['accounts'], list)
    assert len(data['data']['accounts']) > 0

def test_get_trading_pairs_success(client, mock_coinbase_client):
    """Test successful trading pairs retrieval."""
    response = client.get('/api/v1/coinbase_crypto/trading-pairs')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data']['trading_pairs'], list)

def test_place_order_success(client, mock_coinbase_client):
    """Test successful order placement."""
    response = client.post('/api/v1/coinbase_crypto/orders',
                          json={
                              'product_id': 'BTC-USD',
                              'side': 'buy',
                              'order_configuration': {}
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'order_id' in data['data']

def test_get_vaults_success(client, mock_custody_client):
    """Test successful vaults retrieval."""
    response = client.get('/api/v1/coinbase_crypto/vaults')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data']['vault_balances'], list)
