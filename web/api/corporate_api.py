"""
Corporate API - Earnings & Corporate Actions
Phase 63: Endpoints for earnings calendars, dividends, and DRIP settings.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import logging

from services.trading.corporate_service import (
    CorporateService,
    EarningsEvent,
    CorporateAction,
    get_corporate_service
)
from services.trading.ipo_tracker import IPOTracker, get_ipo_tracker, IPOAnalysis

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/corporate", tags=["Corporate"])

class EarningsResponse(BaseModel):
    ticker: str
    date: str
    time: str
    estimated_eps: float
    estimated_revenue: str

class ActionResponse(BaseModel):
    ticker: str
    type: str
    ex_date: str
    details: str

@router.get("/earnings")
async def get_earnings(
    days: int = 30,
    service: CorporateService = Depends(get_corporate_service)
):
    try:
        earnings = await service.get_earnings_calendar(days)
        data = [EarningsResponse(
            ticker=e.ticker,
            date=e.date,
            time=e.time,
            estimated_eps=e.estimated_eps,
            estimated_revenue=e.estimated_revenue
        ).model_dump() for e in earnings]
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Error getting earnings")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/actions")
async def list_actions(
    service: CorporateService = Depends(get_corporate_service)
):
    try:
        actions = await service.get_corporate_actions()
        data = [ActionResponse(
            ticker=a.ticker,
            type=a.type,
            ex_date=a.ex_date,
            details=a.details
        ).model_dump() for a in actions]
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Error listing actions")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post("/drip")
async def toggle_drip(
    enabled: bool,
    service: CorporateService = Depends(get_corporate_service)
):
    try:
        result = await service.toggle_drip(enabled)
        return {"success": True, "data": {"drip_enabled": result}}
    except Exception as e:
        logger.exception("Error toggling DRIP")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/ipo/upcoming")
async def get_upcoming_ipos(
    mock: bool = False,
    days: int = 30,
    tracker: IPOTracker = Depends(get_ipo_tracker)
):
    """
    Retrieve upcoming IPOs with analysis.
    """
    try:
        if mock:
            tracker.finnhub.mock = True
            
        analysis = await tracker.get_upcoming_analysis(days)
        return {"success": True, "data": [a.model_dump() if hasattr(a, 'model_dump') else a for a in analysis]}
    except Exception as e:
        logger.exception("Error getting IPOs")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
