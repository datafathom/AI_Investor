"""
Tests for Workspace API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.workspace_api import workspace_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(workspace_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_user_context(app):
    """Mock user context for authenticated requests."""
    with app.test_request_context():
        from flask import g
        g.user_id = 'user_1'
        yield g


def test_get_workspace_success(client, mock_user_context):
    """Test successful workspace retrieval."""
    with patch('web.api.workspace_api.get_user_preferences_service') as mock_service:
        from services.workspace.user_preferences_service import WorkspaceLayout
        
        mock_workspace = WorkspaceLayout(
            name='Test Workspace',
            widgets=[],
            layout={}
        )
        mock_service.return_value.get_workspace.return_value = mock_workspace
        
        with patch('web.api.workspace_api.login_required', lambda f: f):
            response = client.get('/api/v1/user/workspace?name=Test%20Workspace')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['name'] == 'Test Workspace'


def test_get_workspace_not_found(client, mock_user_context):
    """Test workspace retrieval when not found."""
    with patch('web.api.workspace_api.get_user_preferences_service') as mock_service:
        mock_service.return_value.get_workspace.return_value = None
        
        with patch('web.api.workspace_api.login_required', lambda f: f):
            response = client.get('/api/v1/user/workspace?name=Nonexistent')
            
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data


def test_save_workspace_success(client, mock_user_context):
    """Test successful workspace save."""
    with patch('web.api.workspace_api.get_user_preferences_service') as mock_service:
        mock_service.return_value.save_workspace.return_value = 'workspace_1'
        
        with patch('web.api.workspace_api.login_required', lambda f: f):
            response = client.post('/api/v1/user/workspace',
                                  json={
                                      'name': 'Test Workspace',
                                      'widgets': [],
                                      'layout': {},
                                      'is_default': False
                                  })
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['message'] == 'Workspace saved'
            assert data['id'] == 'workspace_1'


def test_list_workspaces_success(client, mock_user_context):
    """Test successful workspace listing."""
    with patch('web.api.workspace_api.get_user_preferences_service') as mock_service:
        mock_workspaces = [
            {'id': 'ws_1', 'name': 'Workspace 1'},
            {'id': 'ws_2', 'name': 'Workspace 2'}
        ]
        mock_service.return_value.list_workspaces.return_value = mock_workspaces
        
        with patch('web.api.workspace_api.login_required', lambda f: f):
            response = client.get('/api/v1/user/workspaces')
            
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 2
