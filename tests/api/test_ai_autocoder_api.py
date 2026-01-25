"""
Tests for AI Autocoder API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.ai_autocoder_api import ai_autocoder_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(ai_autocoder_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_autocoder_agent():
    """Mock AutocoderAgent."""
    with patch('web.api.ai_autocoder_api._get_autocoder_agent') as mock:
        agent = AsyncMock()
        agent.generate_code.return_value = {'code': 'def test(): pass', 'explanation': 'Test function'}
        agent.execute_code.return_value = {'output': 'Test output', 'success': True}
        agent.get_status.return_value = {'status': 'healthy', 'model': 'gpt-4'}
        mock.return_value = agent
        yield agent


def test_generate_code_success(client, mock_autocoder_agent):
    """Test successful AI code generation."""
    response = client.post('/api/v1/ai/autocoder/generate',
                          json={'prompt': 'Create a function to calculate portfolio returns'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data or 'code' in data


def test_execute_code_success(client, mock_autocoder_agent):
    """Test successful code execution."""
    response = client.post('/api/v1/ai/autocoder/execute',
                          json={'code': 'print("Hello")'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'output' in data or 'result' in data


def test_get_status_success(client, mock_autocoder_agent):
    """Test successful status retrieval."""
    response = client.get('/api/v1/ai/autocoder/status')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data or 'health' in data
