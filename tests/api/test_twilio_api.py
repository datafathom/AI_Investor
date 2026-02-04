"""
Tests for Twilio API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.twilio_api import router, get_twilio_provider


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
def mock_twilio_client(api_app):
    """Mock Twilio Client."""
    service = AsyncMock()
    service.send_sms.return_value = {"sid": "SM123", "status": "sent"}
    
    api_app.dependency_overrides[get_twilio_provider] = lambda: service
    return service


def test_send_alert_success(client, mock_twilio_client):
    """Test sending SMS alert."""
    payload = {"to": "+1234567890", "message": "Hello World"}
    response = client.post('/api/v1/twilio/notifications/twilio/send', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['sid'] == "SM123"


def test_send_alert_missing_fields(client):
    """Test sending SMS with missing fields."""
    payload = {"to": "", "message": ""}
    response = client.post('/api/v1/twilio/notifications/twilio/send', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
