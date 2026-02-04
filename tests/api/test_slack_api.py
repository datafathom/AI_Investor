"""
Tests for Slack API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.slack_api import router, get_slack_provider


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_client(api_app):
    """Mock Slack Client."""
    service = AsyncMock()
    service.post_message.return_value = {"ok": True, "ts": "123.456"}
    service.get_channels.return_value = [{"id": "C123", "name": "general"}]
    
    api_app.dependency_overrides[get_slack_provider] = lambda: service
    return service


def test_post_message_success(client, mock_client):
    """Test posting message."""
    payload = {"channel": "#general", "text": "Hello"}
    response = client.post('/api/v1/team/slack/message', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['ts'] == "123.456"


def test_get_channels_success(client, mock_client):
    """Test getting channels."""
    response = client.get('/api/v1/team/slack/channels')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'][0]['name'] == "general"


def test_missing_params(client):
    """Test missing parameters."""
    payload = {"channel": "#general"}
    response = client.post('/api/v1/team/slack/message', json=payload)
    
    # Pydantic validation error (since text is required in BaseModel)
    assert response.status_code == 422
