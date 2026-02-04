"""
Tests for Master Orchestrator API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.master_orchestrator_api import router, get_master_graph_provider, get_neo4j_provider
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    # Mock current user
    app.dependency_overrides[get_current_user] = lambda: {'id': 'user_1', 'email': 'test@example.com'}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_master_graph(api_app):
    """Mock Master Graph Service."""
    service = MagicMock()
    service.get_graph_data.return_value = {"nodes": [], "links": []}
    service.trigger_reflexivity_shock.return_value = {"impact": 0.5}
    
    api_app.dependency_overrides[get_master_graph_provider] = lambda: service
    return service


@pytest.fixture
def mock_neo4j(api_app):
    """Mock Neo4j Service."""
    service = MagicMock()
    service.execute_query.return_value = [{"name": "Result"}]
    
    api_app.dependency_overrides[get_neo4j_provider] = lambda: service
    return service


def test_get_master_graph_success(client, mock_master_graph):
    """Test getting master graph."""
    response = client.get('/api/v1/master/graph')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'nodes' in data['data']


def test_bolt_proxy_success(client, mock_neo4j):
    """Test bolt proxy query."""
    payload = {"query": "MATCH (n) RETURN n"}
    response = client.post('/api/v1/master/bolt-proxy', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_bolt_proxy_no_query(client, mock_neo4j):
    """Test bolt proxy without query."""
    payload = {"query": ""}
    response = client.post('/api/v1/master/bolt-proxy', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False


def test_trigger_shock_success(client, mock_master_graph):
    """Test triggering shock."""
    payload = {"asset_id": "BTC", "magnitude": -0.2}
    response = client.post('/api/v1/master/shock', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_trigger_shock_no_asset(client, mock_master_graph):
    """Test triggering shock without asset_id."""
    payload = {"asset_id": ""}
    response = client.post('/api/v1/master/shock', json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
