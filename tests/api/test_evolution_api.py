"""
Tests for Evolution API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.evolution_api import router
import web.api.evolution_api as evolution_module


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_genetic_distillery():
    """Mock GeneticDistillery and set the global."""
    distillery = MagicMock()
    distillery.current_generation = 5
    distillery.history = []
    distillery.population = [
        MagicMock(genes={'rsi_period': 14, 'rsi_buy': 30}, fitness=0.85)
    ]
    distillery.initialize_population.return_value = None
    distillery.evolve.return_value = None
    # Set the global distillery
    evolution_module._distillery = distillery
    yield distillery
    # Cleanup
    evolution_module._distillery = None


def test_start_evolution_success(client):
    """Test successful evolution start."""
    response = client.post('/api/v1/evolution/start')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'current_generation' in data['data']


def test_get_status_success(client, mock_genetic_distillery):
    """Test successful status retrieval."""
    response = client.get('/api/v1/evolution/status')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'current_generation' in data['data']


def test_get_status_not_started(client):
    """Test status retrieval when evolution not started."""
    # Ensure distillery is None
    evolution_module._distillery = None
    
    response = client.get('/api/v1/evolution/status')
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
