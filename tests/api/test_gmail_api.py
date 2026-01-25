"""
Tests for Gmail API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.gmail_api import gmail_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(gmail_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_gmail_service():
    """Mock GmailService."""
    with patch('web.api.gmail_api.get_gmail_service') as mock:
        service = AsyncMock()
        service.send_email.return_value = {'message_id': 'msg_123', 'status': 'sent'}
        service.send_templated_email.return_value = {'message_id': 'msg_123', 'status': 'sent'}
        service.preview_template.return_value = {'subject': 'Test', 'body': 'Test body'}
        service.get_sending_stats.return_value = {'sent_today': 10, 'sent_total': 100}
        mock.return_value = service
        yield service


def test_send_email_success(client, mock_gmail_service):
    """Test successful email sending."""
    response = client.post('/api/v1/gmail/send',
                          json={
                              'to': 'test@example.com',
                              'subject': 'Test',
                              'body': 'Test body'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message_id' in data or 'status' in data


def test_send_template_success(client, mock_gmail_service):
    """Test successful templated email sending."""
    response = client.post('/api/v1/gmail/send-template',
                          json={
                              'to': 'test@example.com',
                              'template_id': 'template_1',
                              'variables': {}
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message_id' in data or 'status' in data


def test_preview_template_success(client, mock_gmail_service):
    """Test successful template preview."""
    response = client.get('/api/v1/gmail/preview?template_id=template_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'subject' in data or 'body' in data


def test_get_stats_success(client, mock_gmail_service):
    """Test successful stats retrieval."""
    response = client.get('/api/v1/gmail/stats')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'sent_today' in data or 'sent_total' in data
