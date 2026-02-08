"""
==============================================================================
FILE: web/api/indicators_api.py
ROLE: API Endpoints for Technical Indicators
PURPOSE: Exposes endpoints for indicator library, calculation, and custom creation.
==============================================================================
"""

import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.indicators.indicator_engine import (
    get_indicator_engine,
    IndicatorEngine
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/indicators", tags=["Indicators"])


class CalculateRequest(BaseModel):
    ticker: str
    indicator: str
    params: Dict[str, Any] = {}
    period: str = "1M"


class CustomIndicatorRequest(BaseModel):
    name: str
    formula: str
    params: List[Dict] = []


@router.get("", response_model=List[Dict[str, Any]])
async def list_indicators(
    engine: IndicatorEngine = Depends(get_indicator_engine)
):
    """List all available technical indicators."""
    return engine.list_indicators()


@router.get("/{indicator_id}", response_model=Dict[str, Any])
async def get_indicator_details(
    indicator_id: str,
    engine: IndicatorEngine = Depends(get_indicator_engine)
):
    """Get details for a specific indicator."""
    result = engine.get_indicator_details(indicator_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Indicator '{indicator_id}' not found")
    return result


@router.post("/calculate", response_model=Dict[str, Any])
async def calculate_indicator(
    request: CalculateRequest,
    engine: IndicatorEngine = Depends(get_indicator_engine)
):
    """Calculate indicator values for a ticker."""
    return engine.calculate_indicator(
        ticker=request.ticker,
        indicator_id=request.indicator,
        params=request.params,
        period=request.period
    )


@router.post("/custom", response_model=Dict[str, Any])
async def create_custom_indicator(
    request: CustomIndicatorRequest,
    engine: IndicatorEngine = Depends(get_indicator_engine)
):
    """Create a custom indicator."""
    return engine.create_custom_indicator(
        name=request.name,
        formula=request.formula,
        params=request.params
    )


@router.get("/custom", response_model=List[Dict[str, Any]])
async def list_custom_indicators(
    engine: IndicatorEngine = Depends(get_indicator_engine)
):
    """List all custom indicators."""
    return engine.list_custom_indicators()
