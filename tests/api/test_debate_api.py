"""
Tests for Debate API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.debate_api import debate_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(debate_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_debate_agent():
    """Mock DebateAgent."""
    with patch('web.api.debate_api.get_debate_agent') as mock:
        agent = MagicMock()
        mock.return_value = agent
        yield agent


def test_run_debate_success(client, mock_debate_agent):
    """Test successful debate execution."""
    mock_result = {
        'ticker': 'AAPL',
        'bullish_score': 0.6,
        'bearish_score': 0.4,
        'consensus': 'bullish'
    }
    
    async def mock_conduct_debate(ticker):
        return mock_result
    
    mock_debate_agent.conduct_debate = mock_conduct_debate
    
    response = client.post('/debate/run/AAPL?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'ticker' in data or 'consensus' in data
