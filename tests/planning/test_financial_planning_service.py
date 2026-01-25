"""
Tests for Financial Planning Service
Comprehensive test coverage for financial plans, goal allocation, and projections
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from services.planning.financial_planning_service import FinancialPlanningService
from models.financial_planning import FinancialPlan, FinancialGoal, GoalType


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.planning.financial_planning_service.get_portfolio_aggregator'), \
         patch('services.planning.financial_planning_service.get_cache_service'):
        return FinancialPlanningService()


@pytest.fixture
def mock_goals():
    """Mock financial goals."""
    return [
        {
            'goal_name': 'Retirement',
            'goal_type': GoalType.RETIREMENT,
            'target_amount': 1000000.0,
            'target_date': datetime(2050, 1, 1),
            'priority': 1
        },
        {
            'goal_name': 'House Down Payment',
            'goal_type': GoalType.PURCHASE,
            'target_amount': 50000.0,
            'target_date': datetime(2026, 1, 1),
            'priority': 2
        }
    ]


@pytest.mark.asyncio
async def test_create_financial_plan(service, mock_goals):
    """Test financial plan creation."""
    service._calculate_asset_allocation = AsyncMock(return_value={'stocks': 0.7, 'bonds': 0.3})
    service._calculate_contribution_recommendations = AsyncMock(return_value={
        'Retirement': 1000.0,
        'House Down Payment': 500.0
    })
    service._save_plan = AsyncMock()
    
    result = await service.create_financial_plan(
        user_id="user_123",
        goals=mock_goals,
        monthly_contribution_capacity=2000.0
    )
    
    assert result is not None
    assert isinstance(result, FinancialPlan)
    assert result.user_id == "user_123"
    assert len(result.goals) == 2


@pytest.mark.asyncio
async def test_get_planning_recommendations(service):
    """Test getting planning recommendations."""
    service._get_user_goals = AsyncMock(return_value=[])
    service._calculate_recommendations = AsyncMock(return_value={
        'asset_allocation': {'stocks': 0.7, 'bonds': 0.3},
        'monthly_contribution': 1500.0
    })
    
    result = await service.get_planning_recommendations(
        user_id="user_123"
    )
    
    assert result is not None
    assert 'asset_allocation' in result or hasattr(result, 'asset_allocation')


@pytest.mark.asyncio
async def test_run_scenario_analysis(service, mock_goals):
    """Test scenario analysis."""
    service._simulate_scenario = AsyncMock(return_value={
        'success_probability': 0.75,
        'expected_value': 1200000.0,
        'worst_case': 800000.0
    })
    
    result = await service.run_scenario_analysis(
        user_id="user_123",
        goals=mock_goals,
        scenarios=['optimistic', 'base', 'pessimistic']
    )
    
    assert result is not None
    assert len(result) > 0


@pytest.mark.asyncio
async def test_create_financial_plan_error_handling(service):
    """Test error handling in plan creation."""
    service._calculate_asset_allocation = AsyncMock(side_effect=Exception("Error"))
    
    with pytest.raises(Exception):
        await service.create_financial_plan(
            user_id="user_123",
            goals=[],
            monthly_contribution_capacity=1000.0
        )
