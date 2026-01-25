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
    with patch('web.api.fixed_income_api._service') as mock:
        service = AsyncMock()
        from services.analysis.fixed_income_service import YieldCurve
        mock_curve = YieldCurve(
            date='2024-01-01',
            rates={'1Y': 0.05, '10Y': 0.04},
            is_inverted=True
        )
        service.get_yield_curve.return_value = mock_curve
        service.get_historical_curves.return_value = [mock_curve]
        service.simulate_rate_shock.return_value = {'impact': 0.1}
        service.calculate_duration.return_value = {'duration': 5.5}
        service.calculate_wal.return_value = {'wal': 7.2}
        service.get_liquidity_gaps.return_value = []
        mock.return_value = service
        yield service


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
