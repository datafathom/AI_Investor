"""
Tests for Attribution API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from datetime import datetime, timezone
from web.api.attribution_api import attribution_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(attribution_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_attribution_service():
    """Mock AttributionServiceInstance."""
    with patch('web.api.attribution_api._service') as mock:
        from services.analysis.attribution_service import BrinsonAttribution, DateRange
        mock_result = BrinsonAttribution(
            portfolio_id='portfolio_1',
            benchmark_id='sp500',
            period=DateRange(start='2024-01-01', end='2024-12-31'),
            total_active_return=0.05,
            total_allocation_effect=0.02,
            total_selection_effect=0.03,
            total_interaction_effect=0.0,
            sector_attributions=[],
            regime_shifts=[],
            calculated_at=datetime.now(timezone.utc).isoformat()
        )
        mock.calculate_brinson_attribution = AsyncMock(return_value=mock_result)
        mock.get_available_benchmarks.return_value = [{'id': 'sp500', 'name': 'S&P 500'}]
        mock.compare_benchmarks = AsyncMock(return_value={})
        mock.get_sector_allocation_effect = AsyncMock(return_value=0.02)
        mock.get_selection_effect = AsyncMock(return_value=0.03)
        yield mock


def test_get_attribution_success(client, mock_attribution_service):
    """Test successful attribution retrieval."""
    response = client.get('/portfolio_1?benchmark=sp500&start=2024-01-01&end=2024-12-31')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_get_benchmarks_success(client, mock_attribution_service):
    """Test successful benchmarks retrieval."""
    response = client.get('/benchmarks')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'success' in data or isinstance(data, list)


def test_compare_benchmarks_success(client, mock_attribution_service):
    """Test successful benchmark comparison."""
    response = client.post('/compare',
                          json={
                              'portfolio_id': 'portfolio_1',
                              'benchmarks': ['sp500', 'nasdaq']
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'success' in data or 'comparison' in data
