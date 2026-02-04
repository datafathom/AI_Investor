"""
Tests for Retirement API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.retirement_api import router, get_projection_provider, get_withdrawal_provider
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    # Mock current user
    app.dependency_overrides[get_current_user] = lambda: {'id': 'user_1', 'email': 'test@example.com'}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_projection_service(api_app):
    """Mock Projection Service."""
    service = AsyncMock()
    
    result = MagicMock()
    result.model_dump.return_value = {"probability_of_success": 0.85, "median_ending_balance": 1000000}
    
    service.project_retirement.return_value = result
    service.compare_scenarios.return_value = {"Basic": result}
    
    api_app.dependency_overrides[get_projection_provider] = lambda: service
    return service


@pytest.fixture
def mock_withdrawal_service(api_app):
    """Mock Withdrawal Service."""
    service = AsyncMock()
    
    plan = MagicMock()
    plan.model_dump.return_value = {"plan_id": "plan_123", "annual_withdrawal": 40000}
    
    service.create_withdrawal_plan.return_value = plan
    service._get_account_balances.return_value = {"401k": 500000}
    service._calculate_rmds.return_value = {"401k": 15000}
    service.optimize_withdrawal_rate.return_value = {"optimal_rate": 0.045}
    
    api_app.dependency_overrides[get_withdrawal_provider] = lambda: service
    return service


def test_project_retirement_success(client, mock_projection_service):
    """Test projecting retirement."""
    payload = {
        "scenario": {
            "scenario_name": "Test Scenario",
            "current_age": 30,
            "retirement_age": 65,
            "life_expectancy": 90,
            "current_savings": 50000,
            "annual_contribution": 12000,
            "expected_return": 0.07,
            "inflation_rate": 0.03
        },
        "n_simulations": 100
    }
    response = client.post('/api/v1/retirement/project', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['probability_of_success'] == 0.85


def test_compare_scenarios_success(client, mock_projection_service):
    """Test comparing scenarios."""
    payload = {
        "scenarios": [
            {
                "scenario_name": "Basic",
                "current_age": 30,
                "retirement_age": 65,
                "life_expectancy": 90,
                "current_savings": 50000,
                "annual_contribution": 12000,
                "expected_return": 0.07
            }
        ],
        "n_simulations": 100
    }
    response = client.post('/api/v1/retirement/compare', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert "Basic" in data['data']


def test_create_withdrawal_plan_success(client, mock_withdrawal_service):
    """Test creating withdrawal plan."""
    payload = {"user_id": "user_1", "strategy": "4_percent_rule"}
    response = client.post('/api/v1/retirement/withdrawal/plan', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_rmds_success(client, mock_withdrawal_service):
    """Test getting RMDs."""
    response = client.get('/api/v1/retirement/rmd/user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['401k'] == 15000


def test_optimize_withdrawal_rate_success(client, mock_withdrawal_service):
    """Test optimizing withdrawal rate."""
    payload = {"retirement_savings": 1000000, "annual_expenses": 40000}
    response = client.post('/api/v1/retirement/withdrawal/optimize', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['optimal_rate'] == 0.045
