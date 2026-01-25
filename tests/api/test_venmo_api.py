"""
Tests for Venmo API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.venmo_api import venmo_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(venmo_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_venmo_client():
    """Mock Venmo client."""
    with patch('web.api.venmo_api.get_venmo_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_pay_success(client, mock_venmo_client):
    """Test successful Venmo payment."""
    mock_result = {'status': 'completed', 'payment_id': 'venmo_123'}
    
    async def mock_process_payment(amount, username):
        return mock_result
    
    mock_venmo_client.process_payment = mock_process_payment
    
    response = client.post('/payment/venmo/pay?mock=true',
                          json={'amount': 29.00})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'completed'
