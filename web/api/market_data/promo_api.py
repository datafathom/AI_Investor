"""
==============================================================================
FILE: web/api/market_data/promo_api.py
ROLE: API Endpoints for Volume Promo Spike Detection
PURPOSE: Exposes endpoints for promo spikes, volume baselines, and history.
==============================================================================
"""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Depends

from services.market_data.volume_monitor import (
    get_volume_monitor,
    VolumeMonitor
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Market Data", "Volume"])


@router.get("/", response_model=List[Dict[str, Any]])
async def get_promo_spikes(
    monitor: VolumeMonitor = Depends(get_volume_monitor)
):
    """Get current promo spike detections."""
    return monitor.get_promo_spikes()


@router.get("/baseline/{ticker}", response_model=Dict[str, Any])
async def get_volume_baseline(
    ticker: str,
    monitor: VolumeMonitor = Depends(get_volume_monitor)
):
    """Get volume baseline for a specific ticker."""
    return monitor.get_volume_baseline(ticker)


@router.get("/history/{ticker}", response_model=List[Dict[str, Any]])
async def get_ticker_promo_history(
    ticker: str,
    days: int = 30,
    monitor: VolumeMonitor = Depends(get_volume_monitor)
):
    """Get historical promo events for a ticker."""
    return monitor.get_ticker_promo_history(ticker, days=days)
