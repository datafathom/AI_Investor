"""
Tests for Macro Data API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.macro_data_api import macro_data_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(macro_data_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_fred_service():
    """Mock FRED service."""
    with patch('web.api.macro_data_api._get_fred_service') as mock:
        service = AsyncMock()
        service.get_regime.return_value = {'regime': 'expansion', 'confidence': 0.85}
        service.get_yield_curve.return_value = {'rates': {'1Y': 0.05, '10Y': 0.04}}
        service.get_series.return_value = {'data': []}
        service.get_indicators.return_value = {'gdp': 3.2, 'unemployment': 3.5}
        service.health_check.return_value = {'status': 'healthy'}
        mock.return_value = service
        yield service


def test_get_regime_success(client, mock_fred_service):
    """Test successful regime retrieval."""
    response = client.get('/api/v1/macro-data/regime')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data or 'regime' in data


def test_get_yield_curve_success(client, mock_fred_service):
    """Test successful yield curve retrieval."""
    response = client.get('/api/v1/macro-data/yield-curve')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data or 'rates' in data


def test_get_series_success(client, mock_fred_service):
    """Test successful series data retrieval."""
    response = client.get('/api/v1/macro-data/series/GDP')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data or 'series' in data


def test_get_indicators_success(client, mock_fred_service):
    """Test successful indicators retrieval."""
    response = client.get('/api/v1/macro-data/indicators')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data or 'indicators' in data
