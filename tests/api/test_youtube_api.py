"""
Tests for YouTube API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.youtube_api import youtube_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(youtube_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_youtube_client():
    """Mock YouTubeClient."""
    with patch('web.api.youtube_api.get_youtube_client') as mock:
        client = AsyncMock()
        client.search_videos.return_value = [
            {'video_id': 'vid_1', 'title': 'Test Video', 'channel': 'Test Channel'}
        ]
        client.get_transcript.return_value = {'transcript': 'Test transcript text'}
        client.analyze_video.return_value = {'sentiment': 'positive', 'keywords': ['test']}
        mock.return_value = client
        yield client


def test_search_videos_success(client, mock_youtube_client):
    """Test successful video search."""
    response = client.get('/api/v1/youtube/search?query=investing&limit=5')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'query' in data
    assert 'videos' in data


def test_search_videos_missing_query(client):
    """Test video search without query."""
    response = client.get('/api/v1/youtube/search')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_get_transcript_success(client, mock_youtube_client):
    """Test successful transcript retrieval."""
    response = client.get('/api/v1/youtube/transcript/vid_123')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'transcript' in data or 'video_id' in data


def test_analyze_video_success(client, mock_youtube_client):
    """Test successful video analysis."""
    response = client.get('/api/v1/youtube/analyze/vid_123')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'sentiment' in data or 'analysis' in data
