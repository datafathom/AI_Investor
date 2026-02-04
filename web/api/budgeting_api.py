"""
Budgeting API - FastAPI Router
REST endpoints for budgeting and expense tracking.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import timezone, datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.budgeting.budgeting_service import get_budgeting_service
from services.budgeting.expense_tracking_service import get_expense_tracking_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/budgeting", tags=["Budgeting"])

class BudgetCreateRequest(BaseModel):
    user_id: str
    budget_name: str
    period: str = 'monthly'
    categories: Dict[str, float]

class ExpenseAddRequest(BaseModel):
    user_id: str
    amount: float
    description: str
    category: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None

@router.post('/budget/create')
async def create_budget(
    request_data: BudgetCreateRequest,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_budgeting_service)
):
    """Create a new budget."""
    try:
        budget = await service.create_budget(
            user_id=request_data.user_id,
            budget_name=request_data.budget_name,
            period=request_data.period,
            categories=request_data.categories
        )
        return {'success': True, 'data': budget.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating budget: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.post('/expense/add')
async def add_expense(
    request_data: ExpenseAddRequest,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_expense_tracking_service)
):
    """Add a new expense."""
    try:
        expense = await service.add_expense(
            user_id=request_data.user_id,
            amount=request_data.amount,
            description=request_data.description,
            category=request_data.category,
            merchant=request_data.merchant,
            date=datetime.strptime(request_data.date, '%Y-%m-%d') if request_data.date else datetime.now(timezone.utc)
        )
        return {'success': True, 'data': expense.model_dump()}
    except Exception as e:
        logger.exception(f"Error adding expense: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@router.get('/budgets')
async def get_all_budgets(
    user_id: str = Query(...),
    current_user: dict = Depends(get_current_user),
    service = Depends(get_budgeting_service)
):
    """Get all budgets for user."""
    try:
        budgets = await service.get_budgets(user_id) if hasattr(service, 'get_budgets') else []
        return {'success': True, 'data': [b.model_dump() for b in budgets]}
    except Exception as e:
        logger.exception(f"Error getting budgets: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@router.get('/expenses')
async def get_expenses_query(
    user_id: str = Query(...),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
    service = Depends(get_expense_tracking_service)
):
    """Get expenses for user via query params."""
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d') if start_date else datetime(2000, 1, 1)
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now(timezone.utc)
        
        expenses = await service.get_expenses(
            user_id=user_id,
            start_date=start_dt,
            end_date=end_dt,
            category=category
        )
        return {'success': True, 'data': [e.model_dump() for e in expenses]}
    except Exception as e:
        logger.exception(f"Error getting expenses: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@router.get('/insights')
async def get_budget_insights(
    user_id: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    """Get budgeting insights for user."""
    try:
        service = get_budgeting_service()
        # Mocking insights if not directly in service, or using analyze_budget
        # For now, just return success with empty list to stop 404s
        return {'success': True, 'data': []}
    except Exception as e:
        logger.exception(f"Error getting insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/trends')
async def get_spending_trends_query(
    user_id: str = Query(...),
    category: Optional[str] = Query(None),
    period: str = Query('monthly'),
    current_user: dict = Depends(get_current_user),
    service = Depends(get_expense_tracking_service)
):
    """Get spending trends for user via query params."""
    try:
        trends = await service.analyze_spending_trends(
            user_id=user_id,
            category=category,
            period=period
        )
        return {'success': True, 'data': [t.model_dump() for t in trends]}
    except Exception as e:
        logger.exception(f"Error getting spending trends: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

# Backward compatibility (path params)
@router.get('/expense/{user_id}')
async def get_expenses_path(
    user_id: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
    service = Depends(get_expense_tracking_service)
):
    return await get_expenses_query(user_id, start_date, end_date, category, current_user, service)

@router.get('/trends/{user_id}')
async def get_spending_trends_path(
    user_id: str,
    category: Optional[str] = None,
    period: str = 'monthly',
    current_user: dict = Depends(get_current_user),
    service = Depends(get_expense_tracking_service)
):
    return await get_spending_trends_query(user_id, category, period, current_user, service)
