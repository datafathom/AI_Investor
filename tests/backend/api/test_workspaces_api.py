import pytest
import os
import json
from fastapi.testclient import TestClient
from web.fastapi_gateway import app
from services.workspaces.manager import get_workspace_manager, WORKSPACES_FILE

client = TestClient(app)

# Use a temp file for testing
TEST_WORKSPACES_FILE = "test_workspaces_data.json"

@pytest.fixture(autouse=True)
def mock_storage():
    manager = get_workspace_manager()
    original_file = manager.file_path
    manager.file_path = TEST_WORKSPACES_FILE
    # Start clean
    manager.workspaces = []
    manager._save_data()
    
    yield
    
    # Cleanup
    manager.file_path = original_file
    if os.path.exists(TEST_WORKSPACES_FILE):
        os.remove(TEST_WORKSPACES_FILE)

def test_create_workspace():
    payload = {
        "name": "Test Workspace",
        "layout": {"widgets": ["monitor", "chart"]}
    }
    response = client.post("/api/v1/admin/workspaces", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Workspace"
    assert data["layout"]["widgets"] == ["monitor", "chart"]
    assert "id" in data

def test_list_workspaces():
    # Create one first
    client.post("/api/v1/admin/workspaces", json={"name": "WS1", "layout": {}})
    
    response = client.get("/api/v1/admin/workspaces")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "WS1"

def test_update_workspace():
    # Create
    create_res = client.post("/api/v1/admin/workspaces", json={"name": "WS1", "layout": {}})
    ws_id = create_res.json()["id"]
    
    # Update
    update_res = client.put(f"/api/v1/admin/workspaces/{ws_id}", json={"name": "WS1_Updated"})
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "WS1_Updated"

def test_delete_workspace():
    # Create
    create_res = client.post("/api/v1/admin/workspaces", json={"name": "WS1", "layout": {}})
    ws_id = create_res.json()["id"]
    
    # Delete
    del_res = client.delete(f"/api/v1/admin/workspaces/{ws_id}")
    assert del_res.status_code == 200
    
    # Verify gone
    get_res = client.get(f"/api/v1/admin/workspaces/{ws_id}")
    assert get_res.status_code == 404
