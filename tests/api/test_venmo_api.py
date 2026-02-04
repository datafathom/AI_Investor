"""
Tests for Venmo API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.venmo_api import router, get_venmo_provider


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
def mock_venmo_client(api_app):
    """Mock Venmo Client."""
    service = AsyncMock()
    service.process_payment.return_value = {"payment_id": "V123", "status": "settled"}
    
    api_app.dependency_overrides[get_venmo_provider] = lambda: service
    return service


def test_pay_success(client, mock_venmo_client):
    """Test Venmo payment."""
    payload = {"amount": 29.00}
    response = client.post('/api/v1/venmo/payment/venmo/pay', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['payment_id'] == "V123"
