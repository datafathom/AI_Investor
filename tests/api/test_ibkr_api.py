"""
Tests for Interactive Brokers API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.ibkr_api import ibkr_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(ibkr_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_ibkr_client():
    """Mock IBKRClient."""
    with patch('web.api.ibkr_api.get_ibkr_client') as mock:
        client = AsyncMock()
        client.get_account_summary.return_value = {
            'account_id': 'acc_1',
            'net_liquidation': 100000.0,
            'buying_power': 200000.0
        }
        client.get_positions.return_value = [
            {'symbol': 'AAPL', 'quantity': 100, 'avg_cost': 150.0}
        ]
        client.get_orders.return_value = [{'id': 'order_1', 'symbol': 'AAPL', 'status': 'filled'}]
        client.place_order.return_value = {'order_id': 'order_2', 'status': 'submitted'}
        client.cancel_order.return_value = True
        client.get_margin_requirements.return_value = {'maintenance_margin': 25000.0}
        client.get_currency_exposure.return_value = {'USD': 100000.0, 'EUR': 0.0}
        mock.return_value = client
        yield client


def test_get_account_summary_success(client, mock_ibkr_client):
    """Test successful account summary retrieval."""
    response = client.get('/api/v1/ibkr/account-summary')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'account_id' in data or 'net_liquidation' in data


def test_get_positions_success(client, mock_ibkr_client):
    """Test successful positions retrieval."""
    response = client.get('/api/v1/ibkr/positions')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'positions' in data


def test_place_order_success(client, mock_ibkr_client):
    """Test successful order placement."""
    response = client.post('/api/v1/ibkr/orders',
                          json={
                              'symbol': 'AAPL',
                              'quantity': 100,
                              'order_type': 'market',
                              'side': 'buy'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'order_id' in data or 'status' in data


def test_cancel_order_success(client, mock_ibkr_client):
    """Test successful order cancellation."""
    response = client.delete('/api/v1/ibkr/orders/order_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data or 'status' in data


def test_get_margin_success(client, mock_ibkr_client):
    """Test successful margin requirements retrieval."""
    response = client.get('/api/v1/ibkr/margin')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'maintenance_margin' in data or 'margin' in data
