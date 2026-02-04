
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from web.api.advanced_risk_api import router, get_risk_metrics_service, get_stress_testing_service
from web.auth_utils import get_current_user

@pytest.fixture
def api_app(mock_risk_metrics_service, mock_stress_testing_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_risk_metrics_service] = lambda: mock_risk_metrics_service
    app.dependency_overrides[get_stress_testing_service] = lambda: mock_stress_testing_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_risk_metrics_service():
    """Mock AdvancedRiskMetricsService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_stress_testing_service():
    """Mock StressTestingService."""
    service = AsyncMock()
    return service


def test_get_risk_metrics_success(client, mock_risk_metrics_service):
    """Test successful risk metrics calculation."""
    from schemas.risk import RiskMetrics
    
    mock_metrics = RiskMetrics(
        portfolio_id='portfolio_1',
        calculation_date=datetime.now(timezone.utc),
        var_95=0.05,
        var_99=0.08,
        cvar_95=0.07,
        cvar_99=0.10,
        maximum_drawdown=0.12,
        maximum_drawdown_duration_days=30,
        sharpe_ratio=1.5,
        sortino_ratio=1.8,
        calmar_ratio=1.2,
        volatility=0.15,
        method='historical'
    )
    mock_risk_metrics_service.calculate_risk_metrics.return_value = mock_metrics
    
    response = client.get('/api/v1/risk/metrics/portfolio_1?method=historical&lookback_days=252')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['var_95'] == pytest.approx(0.05)
    assert data['data']['sharpe_ratio'] == pytest.approx(1.5)


def test_get_risk_metrics_error(client, mock_risk_metrics_service):
    """Test risk metrics error handling."""
    mock_risk_metrics_service.calculate_risk_metrics.side_effect = Exception('Calculation error')
    
    response = client.get('/api/v1/risk/metrics/portfolio_1')
    
    assert response.status_code == 500
    data = response.json()
    assert data['success'] is False


def test_run_historical_stress_success(client, mock_stress_testing_service):
    """Test successful historical stress test."""
    from schemas.risk import StressTestResult, StressScenario
    
    scenario = StressScenario(
        scenario_name='2008_financial_crisis',
        description='2008 Financial Crisis',
        market_shock={'Equity': -0.3, 'Fixed Income': -0.05}
    )
    
    mock_result = StressTestResult(
        portfolio_id='portfolio_1',
        scenario=scenario,
        initial_value=100000.0,
        stressed_value=70000.0,
        loss_amount=30000.0,
        loss_percentage=30.0,
        calculation_date=datetime.now(timezone.utc)
    )
    mock_stress_testing_service.run_historical_scenario.return_value = mock_result
    
    response = client.post('/api/v1/risk/stress/historical/portfolio_1',
                          json={'scenario_name': '2008_financial_crisis'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['scenario']['scenario_name'] == '2008_financial_crisis'


def test_run_historical_stress_missing_scenario(client):
    """Test historical stress test without scenario name."""
    response = client.post('/api/v1/risk/stress/historical/portfolio_1', json={})
    
    assert response.status_code == 422 # Pydantic validation error or 400
    # data = response.json()
    # assert data['success'] is False


def test_run_monte_carlo_stress_success(client, mock_stress_testing_service):
    """Test successful Monte Carlo stress test."""
    from schemas.risk import StressTestResult, StressScenario
    
    scenario = StressScenario(
        scenario_name='monte_carlo',
        description='Monte Carlo Simulation',
        market_shock={}
    )
    
    mock_result = StressTestResult(
        portfolio_id='portfolio_1',
        scenario=scenario,
        initial_value=100000.0,
        stressed_value=85000.0,
        loss_amount=15000.0,
        loss_percentage=15.0,
        calculation_date=datetime.now(timezone.utc)
    )
    mock_stress_testing_service.run_monte_carlo_simulation.return_value = mock_result
    
    response = client.post('/api/v1/risk/stress/monte_carlo/portfolio_1',
                          json={'n_simulations': 1000, 'time_horizon_days': 30})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_run_custom_stress_success(client, mock_stress_testing_service):
    """Test successful custom stress test."""
    from schemas.risk import StressTestResult, StressScenario
    
    scenario = StressScenario(
        scenario_name='custom',
        description='Custom Scenario',
        market_shock={'Market': -0.1}
    )
    
    mock_result = StressTestResult(
        portfolio_id='portfolio_1',
        scenario=scenario,
        initial_value=100000.0,
        stressed_value=90000.0,
        loss_amount=10000.0,
        loss_percentage=10.0,
        calculation_date=datetime.now(timezone.utc)
    )
    mock_stress_testing_service.run_custom_stress_scenario.return_value = mock_result
    
    scenario_data = {
        'scenario_name': 'market_crash',
        'description': 'Market Crash',
        'market_shock': {'Equity': -0.2},
        'correlation_breakdown': True
    }
    
    response = client.post('/api/v1/risk/stress/custom/portfolio_1',
                          json={'scenario': scenario_data})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_run_custom_stress_missing_scenario(client):
    """Test custom stress test without scenario."""
    response = client.post('/api/v1/risk/stress/custom/portfolio_1', json={})
    
    assert response.status_code == 422 # 400
    # data = response.json()
    # assert data['success'] is False
