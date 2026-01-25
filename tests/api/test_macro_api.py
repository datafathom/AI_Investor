"""
Tests for Macro API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.macro_api import macro_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(macro_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_macro_service():
    """Mock MacroService."""
    with patch('web.api.macro_api._macro_service') as mock:
        service = AsyncMock()
        service.get_political_insider_trades.return_value = []
        service.get_cpi_data.return_value = {'country': 'US', 'cpi': 3.2, 'date': '2024-01-01'}
        service.get_correlations.return_value = {'gold': 0.8, 'commodities': 0.6}
        service.get_world_map_data.return_value = {}
        service.get_economic_calendar.return_value = []
        mock.return_value = service
        yield service


def test_get_insider_trades_success(client, mock_macro_service):
    """Test successful insider trades retrieval."""
    response = client.get('/insider-trades?region=US')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'success' in data or 'data' in data


def test_get_cpi_success(client, mock_macro_service):
    """Test successful CPI data retrieval."""
    response = client.get('/cpi/US')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'country' in data or 'cpi' in data


def test_get_correlations_success(client, mock_macro_service):
    """Test successful correlations retrieval."""
    response = client.get('/correlations')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict) or 'correlations' in data


def test_get_world_map_success(client, mock_macro_service):
    """Test successful world map data retrieval."""
    response = client.get('/world-map')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict) or 'map' in data
