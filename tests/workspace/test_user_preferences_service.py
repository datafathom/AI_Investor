
import pytest
from unittest.mock import MagicMock, patch
from services.workspace.user_preferences_service import UserPreferencesService, WorkspaceLayout, WindowState

@pytest.fixture
def workspace_service():
    UserPreferencesService._instance = None
    with patch('services.workspace.user_preferences_service.get_database_manager') as mock_db:
        service = UserPreferencesService()
        service.db = MagicMock()
        return service

def test_save_workspace(workspace_service):
    mock_cursor = MagicMock()
    workspace_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ["uuid-123"]
    
    layout = WorkspaceLayout(
        workspace_name="Default",
        windows=[
            WindowState(id="w1", title="Terminal", x=0, y=0, width=400, height=300, zIndex=1)
        ]
    )
    
    ws_id = workspace_service.save_workspace("user-1", layout)
    
    assert ws_id == "uuid-123"
    assert mock_cursor.execute.call_count == 1
    args = mock_cursor.execute.call_args[0]
    assert "INSERT INTO user_workspaces" in args[0]
    assert "user-1" in args[1]
    assert "Default" in args[1]

def test_get_workspace(workspace_service):
    mock_cursor = MagicMock()
    workspace_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    
    # row = id, workspace_name, layout_json, updated_at
    mock_cursor.fetchone.return_value = [
        "uuid-123", "Default", '[{"id": "w1", "title": "Terminal", "x": 0, "y": 0, "width": 400, "height": 300, "z_index": 1}]', None
    ]
    
    ws = workspace_service.get_workspace("user-1", "Default")
    
    assert ws.workspace_name == "Default"
    assert len(ws.windows) == 1
    assert ws.windows[0].id == "w1"

def test_list_workspaces(workspace_service):
    mock_cursor = MagicMock()
    workspace_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ("uuid-1", "Default", True, None),
        ("uuid-2", "Analytics", False, None)
    ]
    
    workspaces = workspace_service.list_workspaces("user-1")
    
    assert len(workspaces) == 2
    assert workspaces[0]["name"] == "Default"
    assert workspaces[1]["name"] == "Analytics"
