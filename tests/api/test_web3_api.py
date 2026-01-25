"""
Tests for Web3 API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.web3_api import web3_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(web3_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_wallet_service():
    """Mock WalletService."""
    with patch('web.api.web3_api._wallet_service') as mock:
        service = AsyncMock()
        from services.crypto.wallet_service import CryptoPortfolio
        mock_portfolio = CryptoPortfolio(
            user_id='user_1',
            total_usd_value=10000.0,
            balances=[],
            wallets=[],
            last_updated=None
        )
        service.get_aggregated_portfolio.return_value = mock_portfolio
        service.get_wallet_balance.return_value = {'balance': 1.5, 'usd_value': 5000.0}
        mock.return_value = service
        yield service


@pytest.fixture
def mock_gas_service():
    """Mock GasService."""
    with patch('web.api.web3_api._gas_service') as mock:
        service = AsyncMock()
        service.get_gas_prices.return_value = {'fast': 50, 'standard': 30}
        service.queue_transaction.return_value = {'queued': True, 'estimated_cost': 0.001}
        mock.return_value = service
        yield service


def test_get_portfolio_success(client, mock_wallet_service):
    """Test successful portfolio retrieval."""
    response = client.get('/portfolio/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_get_balance_success(client, mock_wallet_service):
    """Test successful wallet balance retrieval."""
    response = client.get('/balance/0x1234567890abcdef/ethereum')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'balance' in data or 'address' in data


def test_get_gas_prices_success(client, mock_gas_service):
    """Test successful gas prices retrieval."""
    response = client.get('/gas/ethereum')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'fast' in data or 'gas_prices' in data
