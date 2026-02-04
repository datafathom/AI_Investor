"""
==============================================================================
FILE: services/budgeting/expense_tracking_service.py
ROLE: Expense Tracking Engine
PURPOSE: Tracks expenses with automatic categorization, receipt scanning,
         and spending insights.

INTEGRATION POINTS:
    - BankingService: Transaction data
    - BudgetingService: Budget comparisons
    - ExpenseTrackingAPI: Expense endpoints
    - FrontendBudget: Expense tracking dashboard

FEATURES:
    - Automatic categorization
    - Receipt scanning
    - Spending insights
    - Trend analysis

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from schemas.budgeting import Expense, ExpenseCategory, SpendingTrend
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class ExpenseTrackingService:
    """
    Service for expense tracking and categorization.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        
        # Category keywords for auto-categorization
        self.category_keywords = {
            ExpenseCategory.HOUSING: ['rent', 'mortgage', 'housing', 'apartment'],
            ExpenseCategory.TRANSPORTATION: ['gas', 'uber', 'lyft', 'car', 'transport'],
            ExpenseCategory.FOOD: ['restaurant', 'grocery', 'food', 'dining', 'starbucks'],
            ExpenseCategory.UTILITIES: ['electric', 'water', 'internet', 'phone', 'utility'],
            ExpenseCategory.INSURANCE: ['insurance', 'premium'],
            ExpenseCategory.HEALTHCARE: ['doctor', 'pharmacy', 'medical', 'health'],
            ExpenseCategory.ENTERTAINMENT: ['movie', 'netflix', 'spotify', 'entertainment'],
            ExpenseCategory.SHOPPING: ['amazon', 'store', 'shopping', 'retail'],
            ExpenseCategory.EDUCATION: ['tuition', 'school', 'education', 'course'],
            ExpenseCategory.DEBT: ['loan', 'credit', 'debt', 'payment']
        }
    
    async def add_expense(
        self,
        user_id: str,
        amount: float,
        description: str,
        category: Optional[str] = None,
        merchant: Optional[str] = None,
        date: Optional[datetime] = None
    ) -> Expense:
        """
        Add expense transaction.
        
        Args:
            user_id: User identifier
            amount: Expense amount
            description: Expense description
            category: Optional category (auto-detected if not provided)
            merchant: Optional merchant name
            date: Optional date (default: now)
            
        Returns:
            Expense object
        """
        logger.info(f"Adding expense for user {user_id}")
        
        # Auto-categorize if not provided
        if not category:
            category = await self._auto_categorize(description, merchant)
        
        expense = Expense(
            expense_id=f"exp_{user_id}_{datetime.now(timezone.utc).timestamp()}",
            user_id=user_id,
            amount=amount,
            category=ExpenseCategory(category),
            description=description,
            merchant=merchant,
            date=date or datetime.now(timezone.utc)
        )
        
        # Save expense
        await self._save_expense(expense)
        
        return expense
    
    async def get_expenses(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
        category: Optional[str] = None
    ) -> List[Expense]:
        """
        Get expenses for user within date range.
        
        Args:
            user_id: User identifier
            start_date: Start date
            end_date: End date
            category: Optional category filter
            
        Returns:
            List of Expense objects
        """
        # In production, fetch from database
        # For now, return mock data
        return []

    async def get_spending_insights(self, user_id: str) -> Dict[str, Any]:
        """
        Get spending insights (total spending, top categories).
        """
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=30)
        expenses = await self.get_expenses(user_id, start_date, end_date)
        total_spending = sum(e.amount for e in expenses)
        
        return {
            "total_spending": total_spending,
            "period": "30 days"
        }
    
    async def analyze_spending_trends(
        self,
        user_id: str,
        category: Optional[str] = None,
        period: str = "monthly"
    ) -> List[SpendingTrend]:
        """
        Analyze spending trends by category.
        
        Args:
            user_id: User identifier
            category: Optional category filter
            period: Analysis period ("monthly", "yearly")
            
        Returns:
            List of SpendingTrend objects
        """
        logger.info(f"Analyzing spending trends for user {user_id}")
        
        # Get expenses
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=90)  # 3 months
        
        expenses = await self.get_expenses(user_id, start_date, end_date, category)
        
        # Group by category and calculate trends
        trends = []
        categories_to_analyze = [category] if category else [c.value for c in ExpenseCategory]
        
        for cat in categories_to_analyze:
            cat_expenses = [e for e in expenses if e.category.value == cat]
            
            if not cat_expenses:
                continue
            
            # Calculate average spending
            total_spending = sum(e.amount for e in cat_expenses)
            num_periods = 3  # 3 months
            average_spending = total_spending / num_periods
            
            # Calculate trend (simplified)
            if len(cat_expenses) >= 2:
                recent = sum(e.amount for e in cat_expenses[-10:])
                older = sum(e.amount for e in cat_expenses[:-10]) if len(cat_expenses) > 10 else recent
                percentage_change = ((recent - older) / older * 100) if older > 0 else 0.0
                
                if percentage_change > 5:
                    trend_direction = "increasing"
                elif percentage_change < -5:
                    trend_direction = "decreasing"
                else:
                    trend_direction = "stable"
            else:
                percentage_change = 0.0
                trend_direction = "stable"
            
            trends.append(SpendingTrend(
                category=cat,
                period=period,
                average_spending=average_spending,
                trend_direction=trend_direction,
                percentage_change=percentage_change
            ))
        
        return trends
    
    async def _auto_categorize(
        self,
        description: str,
        merchant: Optional[str]
    ) -> str:
        """Auto-categorize expense based on description and merchant."""
        text = f"{description} {merchant or ''}".lower()
        
        # Check keywords
        for category, keywords in self.category_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category.value
        
        return ExpenseCategory.OTHER.value
    
    async def _save_expense(self, expense: Expense):
        """Save expense to cache or database."""
        cache_key = f"expense:{expense.user_id}:{expense.expense_id}"
        self.cache_service.set(cache_key, expense.model_dump(), ttl=86400 * 365)


# Singleton instance
_expense_tracking_service: Optional[ExpenseTrackingService] = None


def get_expense_tracking_service() -> ExpenseTrackingService:
    """Get singleton expense tracking service instance."""
    global _expense_tracking_service
    if _expense_tracking_service is None:
        _expense_tracking_service = ExpenseTrackingService()
    return _expense_tracking_service
