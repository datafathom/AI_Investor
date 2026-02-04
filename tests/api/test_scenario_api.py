"""
Tests for Scenario API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.scenario_api import router
from services.analysis.scenario_service import get_scenario_service, ScenarioService


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_service(api_app):
    """Mock Scenario Service."""
    service = AsyncMock(spec=ScenarioService)
    
    result = MagicMock()
    result.portfolio_impact = -0.1
    result.new_portfolio_value = 900000
    result.net_impact = -100000
    result.hedge_offset = 20000
    
    recovery = MagicMock()
    recovery.recovery_days = 180
    recovery.recovery_path = [1, 2, 3]
    recovery.worst_case_days = 365
    
    service.apply_shock.return_value = result
    service.calculate_hedge_sufficiency.return_value = 0.8
    service.project_recovery_timeline.return_value = recovery
    service.run_refined_monte_carlo.return_value = {"percentiles": [10, 50, 90]}
    service.calculate_liquidity_drain.return_value = {"drain": 50000}
    
    api_app.dependency_overrides[get_scenario_service] = lambda: service
    return service


def test_simulate_scenario_success(client, mock_service):
    """Test simulating scenario."""
    payload = {
        "id": "crash_2024",
        "equity_drop": 0.2,
        "bond_drop": 0.05,
        "gold_change": 0.1
    }
    response = client.post('/api/v1/scenario/simulate', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['impact']['portfolio_impact_pct'] == -0.1


def test_run_refined_mc_success(client, mock_service):
    """Test refined MC."""
    response = client.get('/api/v1/scenario/monte-carlo-refined?scenario_id=crash&initial_value=1000000')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_simulate_bank_run_success(client, mock_service):
    """Test bank run simulation."""
    response = client.get('/api/v1/scenario/bank-run?stress_level=2.0')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
