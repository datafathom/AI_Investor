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
        from services.analysis.scenario_service import ScenarioResult
        mock_result = ScenarioResult(
            portfolio_impact=0.15,
            new_portfolio_value=850000.0,
            net_impact=-150000.0,
            hedge_offset=50000.0
        )
        service.apply_shock.return_value = mock_result
        service.calculate_hedge_sufficiency.return_value = 0.75
        service.project_recovery_timeline.return_value = {'months': 12}
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
    data = response.get_json()
    assert 'impact' in data
    assert 'hedge_sufficiency' in data
