"""
Tests for Advanced Risk Management API Endpoints
Phase 3: Advanced Risk Metrics & Stress Testing
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.advanced_risk_api import advanced_risk_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(advanced_risk_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_risk_metrics_service():
    """Mock AdvancedRiskMetricsService."""
    with patch('web.api.advanced_risk_api.get_risk_metrics_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_stress_testing_service():
    """Mock StressTestingService."""
    with patch('web.api.advanced_risk_api.get_stress_testing_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_get_risk_metrics_success(client, mock_risk_metrics_service):
    """Test successful risk metrics calculation."""
    from models.risk import RiskMetrics
    
    mock_metrics = RiskMetrics(
        portfolio_id='portfolio_1',
        var_95=0.05,
        cvar_95=0.07,
        max_drawdown=0.12,
        sharpe_ratio=1.5
    )
    mock_risk_metrics_service.calculate_risk_metrics.return_value = mock_metrics
    
    response = client.get('/api/risk/metrics/portfolio_1?method=historical&lookback_days=252')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['var_95'] == 0.05
    assert data['data']['sharpe_ratio'] == 1.5


@pytest.mark.asyncio
async def test_get_risk_metrics_error(client, mock_risk_metrics_service):
    """Test risk metrics error handling."""
    mock_risk_metrics_service.calculate_risk_metrics.side_effect = Exception('Calculation error')
    
    response = client.get('/api/risk/metrics/portfolio_1')
    
    assert response.status_code == 500
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_run_historical_stress_success(client, mock_stress_testing_service):
    """Test successful historical stress test."""
    from models.risk import StressTestResult
    
    mock_result = StressTestResult(
        portfolio_id='portfolio_1',
        scenario_name='2008_financial_crisis',
        portfolio_value_before=100000.0,
        portfolio_value_after=70000.0,
        loss_percent=30.0
    )
    mock_stress_testing_service.run_historical_scenario.return_value = mock_result
    
    response = client.post('/api/risk/stress/historical/portfolio_1',
                          json={'scenario_name': '2008_financial_crisis'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['scenario_name'] == '2008_financial_crisis'


@pytest.mark.asyncio
async def test_run_historical_stress_missing_scenario(client):
    """Test historical stress test without scenario name."""
    response = client.post('/api/risk/stress/historical/portfolio_1', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_run_monte_carlo_stress_success(client, mock_stress_testing_service):
    """Test successful Monte Carlo stress test."""
    from models.risk import StressTestResult
    
    mock_result = StressTestResult(
        portfolio_id='portfolio_1',
        scenario_name='monte_carlo',
        portfolio_value_before=100000.0,
        portfolio_value_after=85000.0,
        loss_percent=15.0
    )
    mock_stress_testing_service.run_monte_carlo_simulation.return_value = mock_result
    
    response = client.post('/api/risk/stress/monte_carlo/portfolio_1',
                          json={'num_simulations': 1000, 'time_horizon_days': 30})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_run_custom_stress_success(client, mock_stress_testing_service):
    """Test successful custom stress test."""
    from models.risk import StressTestResult, StressScenario
    
    mock_result = StressTestResult(
        portfolio_id='portfolio_1',
        scenario_name='custom',
        portfolio_value_before=100000.0,
        portfolio_value_after=90000.0,
        loss_percent=10.0
    )
    mock_stress_testing_service.run_custom_scenario.return_value = mock_result
    
    scenario_data = {
        'name': 'market_crash',
        'market_shock': -0.2,
        'correlation_breakdown': True
    }
    
    response = client.post('/api/risk/stress/custom/portfolio_1',
                          json={'scenario': scenario_data})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_run_custom_stress_missing_scenario(client):
    """Test custom stress test without scenario."""
    response = client.post('/api/risk/stress/custom/portfolio_1', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
