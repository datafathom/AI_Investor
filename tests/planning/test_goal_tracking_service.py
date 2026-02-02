"""
Tests for Goal Tracking Service
Comprehensive test coverage for goal progress tracking and status updates
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch
from services.planning.goal_tracking_service import GoalTrackingService
from models.financial_planning import FinancialGoal, GoalStatus, GoalType


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.planning.goal_tracking_service.get_financial_planning_service'), \
         patch('services.planning.goal_tracking_service.get_cache_service'):
        return GoalTrackingService()


@pytest.fixture
def mock_goal():
    """Mock financial goal."""
    return FinancialGoal(
        goal_id="goal_123",
        user_id="user_123",
        goal_name="Test Goal",
        goal_type=GoalType.RETIREMENT,
        target_amount=100000.0,
        current_amount=50000.0,
        target_date=datetime(2050, 1, 1),
        status=GoalStatus.IN_PROGRESS,
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )


@pytest.mark.asyncio
async def test_update_goal_progress(service, mock_goal):
    """Test updating goal progress."""
    service._get_goal = AsyncMock(return_value=mock_goal)
    service._calculate_status = AsyncMock(return_value=GoalStatus.IN_PROGRESS)
    service._save_goal = AsyncMock()
    
    result = await service.update_goal_progress(
        goal_id="goal_123",
        current_amount=60000.0
    )
    
    assert result is not None
    assert result.current_amount == 60000.0
    assert result.updated_date is not None


@pytest.mark.asyncio
async def test_update_goal_progress_achieved(service, mock_goal):
    """Test goal progress update when goal is achieved."""
    service._get_goal = AsyncMock(return_value=mock_goal)
    service._calculate_status = AsyncMock(return_value=GoalStatus.COMPLETED)
    service._save_goal = AsyncMock()
    
    result = await service.update_goal_progress(
        goal_id="goal_123",
        current_amount=100000.0  # Reached target
    )
    
    assert result is not None
    assert result.status == GoalStatus.COMPLETED


@pytest.mark.asyncio
async def test_get_goals(service):
    """Test getting user goals."""
    service._get_user_goals_from_db = AsyncMock(return_value=[
        FinancialGoal(
            goal_id="goal_1",
            user_id="user_123",
            goal_name="Goal 1",
            goal_type=GoalType.RETIREMENT,
            target_amount=100000.0,
            current_amount=50000.0,
            target_date=datetime(2050, 1, 1),
            status=GoalStatus.IN_PROGRESS,
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
    ])
    
    result = await service.get_goals("user_123")
    
    assert result is not None
    assert len(result) == 1


@pytest.mark.asyncio
async def test_update_goal_progress_not_found(service):
    """Test updating progress for non-existent goal."""
    service._get_goal = AsyncMock(return_value=None)
    
    with pytest.raises(ValueError, match="not found"):
        await service.update_goal_progress(
            goal_id="nonexistent",
            current_amount=1000.0
        )
