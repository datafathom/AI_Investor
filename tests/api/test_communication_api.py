"""
Tests for Communication API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.communication_api import communication_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(communication_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_briefing_service():
    """Mock BriefingService."""
    with patch('web.api.communication_api.get_briefing_service') as mock:
        service = MagicMock()
        service.generate_briefing.return_value = 'Good morning, Commander. Your portfolio is performing well.'
        mock.return_value = service
        yield service


@pytest.fixture
def mock_notification_manager():
    """Mock NotificationManager."""
    with patch('web.api.communication_api.get_notification_manager') as mock:
        manager = MagicMock()
        manager.send_alert.return_value = {'status': 'sent', 'channel': 'email'}
        mock.return_value = manager
        yield manager


def test_get_morning_briefing_success(client, mock_briefing_service):
    """Test successful morning briefing retrieval."""
    response = client.get('/api/v1/communication/briefing?name=Test&value=100000&fear=50&sentiment=NEUTRAL')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'briefing_text' in data
    assert 'meta' in data


def test_trigger_test_alert_success(client, mock_notification_manager):
    """Test successful test alert triggering."""
    response = client.post('/api/v1/communication/test-alert',
                          json={'message': 'Test Alert', 'priority': 'INFO'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data or 'message' in data
