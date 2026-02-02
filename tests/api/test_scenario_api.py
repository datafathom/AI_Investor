"""
Tests for Scenario API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.scenario_api import router


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
def mock_scenario_service():
    """Mock ScenarioService."""
    with patch('web.api.scenario_api.get_scenario_service') as mock:
        service = AsyncMock()
        from services.analysis.scenario_service import ScenarioResult, RecoveryProjection
        mock_result = ScenarioResult(
            scenario_id='recession',
            portfolio_impact=0.15,
            new_portfolio_value=850000.0,
            positions_affected=[{'type': 'Equities', 'impact': -20.0}],
            hedge_offset=50000.0,
            net_impact=-150000.0
        )
        service.apply_shock.return_value = mock_result
        service.calculate_hedge_sufficiency.return_value = 0.75
        mock_recovery = RecoveryProjection(
            recovery_days=120,
            recovery_path=[850000.0, 1000000.0],
            worst_case_days=200,
            best_case_days=60
        )
        service.project_recovery_timeline.return_value = mock_recovery
        mock.return_value = service
        yield service


def test_simulate_scenario_success(client, mock_scenario_service):
    """Test successful scenario simulation."""
    response = client.post('/api/v1/scenario/simulate?portfolio_id=portfolio_1',
                          json={
                              'id': 'recession',
                              'equity_drop': 0.2,
                              'bond_drop': 0.1,
                              'gold_change': 0.05
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert 'impact' in data
    assert 'hedge_sufficiency' in data
