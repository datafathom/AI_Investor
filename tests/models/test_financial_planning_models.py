"""
Tests for Financial Planning Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.financial_planning import (
    GoalType,
    GoalStatus,
    FinancialGoal,
    GoalProjection,
    AssetAllocationRecommendation,
    FinancialPlan
)


class TestGoalEnums:
    """Tests for goal enums."""
    
    def test_goal_type_enum(self):
        """Test goal type enum values."""
        assert GoalType.RETIREMENT == "retirement"
        assert GoalType.HOUSE == "house"
        assert GoalType.EDUCATION == "education"
    
    def test_goal_status_enum(self):
        """Test goal status enum values."""
        assert GoalStatus.NOT_STARTED == "not_started"
        assert GoalStatus.IN_PROGRESS == "in_progress"
        assert GoalStatus.COMPLETED == "completed"


class TestFinancialGoal:
    """Tests for FinancialGoal model."""
    
    def test_valid_financial_goal(self):
        """Test valid financial goal creation."""
        goal = FinancialGoal(
            goal_id="goal_1",
            user_id="user_1",
            goal_name="Retirement",
            goal_type=GoalType.RETIREMENT,
            target_amount=1000000.0,
            current_amount=100000.0,
            target_date=datetime(2050, 1, 1),
            priority=10,
            status=GoalStatus.IN_PROGRESS,
            monthly_contribution=1000.0,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert goal.goal_id == "goal_1"
        assert goal.target_amount == 1000000.0
        assert goal.status == GoalStatus.IN_PROGRESS
    
    def test_financial_goal_defaults(self):
        """Test financial goal with default values."""
        goal = FinancialGoal(
            goal_id="goal_1",
            user_id="user_1",
            goal_name="Test Goal",
            goal_type=GoalType.CUSTOM,
            target_amount=10000.0,
            target_date=datetime(2025, 1, 1),
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert goal.current_amount == 0.0
        assert goal.priority == 5
        assert goal.status == GoalStatus.NOT_STARTED


class TestGoalProjection:
    """Tests for GoalProjection model."""
    
    def test_valid_goal_projection(self):
        """Test valid goal projection creation."""
        projection = GoalProjection(
            goal_id="goal_1",
            current_amount=100000.0,
            target_amount=1000000.0,
            projected_amount=500000.0,
            projected_date=datetime(2045, 1, 1),
            months_to_completion=240,
            required_monthly_contribution=2000.0,
            on_track=True,
            confidence_level=0.85
        )
        assert projection.goal_id == "goal_1"
        assert projection.on_track is True
        assert projection.confidence_level == 0.85


class TestAssetAllocationRecommendation:
    """Tests for AssetAllocationRecommendation model."""
    
    def test_valid_allocation_recommendation(self):
        """Test valid allocation recommendation creation."""
        recommendation = AssetAllocationRecommendation(
            goal_id="goal_1",
            recommended_allocation={"stocks": 0.7, "bonds": 0.3},
            risk_level="moderate",
            expected_return=0.08,
            expected_volatility=0.12,
            rationale="Balanced approach for retirement goal"
        )
        assert recommendation.goal_id == "goal_1"
        assert recommendation.risk_level == "moderate"
        assert recommendation.expected_return == 0.08


class TestFinancialPlan:
    """Tests for FinancialPlan model."""
    
    def test_valid_financial_plan(self):
        """Test valid financial plan creation."""
        plan = FinancialPlan(
            plan_id="plan_1",
            user_id="user_1",
            goals=[],
            total_target_amount=1000000.0,
            total_current_amount=100000.0,
            monthly_contribution_capacity=2000.0,
            recommended_allocations={},
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert plan.plan_id == "plan_1"
        assert plan.total_target_amount == 1000000.0
        assert plan.monthly_contribution_capacity == 2000.0
