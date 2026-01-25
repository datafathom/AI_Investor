"""
Tests for Evolution API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.evolution_api import evolution_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(evolution_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_genetic_distillery():
    """Mock GeneticDistillery."""
    with patch('web.api.evolution_api.get_genetic_distillery') as mock:
        distillery = MagicMock()
        distillery.current_generation = 5
        distillery.history = []
        distillery.population = [
            MagicMock(genes={'rsi_period': 14, 'rsi_buy': 30}, fitness=0.85)
        ]
        distillery.initialize_population.return_value = None
        distillery.evolve.return_value = None
        mock.return_value = distillery
        yield distillery


def test_start_evolution_success(client, mock_genetic_distillery):
    """Test successful evolution start."""
    response = client.post('/api/v1/evolution/start')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'current_generation' in data


def test_get_status_success(client, mock_genetic_distillery):
    """Test successful status retrieval."""
    # Set global distillery for status endpoint
    import web.api.evolution_api as evolution_module
    evolution_module.distillery = mock_genetic_distillery
    
    response = client.get('/api/v1/evolution/status')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'current_generation' in data


def test_get_status_not_started(client):
    """Test status retrieval when evolution not started."""
    import web.api.evolution_api as evolution_module
    evolution_module.distillery = None
    
    response = client.get('/api/v1/evolution/status')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data or 'message' in data
