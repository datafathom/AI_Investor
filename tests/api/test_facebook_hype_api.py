"""
Tests for Facebook Hype API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.facebook_hype_api import facebook_hype_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(facebook_hype_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_facebook_hype_service():
    """Mock FacebookHypeService."""
    with patch('web.api.facebook_hype_api.get_facebook_hype_service') as mock:
        service = AsyncMock()
        service.monitor_page.return_value = {'monitor_id': 'mon_1', 'status': 'active'}
        service.get_aggregates.return_value = {'hourly_mentions': []}
        service.check_spike.return_value = {'spike_detected': False, 'current_rate': 10}
        mock.return_value = service
        yield service


def test_monitor_page_success(client, mock_facebook_hype_service):
    """Test successful page monitoring."""
    response = client.post('/api/v1/facebook/monitor',
                          json={
                              'page_id': 'page_123',
                              'ticker': 'AAPL'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'monitor_id' in data or 'status' in data


def test_get_aggregates_success(client, mock_facebook_hype_service):
    """Test successful aggregates retrieval."""
    response = client.get('/api/v1/facebook/aggregates?ticker=AAPL')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'hourly_mentions' in data or 'aggregates' in data


def test_check_spike_success(client, mock_facebook_hype_service):
    """Test successful spike check."""
    response = client.post('/api/v1/facebook/check-spike',
                          json={'ticker': 'AAPL', 'threshold': 50})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'spike_detected' in data or 'current_rate' in data
