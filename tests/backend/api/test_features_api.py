import pytest
import os
import json
from fastapi.testclient import TestClient
from web.fastapi_gateway import app
from services.system.feature_flags import get_feature_flag_manager, FLAGS_FILE

client = TestClient(app)

TEST_FLAGS_FILE = "test_feature_flags.json"

@pytest.fixture(autouse=True)
def mock_flags_file():
    manager = get_feature_flag_manager()
    original_file = manager.file_path
    manager.file_path = TEST_FLAGS_FILE
    
    # Reset
    manager.flags = {"TEST_FLAG": False}
    manager._save_flags()
    
    yield
    
    # Cleanup
    manager.file_path = original_file
    if os.path.exists(TEST_FLAGS_FILE):
        os.remove(TEST_FLAGS_FILE)

def test_list_flags():
    response = client.get("/api/v1/admin/features")
    assert response.status_code == 200
    data = response.json()
    assert "TEST_FLAG" in data
    assert data["TEST_FLAG"] is False

def test_update_flag():
    response = client.put("/api/v1/admin/features/TEST_FLAG", json={"enabled": True})
    assert response.status_code == 200
    assert response.json()["enabled"] is True
    
    # Verify persistence
    response = client.get("/api/v1/admin/features")
    assert response.json()["TEST_FLAG"] is True
