"""
Tests for Discord API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.discord_api import discord_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(discord_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_discord_bot():
    """Mock DiscordBot."""
    with patch('web.api.discord_api.get_discord_bot') as mock:
        bot = AsyncMock()
        bot.get_recent_mentions.return_value = [
            {'message_id': 'msg_1', 'content': 'Test mention', 'timestamp': '2024-01-01'}
        ]
        bot.get_hype_score.return_value = {'score': 0.75, 'trend': 'bullish'}
        mock.return_value = bot
        yield bot


def test_get_mentions_success(client, mock_discord_bot):
    """Test successful mentions retrieval."""
    response = client.get('/api/v1/discord/mentions/AAPL?limit=10')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'ticker' in data
    assert 'mentions' in data


def test_get_hype_success(client, mock_discord_bot):
    """Test successful hype score retrieval."""
    response = client.get('/api/v1/discord/hype/AAPL')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'score' in data or 'hype' in data
