"""
==============================================================================
FILE: services/budgeting/budgeting_service.py
ROLE: Budgeting Service
PURPOSE: Manages category-based budgets, spending limits, and trend analysis
         for personal finance management.

INTEGRATION POINTS:
    - ExpenseTrackingService: Actual spending data
    - BankingService: Transaction data
    - BudgetingAPI: Budget endpoints
    - FrontendBudget: Budget dashboard

FEATURES:
    - Category-based budgets
    - Spending limits
    - Trend analysis
    - Budget alerts

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from models.budgeting import Budget, BudgetAnalysis, ExpenseCategory
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class BudgetingService:
    """
    Service for budget creation and management.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        
    async def create_budget(
        self,
        user_id: str,
        budget_name: str,
        period: str,
        categories: Dict[str, float]
    ) -> Budget:
        """
        Create a new budget.
        
        Args:
            user_id: User identifier
            budget_name: Name of budget
            period: Budget period ("monthly", "yearly")
            categories: Dictionary of {category: budgeted_amount}
            
        Returns:
            Budget object
        """
        logger.info(f"Creating budget {budget_name} for user {user_id}")
        
        total_budget = sum(categories.values())
        
        budget = Budget(
            budget_id=f"budget_{user_id}_{datetime.now(timezone.utc).timestamp()}",
            user_id=user_id,
            budget_name=budget_name,
            period=period,
            categories=categories,
            total_budget=total_budget,
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
        
        # Cache budget
        cache_key = f"budget:{user_id}:{budget.budget_id}"
        self.cache_service.set(cache_key, budget.dict(), ttl=86400 * 365)
        
        return budget
    
    async def get_budget_analysis(
        self,
        budget_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> BudgetAnalysis:
        """
        Analyze budget vs actual spending.
        
        Args:
            budget_id: Budget identifier
            start_date: Optional analysis period start (default: last 30 days)
            end_date: Optional analysis period end (default: now)
            
        Returns:
            BudgetAnalysis with spending comparison
        """
        logger.info(f"Analyzing budget {budget_id}")
        
        if not end_date:
            end_date = datetime.now(timezone.utc)
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        # Get budget
        budget = await self._get_budget(budget_id)
        if not budget:
            raise ValueError(f"Budget {budget_id} not found")
        
        # Get actual spending (from expense tracking service)
        from services.budgeting.expense_tracking_service import get_expense_tracking_service
        expense_service = get_expense_tracking_service()
        expenses = await expense_service.get_expenses(
            budget.user_id, start_date, end_date
        )
        
        # Calculate spending by category
        spending_by_category = {}
        for expense in expenses:
            category = expense.category.value
            spending_by_category[category] = spending_by_category.get(category, 0.0) + expense.amount
        
        # Calculate analysis
        total_budgeted = budget.total_budget
        total_spent = sum(expense.amount for expense in expenses)
        remaining = total_budgeted - total_spent
        
        # Category analysis
        category_analysis = {}
        over_budget = []
        under_budget = []
        
        for category, budgeted in budget.categories.items():
            spent = spending_by_category.get(category, 0.0)
            category_remaining = budgeted - spent
            percentage = (spent / budgeted * 100) if budgeted > 0 else 0.0
            
            category_analysis[category] = {
                'budgeted': budgeted,
                'spent': spent,
                'remaining': category_remaining,
                'percentage': percentage
            }
            
            if spent > budgeted:
                over_budget.append(category)
            elif spent < budgeted * 0.8:  # Under 80% of budget
                under_budget.append(category)
        
        return BudgetAnalysis(
            budget_id=budget_id,
            period_start=start_date,
            period_end=end_date,
            total_budgeted=total_budgeted,
            total_spent=total_spent,
            remaining=remaining,
            category_analysis=category_analysis,
            over_budget_categories=over_budget,
            under_budget_categories=under_budget
        )
    
    async def _get_budget(self, budget_id: str) -> Optional[Budget]:
        """Get budget from cache."""
        # Simplified: would search cache or database
        return None


# Singleton instance
_budgeting_service: Optional[BudgetingService] = None


def get_budgeting_service() -> BudgetingService:
    """Get singleton budgeting service instance."""
    global _budgeting_service
    if _budgeting_service is None:
        _budgeting_service = BudgetingService()
    return _budgeting_service
