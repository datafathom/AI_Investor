import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)

def test_get_status():
    response = client.get("/api/v1/admin/deployments/status")
    assert response.status_code == 200
    data = response.json()
    assert "active_env" in data
    assert "traffic_split" in data
    assert "environments" in data
    assert "blue" in data["environments"]
    assert "green" in data["environments"]

def test_switch_environment():
    # Switch to Green
    response = client.post("/api/v1/admin/deployments/switch", json={"target_env": "green"})
    assert response.status_code == 200
    data = response.json()
    assert data["active_env"] == "green"
    assert data["traffic_split"]["green"] == 100
    assert data["traffic_split"]["blue"] == 0

    # Switch back to Blue
    response = client.post("/api/v1/admin/deployments/switch", json={"target_env": "blue"})
    assert response.status_code == 200
    assert response.json()["active_env"] == "blue"

def test_invalid_switch():
    response = client.post("/api/v1/admin/deployments/switch", json={"target_env": "yellow"})
    assert response.status_code == 400

def test_usage_traffic_split():
    response = client.post("/api/v1/admin/deployments/traffic", json={"blue": 80, "green": 20})
    assert response.status_code == 200
    data = response.json()
    assert data["traffic_split"]["blue"] == 80
    assert data["traffic_split"]["green"] == 20

def test_rollback():
    # Ensure starting state
    client.post("/api/v1/admin/deployments/switch", json={"target_env": "blue"})
    
    # Rollback should go to Green
    response = client.post("/api/v1/admin/deployments/rollback")
    assert response.status_code == 200
    assert response.json()["active_env"] == "green"
