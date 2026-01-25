"""
Tests for Budgeting Service
Comprehensive test coverage for budget creation, analysis, and tracking
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.budgeting.budgeting_service import BudgetingService
from models.budgeting import Budget


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.budgeting.budgeting_service.get_cache_service'):
        return BudgetingService()


@pytest.mark.asyncio
async def test_create_budget(service):
    """Test budget creation."""
    categories = {'Groceries': 500.0, 'Transportation': 300.0, 'Entertainment': 200.0}
    
    result = await service.create_budget(
        user_id="user_123",
        budget_name="Monthly Budget",
        period="monthly",
        categories=categories
    )
    
    assert result is not None
    assert isinstance(result, Budget)
    assert result.user_id == "user_123"
    assert result.total_budget == 1000.0
    assert len(result.categories) == 3


@pytest.mark.asyncio
async def test_get_budget_analysis(service):
    """Test budget analysis."""
    service._get_budget = AsyncMock(return_value=Budget(
        budget_id="budget_123",
        user_id="user_123",
        budget_name="Test Budget",
        period="monthly",
        categories={'Groceries': 500.0},
        total_budget=500.0,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    ))
    service._get_actual_spending = AsyncMock(return_value={'Groceries': 450.0})
    
    result = await service.get_budget_analysis("budget_123")
    
    assert result is not None
    assert 'budget_vs_actual' in result or hasattr(result, 'budget_vs_actual')


@pytest.mark.asyncio
async def test_create_budget_error_handling(service):
    """Test error handling in budget creation."""
    service.cache_service.set = Mock(side_effect=Exception("Cache error"))
    
    with pytest.raises(Exception):
        await service.create_budget(
            user_id="user_123",
            budget_name="Error Budget",
            period="monthly",
            categories={}
        )
