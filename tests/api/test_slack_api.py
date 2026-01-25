"""
Tests for Slack API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.slack_api import slack_api_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(slack_api_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_slack_client():
    """Mock Slack client."""
    with patch('web.api.slack_api.get_slack_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_post_message_success(client, mock_slack_client):
    """Test successful message posting."""
    mock_result = {'ok': True, 'ts': '1234567890.123456'}
    
    async def mock_post_message(channel, text):
        return mock_result
    
    mock_slack_client.post_message = mock_post_message
    
    response = client.post('/team/slack/message?mock=true',
                          json={'channel': '#general', 'text': 'Hello World'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data.get('ok') is True or 'ts' in data


def test_post_message_missing_params(client):
    """Test message posting with missing parameters."""
    response = client.post('/team/slack/message?mock=true',
                          json={'channel': '#general'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_get_channels_success(client, mock_slack_client):
    """Test successful channels retrieval."""
    mock_channels = [{'id': 'C123', 'name': 'general'}]
    
    async def mock_get_channels():
        return mock_channels
    
    mock_slack_client.get_channels = mock_get_channels
    
    response = client.get('/team/slack/channels?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or 'channels' in data
