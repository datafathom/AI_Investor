"""
Tests for Financial Planning API Endpoints
Phase 7: Financial Planning & Goal Tracking
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.financial_planning_api import financial_planning_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(financial_planning_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_planning_service():
    """Mock FinancialPlanningService."""
    with patch('web.api.financial_planning_api.get_financial_planning_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_goal_tracking_service():
    """Mock GoalTrackingService."""
    with patch('web.api.financial_planning_api.get_goal_tracking_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_plan_success(client, mock_planning_service):
    """Test successful plan creation."""
    from models.financial_planning import FinancialPlan
    
    mock_plan = FinancialPlan(
        plan_id='plan_1',
        user_id='user_1',
        goals=[],
        monthly_contribution_capacity=1000.0
    )
    mock_planning_service.create_financial_plan.return_value = mock_plan
    
    response = client.post('/api/planning/plan/create',
                          json={
                              'user_id': 'user_1',
                              'goals': [],
                              'monthly_contribution_capacity': 1000.0
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_create_plan_missing_params(client):
    """Test plan creation with missing parameters."""
    response = client.post('/api/planning/plan/create', json={'user_id': 'user_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_get_plan_success(client, mock_planning_service):
    """Test successful plan retrieval."""
    from models.financial_planning import FinancialPlan
    
    mock_plan = FinancialPlan(
        plan_id='plan_1',
        user_id='user_1',
        goals=[],
        monthly_contribution_capacity=1000.0
    )
    mock_planning_service.get_financial_plan.return_value = mock_plan
    
    response = client.get('/api/planning/plan/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_project_goal_success(client, mock_goal_tracking_service):
    """Test goal projection."""
    from models.financial_planning import GoalProjection
    
    mock_projection = GoalProjection(
        goal_id='goal_1',
        projected_completion_date='2025-12-31',
        required_monthly_contribution=500.0
    )
    mock_goal_tracking_service.project_goal_completion.return_value = mock_projection
    
    response = client.post('/api/planning/goal/project/goal_1', json={})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_get_goal_progress_success(client, mock_goal_tracking_service):
    """Test successful goal progress retrieval."""
    from models.financial_planning import GoalProgress
    
    mock_progress = GoalProgress(
        goal_id='goal_1',
        current_value=5000.0,
        target_value=10000.0,
        progress_percent=50.0
    )
    mock_goal_tracking_service.get_goal_progress.return_value = mock_progress
    
    response = client.get('/api/planning/goal/goal_1/progress')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['progress_percent'] == 50.0
