"""
Tests for Politics API Endpoints
"""

import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.politics_api import router, get_congress_provider


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
def mock_congress_tracker(api_app):
    """Mock Congress Tracker Service."""
    service = MagicMock()
    service.fetch_latest_disclosures.return_value = [{"ticker": "AAPL", "representative": "Nancy"}]
    service.get_political_alpha_signal.return_value = 0.85
    service.correlate_with_lobbying.return_value = {
        "lobbying_intensity": 0.92,
        "confidence": 0.88
    }
    
    api_app.dependency_overrides[get_congress_provider] = lambda: service
    return service


def test_get_disclosures_success(client, mock_congress_tracker):
    """Test getting disclosures."""
    response = client.get('/api/v1/politics/disclosures')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['count'] == 1


def test_get_alpha_score_success(client, mock_congress_tracker):
    """Test getting alpha score."""
    response = client.get('/api/v1/politics/alpha/AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['alpha_score'] == 0.85


def test_get_alpha_score_failure(client, mock_congress_tracker):
    """Test alpha score failure."""
    mock_congress_tracker.get_political_alpha_signal.side_effect = Exception("Service error")
    response = client.get('/api/v1/politics/alpha/AAPL')
    
    assert response.status_code == 500
    data = response.json()
    assert data['success'] is False
