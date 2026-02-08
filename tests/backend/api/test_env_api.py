import pytest
import os
from fastapi.testclient import TestClient
from web.fastapi_gateway import app
from services.system.env_manager import get_env_manager, ENV_FILE

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_env_file():
    manager = get_env_manager()
    # Mocking os.environ partially is hard safely, 
    # but we can rely on the fact that existing env vars are loaded.
    # We will test the API logic.
    yield

def test_list_env_vars():
    response = client.get("/api/v1/admin/env")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Ensure masking
    for item in data:
        if item["is_sensitive"]:
            assert item["value"] == "******"

def test_update_env_var():
    # Use a safe test key
    TEST_KEY = "TEST_API_VAR_XYZ"
    TEST_VAL = "12345"
    
    response = client.post("/api/v1/admin/env", json={"key": TEST_KEY, "value": TEST_VAL})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify it appears in list
    response = client.get("/api/v1/admin/env")
    data = response.json()
    matching = [d for d in data if d["key"] == TEST_KEY]
    assert len(matching) == 1
    assert matching[0]["value"] == TEST_VAL
    
    # Cleanup env var (best effort)
    if TEST_KEY in os.environ:
        del os.environ[TEST_KEY]
