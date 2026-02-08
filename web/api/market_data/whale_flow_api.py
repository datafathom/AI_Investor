"""
==============================================================================
FILE: web/api/market_data/whale_flow_api.py
ROLE: API Endpoints for Whale Flow Analysis
PURPOSE: Exposes endpoints for 13F filings, crowding, and holder details.
==============================================================================
"""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Depends

from services.market_data.whale_flow_service import (
    get_whale_flow_service,
    WhaleFlowService
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Market Data", "Institutional"])


@router.get("/", response_model=Dict[str, Any])
async def get_whale_flow_summary(
    service: WhaleFlowService = Depends(get_whale_flow_service)
):
    """Get summary of recent whale activity."""
    return service.get_whale_flow_summary()


@router.get("/filings", response_model=List[Dict[str, Any]])
async def get_recent_filings(
    limit: int = 20,
    service: WhaleFlowService = Depends(get_whale_flow_service)
):
    """Get recent 13F filings."""
    return service.get_recent_filings(limit=limit)


@router.get("/crowding", response_model=List[Dict[str, Any]])
async def get_sector_crowding(
    service: WhaleFlowService = Depends(get_whale_flow_service)
):
    """Analyze sector crowding from institutional positions."""
    return service.get_sector_crowding()


@router.get("/holders/{holder_name}", response_model=Dict[str, Any])
async def get_holder_details(
    holder_name: str,
    service: WhaleFlowService = Depends(get_whale_flow_service)
):
    """Get detailed holdings for a specific holder."""
    return service.get_holder_details(holder_name)


@router.get("/ticker/{ticker}", response_model=Dict[str, Any])
async def get_ticker_whale_activity(
    ticker: str,
    service: WhaleFlowService = Depends(get_whale_flow_service)
):
    """Get whale activity for a specific ticker."""
    return service.get_ticker_whale_activity(ticker)
