"""
Tests for Expense Tracking Service
Comprehensive test coverage for expense tracking and categorization
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.budgeting.expense_tracking_service import ExpenseTrackingService
from models.budgeting import Expense, ExpenseCategory


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.budgeting.expense_tracking_service.get_cache_service'):
        return ExpenseTrackingService()


@pytest.mark.asyncio
async def test_add_expense(service):
    """Test adding expense."""
    service._categorize_expense = AsyncMock(return_value=ExpenseCategory.FOOD)
    service._save_expense = AsyncMock()
    
    result = await service.add_expense(
        user_id="user_123",
        amount=50.0,
        merchant="Restaurant",
        date=datetime.utcnow()
    )
    
    assert result is not None
    assert isinstance(result, Expense)
    assert result.amount == 50.0
    assert result.category == ExpenseCategory.FOOD


@pytest.mark.asyncio
async def test_get_spending_insights(service):
    """Test getting spending insights."""
    service._get_expenses = AsyncMock(return_value=[
        Expense(expense_id="1", user_id="user_123", amount=50.0, category=ExpenseCategory.FOOD, date=datetime.utcnow()),
        Expense(expense_id="2", user_id="user_123", amount=100.0, category=ExpenseCategory.TRANSPORTATION, date=datetime.utcnow()),
    ])
    
    result = await service.get_spending_insights("user_123")
    
    assert result is not None
    assert 'total_spending' in result or hasattr(result, 'total_spending')
