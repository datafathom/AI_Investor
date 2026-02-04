"""
Tests for Onboarding API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.onboarding_api import router
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    # Mock current user
    app.dependency_overrides[get_current_user] = lambda: {'id': 'user_1', 'email': 'test@example.com'}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_get_onboarding_status_success(client):
    """Test getting onboarding status."""
    response = client.get('/api/v1/onboarding/status')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['current_step'] == 1


def test_update_onboarding_step_success(client):
    """Test updating onboarding step."""
    payload = {"step": 2, "data": {"experience": "intermediate"}}
    response = client.post('/api/v1/onboarding/step', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['current_step'] == 2


def test_update_onboarding_step_invalid(client):
    """Test updating with invalid step."""
    payload = {"step": 99}
    response = client.post('/api/v1/onboarding/step', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False


def test_complete_onboarding_success(client):
    """Test completing onboarding."""
    payload = {
        "preferences": {
            "experience_level": "low",
            "risk_tolerance": "moderate"
        }
    }
    response = client.post('/api/v1/onboarding/complete', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['completed'] is True


def test_complete_onboarding_missing_fields(client):
    """Test completing with missing required fields."""
    payload = {"preferences": {"experience_level": "low"}}
    response = client.post('/api/v1/onboarding/complete', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False


def test_get_preferences_success(client):
    """Test getting preferences."""
    response = client.get('/api/v1/onboarding/preferences')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_update_preferences_success(client):
    """Test updating preferences."""
    payload = {"preferences": {"theme": "dark"}}
    response = client.put('/api/v1/onboarding/preferences', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_skip_onboarding_success(client):
    """Test skipping onboarding."""
    response = client.post('/api/v1/onboarding/skip')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['skipped'] is True


def test_reset_onboarding_success(client):
    """Test resetting onboarding."""
    response = client.post('/api/v1/onboarding/reset')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['reset'] is True
