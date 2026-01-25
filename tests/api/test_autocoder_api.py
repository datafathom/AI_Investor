"""
Tests for Autocoder API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.autocoder_api import autocoder_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(autocoder_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_autocoder():
    """Mock Autocoder."""
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
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'code' in data


def test_validate_code_success(client, mock_autocoder):
    """Test successful code validation."""
    response = client.post('/api/v1/dev/validate',
                          json={'code': 'def test(): pass'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'is_valid' in data


def test_deploy_module_success(client, mock_autocoder):
    """Test successful module deployment."""
    response = client.post('/api/v1/dev/deploy',
                          json={
                              'name': 'test_module',
                              'code': 'def test(): pass'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'module_name' in data
