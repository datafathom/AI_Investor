"""
Morning Briefing API - FastAPI Router
Exposes Daily Briefing capabilities to the frontend.
"""

import logging
from typing import Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.ai.briefing_generator import get_briefing_generator as _get_briefing_generator

def get_briefing_gen(mock: bool = True):
    """Dependency for getting the briefing generator."""
    return _get_briefing_generator(mock=mock)

logger = logging.getLogger(__name__)

# Updated prefix to match frontend's /ai/briefing/daily
router = APIRouter(prefix="/api/v1/ai/briefing", tags=["Briefing"])

@router.get('/daily')
async def get_daily_briefing(
    mock: bool = True,
    generator = Depends(get_briefing_gen),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get the daily morning briefing.
    """
    try:
        result = await generator.get_daily_briefing()
        return {"success": True, "data": result}
    except Exception as e:
        logger.error("Failed to fetch daily briefing: %s", e)
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
