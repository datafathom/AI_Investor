"""
Tests for Search API Endpoints
"""

import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.search_api import router, get_master_graph_provider


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_graph(api_app):
    """Mock MasterGraph."""
    service = MagicMock()
    service.get_search_entities.return_value = [
        {"id": "s-aapl", "label": "AAPL", "type": "ticker"},
        {"id": "a-1", "label": "Agent Alpha", "type": "agent"},
        {"id": "c-1", "label": "Client X", "type": "client"}
    ]
    
    api_app.dependency_overrides[get_master_graph_provider] = lambda: service
    return service


def test_get_search_index_success(client, mock_graph):
    """Test getting search index."""
    response = client.get('/api/v1/search/index')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['symbols']) == 1
    assert data['data']['symbols'][0]['label'] == "AAPL"


def test_get_search_index_fallback(client, mock_graph):
    """Test fallback when graph is empty."""
    mock_graph.get_search_entities.return_value = []
    response = client.get('/api/v1/search/index')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['symbols']) == 2
    assert data['data']['symbols'][0]['label'] == "NVDA"


def test_search_query_success(client):
    """Test search query."""
    response = client.get('/api/v1/search/query?q=nvidia')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 2
    assert "nvidia" in data['data'][0]['label']
