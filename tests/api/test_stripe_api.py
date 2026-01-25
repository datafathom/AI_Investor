"""
Tests for Stripe API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.stripe_api import stripe_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(stripe_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_stripe_client():
    """Mock Stripe client."""
    with patch('web.api.stripe_api.get_stripe_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_get_subscription_success(client, mock_stripe_client):
    """Test successful subscription retrieval."""
    mock_subscription = {
        'subscription_id': 'sub_1',
        'plan': 'pro',
        'status': 'active'
    }
    
    async def mock_get_subscription(user_id):
        return mock_subscription
    
    mock_stripe_client.get_subscription = mock_get_subscription
    
    response = client.get('/billing/subscription?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'active'


def test_create_checkout_success(client, mock_stripe_client):
    """Test successful checkout session creation."""
    mock_checkout = {
        'session_id': 'cs_123',
        'url': 'https://checkout.stripe.com/pay/cs_123'
    }
    
    async def mock_create_checkout(user_id, plan_id):
        return mock_checkout
    
    mock_stripe_client.create_checkout_session = mock_create_checkout
    
    response = client.post('/billing/checkout?mock=true',
                          json={'plan_id': 'price_pro_monthly'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'session_id' in data


def test_create_checkout_missing_plan_id(client):
    """Test checkout creation without plan_id."""
    response = client.post('/billing/checkout?mock=true', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
