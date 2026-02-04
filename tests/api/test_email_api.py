"""
Tests for Email API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.email_api import router, get_sendgrid_provider


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
def mock_sendgrid_client(api_app):
    """Mock SendGrid client."""
    client = AsyncMock()
    api_app.dependency_overrides[get_sendgrid_provider] = lambda: client
    return client


def test_send_test_email_success(client, mock_sendgrid_client):
    """Test successful email sending."""
    mock_result = {'message_id': 'msg_123', 'status': 'sent'}
    mock_sendgrid_client.send_email.return_value = mock_result
    
    response = client.post('/api/v1/email/notifications/email/send?mock=true',
                          json={
                              'to': 'user@example.com',
                              'subject': 'Test',
                              'content': 'Hello'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['message_id'] == 'msg_123'


def test_send_email_missing_to(client):
    """Test email sending without recipient."""
    response = client.post('/api/v1/email/notifications/email/send?mock=true',
                          json={'subject': 'Test', 'content': 'Hello'})
    
    # Pydantic validation error or explicit check
    # Pydantic will return 422 if 'to' is missing in SendEmailRequest
    assert response.status_code == 422


def test_update_subscriptions_success(client, mock_sendgrid_client):
    """Test successful subscription update."""
    mock_result = {'status': 'updated'}
    mock_sendgrid_client.update_subscriptions.return_value = mock_result
    
    response = client.post('/api/v1/email/notifications/email/subscribe?mock=true',
                          json={
                              'email': 'user@example.com',
                              'preferences': {'daily': True}
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'updated'
