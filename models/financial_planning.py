"""
==============================================================================
FILE: models/financial_planning.py
ROLE: Financial Planning Data Models
PURPOSE: Pydantic models for financial goals, planning, and projections.

INTEGRATION POINTS:
    - FinancialPlanningService: Goal-based planning
    - GoalTrackingService: Goal progress tracking
    - FinancialPlanningAPI: API response models
    - FrontendPlanning: Planning dashboard widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class GoalType(str, Enum):
    """Financial goal types."""
    RETIREMENT = "retirement"
    HOUSE = "house"
    EDUCATION = "education"
    VACATION = "vacation"
    EMERGENCY_FUND = "emergency_fund"
    DEBT_PAYOFF = "debt_payoff"
    CUSTOM = "custom"


class GoalStatus(str, Enum):
    """Goal status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    COMPLETED = "completed"


class FinancialGoal(BaseModel):
    """Financial goal definition."""
    goal_id: str
    user_id: str
    goal_name: str
    goal_type: GoalType
    target_amount: float
    current_amount: float = 0.0
    target_date: datetime
    priority: int = 5  # 1-10 scale
    status: GoalStatus = GoalStatus.NOT_STARTED
    monthly_contribution: Optional[float] = None
    created_date: datetime
    updated_date: datetime


class GoalProjection(BaseModel):
    """Goal projection and timeline analysis."""
    goal_id: str
    current_amount: float
    target_amount: float
    projected_amount: float
    projected_date: datetime
    months_to_completion: int
    required_monthly_contribution: float
    on_track: bool
    confidence_level: float  # 0-1


class AssetAllocationRecommendation(BaseModel):
    """Asset allocation recommendation for goal."""
    goal_id: str
    recommended_allocation: Dict[str, float]  # {asset_class: weight}
    risk_level: str  # conservative, moderate, aggressive
    expected_return: float
    expected_volatility: float
    rationale: str


class FinancialPlan(BaseModel):
    """Complete financial plan."""
    plan_id: str
    user_id: str
    goals: List[FinancialGoal]
    total_target_amount: float
    total_current_amount: float
    monthly_contribution_capacity: float
    recommended_allocations: Dict[str, AssetAllocationRecommendation]
    created_date: datetime
    updated_date: datetime
