import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)

def test_get_health_services():
    response = client.get("/api/v1/admin/health/services")
    assert response.status_code == 200
    data = response.json()
    assert "services" in data
    assert "overall" in data

def test_get_latency_summary():
    response = client.get("/api/v1/admin/latency/summary")
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data

def test_get_websocket_stats():
    response = client.get("/api/v1/admin/websocket/stats")
    assert response.status_code == 200
    data = response.json()
    assert "active" in data
    assert "total_served" in data

def test_get_middleware_pipeline():
    response = client.get("/api/v1/admin/middleware/pipeline")
    assert response.status_code == 200
    data = response.json()
    assert "steps" in data

def test_get_alert_rules():
    response = client.get("/api/v1/admin/alerts/rules")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "id" in data[0]
        assert "name" in data[0]
