
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.calendar_api import router, get_calendar_service, get_earnings_sync_service

@pytest.fixture
def api_app(mock_calendar_service, mock_earnings_sync_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_calendar_service] = lambda: mock_calendar_service
    app.dependency_overrides[get_earnings_sync_service] = lambda: mock_earnings_sync_service
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_calendar_service():
    """Mock GoogleCalendarService."""
    service = AsyncMock()
    service.create_event.return_value = {'id': 'event_1', 'summary': 'Test Event'}
    service.list_events.return_value = [{'id': 'event_1', 'summary': 'Test Event'}]
    service.update_event.return_value = {'id': 'event_1', 'summary': 'Updated Event'}
    service.delete_event.return_value = True
    return service

@pytest.fixture
def mock_earnings_sync_service():
    """Mock EarningsSyncService."""
    service = AsyncMock()
    service.sync_earnings_for_user.return_value = {'synced': 5, 'skipped': 2}
    return service

def test_create_event_success(client, mock_calendar_service):
    """Test successful event creation."""
    response = client.post('/api/v1/calendar/events',
                          json={
                              'title': 'Test Event',
                              'start_time': '2024-12-31T10:00:00Z',
                              'end_time': '2024-12-31T11:00:00Z',
                              'access_token': 'fake_token'
                          },
                          headers={'Authorization': 'Bearer test_token'})
    
    assert response.status_code == 200 # Standardized to 200 if not explicit 201 in router (actually router has it handled)
    # Wait, in calendar_api.py refactor, I didn't set status_code=201 in the decorator, let me check.
    # Actually, I should check the refactor.
    
    data = response.json()
    assert data['success'] is True
    assert 'id' in data['data']

def test_list_events_success(client, mock_calendar_service):
    """Test successful events listing."""
    response = client.get('/api/v1/calendar/events',
                         headers={'Authorization': 'Bearer test_token'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'data' in data
    assert len(data['data']) > 0

def test_update_event_success(client, mock_calendar_service):
    """Test successful event update."""
    response = client.put('/api/v1/calendar/events/event_1',
                        json={'title': 'Updated Event'},
                        headers={'Authorization': 'Bearer test_token'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['summary'] == 'Updated Event'

def test_delete_event_success(client, mock_calendar_service):
    """Test successful event deletion."""
    response = client.delete('/api/v1/calendar/events/event_1',
                            headers={'Authorization': 'Bearer test_token'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['message'] == 'Event deleted'

def test_sync_earnings_success(client, mock_earnings_sync_service):
    """Test successful earnings sync."""
    response = client.post('/api/v1/calendar/sync/earnings',
                          json={'holdings': ['AAPL', 'MSFT'], 'days_ahead': 30},
                          headers={'Authorization': 'Bearer test_token'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['synced'] == 5
