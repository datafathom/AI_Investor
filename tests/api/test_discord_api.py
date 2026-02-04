"""
Tests for Discord API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.discord_api import router, get_discord_bot_provider


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
def mock_discord_bot(api_app):
    """Mock DiscordBot."""
    bot = AsyncMock()
    bot.get_recent_mentions.return_value = [
        {'message_id': 'msg_1', 'content': 'Test mention', 'timestamp': '2024-01-01'}
    ]
    bot.get_hype_score.return_value = {'score': 0.75, 'trend': 'bullish'}
    api_app.dependency_overrides[get_discord_bot_provider] = lambda: bot
    return bot


def test_get_mentions_success(client, mock_discord_bot):
    """Test successful mentions retrieval."""
    response = client.get('/api/v1/discord/mentions/AAPL?limit=10')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['ticker'] == 'AAPL'
    assert len(data['data']['mentions']) == 1


def test_get_hype_success(client, mock_discord_bot):
    """Test successful hype score retrieval."""
    response = client.get('/api/v1/discord/hype/AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['score'] == 0.75
