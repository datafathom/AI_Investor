"""
Tests for Robinhood API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.robinhood_api import robinhood_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(robinhood_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_robinhood_client():
    """Mock RobinhoodClient."""
    with patch('web.api.robinhood_api.get_robinhood_client') as mock:
        client = AsyncMock()
        client.connect_account.return_value = {'status': 'connected', 'account_id': 'acc_1'}
        client.get_holdings.return_value = [{'symbol': 'AAPL', 'quantity': 100, 'avg_price': 150.0}]
        client.get_orders.return_value = [{'id': 'order_1', 'symbol': 'AAPL', 'status': 'filled'}]
        client.get_transactions.return_value = [{'id': 'tx_1', 'type': 'buy', 'amount': 1000.0}]
        client.calculate_cost_basis.return_value = {'total_cost': 15000.0, 'avg_cost': 150.0}
        mock.return_value = client
        yield client


def test_connect_account_success(client, mock_robinhood_client):
    """Test successful account connection."""
    response = client.post('/api/v1/robinhood/connect',
                          json={
                              'username': 'test_user',
                              'password': 'test_pass'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data or 'account_id' in data


def test_get_holdings_success(client, mock_robinhood_client):
    """Test successful holdings retrieval."""
    response = client.get('/api/v1/robinhood/holdings')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'holdings' in data


def test_get_orders_success(client, mock_robinhood_client):
    """Test successful orders retrieval."""
    response = client.get('/api/v1/robinhood/orders')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'orders' in data


def test_get_cost_basis_success(client, mock_robinhood_client):
    """Test successful cost basis calculation."""
    response = client.get('/api/v1/robinhood/cost-basis?symbol=AAPL')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_cost' in data or 'avg_cost' in data
