"""
Tests for Attribution API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
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
    """Mock AttributionService."""
    with patch('web.api.attribution_api._service') as mock:
        service = AsyncMock()
        from services.analysis.attribution_service import AttributionResult
        mock_result = AttributionResult(
            portfolio_id='portfolio_1',
            benchmark_id='sp500',
            period=None,
            total_return=0.15,
            benchmark_return=0.10,
            active_return=0.05,
            allocation_effect=0.02,
            selection_effect=0.03
        )
        service.calculate_brinson_attribution.return_value = mock_result
        service.get_available_benchmarks.return_value = ['sp500', 'nasdaq']
        service.compare_benchmarks.return_value = {}
        mock.return_value = service
        yield service


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
