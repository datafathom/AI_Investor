import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)

def test_event_bus_stats():
    response = client.get("/api/v1/admin/event-bus/stats")
    assert response.status_code == 200
    assert "topics" in response.json()
    assert "total_messages" in response.json()

def test_cache_stats():
    response = client.get("/api/v1/admin/cache/stats")
    assert response.status_code == 200
    assert "performance_cache" in response.json()
    assert "agent_response_cache" in response.json()

def test_kafka_metrics():
    response = client.get("/api/v1/admin/kafka/metrics")
    assert response.status_code == 200
    assert "broker_status" in response.json()
    assert "groups" in response.json()

def test_storage_pools():
    response = client.get("/api/v1/admin/storage/pools")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if len(response.json()) > 0:
        assert "name" in response.json()[0]

def test_graph_schema():
    response = client.get("/api/v1/admin/graph/schema")
    assert response.status_code == 200
    assert "nodes" in response.json()
    assert "relationships" in response.json()

def test_log_files():
    response = client.get("/api/v1/admin/logs/files")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
