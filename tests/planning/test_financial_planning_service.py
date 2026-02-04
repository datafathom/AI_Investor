"""
Tests for Financial Planning Service
Comprehensive test coverage for financial plans, goal allocation, and projections
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from services.planning.financial_planning_service import FinancialPlanningService
from schemas.financial_planning import FinancialPlan, FinancialGoal, GoalType, AssetAllocationRecommendation


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
            'goal_type': GoalType.HOUSE,
            'target_amount': 50000.0,
            'target_date': datetime(2026, 1, 1),
            'priority': 2
        }
    ]


@pytest.mark.asyncio
async def test_create_financial_plan(service, mock_goals):
    """Test financial plan creation."""
    # Mock recommendation object
    mock_allocation = AssetAllocationRecommendation(
        goal_id="test_goal",
        recommended_allocation={'stocks': 0.7, 'bonds': 0.3},
        risk_level="moderate",
        expected_return=0.06,
        expected_volatility=0.12,
        rationale="Test rationale"
    )
    service._recommend_asset_allocation = AsyncMock(return_value=mock_allocation)
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
async def test_create_financial_plan_error_handling(service):
    """Test error handling in plan creation."""
    service._recommend_asset_allocation = AsyncMock(side_effect=Exception("Error"))
    
    with pytest.raises(Exception):
        await service.create_financial_plan(
            user_id="user_123",
            goals=[{
                'goal_name': 'Test Goal',
                'goal_type': GoalType.HOUSE,
                'target_amount': 1000.0,
                'target_date': datetime(2030, 1, 1),
                'priority': 1
            }],
            monthly_contribution_capacity=1000.0
        )
