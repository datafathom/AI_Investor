"""
==============================================================================
FILE: web/api/market/regime_api.py
ROLE: API Endpoints for Market Regime Classification
PURPOSE: Exposes endpoints for current regime, history, and forecasts.
==============================================================================
"""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Depends

from services.market.regime_classifier import (
    get_regime_classifier,
    MarketRegimeClassifier
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/regime", tags=["Market", "Analysis"])


@router.get("", response_model=Dict[str, Any])
async def get_current_regime(
    classifier: MarketRegimeClassifier = Depends(get_regime_classifier)
):
    """Get the current market regime classification."""
    return classifier.get_current_regime()


@router.get("/history", response_model=List[Dict[str, Any]])
async def get_regime_history(
    days: int = 180,
    classifier: MarketRegimeClassifier = Depends(get_regime_classifier)
):
    """Get historical market regimes."""
    return classifier.get_regime_history(days=days)


@router.get("/forecast", response_model=Dict[str, Any])
async def get_regime_forecast(
    classifier: MarketRegimeClassifier = Depends(get_regime_classifier)
):
    """Get forecasted market regime."""
    return classifier.get_regime_forecast()
