"""
Tests for remaining Batch 8 APIs (Web3, Workspace, YouTube)
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.web3_api import router as web3_router
from web.api.workspace_api import router as workspace_router, get_user_preferences_provider
from web.api.youtube_api import router as youtube_router, get_youtube_provider


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(web3_router)
    app.include_router(workspace_router)
    app.include_router(youtube_router)
    return TestClient(app)


@pytest.fixture
def mock_user_prefs(client):
    service = MagicMock()
    # Mock get_workspace to return a mock model with model_dump
    workspace = MagicMock()
    workspace.model_dump.return_value = {"name": "test", "layout": {}}
    service.get_workspace.return_value = workspace
    service.list_workspaces.return_value = []
    service.save_workspace.return_value = "ws_123"
    
    client.app.dependency_overrides[get_user_preferences_provider] = lambda: service
    return service


@pytest.fixture
def mock_youtube(client):
    service = AsyncMock()
    service.search_videos.return_value = [{"title": "Video 1"}]
    service.get_channel_statistics.return_value = {"subscribers": 1000}
    
    client.app.dependency_overrides[get_youtube_provider] = lambda: service
    return service


# --- Web3 Tests ---

def test_web3_portfolio_success(client):
    response = client.get('/api/v1/web3/portfolio/current')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'total_value_usd' in data['data']


# --- Workspace Tests ---

def test_get_workspace_success(client, mock_user_prefs):
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "user_1"}
    
    response = client.get('/api/v1/user/workspace?name=test')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['name'] == "test"


# --- YouTube Tests ---

@pytest.mark.asyncio
async def test_youtube_search_success(client, mock_youtube):
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "user_1"}
    
    response = client.get('/api/v1/youtube/search?q=trading')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['videos']) == 1
