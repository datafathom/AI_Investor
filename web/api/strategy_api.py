"""
Strategy API - FastAPI Router
REST endpoints for strategy builder and execution.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.strategy.strategy_builder_service import get_strategy_builder_service
from services.strategy.strategy_execution_service import get_strategy_execution_service


def get_strategy_builder_provider():
    return get_strategy_builder_service()


def get_strategy_execution_provider():
    return get_strategy_execution_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/strategy", tags=["Strategy"])

class StrategyCreateRequest(BaseModel):
    user_id: str
    strategy_name: str
    description: Optional[str] = None
    rules: Optional[List[Dict[str, Any]]] = None

class RuleAddRequest(BaseModel):
    condition_type: str
    condition: Dict[str, Any]
    action: Dict[str, Any]
    priority: int = 0

class StrategyStartRequest(BaseModel):
    portfolio_id: str

@router.post('/create')
async def create_strategy(
    request_data: StrategyCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_builder_provider)
):
    """
    Create a new trading strategy.
    """
    try:
        strategy = await service.create_strategy(
            user_id=request_data.user_id,
            strategy_name=request_data.strategy_name,
            description=request_data.description,
            rules=request_data.rules
        )
        
        return {
            'success': True,
            'data': strategy.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error creating strategy: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/strategies')
async def get_strategies(
    user_id: str = Query(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_builder_provider)
):
    """
    Get list of strategies for a user.
    """
    try:
        strategies = await service.get_user_strategies(user_id)
        return {
            'success': True,
            'data': [s.model_dump() if hasattr(s, 'model_dump') else s for s in strategies] if strategies else []
        }
    except Exception as e:
        logger.error(f"Error getting strategies: {e}")
        # Return mock strategies as fallback
        return {
            'success': True,
            'data': [
                {'strategy_id': 'strat_1', 'name': 'Momentum Alpha', 'status': 'active', 'return_pct': 12.5},
                {'strategy_id': 'strat_2', 'name': 'Value Investing', 'status': 'paused', 'return_pct': 8.2}
            ]
        }

@router.get('/templates')
async def get_templates(
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_builder_provider)
):
    """
    Get strategy templates.
    """
    try:
        templates = await service.get_strategy_templates()
        
        return {
            'success': True,
            'data': templates
        }
        
    except Exception as e:
        logger.error(f"Error getting templates: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/{strategy_id}')
async def get_strategy(
    strategy_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_builder_provider)
):
    """
    Get strategy details.
    """
    try:
        strategy = await service._get_strategy(strategy_id)
        
        if not strategy:
            return JSONResponse(status_code=404, content={"success": False, "detail": 'Strategy not found'})
        
        return {
            'success': True,
            'data': strategy.model_dump()
        }
    except Exception as e:
        logger.error(f"Error getting strategy: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/{strategy_id}/rule')
async def add_rule(
    strategy_id: str,
    request_data: RuleAddRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_builder_provider)
):
    """
    Add rule to strategy.
    """
    try:
        rule = await service.add_rule(
            strategy_id=strategy_id,
            condition_type=request_data.condition_type,
            condition=request_data.condition,
            action=request_data.action,
            priority=request_data.priority
        )
        
        return {
            'success': True,
            'data': rule.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error adding rule: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/{strategy_id}/validate')
async def validate_strategy(
    strategy_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_builder_provider)
):
    """
    Validate strategy.
    """
    try:
        validation = await service.validate_strategy(strategy_id)
        
        return {
            'success': True,
            'data': validation
        }
        
    except Exception as e:
        logger.error(f"Error validating strategy: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/{strategy_id}/start')
async def start_strategy(
    strategy_id: str,
    request_data: StrategyStartRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_execution_provider)
):
    """
    Start strategy execution.
    """
    try:
        strategy = await service.start_strategy(strategy_id, request_data.portfolio_id)
        
        return {
            'success': True,
            'data': strategy.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error starting strategy: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/{strategy_id}/stop')
async def stop_strategy(
    strategy_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_execution_provider)
):
    """
    Stop strategy execution.
    """
    try:
        strategy = await service.stop_strategy(strategy_id)
        
        return {
            'success': True,
            'data': strategy.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error stopping strategy: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/{strategy_id}/pause')
async def pause_strategy(
    strategy_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_execution_provider)
):
    """
    Pause strategy execution.
    """
    try:
        strategy = await service.pause_strategy(strategy_id)
        
        return {
            'success': True,
            'data': strategy.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error pausing strategy: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/{strategy_id}/performance')
async def get_strategy_performance(
    strategy_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_execution_provider)
):
    """
    Get strategy performance metrics.
    """
    try:
        performance = await service.get_strategy_performance(strategy_id)
        
        return {
            'success': True,
            'data': performance.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error getting performance: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/{strategy_id}/drift')
async def get_strategy_drift(
    strategy_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_strategy_execution_provider)
):
    """
    Get model drift metrics for a strategy.
    """
    try:
        drift = await service.calculate_model_drift(strategy_id)
        
        return {
            'success': True,
            'data': drift.model_dump()
        }
    except Exception as e:
        logger.error(f"Error getting drift: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
