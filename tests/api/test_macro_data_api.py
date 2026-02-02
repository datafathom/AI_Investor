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
    """Mock FRED service with correct method names."""
    with patch('web.api.macro_data_api._get_fred_service') as mock:
        service = AsyncMock()
        
        # Mock get_macro_regime with proper return structure
        mock_regime = MagicMock()
        mock_regime.status = 'expansion'
        mock_regime.signals = {}
        mock_regime.metrics = {}
        mock_regime.health_score = 0.85
        mock_regime.timestamp = MagicMock()
        mock_regime.timestamp.isoformat.return_value = '2026-01-21T12:00:00'
        service.get_macro_regime.return_value = mock_regime
        
        # Mock get_yield_curve_data
        service.get_yield_curve_data.return_value = {'2Y': 0.045, '10Y': 0.04}
        
        # Mock get_series and related methods
        mock_datapoint = MagicMock()
        mock_datapoint.date = '2026-01-21'
        mock_datapoint.value = 3.2
        service.get_series.return_value = [mock_datapoint]
        
        # Mock get_series_metadata
        mock_metadata = MagicMock()
        mock_metadata.title = 'GDP'
        mock_metadata.units = 'Billions'
        mock_metadata.frequency = 'Quarterly'
        service.get_series_metadata.return_value = mock_metadata
        
        # Mock get_latest_value and calculate_yoy_change for indicators
        service.get_latest_value.return_value = 3.5
        service.calculate_yoy_change.return_value = 2.1
        
        mock.return_value = service
        yield service


def test_get_regime_success(client, mock_fred_service):
    """Test successful regime retrieval."""
    response = client.get('/regime')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data


def test_get_yield_curve_success(client, mock_fred_service):
    """Test successful yield curve retrieval."""
    response = client.get('/yield-curve')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data


def test_get_series_success(client, mock_fred_service):
    """Test successful series data retrieval."""
    response = client.get('/series/GDP')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data


def test_get_indicators_success(client, mock_fred_service):
    """Test successful indicators retrieval."""
    response = client.get('/indicators')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
