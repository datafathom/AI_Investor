"""
Tests for Fixed Income API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.fixed_income_api import fixed_income_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(fixed_income_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_fixed_income_service():
    """Mock FixedIncomeService."""
    # Use new=AsyncMock to ensure the mocked object behaves like an async object
    # OR configure methods to be async. Since _service is instance, we replace it.
    with patch('web.api.fixed_income_api._service') as mock_service:
        from services.analysis.fixed_income_service import YieldCurve
        mock_curve = YieldCurve(
            date='2024-01-01',
            rates={'1Y': 0.05, '10Y': 0.04},
            is_inverted=True
        )
        
        # Configure methods to return awaitables (coroutines)
        # We can simulate this by assigning an AsyncMock to the method name
        mock_service.get_yield_curve = AsyncMock(return_value=mock_curve)
        mock_service.get_historical_curves = AsyncMock(return_value=[mock_curve])
        
        mock_impact = MagicMock()
        mock_impact.shock_basis_points = 100
        mock_impact.portfolio_value_before = 1000000
        mock_impact.portfolio_value_after = 990000
        mock_impact.dollar_change = -10000
        mock_impact.percentage_change = -1.0
        mock_service.get_rate_shock_impact = AsyncMock(return_value=mock_impact)
        
        mock_metrics = MagicMock()
        mock_metrics.macaulay_duration = 5.2
        mock_metrics.modified_duration = 5.0
        mock_metrics.convexity = 20.0
        mock_metrics.dollar_duration = 5000.0
        mock_service.calculate_duration = AsyncMock(return_value=mock_metrics)
        
        mock_service.calculate_weighted_average_life = AsyncMock(return_value=7.2)
        mock_service.get_liquidity_gap_analysis = AsyncMock(return_value=[])
        mock_service.detect_inversion = AsyncMock(return_value=True)
        # Note: _get_mock_portfolio is sync
        mock_service._get_mock_portfolio.return_value = []
        
        yield mock_service


def test_get_yield_curve_success(client, mock_fixed_income_service):
    """Test successful yield curve retrieval."""
    response = client.get('/yield-curve')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_get_yield_curve_history_success(client, mock_fixed_income_service):
    """Test successful historical yield curve retrieval."""
    response = client.get('/yield-curve/history?months=12')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_rate_shock_success(client, mock_fixed_income_service):
    """Test successful rate shock simulation."""
    response = client.post('/rate-shock',
                          json={'shock_bps': 100, 'portfolio_id': 'portfolio_1'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
