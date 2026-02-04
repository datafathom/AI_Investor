"""
Tests for Incident API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.incident_api import router, get_pagerduty_provider


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
def mock_pagerduty_client(api_app):
    """Mock PagerDuty Client."""
    client_instance = AsyncMock()
    client_instance.trigger_incident.return_value = {'incident_id': 'PD123', 'status': 'triggered'}
    client_instance.get_incidents.return_value = [{'id': 'PD123', 'title': 'Test Incident'}]
    
    # The provider returns the factory function
    api_app.dependency_overrides[get_pagerduty_provider] = lambda: (lambda mock=True: client_instance)
    return client_instance


def test_trigger_incident_success(client, mock_pagerduty_client):
    """Test triggering an incident."""
    response = client.post('/api/v1/incident/ops/incidents/trigger',
                           json={'title': 'System Overload', 'urgency': 'high'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['incident_id'] == 'PD123'


def test_get_incidents_success(client, mock_pagerduty_client):
    """Test getting incidents."""
    response = client.get('/api/v1/incident/ops/incidents')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'Test Incident'
