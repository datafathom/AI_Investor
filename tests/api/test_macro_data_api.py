"""
Tests for Macro Data API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.macro_data_api import router, get_fred_provider


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
def mock_fred_service(api_app):
    """Mock FRED Service."""
    service = AsyncMock()
    
    # Mock regime
    regime = MagicMock()
    regime.status = "Expansion"
    regime.signals = ["High Yield Narrowing"]
    regime.metrics = {"GDP": 2.5}
    regime.health_score = 75
    regime.timestamp.isoformat.return_value = "2026-01-01T00:00:00"
    service.get_macro_regime.return_value = regime
    
    # Mock curve
    service.get_yield_curve_data.return_value = {"2Y": 4.5, "10Y": 4.2}
    
    # Mock series
    dp = MagicMock()
    dp.date = "2026-01-01"
    dp.value = 310.5
    service.get_series.return_value = [dp]
    
    metadata = MagicMock()
    metadata.title = "Consumer Price Index"
    metadata.units = "Index"
    metadata.frequency = "Monthly"
    service.get_series_metadata.return_value = metadata
    
    # Mock indicators
    service.get_latest_value.return_value = 310.5
    service.calculate_yoy_change.return_value = 3.2
    
    api_app.dependency_overrides[get_fred_provider] = lambda: service
    return service


def test_get_regime_success(client, mock_fred_service):
    """Test getting macro regime."""
    response = client.get('/api/v1/macro_data/regime')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['content']['status'] == "Expansion"


def test_get_yield_curve_success(client, mock_fred_service):
    """Test getting yield curve."""
    response = client.get('/api/v1/macro_data/yield-curve')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['content']['is_inverted'] is True


def test_get_series_success(client, mock_fred_service):
    """Test getting historical series."""
    response = client.get('/api/v1/macro_data/series/CPIAUCSL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['content']['series_id'] == "CPIAUCSL"


def test_get_indicators_success(client, mock_fred_service):
    """Test getting key indicators."""
    response = client.get('/api/v1/macro_data/indicators')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['content']['indicators']) > 0


def test_get_health_success(client):
    """Test health check."""
    response = client.get('/api/v1/macro_data/health')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['content']['source'] == "FRED"
