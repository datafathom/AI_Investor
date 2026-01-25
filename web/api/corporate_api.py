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

@router.get("/earnings", response_model=List[EarningsResponse])
async def get_earnings(
    days: int = 30,
    service: CorporateService = Depends(get_corporate_service)
):
    earnings = await service.get_earnings_calendar(days)
    return [EarningsResponse(
        ticker=e.ticker,
        date=e.date,
        time=e.time,
        estimated_eps=e.estimated_eps,
        estimated_revenue=e.estimated_revenue
    ) for e in earnings]

@router.get("/actions", response_model=List[ActionResponse])
async def list_actions(
    service: CorporateService = Depends(get_corporate_service)
):
    actions = await service.get_corporate_actions()
    return [ActionResponse(
        ticker=a.ticker,
        type=a.type,
        ex_date=a.ex_date,
        details=a.details
    ) for a in actions]

@router.post("/drip")
async def toggle_drip(
    enabled: bool,
    service: CorporateService = Depends(get_corporate_service)
):
    result = await service.toggle_drip(enabled)
    return {"status": "success", "drip_enabled": result}

@router.get("/ipo/upcoming", response_model=List[IPOAnalysis])
async def get_upcoming_ipos(
    mock: bool = False,
    days: int = 30,
    tracker: IPOTracker = Depends(get_ipo_tracker)
):
    """
    Retrieve upcoming IPOs with analysis.
    """
    if mock:
        tracker.finnhub.mock = True
        
    analysis = await tracker.get_upcoming_analysis(days)
    return analysis
