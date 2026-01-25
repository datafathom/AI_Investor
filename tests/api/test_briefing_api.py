"""
Tests for Briefing API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.briefing_api import briefing_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(briefing_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_briefing_generator():
    """Mock BriefingGenerator."""
    with patch('web.api.briefing_api.get_briefing_generator') as mock:
        generator = MagicMock()
        mock.return_value = generator
        yield generator


def test_get_daily_briefing_success(client, mock_briefing_generator):
    """Test successful daily briefing retrieval."""
    mock_result = {'briefing': 'Good morning, Commander. Your portfolio is performing well.'}
    
    async def mock_get_briefing():
        return mock_result
    
    mock_briefing_generator.get_daily_briefing = mock_get_briefing
    
    response = client.get('/briefing/daily?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'briefing' in data or 'content' in data
