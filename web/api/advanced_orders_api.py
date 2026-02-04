"""
Advanced Orders API - FastAPI Router
REST endpoints for advanced order types and smart execution.
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.execution.advanced_order_service import get_advanced_order_service
from services.execution.smart_execution_service import get_smart_execution_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/execution", tags=["Execution"])

# --- Request Models ---

class TrailingStopRequest(BaseModel):
    user_id: str
    symbol: str
    quantity: int
    trailing_type: str = 'percentage'
    trailing_value: float
    initial_stop_price: Optional[float] = None

class BracketOrderRequest(BaseModel):
    user_id: str
    symbol: str
    quantity: int
    entry_price: float
    profit_target_price: Optional[float] = None
    stop_loss_price: Optional[float] = None

class OCOOrderRequest(BaseModel):
    user_id: str
    symbol: str
    quantity: int
    order1: Dict[str, Any]
    order2: Dict[str, Any]

class ConditionalOrderRequest(BaseModel):
    user_id: str
    symbol: str
    quantity: int
    order_type: str = 'market'
    condition_type: str
    condition_value: float

class PriceUpdateRequest(BaseModel):
    current_price: float

class TWAPRequest(BaseModel):
    symbol: str
    total_quantity: int
    time_window_minutes: int = 60
    start_time: Optional[str] = None

class VWAPRequest(BaseModel):
    symbol: str
    total_quantity: int
    time_window_minutes: int = 60
    start_time: Optional[str] = None

class ImplementationShortfallRequest(BaseModel):
    symbol: str
    total_quantity: int
    urgency: float = 0.5

# --- Endpoints ---

@router.post('/trailing-stop')
async def create_trailing_stop(
    request_data: TrailingStopRequest,
    service = Depends(get_advanced_order_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create trailing stop order."""
    try:
        order = await service.create_trailing_stop(
            user_id=request_data.user_id,
            symbol=request_data.symbol,
            quantity=request_data.quantity,
            trailing_type=request_data.trailing_type,
            trailing_value=request_data.trailing_value,
            initial_stop_price=request_data.initial_stop_price
        )
        return {'success': True, 'data': order.model_dump()}
    except Exception as e:
        logger.error(f"Error creating trailing stop: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/bracket')
async def create_bracket_order(
    request_data: BracketOrderRequest,
    service = Depends(get_advanced_order_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create bracket order."""
    try:
        bracket = await service.create_bracket_order(
            user_id=request_data.user_id,
            symbol=request_data.symbol,
            quantity=request_data.quantity,
            entry_price=request_data.entry_price,
            profit_target_price=request_data.profit_target_price,
            stop_loss_price=request_data.stop_loss_price
        )
        return {'success': True, 'data': bracket.model_dump()}
    except Exception as e:
        logger.error(f"Error creating bracket order: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/oco')
async def create_oco_order(
    request_data: OCOOrderRequest,
    service = Depends(get_advanced_order_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create OCO (One-Cancels-Other) order."""
    try:
        oco = await service.create_oco_order(
            user_id=request_data.user_id,
            symbol=request_data.symbol,
            quantity=request_data.quantity,
            order1=request_data.order1,
            order2=request_data.order2
        )
        return {'success': True, 'data': oco}
    except Exception as e:
        logger.error(f"Error creating OCO order: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/conditional')
async def create_conditional_order(
    request_data: ConditionalOrderRequest,
    service = Depends(get_advanced_order_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create conditional order."""
    try:
        order = await service.create_conditional_order(
            user_id=request_data.user_id,
            symbol=request_data.symbol,
            quantity=request_data.quantity,
            order_type=request_data.order_type,
            condition_type=request_data.condition_type,
            condition_value=request_data.condition_value
        )
        return {'success': True, 'data': order.model_dump()}
    except Exception as e:
        logger.error(f"Error creating conditional order: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.put('/trailing-stop/{order_id}/update')
async def update_trailing_stop(
    order_id: str,
    request_data: PriceUpdateRequest,
    service = Depends(get_advanced_order_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update trailing stop with current price."""
    try:
        updated_order = await service.update_trailing_stop(order_id, request_data.current_price)
        return {'success': True, 'data': updated_order.model_dump()}
    except Exception as e:
        logger.error(f"Error updating trailing stop: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/twap')
async def execute_twap(
    request_data: TWAPRequest,
    service = Depends(get_smart_execution_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Execute order using TWAP algorithm."""
    try:
        start_time = datetime.fromisoformat(request_data.start_time) if request_data.start_time else None
        executions = await service.execute_twap(
            symbol=request_data.symbol,
            total_quantity=request_data.total_quantity,
            time_window_minutes=request_data.time_window_minutes,
            start_time=start_time
        )
        return {'success': True, 'data': [e.model_dump() for e in executions]}
    except Exception as e:
        logger.error(f"Error executing TWAP: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/vwap')
async def execute_vwap(
    request_data: VWAPRequest,
    service = Depends(get_smart_execution_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Execute order using VWAP algorithm."""
    try:
        start_time = datetime.fromisoformat(request_data.start_time) if request_data.start_time else None
        executions = await service.execute_vwap(
            symbol=request_data.symbol,
            total_quantity=request_data.total_quantity,
            time_window_minutes=request_data.time_window_minutes,
            start_time=start_time
        )
        return {'success': True, 'data': [e.model_dump() for e in executions]}
    except Exception as e:
        logger.error(f"Error executing VWAP: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/implementation-shortfall')
async def execute_implementation_shortfall(
    request_data: ImplementationShortfallRequest,
    service = Depends(get_smart_execution_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Execute order using Implementation Shortfall algorithm."""
    try:
        executions = await service.execute_implementation_shortfall(
            symbol=request_data.symbol,
            total_quantity=request_data.total_quantity,
            urgency=request_data.urgency
        )
        return {'success': True, 'data': [e.model_dump() for e in executions]}
    except Exception as e:
        logger.error(f"Error executing Implementation Shortfall: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
