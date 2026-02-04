"""
Tests for Stripe API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.stripe_api import router, get_stripe_client


@pytest.fixture
def mock_stripe_client():
    """Mock Stripe client."""
    client = MagicMock()
    # Mock async methods
    client.get_subscription = MagicMock()
    client.create_checkout_session = MagicMock()
    return client


@pytest.fixture
def api_app(mock_stripe_client):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_stripe_client] = lambda mock=True: mock_stripe_client
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_get_subscription_success(client, mock_stripe_client):
    """Test successful subscription retrieval."""
    mock_subscription = {
        'subscription_id': 'sub_1',
        'plan': 'pro',
        'status': 'active'
    }
    
    async def mock_get_sub(user_id):
        return mock_subscription
    
    mock_stripe_client.get_subscription.side_effect = mock_get_sub
    
    response = client.get('/api/v1/stripe/billing/subscription?mock=true')
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'active'


def test_create_checkout_success(client, mock_stripe_client):
    """Test successful checkout session creation."""
    mock_checkout = {
        'session_id': 'cs_123',
        'url': 'https://checkout.stripe.com/pay/cs_123'
    }
    
    async def mock_create(user_id, plan_id):
        return mock_checkout
    
    mock_stripe_client.create_checkout_session.side_effect = mock_create
    
    response = client.post('/api/v1/stripe/billing/checkout?mock=true',
                          json={'plan_id': 'price_pro_monthly'})
    
    assert response.status_code == 200
    data = response.json()
    assert 'session_id' in data or 'id' in data


def test_create_checkout_missing_plan_id(client):
    """Test checkout creation without plan_id."""
    # This will fail Pydantic validation and return 422
    response = client.post('/api/v1/stripe/billing/checkout?mock=true', json={})
    
    assert response.status_code == 422
