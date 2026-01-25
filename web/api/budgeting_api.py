"""
==============================================================================
FILE: web/api/budgeting_api.py
ROLE: Budgeting API Endpoints
PURPOSE: REST endpoints for budgeting and expense tracking.

INTEGRATION POINTS:
    - BudgetingService: Budget management
    - ExpenseTrackingService: Expense tracking
    - FrontendBudget: Budget dashboard widgets

ENDPOINTS:
    - POST /api/budgeting/budget/create
    - GET /api/budgeting/budget/:budget_id/analyze
    - POST /api/budgeting/expense/add
    - GET /api/budgeting/expense/:user_id
    - GET /api/budgeting/trends/:user_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from services.budgeting.budgeting_service import get_budgeting_service
from services.budgeting.expense_tracking_service import get_expense_tracking_service

logger = logging.getLogger(__name__)

budgeting_bp = Blueprint('budgeting', __name__, url_prefix='/api/budgeting')


@budgeting_bp.route('/budget/create', methods=['POST'])
async def create_budget():
    """
    Create a new budget.
    
    Request body:
        user_id: User identifier
        budget_name: Name of budget
        period: Budget period (monthly, yearly)
        categories: Dictionary of {category: budgeted_amount}
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        budget_name = data.get('budget_name')
        period = data.get('period', 'monthly')
        categories = data.get('categories', {})
        
        if not user_id or not budget_name or not categories:
            return jsonify({
                'success': False,
                'error': 'user_id, budget_name, and categories are required'
            }), 400
        
        service = get_budgeting_service()
        budget = await service.create_budget(
            user_id=user_id,
            budget_name=budget_name,
            period=period,
            categories=categories
        )
        
        return jsonify({
            'success': True,
            'data': budget.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating budget: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@budgeting_bp.route('/budget/<budget_id>/analyze', methods=['GET'])
async def analyze_budget(budget_id: str):
    """
    Analyze budget vs actual spending.
    
    Query params:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        if not start_date_str or not end_date_str:
            return jsonify({
                'success': False,
                'error': 'start_date and end_date are required'
            }), 400
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        service = get_budgeting_service()
        analysis = await service.analyze_budget(
            budget_id=budget_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify({
            'success': True,
            'data': analysis.dict()
        })
        
    except Exception as e:
        logger.error(f"Error analyzing budget: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@budgeting_bp.route('/expense/add', methods=['POST'])
async def add_expense():
    """
    Add expense transaction.
    
    Request body:
        user_id: User identifier
        amount: Expense amount
        description: Expense description
        category: Optional category
        merchant: Optional merchant name
        date: Optional date (YYYY-MM-DD)
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        amount = float(data.get('amount', 0))
        description = data.get('description', '')
        category = data.get('category')
        merchant = data.get('merchant')
        date_str = data.get('date')
        
        if not user_id or not amount or not description:
            return jsonify({
                'success': False,
                'error': 'user_id, amount, and description are required'
            }), 400
        
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None
        
        service = get_expense_tracking_service()
        expense = await service.add_expense(
            user_id=user_id,
            amount=amount,
            description=description,
            category=category,
            merchant=merchant,
            date=date
        )
        
        return jsonify({
            'success': True,
            'data': expense.dict()
        })
        
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@budgeting_bp.route('/expense/<user_id>', methods=['GET'])
async def get_expenses(user_id: str):
    """
    Get expenses for user.
    
    Query params:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        category: Optional category filter
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        category = request.args.get('category')
        
        if not start_date_str or not end_date_str:
            return jsonify({
                'success': False,
                'error': 'start_date and end_date are required'
            }), 400
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        service = get_expense_tracking_service()
        expenses = await service.get_expenses(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            category=category
        )
        
        return jsonify({
            'success': True,
            'data': [e.dict() for e in expenses]
        })
        
    except Exception as e:
        logger.error(f"Error getting expenses: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@budgeting_bp.route('/trends/<user_id>', methods=['GET'])
async def get_spending_trends(user_id: str):
    """
    Get spending trends for user.
    
    Query params:
        category: Optional category filter
        period: Analysis period (monthly, yearly)
    """
    try:
        category = request.args.get('category')
        period = request.args.get('period', 'monthly')
        
        service = get_expense_tracking_service()
        trends = await service.analyze_spending_trends(
            user_id=user_id,
            category=category,
            period=period
        )
        
        return jsonify({
            'success': True,
            'data': [t.dict() for t in trends]
        })
        
    except Exception as e:
        logger.error(f"Error getting spending trends: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
