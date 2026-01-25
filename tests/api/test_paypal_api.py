"""
Tests for PayPal API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.paypal_api import paypal_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(paypal_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_paypal_client():
    """Mock PayPal client."""
    with patch('web.api.paypal_api.get_paypal_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_create_order_success(client, mock_paypal_client):
    """Test successful order creation."""
    mock_order = {'order_id': 'PAYPAL_123', 'status': 'created'}
    
    async def mock_create_order(amount, currency):
        return mock_order
    
    mock_paypal_client.create_order = mock_create_order
    
    response = client.post('/payment/paypal/create-order?mock=true',
                          json={'amount': 29.00, 'currency': 'USD'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['order_id'] == 'PAYPAL_123'


def test_capture_order_success(client, mock_paypal_client):
    """Test successful order capture."""
    mock_capture = {'status': 'completed', 'transaction_id': 'tx_123'}
    
    async def mock_capture_order(order_id):
        return mock_capture
    
    mock_paypal_client.capture_order = mock_capture_order
    
    response = client.post('/payment/paypal/capture-order?mock=true',
                          json={'order_id': 'PAYPAL_123'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'completed'


def test_capture_order_missing_order_id(client):
    """Test order capture without order_id."""
    response = client.post('/payment/paypal/capture-order?mock=true', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
