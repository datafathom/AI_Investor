"""
Financial Planning API - FastAPI Router
REST endpoints for financial planning and goal tracking.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.planning.financial_planning_service import get_financial_planning_service
from services.planning.goal_tracking_service import get_goal_tracking_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/financial_planning", tags=["Financial Planning"])

class PlanCreateRequest(BaseModel):
    user_id: str
    goals: List[Dict[str, Any]]
    monthly_contribution_capacity: float = 0.0

class GoalProjectionRequest(BaseModel):
    expected_return: Optional[float] = None
    monthly_contribution: Optional[float] = None

class GoalProgressUpdateRequest(BaseModel):
    current_amount: float

@router.post('/plan/create')
async def create_plan(
    request_data: PlanCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service = Depends(get_financial_planning_service)
):
    """Create a new financial plan."""
    try:
        plan = await service.create_financial_plan(
            user_id=request_data.user_id,
            goals=request_data.goals,
            monthly_contribution_capacity=request_data.monthly_contribution_capacity
        )
        
        return {
            'success': True,
            'data': plan.model_dump()
        }
    except Exception as e:
        logger.error(f"Error creating financial plan: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@router.get('/plan/{user_id}')
async def get_plan(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service = Depends(get_financial_planning_service)
):
    """Get financial plan for user."""
    try:
        plan = await service.get_financial_plan(user_id)
        if not plan:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=404, content={"success": False, "error": "Plan not found"})
        
        return {
            'success': True,
            'data': plan.model_dump()
        }
    except Exception as e:
        logger.error(f"Error getting financial plan: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@router.post('/goal/project/{goal_id}')
async def project_goal(
    goal_id: str,
    request_data: GoalProjectionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Project goal timeline."""
    try:
        tracking_service = get_goal_tracking_service()
        goal = await tracking_service._get_goal(goal_id)
        
        if not goal:
            raise HTTPException(status_code=404, detail='Goal not found')
        
        planning_service = get_financial_planning_service()
        projection = await planning_service.project_goal_timeline(
            goal=goal,
            expected_return=request_data.expected_return,
            monthly_contribution=request_data.monthly_contribution
        )
        
        return {
            'success': True,
            'data': projection.model_dump()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error projecting goal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/goal/optimize/{plan_id}')
async def optimize_contributions(
    plan_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Optimize contributions across goals in plan."""
    try:
        from services.system.cache_service import get_cache_service
        cache_service = get_cache_service()
        plan_data = cache_service.get(f"plan:{plan_id}")
        
        if not plan_data:
            raise HTTPException(status_code=404, detail='Plan not found')
        
        from schemas.financial_planning import FinancialPlan
        plan = FinancialPlan(**plan_data)
        
        planning_service = get_financial_planning_service()
        optimized = await planning_service.optimize_goal_contributions(plan)
        
        return {
            'success': True,
            'data': optimized
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error optimizing contributions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/goal/{goal_id}/progress')
async def get_goal_progress(
    goal_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get goal progress information."""
    try:
        tracking_service = get_goal_tracking_service()
        progress = await tracking_service.get_goal_progress(goal_id)
        
        return {
            'success': True,
            'data': progress
        }
    except Exception as e:
        logger.error(f"Error getting goal progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/goal/{goal_id}/update')
async def update_goal_progress(
    goal_id: str,
    request_data: GoalProgressUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update goal progress."""
    try:
        tracking_service = get_goal_tracking_service()
        updated_goal = await tracking_service.update_goal_progress(
            goal_id=goal_id,
            current_amount=request_data.current_amount
        )
        
        return {
            'success': True,
            'data': updated_goal.model_dump()
        }
    except Exception as e:
        logger.error(f"Error updating goal progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))
