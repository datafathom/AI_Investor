
import pytest
from unittest.mock import MagicMock, patch
from web.app import create_app

@pytest.fixture
def client():
    app, socketio = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_user_pref_service():
    with patch('web.api.workspace_api.get_user_preferences_service') as mock:
        yield mock

@pytest.fixture
def mock_token():
    # web.auth_utils uses jwt
    with patch('web.auth_utils.jwt.decode') as mock:
        yield mock

def test_get_workspace_not_found(client, mock_user_pref_service, mock_token):
    mock_token.return_value = {'sub': 'user-1', 'tenant_id': 'default', 'role': 'trader'}
    mock_service = mock_user_pref_service.return_value
    mock_service.get_workspace.return_value = None
    
    headers = {'Authorization': 'Bearer some-token'}
    response = client.get('/api/v1/user/workspace?name=Missing', headers=headers)
    
    assert response.status_code == 404
    assert response.json['error'] == 'Workspace not found'

def test_save_workspace_success(client, mock_user_pref_service, mock_token):
    mock_token.return_value = {'sub': 'user-1', 'tenant_id': 'default', 'role': 'trader'}
    mock_service = mock_user_pref_service.return_value
    mock_service.save_workspace.return_value = "new-uuid"
    
    payload = {
        "workspace_name": "NewWorkspace",
        "windows": [
            {"id": "w1", "title": "Test", "x": 10, "y": 10, "width": 100, "height": 100}
        ]
    }
    
    headers = {'Authorization': 'Bearer some-token'}
    response = client.post('/api/v1/user/workspace', json=payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json['id'] == "new-uuid"
