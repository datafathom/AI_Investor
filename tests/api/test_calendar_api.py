"""
Tests for Calendar API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.calendar_api import calendar_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(calendar_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_calendar_service():
    """Mock GoogleCalendarService."""
    with patch('web.api.calendar_api.get_google_calendar_service') as mock:
        service = AsyncMock()
        service.create_event.return_value = {'id': 'event_1', 'summary': 'Test Event'}
        service.list_events.return_value = [{'id': 'event_1', 'summary': 'Test Event'}]
        service.update_event.return_value = {'id': 'event_1', 'summary': 'Updated Event'}
        service.delete_event.return_value = True
        mock.return_value = service
        yield service


def test_create_event_success(client, mock_calendar_service):
    """Test successful event creation."""
    response = client.post('/api/v1/calendar/events',
                          json={
                              'summary': 'Test Event',
                              'start': '2024-12-31T10:00:00',
                              'end': '2024-12-31T11:00:00'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data or 'event_id' in data


def test_list_events_success(client, mock_calendar_service):
    """Test successful events listing."""
    response = client.get('/api/v1/calendar/events')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'events' in data


def test_update_event_success(client, mock_calendar_service):
    """Test successful event update."""
    response = client.put('/api/v1/calendar/events/event_1',
                        json={'summary': 'Updated Event'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data or 'summary' in data


def test_delete_event_success(client, mock_calendar_service):
    """Test successful event deletion."""
    response = client.delete('/api/v1/calendar/events/event_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data or 'status' in data
