"""
Tests for Retirement Planning API Endpoints
Phase 8: Retirement Planning & Withdrawal Strategies
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.retirement_api import retirement_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(retirement_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_retirement_projection_service():
    """Mock RetirementProjectionService."""
    with patch('web.api.retirement_api.get_retirement_projection_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_withdrawal_strategy_service():
    """Mock WithdrawalStrategyService."""
    with patch('web.api.retirement_api.get_withdrawal_strategy_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_project_retirement_success(client, mock_retirement_projection_service):
    """Test successful retirement projection."""
    from models.retirement import RetirementProjection, RetirementScenario
    
    mock_projection = RetirementProjection(
        scenario_id='scenario_1',
        success_probability=0.85,
        median_ending_balance=500000.0
    )
    mock_retirement_projection_service.project_retirement.return_value = mock_projection
    
    scenario_data = {
        'current_age': 35,
        'retirement_age': 65,
        'current_savings': 100000.0,
        'annual_contribution': 10000.0
    }
    
    response = client.post('/api/retirement/project',
                          json={'scenario': scenario_data, 'n_simulations': 10000})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_project_retirement_missing_scenario(client):
    """Test retirement projection without scenario."""
    response = client.post('/api/retirement/project', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_compare_scenarios_success(client, mock_retirement_projection_service):
    """Test successful scenario comparison."""
    from models.retirement import ScenarioComparison
    
    mock_comparison = ScenarioComparison(
        scenarios=[],
        best_scenario_id='scenario_1'
    )
    mock_retirement_projection_service.compare_scenarios.return_value = mock_comparison
    
    response = client.post('/api/retirement/compare',
                          json={'scenarios': []})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
