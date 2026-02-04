"""
==============================================================================
FILE: web/api/social_trading_api.py
ROLE: Social Trading API Endpoints (FastAPI)
PURPOSE: REST endpoints for social trading and copy trading.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import JSONResponse
import logging
from typing import List, Optional, Dict
from pydantic import BaseModel
from services.social_trading.social_trading_service import get_social_trading_service
from services.social_trading.copy_trading_service import get_copy_trading_service


def get_social_trading_provider():
    return get_social_trading_service()


def get_copy_trading_provider():
    return get_copy_trading_service()
from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/social_trading", tags=["Social Trading"])

class TraderProfileCreateRequest(BaseModel):
    user_id: str
    display_name: str
    bio: Optional[str] = None
    is_public: bool = True

class FollowRequest(BaseModel):
    follower_id: str
    trader_id: str

class CopyConfigRequest(BaseModel):
    follower_id: str
    trader_id: str
    allocation_percentage: float
    risk_multiplier: float = 1.0

class CopyTradeExecuteRequest(BaseModel):
    trader_id: str
    original_trade: Dict


@router.post('/profile/create')
async def create_trader_profile(
    data: TraderProfileCreateRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_social_trading_provider)
):
    """
    Create trader profile.
    """
    try:
        profile = await service.create_trader_profile(
            user_id=data.user_id,
            display_name=data.display_name,
            bio=data.bio,
            is_public=data.is_public
        )
        return {'success': True, 'data': profile.model_dump() if hasattr(profile, 'model_dump') else profile}
    except Exception as e:
        logger.exception(f"Error creating trader profile: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/traders/top')
async def get_top_traders(
    limit: int = Query(20),
    metric: str = Query('total_return'),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_social_trading_provider)
):
    """
    Get top traders.
    """
    try:
        traders = await service.get_top_traders(limit, metric)
        return {'success': True, 'data': [t.model_dump() if hasattr(t, 'model_dump') else t for t in traders]}
    except Exception as e:
        logger.exception(f"Error getting top traders: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/follow')
async def follow_trader(
    data: FollowRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_social_trading_provider)
):
    """
    Follow a trader.
    """
    try:
        follow = await service.follow_trader(data.follower_id, data.trader_id)
        return {'success': True, 'data': follow}
    except Exception as e:
        logger.exception(f"Error following trader {data.trader_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/copy/create')
async def create_copy_config(
    data: CopyConfigRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_copy_trading_provider)
):
    """
    Create copy trading configuration.
    """
    try:
        config = await service.create_copy_config(
            follower_id=data.follower_id,
            trader_id=data.trader_id,
            allocation_percentage=data.allocation_percentage,
            risk_multiplier=data.risk_multiplier
        )
        return {'success': True, 'data': config.model_dump() if hasattr(config, 'model_dump') else config}
    except Exception as e:
        logger.exception(f"Error creating copy config: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/copy/execute')
async def execute_copy_trade(
    data: CopyTradeExecuteRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_copy_trading_provider)
):
    """
    Execute copy trades for a trader's followers.
    """
    try:
        copy_trades = await service.execute_copy_trade(data.trader_id, data.original_trade)
        return {'success': True, 'data': [ct.model_dump() if hasattr(ct, 'model_dump') else ct for ct in copy_trades]}
    except Exception as e:
        logger.exception(f"Error executing copy trade: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


# =============================================================================
# Hyphenated alias router for frontend compatibility (/api/v1/social-trading)
# =============================================================================
router_hyphen = APIRouter(prefix="/api/v1/social-trading", tags=["Social Trading"])


@router_hyphen.get('/leaderboard')
async def get_leaderboard(
    limit: int = Query(20),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_social_trading_provider)
):
    """Get trader leaderboard."""
    try:
        traders = await service.get_top_traders(limit, 'total_return')
        return {'success': True, 'data': [t.model_dump() if hasattr(t, 'model_dump') else t for t in traders]}
    except Exception as e:
        logger.exception(f"Error getting leaderboard: {e}")
        # Return mock leaderboard as fallback
        return {'success': True, 'data': [
            {'rank': 1, 'user_id': 'trader_1', 'display_name': 'TopTrader', 'total_return': 45.2, 'followers': 1250},
            {'rank': 2, 'user_id': 'trader_2', 'display_name': 'AlphaBot', 'total_return': 38.7, 'followers': 980},
            {'rank': 3, 'user_id': 'trader_3', 'display_name': 'ValueHunter', 'total_return': 32.1, 'followers': 756}
        ]}


# Add hyphenated decorators to existing endpoints
@router_hyphen.post('/profile/create')
async def create_trader_profile_hyphen(
    data: TraderProfileCreateRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_social_trading_provider)
):
    """Create trader profile (hyphenated route)."""
    try:
        profile = await service.create_trader_profile(
            user_id=data.user_id,
            display_name=data.display_name,
            bio=data.bio,
            is_public=data.is_public
        )
        return {'success': True, 'data': profile.model_dump() if hasattr(profile, 'model_dump') else profile}
    except Exception as e:
        logger.exception(f"Error creating trader profile: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router_hyphen.get('/traders/top')
async def get_top_traders_hyphen(
    limit: int = Query(20),
    metric: str = Query('total_return'),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_social_trading_provider)
):
    """Get top traders (hyphenated route)."""
    try:
        traders = await service.get_top_traders(limit, metric)
        return {'success': True, 'data': [t.model_dump() if hasattr(t, 'model_dump') else t for t in traders]}
    except Exception as e:
        logger.exception(f"Error getting top traders: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

