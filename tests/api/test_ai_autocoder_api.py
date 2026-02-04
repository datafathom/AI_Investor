"""
Tests for AI Autocoder API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.ai_autocoder_api import router, _get_autocoder_agent


@pytest.fixture
def mock_autocoder_agent():
    """Mock AutocoderAgent."""
    class MockAgent:
        def __init__(self):
            class Simple: pass
            self.model_config = Simple()
            self.model_config.provider = Simple()
            self.model_config.provider.value = "openai"
            self.model_config.model_id = "gpt-4"
            self.sandbox = Simple()
            self.sandbox.timeout = 30
            
            async def mock_exec(code, ctx):
                class Res: pass
                res = Res()
                res.success = True
                res.output = "Test output"
                res.error = None
                res.execution_time_ms = 10
                return res
            self.sandbox.execute = mock_exec

        async def generate_code(self, prompt, context, execute):
            return {
                'code': 'def test(): pass', 
                'model': 'gpt-4',
                'tokens_used': 100,
                'execution_result': 'Success'
            }
        
        def health_check(self):
            return {'agent': 'autocoder', 'active': True}

    return MockAgent()


@pytest.fixture
def api_app(mock_autocoder_agent):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[_get_autocoder_agent] = lambda: mock_autocoder_agent
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_generate_code_success(client, mock_autocoder_agent):
    """Test successful AI code generation."""
    response = client.post('/api/v1/ai/autocoder/generate',
                          json={'prompt': 'Create a function to calculate portfolio returns'})
    
    assert response.status_code == 200
    res_json = response.json()
    assert 'data' in res_json
    data = res_json['data']
    assert 'code' in data


def test_execute_code_success(client, mock_autocoder_agent):
    """Test successful code execution."""
    response = client.post('/api/v1/ai/autocoder/execute',
                          json={'code': 'print("Hello")'})
    
    assert response.status_code == 200
    res_json = response.json()
    assert 'data' in res_json
    data = res_json['data']
    assert data['success'] is True
    assert data['output'] == "Test output"


def test_get_status_success(client, mock_autocoder_agent):
    """Test successful status retrieval."""
    response = client.get('/api/v1/ai/autocoder/status')
    
    assert response.status_code == 200
    res_json = response.json()
    assert 'data' in res_json
    data = res_json['data']
    assert data['agent'] == 'autocoder'
    assert data['active'] is True
