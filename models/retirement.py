"""
==============================================================================
FILE: models/retirement.py
ROLE: Retirement Planning Data Models
PURPOSE: Pydantic models for retirement planning, projections, and withdrawal
         strategies.

INTEGRATION POINTS:
    - RetirementProjectionService: Retirement projections
    - WithdrawalStrategyService: Withdrawal optimization
    - RetirementAPI: API response models
    - FrontendRetirement: Retirement dashboard widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class WithdrawalStrategy(str, Enum):
    """Withdrawal strategy types."""
    FIXED_AMOUNT = "fixed_amount"
    PERCENTAGE = "percentage"
    INFLATION_ADJUSTED = "inflation_adjusted"
    GUYTON_KINGSTON = "guyton_kingston"
    PERPETUAL = "perpetual"


class RetirementScenario(BaseModel):
    """Retirement scenario parameters."""
    scenario_name: str
    current_age: int
    retirement_age: int
    life_expectancy: int
    current_savings: float
    annual_contribution: float
    expected_return: float
    inflation_rate: float = 0.03
    withdrawal_rate: float = 0.04
    social_security_benefit: Optional[float] = None


class RetirementProjection(BaseModel):
    """Retirement projection result."""
    scenario_id: str
    projected_retirement_savings: float
    projected_annual_income: float
    years_in_retirement: int
    probability_of_success: float
    monte_carlo_results: Dict[str, float]  # {percentile: value}
    projected_timeline: List[Dict]  # Year-by-year projections


class WithdrawalPlan(BaseModel):
    """Withdrawal plan for retirement."""
    plan_id: str
    strategy: WithdrawalStrategy
    initial_withdrawal_amount: float
    withdrawal_rate: float
    inflation_adjustment: bool
    account_sequence: List[str]  # Order of account withdrawals
    rmd_calculations: Optional[Dict] = None  # Required Minimum Distributions


class RMDCalculation(BaseModel):
    """Required Minimum Distribution calculation."""
    account_type: str  # IRA, 401k, etc.
    account_balance: float
    age: int
    rmd_amount: float
    distribution_date: datetime
