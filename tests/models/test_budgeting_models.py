"""
Tests for Budgeting Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.budgeting import (
    ExpenseCategory,
    Budget,
    Expense,
    BudgetAnalysis,
    SpendingTrend
)


class TestExpenseCategoryEnum:
    """Tests for ExpenseCategory enum."""
    
    def test_expense_category_enum(self):
        """Test expense category enum values."""
        assert ExpenseCategory.HOUSING == "housing"
        assert ExpenseCategory.FOOD == "food"
        assert ExpenseCategory.TRANSPORTATION == "transportation"
        assert ExpenseCategory.ENTERTAINMENT == "entertainment"


class TestBudget:
    """Tests for Budget model."""
    
    def test_valid_budget(self):
        """Test valid budget creation."""
        budget = Budget(
            budget_id='budget_1',
            user_id='user_1',
            budget_name='Monthly Budget',
            period='monthly',
            categories={'food': 500.0, 'transportation': 300.0},
            total_budget=800.0,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert budget.budget_id == 'budget_1'
        assert budget.period == 'monthly'
        assert budget.total_budget == 800.0
        assert len(budget.categories) == 2


class TestExpense:
    """Tests for Expense model."""
    
    def test_valid_expense(self):
        """Test valid expense creation."""
        expense = Expense(
            expense_id='expense_1',
            user_id='user_1',
            amount=50.0,
            category=ExpenseCategory.FOOD,
            description='Groceries',
            merchant='Grocery Store',
            date=datetime.now(),
            account_id='account_1',
            receipt_url=None
        )
        assert expense.expense_id == 'expense_1'
        assert expense.amount == 50.0
        assert expense.category == ExpenseCategory.FOOD
    
    def test_expense_optional_fields(self):
        """Test expense with optional fields."""
        expense = Expense(
            expense_id='expense_1',
            user_id='user_1',
            amount=50.0,
            category=ExpenseCategory.FOOD,
            description='Groceries',
            date=datetime.now()
        )
        assert expense.merchant is None
        assert expense.account_id is None
        assert expense.receipt_url is None


class TestBudgetAnalysis:
    """Tests for BudgetAnalysis model."""
    
    def test_valid_budget_analysis(self):
        """Test valid budget analysis creation."""
        analysis = BudgetAnalysis(
            budget_id='budget_1',
            period_start=datetime(2024, 1, 1),
            period_end=datetime(2024, 1, 31),
            total_budgeted=800.0,
            total_spent=750.0,
            remaining=50.0,
            category_analysis={},
            over_budget_categories=[],
            under_budget_categories=['food']
        )
        assert analysis.budget_id == 'budget_1'
        assert analysis.total_budgeted == 800.0
        assert analysis.remaining == 50.0


class TestSpendingTrend:
    """Tests for SpendingTrend model."""
    
    def test_valid_spending_trend(self):
        """Test valid spending trend creation."""
        trend = SpendingTrend(
            category='food',
            period='monthly',
            average_spending=500.0,
            trend_direction='increasing',
            percentage_change=0.1,
            forecast=550.0
        )
        assert trend.category == 'food'
        assert trend.trend_direction == 'increasing'
        assert trend.percentage_change == 0.1
