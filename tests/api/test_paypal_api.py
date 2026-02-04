"""
Tests for PayPal API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.paypal_api import router, get_paypal_provider


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_paypal_client(api_app):
    """Mock PayPal Client."""
    service = AsyncMock()
    service.create_order.return_value = {"id": "PAYPAL_123", "status": "CREATED"}
    service.capture_order.return_value = {"id": "PAYPAL_123", "status": "COMPLETED"}
    
    api_app.dependency_overrides[get_paypal_provider] = lambda: service
    return service


def test_create_order_success(client, mock_paypal_client):
    """Test creating PayPal order."""
    payload = {"amount": 29.0, "currency": "USD"}
    response = client.post('/api/v1/paypal/payment/paypal/create-order', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['id'] == "PAYPAL_123"


def test_create_order_failure(client, mock_paypal_client):
    """Test creating PayPal order failure."""
    mock_paypal_client.create_order.side_effect = RuntimeError("API down")
    payload = {"amount": 29.0, "currency": "USD"}
    response = client.post('/api/v1/paypal/payment/paypal/create-order', json=payload)
    
    assert response.status_code == 500
    data = response.json()
    assert data['success'] is False


def test_capture_order_success(client, mock_paypal_client):
    """Test capturing PayPal order."""
    payload = {"order_id": "PAYPAL_123"}
    response = client.post('/api/v1/paypal/payment/paypal/capture-order', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "COMPLETED"


def test_capture_order_no_id(client, mock_paypal_client):
    """Test capturing without order ID."""
    payload = {"order_id": ""}
    response = client.post('/api/v1/paypal/payment/paypal/capture-order', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
