"""
Tests for Solana API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.solana_api import router, get_solana_provider, get_token_registry_provider


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_service(api_app):
    """Mock Solana Service."""
    service = AsyncMock()
    service.get_sol_balance.return_value = 1.5
    service.get_spl_tokens.return_value = [{"symbol": "USDC", "balance": 100}]
    service.get_transaction_history.return_value = [{"sig": "tx1", "slot": 1000}]
    
    api_app.dependency_overrides[get_solana_provider] = lambda: service
    return service


@pytest.fixture
def mock_registry(api_app):
    """Mock Token Registry."""
    registry = MagicMock()
    registry.get_token_info.return_value = {"name": "USD Coin", "symbol": "USDC"}
    
    api_app.dependency_overrides[get_token_registry_provider] = lambda: registry
    return registry


def test_get_balance_success(client, mock_service):
    """Test getting balance."""
    response = client.get('/api/v1/solana/balance/addr1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['balance_sol'] == 1.5


def test_get_tokens_success(client, mock_service):
    """Test getting tokens."""
    response = client.get('/api/v1/solana/tokens/addr1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['tokens']) == 1


def test_get_transactions_success(client, mock_service):
    """Test getting transactions."""
    response = client.get('/api/v1/solana/transactions/addr1?limit=10')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['transactions']) == 1


def test_get_token_info_success(client, mock_registry):
    """Test getting token info."""
    response = client.get('/api/v1/solana/token-info/mint1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['token_info']['symbol'] == "USDC"
