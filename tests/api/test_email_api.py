"""
Tests for Email API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.email_api import email_api_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(email_api_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_sendgrid_client():
    """Mock SendGrid client."""
    with patch('web.api.email_api.get_sendgrid_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_send_test_email_success(client, mock_sendgrid_client):
    """Test successful email sending."""
    mock_result = {'message_id': 'msg_123', 'status': 'sent'}
    
    async def mock_send_email(to, subject, content):
        return mock_result
    
    mock_sendgrid_client.send_email = mock_send_email
    
    response = client.post('/notifications/email/send?mock=true',
                          json={
                              'to': 'user@example.com',
                              'subject': 'Test',
                              'content': 'Hello'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message_id' in data or 'status' in data


def test_send_email_missing_to(client):
    """Test email sending without recipient."""
    response = client.post('/notifications/email/send?mock=true',
                          json={'subject': 'Test', 'content': 'Hello'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_update_subscriptions_success(client, mock_sendgrid_client):
    """Test successful subscription update."""
    mock_result = {'status': 'updated'}
    
    async def mock_update_subscriptions(email, preferences):
        return mock_result
    
    mock_sendgrid_client.update_subscriptions = mock_update_subscriptions
    
    response = client.post('/notifications/email/subscribe?mock=true',
                          json={
                              'email': 'user@example.com',
                              'preferences': {'daily': True}
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data or 'message' in data
