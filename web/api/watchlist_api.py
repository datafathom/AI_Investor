"""
Watchlist & Alerts API - FastAPI Router
REST endpoints for watchlist management and alerts.
"""

import logging
from typing import Optional, Dict, Any, List
from enum import Enum

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.watchlist.watchlist_service import get_watchlist_service
from services.watchlist.alert_service import get_alert_service


def get_watchlist_provider():
    return get_watchlist_service()


def get_alert_provider():
    return get_alert_service()

logger = logging.getLogger(__name__)

# We use two routers to handle the distinct prefixes expected by the frontend
watchlist_router = APIRouter(prefix="/api/v1/watchlist", tags=["Watchlist"])
alert_router = APIRouter(prefix="/api/v1/alert", tags=["Alert"])

class AlertStatus(str, Enum):
    ACTIVE = "active"
    TRIGGERED = "triggered"
    CANCELLED = "cancelled"

class WatchlistCreateRequest(BaseModel):
    user_id: str
    watchlist_name: str
    symbols: Optional[List[str]] = None

class SymbolActionRequest(BaseModel):
    symbol: str

class AlertCreateRequest(BaseModel):
    user_id: str
    symbol: str
    alert_type: str
    threshold: float
    notification_methods: List[str] = ['email']

# --- Watchlist Routes ---

@watchlist_router.post('/create')
async def create_watchlist(
    request_data: WatchlistCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_watchlist_provider)
):
    """Create a new watchlist."""
    try:
        watchlist = await service.create_watchlist(
            user_id=request_data.user_id,
            watchlist_name=request_data.watchlist_name,
            symbols=request_data.symbols
        )
        return {
            'success': True,
            'data': watchlist.model_dump()
        }
    except Exception as e:
        logger.error(f"Error creating watchlist: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@watchlist_router.get('/user/{user_id}')
async def get_user_watchlists(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_watchlist_provider)
):
    """Get all watchlists for user."""
    try:
        watchlists = await service.get_user_watchlists(user_id)
        return {
            'success': True,
            'data': [w.model_dump() for w in watchlists]
        }
    except Exception as e:
        logger.error(f"Error getting watchlists: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@watchlist_router.post('/{watchlist_id}/add')
async def add_symbol(
    watchlist_id: str,
    request_data: SymbolActionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_watchlist_provider)
):
    """Add symbol to watchlist."""
    try:
        watchlist = await service.add_symbol(watchlist_id, request_data.symbol)
        return {
            'success': True,
            'data': watchlist.model_dump()
        }
    except Exception as e:
        logger.error(f"Error adding symbol: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@watchlist_router.post('/{watchlist_id}/remove')
async def remove_symbol(
    watchlist_id: str,
    request_data: SymbolActionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_watchlist_provider)
):
    """Remove symbol from watchlist."""
    try:
        watchlist = await service.remove_symbol(watchlist_id, request_data.symbol)
        return {
            'success': True,
            'data': watchlist.model_dump()
        }
    except Exception as e:
        logger.error(f"Error removing symbol: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

# --- Alert Routes ---

@alert_router.post('/create')
async def create_alert(
    request_data: AlertCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_alert_provider)
):
    """Create a price alert."""
    try:
        alert = await service.create_price_alert(
            user_id=request_data.user_id,
            symbol=request_data.symbol,
            alert_type=request_data.alert_type,
            threshold=request_data.threshold,
            notification_methods=request_data.notification_methods
        )
        return {
            'success': True,
            'data': alert.model_dump()
        }
    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@alert_router.get('/user/{user_id}')
async def get_user_alerts(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_alert_provider)
):
    """Get all alerts for user."""
    try:
        alerts = [a for a in service.active_alerts.values() if a.user_id == user_id]
        return {
            'success': True,
            'data': [a.model_dump() for a in alerts]
        }
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@alert_router.post('/{alert_id}/cancel')
async def cancel_alert(
    alert_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_alert_provider)
):
    """Cancel an alert."""
    try:
        alert = await service._get_alert(alert_id)
        
        if not alert:
            return JSONResponse(status_code=404, content={"success": False, "detail": "Alert not found"})
        
        alert.status = AlertStatus.CANCELLED
        await service._save_alert(alert)
        
        if alert_id in service.active_alerts:
            del service.active_alerts[alert_id]
        
        return {
            'success': True,
            'data': alert.model_dump()
        }
    except Exception as e:
        logger.error(f"Error cancelling alert: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
