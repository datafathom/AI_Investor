"""
Tests for Debate API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.debate_api import router, get_debate_provider


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
def mock_debate_agent(api_app):
    """Mock DebateAgent."""
    agent = AsyncMock()
    # transcript and consensus are attributes, not methods
    agent.transcript = []
    agent.consensus = {}
    api_app.dependency_overrides[get_debate_provider] = lambda: agent
    return agent


def test_run_debate_success(client, mock_debate_agent):
    """Test successful debate execution."""
    mock_result = {
        'ticker': 'AAPL',
        'bullish_score': 0.6,
        'bearish_score': 0.4,
        'consensus': 'bullish'
    }
    
    mock_debate_agent.conduct_debate.return_value = mock_result
    
    response = client.post('/api/v1/ai/debate/run/AAPL?mock=true')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['ticker'] == 'AAPL'
    assert data['data']['consensus'] == 'bullish'


def test_start_debate_success(client, mock_debate_agent):
    """Test starting a debate via the /start endpoint."""
    mock_result = {
        'ticker': 'SPY',
        'status': 'started'
    }
    mock_debate_agent.conduct_debate.return_value = mock_result
    
    response = client.post('/api/v1/ai/debate/start', json={'ticker': 'SPY'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['ticker'] == 'SPY'


def test_stream_debate_success(client, mock_debate_agent):
    """Test streaming debate state."""
    mock_debate_agent.transcript = ["Argument 1"]
    mock_debate_agent.consensus = {"bias": "neutral"}
    
    response = client.get('/api/v1/ai/debate/stream')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'active'
    assert data['data']['transcript'] == ["Argument 1"]
