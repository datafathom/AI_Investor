"""
Tests for Autocoder API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.autocoder_api import router


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
def mock_autocoder():
    """Mock Autocoder."""
    # patch the import in web.api.autocoder_api
    with patch('web.api.autocoder_api.get_autocoder') as mock:
        coder = MagicMock()
        coder.generate_code.return_value = 'def test_function(): pass'
        coder.validate_code.return_value = True
        coder.deploy_module.return_value = MagicMock()
        mock.return_value = coder
        yield coder


def test_generate_code_success(client, mock_autocoder):
    """Test successful code generation."""
    response = client.post('/api/v1/dev/generate',
                          json={'task': 'Create a test adapter'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'code' in data


def test_validate_code_success(client, mock_autocoder):
    """Test successful code validation."""
    response = client.post('/api/v1/dev/validate',
                          json={'code': 'def test(): pass'})
    
    assert response.status_code == 200
    data = response.json()
    assert 'is_valid' in data


def test_deploy_module_success(client, mock_autocoder):
    """Test successful module deployment."""
    response = client.post('/api/v1/dev/deploy',
                          json={
                              'name': 'test_module',
                              'code': 'def test(): pass'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'module_name' in data
