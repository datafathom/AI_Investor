
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.coinbase_api import router, get_coinbase_service

@pytest.fixture
def api_app(mock_coinbase_client):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_coinbase_service] = lambda: mock_coinbase_client
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_coinbase_client():
    """Mock Coinbase client."""
    client = AsyncMock()
    return client

def test_connect_wallet_success(client, mock_coinbase_client):
    """Test successful wallet connection."""
    mock_result = {'status': 'connected', 'wallet_id': 'wallet_1'}
    
    # client.connect_wallet is async
    mock_coinbase_client.connect_wallet.return_value = mock_result
    
    response = client.post('/api/v1/coinbase/wallet/coinbase/connect?mock=true')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'connected'

def test_get_balance_success(client, mock_coinbase_client):
    """Test successful balance retrieval."""
    mock_balance = {'BTC': 1.5, 'ETH': 10.0, 'USD': 5000.0}
    
    mock_coinbase_client.get_wallet_balance.return_value = mock_balance
    
    response = client.get('/api/v1/coinbase/wallet/coinbase/balance?mock=true')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'BTC' in data['data']

def test_get_transactions_success(client, mock_coinbase_client):
    """Test successful transactions retrieval."""
    mock_transactions = [
        {'id': 'tx_1', 'type': 'buy', 'amount': 1000.0}
    ]
    
    mock_coinbase_client.get_transactions.return_value = mock_transactions
    
    response = client.get('/api/v1/coinbase/wallet/coinbase/transactions?mock=true')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)
