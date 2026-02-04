"""
Tests for Financial Planning API Endpoints
Phase 7: Financial Planning & Goal Tracking
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.financial_planning_api import router, get_financial_planning_service, get_goal_tracking_service
from web.auth_utils import get_current_user


@pytest.fixture
def api_app(mock_planning_service, mock_goal_tracking_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_financial_planning_service] = lambda: mock_planning_service
    app.dependency_overrides[get_goal_tracking_service] = lambda: mock_goal_tracking_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_planning_service():
    """Mock FinancialPlanningService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_goal_tracking_service():
    """Mock GoalTrackingService."""
    service = AsyncMock()
    return service


def test_create_plan_success(client, mock_planning_service):
    """Test successful plan creation."""
    from schemas.financial_planning import FinancialPlan
    from datetime import datetime, timezone
    
    mock_plan = FinancialPlan(
        plan_id='plan_1',
        user_id='user_1',
        goals=[],
        total_target_amount=100000.0,
        total_current_amount=50000.0,
        monthly_contribution_capacity=1000.0,
        recommended_allocations={},
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_planning_service.create_financial_plan.return_value = mock_plan
    
    response = client.post('/api/v1/financial_planning/plan/create',
                          json={
                              'user_id': 'user_1',
                              'goals': [],
                              'monthly_contribution_capacity': 1000.0
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_create_plan_missing_params(client):
    """Test plan creation with missing parameters."""
    response = client.post('/api/v1/financial_planning/plan/create', 
                          json={'user_id': 'user_1'})
    
    # Pydantic validation error
    assert response.status_code in [400, 422]


def test_get_plan_success(client, mock_planning_service):
    """Test successful plan retrieval."""
    from schemas.financial_planning import FinancialPlan
    from datetime import datetime, timezone
    
    mock_plan = FinancialPlan(
        plan_id='plan_1',
        user_id='user_1',
        goals=[],
        total_target_amount=100000.0,
        total_current_amount=50000.0,
        monthly_contribution_capacity=1000.0,
        recommended_allocations={},
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_planning_service.get_financial_plan = AsyncMock(return_value=mock_plan)
    
    response = client.get('/api/v1/financial_planning/plan/user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
