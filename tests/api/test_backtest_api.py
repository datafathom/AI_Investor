
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.backtest_api import router, get_monte_carlo_service


@pytest.fixture
def api_app(mock_monte_carlo_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_monte_carlo_service] = lambda: mock_monte_carlo_service
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_monte_carlo_service():
    """Mock MonteCarloService."""
    service = MagicMock()
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
    service.detect_overfit.return_value = (True, 0.5)
    return service


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
    assert data['success'] is True
    assert 'paths' in data['data']
    assert 'ruin_probability' in data['data']
    assert 'median_final' in data['data']


def test_get_drawdown_metrics_success(client, mock_monte_carlo_service):
    """Test successful drawdown metrics retrieval."""
    response = client.get('/api/v1/backtest/drawdown')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'max_drawdown' in data['data']
    assert 'avg_drawdown' in data['data']
    assert 'ulcer_index' in data['data']

def test_check_overfit_success(client, mock_monte_carlo_service):
    """Test successful overfit check."""
    response = client.get('/api/v1/backtest/overfit?is_sharpe=1.5&oos_sharpe=1.0')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['is_overfit'] is True
    assert data['data']['variance'] == 0.5
