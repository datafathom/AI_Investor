"""
==============================================================================
FILE: models/budgeting.py
ROLE: Budgeting Data Models
PURPOSE: Pydantic models for budgeting, expense tracking, and spending analysis.

INTEGRATION POINTS:
    - BudgetingService: Budget creation and management
    - ExpenseTrackingService: Expense categorization and tracking
    - BudgetingAPI: API response models
    - FrontendBudget: Budget dashboard widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class ExpenseCategory(str, Enum):
    """Expense categories."""
    HOUSING = "housing"
    TRANSPORTATION = "transportation"
    FOOD = "food"
    UTILITIES = "utilities"
    INSURANCE = "insurance"
    HEALTHCARE = "healthcare"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    EDUCATION = "education"
    SAVINGS = "savings"
    DEBT = "debt"
    OTHER = "other"


class Budget(BaseModel):
    """Budget definition."""
    budget_id: str
    user_id: str
    budget_name: str
    period: str  # "monthly", "yearly"
    categories: Dict[str, float]  # {category: budgeted_amount}
    total_budget: float
    created_date: datetime
    updated_date: datetime


class Expense(BaseModel):
    """Expense transaction."""
    expense_id: str
    user_id: str
    amount: float
    category: ExpenseCategory
    description: str
    merchant: Optional[str] = None
    date: datetime
    account_id: Optional[str] = None
    receipt_url: Optional[str] = None


class BudgetAnalysis(BaseModel):
    """Budget vs actual analysis."""
    budget_id: str
    period_start: datetime
    period_end: datetime
    total_budgeted: float
    total_spent: float
    remaining: float
    category_analysis: Dict[str, Dict]  # {category: {budgeted, spent, remaining, percentage}}
    over_budget_categories: List[str]
    under_budget_categories: List[str]


class SpendingTrend(BaseModel):
    """Spending trend analysis."""
    category: str
    period: str
    average_spending: float
    trend_direction: str  # "increasing", "decreasing", "stable"
    percentage_change: float
    forecast: Optional[float] = None
