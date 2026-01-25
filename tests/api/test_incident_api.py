"""
Tests for Incident API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.incident_api import incident_api_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(incident_api_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_pagerduty_client():
    """Mock PagerDuty client."""
    with patch('web.api.incident_api.get_pagerduty_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_trigger_incident_success(client, mock_pagerduty_client):
    """Test successful incident triggering."""
    mock_result = {'incident_id': 'inc_123', 'status': 'triggered'}
    
    async def mock_trigger(title, urgency):
        return mock_result
    
    mock_pagerduty_client.trigger_incident = mock_trigger
    
    response = client.post('/ops/incidents/trigger?mock=true',
                          json={'title': 'System Down', 'urgency': 'high'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'incident_id' in data or 'status' in data


def test_trigger_incident_missing_title(client):
    """Test incident triggering without title."""
    response = client.post('/ops/incidents/trigger?mock=true',
                          json={'urgency': 'high'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_get_incidents_success(client, mock_pagerduty_client):
    """Test successful incidents retrieval."""
    mock_incidents = [{'id': 'inc_1', 'title': 'Test Incident', 'status': 'open'}]
    
    async def mock_get_incidents():
        return mock_incidents
    
    mock_pagerduty_client.get_incidents = mock_get_incidents
    
    response = client.get('/ops/incidents?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'incidents' in data
