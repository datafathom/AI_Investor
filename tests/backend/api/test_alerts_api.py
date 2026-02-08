import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)

def test_list_rules():
    response = client.get("/api/v1/admin/alerts/rules")
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_rule():
    payload = {
        "name": "TEST_RULE",
        "metric": "cpu",
        "threshold": 90.0,
        "comparison": ">",
        "duration": 60,
        "severity": "warning",
        "enabled": True,
        "channels": ["slack"]
    }
    response = client.post("/api/v1/admin/alerts/rules", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TEST_RULE"
    assert "id" in data
    return data["id"]

def test_create_invalid_metric():
    payload = {
        "name": "INVALID_RULE",
        "metric": "invalid_metric_xyz",
        "threshold": 90.0,
        "comparison": ">",
        "duration": 60,
        "severity": "warning"
    }
    response = client.post("/api/v1/admin/alerts/rules", json=payload)
    assert response.status_code == 400

def test_update_rule():
    # First create
    rule_id = test_create_rule()
    
    # Then update
    update_payload = {"threshold": 95.5, "enabled": False}
    response = client.put(f"/api/v1/admin/alerts/rules/{rule_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["threshold"] == 95.5
    assert data["enabled"] == False

def test_delete_rule():
    # First create
    rule_id = test_create_rule()
    
    # Then delete
    response = client.delete(f"/api/v1/admin/alerts/rules/{rule_id}")
    assert response.status_code == 200
    
    # Verify gone
    update_response = client.put(f"/api/v1/admin/alerts/rules/{rule_id}", json={"threshold": 10})
    assert update_response.status_code == 404

def test_channels_list():
    response = client.get("/api/v1/admin/alerts/channels")
    assert response.status_code == 200
    assert "slack" in response.json()
