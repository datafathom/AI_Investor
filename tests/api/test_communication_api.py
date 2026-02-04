
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.communication_api import router, get_briefing_provider, get_notification_provider

@pytest.fixture
def api_app(mock_briefing_service, mock_notification_manager):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_briefing_provider] = lambda: mock_briefing_service
    app.dependency_overrides[get_notification_provider] = lambda: mock_notification_manager
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_briefing_service():
    """Mock BriefingService."""
    service = MagicMock()
    service.generate_briefing.return_value = 'Good morning, Commander. Your portfolio is performing well.'
    return service

@pytest.fixture
def mock_notification_manager():
    """Mock NotificationManager."""
    manager = MagicMock()
    manager.send_alert.return_value = None
    manager.history = [{'channels': ['email']}]
    return manager

def test_get_morning_briefing_success(client, mock_briefing_service):
    """Test successful morning briefing retrieval."""
    response = client.get('/api/v1/communication/briefing?name=Test&value=100000&fear=50&sentiment=NEUTRAL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'briefing_text' in data['data']
    assert 'meta' in data['data']

def test_trigger_test_alert_success(client, mock_notification_manager):
    """Test successful test alert triggering."""
    response = client.post('/api/v1/communication/test-alert',
                          json={'message': 'Test Alert', 'priority': 'INFO'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'sent'
    assert 'channels' in data['data']
