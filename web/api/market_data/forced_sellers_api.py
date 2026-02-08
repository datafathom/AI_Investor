"""
==============================================================================
FILE: web/api/market_data/forced_sellers_api.py
ROLE: API Endpoints for Forced Seller Risk Analysis
PURPOSE: Exposes endpoints for fragility scores, heatmaps, and liquidity traps.
==============================================================================
"""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException

from services.market_data.forced_seller_svc import (
    get_forced_seller_service,
    ForcedSellerService
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Market Data", "Risk"])


@router.get("/", response_model=List[Dict[str, Any]])
async def list_forced_seller_risks(
    limit: int = 10,
    service: ForcedSellerService = Depends(get_forced_seller_service)
):
    """List top tickers by fragility score."""
    return service.get_top_fragile_tickers(limit=limit)


@router.get("/heatmap", response_model=List[Dict[str, Any]])
async def get_passive_heatmap(
    service: ForcedSellerService = Depends(get_forced_seller_service)
):
    """Returns passive ownership data aggregated by sector."""
    return service.get_passive_heatmap()


@router.get("/liquidity-traps", response_model=List[Dict[str, Any]])
async def get_liquidity_traps(
    service: ForcedSellerService = Depends(get_forced_seller_service)
):
    """Returns active liquidity traps where bid-ask spread > 2.5x."""
    return service.get_liquidity_traps()


@router.get("/fragility/{ticker}", response_model=Dict[str, Any])
async def get_ticker_fragility(
    ticker: str,
    service: ForcedSellerService = Depends(get_forced_seller_service)
):
    """Get detailed fragility score for a specific ticker."""
    return service.calculate_fragility_score(ticker.upper())
