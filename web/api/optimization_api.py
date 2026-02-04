"""
Optimization API - FastAPI Router
REST endpoints for portfolio optimization and rebalancing.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.optimization.portfolio_optimizer_service import get_optimizer_service
from services.optimization.rebalancing_service import get_rebalancing_service
from schemas.optimization import OptimizationConstraints, RebalancingRecommendation


def get_optimizer_provider():
    return get_optimizer_service()


def get_rebalancing_provider():
    return get_rebalancing_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/optimization", tags=["Optimization"])
# Alias for hyphenated frontend services
router_hyphen = APIRouter(prefix="/api/v1/optimization", tags=["Optimization Alias"])

class OptimizeRequest(BaseModel):
    objective: str = 'maximize_sharpe'
    method: str = 'mean_variance'
    constraints: Optional[OptimizationConstraints] = None
    risk_model: str = 'historical'
    lookback_days: int = 252

class RebalanceRecommendRequest(BaseModel):
    strategy: str = 'threshold'

class RebalanceExecuteRequest(BaseModel):
    recommendation: RebalancingRecommendation
    approved: bool = False

@router.post('/optimize/{portfolio_id}')
async def optimize_portfolio(
    portfolio_id: str,
    request_data: OptimizeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_optimizer_provider)
):
    """
    Optimize portfolio for given objective.
    """
    try:
        result = await service.optimize(
            portfolio_id=portfolio_id,
            objective=request_data.objective,
            method=request_data.method,
            constraints=request_data.constraints,
            risk_model=request_data.risk_model,
            lookback_days=request_data.lookback_days
        )
        
        return {
            'success': True,
            'data': result.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error optimizing portfolio: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/rebalancing/check/{portfolio_id}')
async def check_rebalancing(
    portfolio_id: str,
    threshold: float = 0.05,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_rebalancing_provider)
):
    """
    Check if portfolio needs rebalancing.
    """
    try:
        needs_rebalancing = await service.check_rebalancing_needed(
            portfolio_id=portfolio_id,
            threshold=threshold
        )
        
        return {
            'success': True,
            'data': {
                'needs_rebalancing': needs_rebalancing,
                'threshold': threshold
            }
        }
        
    except Exception as e:
        logger.error(f"Error checking rebalancing: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/rebalancing/recommend/{portfolio_id}')
@router.get('/rebalancing-recommendations')
@router_hyphen.get('/rebalancing-recommendations')
async def recommend_rebalancing(
    portfolio_id: Optional[str] = None,
    strategy: str = 'threshold',
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_rebalancing_provider)
):
    """
    Generate rebalancing recommendation.
    Supports both POST with path param and GET with query param.
    """
    try:
        pid = portfolio_id or "default-portfolio"
        recommendation = await service.generate_rebalancing_recommendation(
            portfolio_id=pid,
            strategy=strategy
        )
        
        return {
            'success': True,
            'data': recommendation.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error generating rebalancing recommendation: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/rebalancing/execute/{portfolio_id}')
async def execute_rebalancing(
    portfolio_id: str,
    request_data: RebalanceExecuteRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_rebalancing_provider)
):
    """
    Execute rebalancing trades.
    """
    try:
        history = await service.execute_rebalancing(
            portfolio_id=portfolio_id,
            recommendation=request_data.recommendation,
            approved=request_data.approved
        )
        
        return {
            'success': True,
            'data': history.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error executing rebalancing: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/rebalancing/history/{portfolio_id}')
@router.get('/rebalancing-history')
@router_hyphen.get('/rebalancing-history')
async def get_rebalancing_history(
    portfolio_id: Optional[str] = None,
    limit: int = 10,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_rebalancing_provider)
):
    """
    Get rebalancing history for portfolio.
    """
    try:
        pid = portfolio_id or "default-portfolio"
        history = await service.get_rebalancing_history(
            portfolio_id=pid,
            limit=limit
        )
        
        return {
            'success': True,
            'data': [h.model_dump() for h in history]
        }
        
    except Exception as e:
        logger.error(f"Error getting rebalancing history: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
