"""
Tests for Backtest API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.backtest_api import router


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_monte_carlo_service():
    """Mock MonteCarloService."""
    with patch('web.api.backtest_api.get_monte_carlo_service') as mock:
        service = AsyncMock()
        from services.analysis.monte_carlo_service import SimulationResult, DrawdownMetrics
        mock_result = SimulationResult(
            paths=[[1000000.0, 1050000.0, 1100000.0]],
            quantiles={'p10': [900000.0], 'p90': [1200000.0]},
            ruin_probability=0.05,
            median_final=1100000.0,
            mean_final=1105000.0
        )
        service.run_gbm_simulation.return_value = mock_result
        mock_metrics = DrawdownMetrics(
            max_drawdown=0.15,
            avg_drawdown=0.05,
            max_duration_days=30,
            ulcer_index=0.08,
            pain_index=0.10,
            recovery_days=45
        )
        service.calculate_drawdown_metrics.return_value = mock_metrics
        mock.return_value = service
        yield service


def test_run_monte_carlo_success(client, mock_monte_carlo_service):
    """Test successful Monte Carlo simulation."""
    response = client.post('/api/v1/backtest/monte-carlo',
                          json={
                              'initial_value': 1000000.0,
                              'mu': 0.08,
                              'sigma': 0.15,
                              'days': 252,
                              'paths': 1000
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert 'paths' in data
    assert 'ruin_probability' in data
    assert 'median_final' in data


def test_get_drawdown_metrics_success(client, mock_monte_carlo_service):
    """Test successful drawdown metrics retrieval."""
    response = client.get('/api/v1/backtest/drawdown')
    
    assert response.status_code == 200
    data = response.json()
    assert 'max_drawdown' in data
    assert 'avg_drawdown' in data
    assert 'ulcer_index' in data
