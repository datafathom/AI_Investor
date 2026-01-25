"""
Tests for Twilio API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.twilio_api import twilio_api_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(twilio_api_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_twilio_client():
    """Mock Twilio client."""
    with patch('web.api.twilio_api.get_twilio_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_send_alert_success(client, mock_twilio_client):
    """Test successful SMS alert sending."""
    mock_result = {'sid': 'SM123', 'status': 'sent'}
    
    async def mock_send_sms(to, message):
        return mock_result
    
    mock_twilio_client.send_sms = mock_send_sms
    
    response = client.post('/notifications/twilio/send?mock=true',
                          json={'to': '+15551234567', 'message': 'Test Alert'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'sid' in data or 'status' in data


def test_send_alert_missing_params(client):
    """Test SMS sending with missing parameters."""
    response = client.post('/notifications/twilio/send?mock=true',
                          json={'to': '+15551234567'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
