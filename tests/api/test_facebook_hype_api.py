"""
Tests for Facebook Hype API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.facebook_hype_api import router, get_facebook_hype_provider


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
def mock_facebook_hype_service(api_app):
    """Mock FacebookHypeService."""
    service = AsyncMock()
    service.monitor_page.return_value = {'monitor_id': 'mon_1', 'status': 'active'}
    service.get_hourly_aggregates.return_value = {'hourly_mentions': []}
    service.check_for_spikes.return_value = None  # No spike
    api_app.dependency_overrides[get_facebook_hype_provider] = lambda: service
    return service


def test_monitor_page_missing_token(client):
    """Test page monitoring without access token."""
    response = client.post('/api/v1/facebook_hype/monitor',
                          json={
                              'page_id': 'page_123',
                              'tickers': ['AAPL']
                          })
    
    # Returns 401 for missing token
    assert response.status_code == 401


def test_monitor_page_with_token(client):
    """Test page monitoring with access token in body."""
    with patch('services.social.facebook_hype_service.get_facebook_hype_service') as mock_service:
        service = AsyncMock()
        service.monitor_page.return_value = {'monitor_id': 'mon_1', 'status': 'active'}
        mock_service.return_value = service
        
        response = client.post('/api/v1/facebook_hype/monitor',
                              json={
                                  'page_id': 'page_123',
                                  'tickers': ['AAPL'],
                                  'access_token': 'test_token'
                              })
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True


def test_get_aggregates_success(client):
    """Test successful aggregates retrieval."""
    with patch('services.social.facebook_hype_service.get_facebook_hype_service') as mock_service:
        service = AsyncMock()
        service.get_hourly_aggregates.return_value = {'hourly_mentions': []}
        mock_service.return_value = service
        
        response = client.get('/api/v1/facebook_hype/aggregates?ticker=AAPL')
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True


def test_check_spike_no_spike(client):
    """Test spike check when no spike detected."""
    with patch('services.social.facebook_hype_service.get_facebook_hype_service') as mock_service:
        service = AsyncMock()
        service.check_for_spikes.return_value = None
        mock_service.return_value = service
        
        response = client.post('/api/v1/facebook_hype/check-spike',
                              json={'page_id': 'page_123', 'ticker': 'AAPL', 'threshold_multiplier': 2.0})
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data']['spike_detected'] is False
