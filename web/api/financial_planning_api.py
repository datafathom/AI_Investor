"""
==============================================================================
FILE: web/api/financial_planning_api.py
ROLE: Financial Planning API Endpoints
PURPOSE: REST endpoints for financial planning and goal tracking.

INTEGRATION POINTS:
    - FinancialPlanningService: Plan creation and projections
    - GoalTrackingService: Goal progress tracking
    - FrontendPlanning: Planning dashboard widgets

ENDPOINTS:
    - POST /api/planning/plan/create
    - GET /api/planning/plan/:user_id
    - POST /api/planning/goal/project/:goal_id
    - POST /api/planning/goal/optimize/:plan_id
    - GET /api/planning/goal/:goal_id/progress
    - PUT /api/planning/goal/:goal_id/update

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from services.planning.financial_planning_service import get_financial_planning_service
from services.planning.goal_tracking_service import get_goal_tracking_service

logger = logging.getLogger(__name__)

financial_planning_bp = Blueprint('financial_planning', __name__, url_prefix='/api/planning')


@financial_planning_bp.route('/plan/create', methods=['POST'])
async def create_plan():
    """
    Create a new financial plan.
    
    Request body:
        user_id: User identifier
        goals: List of goal objects
        monthly_contribution_capacity: Total monthly contribution capacity
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        goals = data.get('goals', [])
        monthly_contribution_capacity = float(data.get('monthly_contribution_capacity', 0))
        
        if not user_id or not goals:
            return jsonify({
                'success': False,
                'error': 'user_id and goals are required'
            }), 400
        
        service = get_financial_planning_service()
        plan = await service.create_financial_plan(
            user_id=user_id,
            goals=goals,
            monthly_contribution_capacity=monthly_contribution_capacity
        )
        
        return jsonify({
            'success': True,
            'data': plan.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating financial plan: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@financial_planning_bp.route('/plan/<user_id>', methods=['GET'])
async def get_plan(user_id: str):
    """
    Get financial plan for user.
    """
    try:
        from services.system.cache_service import get_cache_service
        cache_service = get_cache_service()
        plan_data = cache_service.get(f"financial_plan:{user_id}")
        
        if not plan_data:
            return jsonify({
                'success': False,
                'error': 'Plan not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': plan_data
        })
        
    except Exception as e:
        logger.error(f"Error getting financial plan: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@financial_planning_bp.route('/goal/project/<goal_id>', methods=['POST'])
async def project_goal(goal_id: str):
    """
    Project goal timeline.
    
    Request body:
        expected_return: Optional expected annual return
        monthly_contribution: Optional monthly contribution
    """
    try:
        data = request.get_json() or {}
        expected_return = data.get('expected_return')
        monthly_contribution = data.get('monthly_contribution')
        
        # Get goal
        from services.planning.goal_tracking_service import get_goal_tracking_service
        tracking_service = get_goal_tracking_service()
        goal = await tracking_service._get_goal(goal_id)
        
        if not goal:
            return jsonify({
                'success': False,
                'error': 'Goal not found'
            }), 404
        
        planning_service = get_financial_planning_service()
        projection = await planning_service.project_goal_timeline(
            goal=goal,
            expected_return=expected_return,
            monthly_contribution=monthly_contribution
        )
        
        return jsonify({
            'success': True,
            'data': projection.dict()
        })
        
    except Exception as e:
        logger.error(f"Error projecting goal: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@financial_planning_bp.route('/goal/optimize/<plan_id>', methods=['POST'])
async def optimize_contributions(plan_id: str):
    """
    Optimize contributions across goals in plan.
    """
    try:
        # Get plan
        from services.system.cache_service import get_cache_service
        cache_service = get_cache_service()
        plan_data = cache_service.get(f"plan:{plan_id}")
        
        if not plan_data:
            return jsonify({
                'success': False,
                'error': 'Plan not found'
            }), 404
        
        from models.financial_planning import FinancialPlan
        plan = FinancialPlan(**plan_data)
        
        planning_service = get_financial_planning_service()
        optimized = await planning_service.optimize_goal_contributions(plan)
        
        return jsonify({
            'success': True,
            'data': optimized
        })
        
    except Exception as e:
        logger.error(f"Error optimizing contributions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@financial_planning_bp.route('/goal/<goal_id>/progress', methods=['GET'])
async def get_goal_progress(goal_id: str):
    """
    Get goal progress information.
    """
    try:
        tracking_service = get_goal_tracking_service()
        progress = await tracking_service.get_goal_progress(goal_id)
        
        return jsonify({
            'success': True,
            'data': progress
        })
        
    except Exception as e:
        logger.error(f"Error getting goal progress: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@financial_planning_bp.route('/goal/<goal_id>/update', methods=['PUT'])
async def update_goal_progress(goal_id: str):
    """
    Update goal progress.
    
    Request body:
        current_amount: Current amount saved
    """
    try:
        data = request.get_json() or {}
        current_amount = float(data.get('current_amount', 0))
        
        tracking_service = get_goal_tracking_service()
        updated_goal = await tracking_service.update_goal_progress(
            goal_id=goal_id,
            current_amount=current_amount
        )
        
        return jsonify({
            'success': True,
            'data': updated_goal.dict()
        })
        
    except Exception as e:
        logger.error(f"Error updating goal progress: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
