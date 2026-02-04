"""
==============================================================================
FILE: web/api/ai_predictions_api.py
ROLE: AI Predictions API Endpoints (FastAPI)
PURPOSE: REST endpoints for price predictions and market forecasting.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from services.ai_predictions.prediction_engine import get_prediction_engine
from services.ai_predictions.ai_analytics_service import get_ai_analytics_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ai-predictions", tags=["AI Predictions"])

class PredictionRequest(BaseModel):
    symbol: str
    time_horizon: Optional[str] = "1m"
    model_version: Optional[str] = "v1.0"

class NewsImpactRequest(BaseModel):
    symbol: str
    news_sentiment: float = 0.0

@router.post("/price")
async def predict_price(
    request: PredictionRequest,
    engine = Depends(get_prediction_engine)
):
    """Predict future price."""
    try:
        prediction = await engine.predict_price(
            request.symbol, 
            request.time_horizon, 
            request.model_version
        )
        return {"success": True, "data": prediction.model_dump()}
    except Exception as e:
        logger.exception("Error predicting price")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trend")
async def predict_trend(
    request: PredictionRequest,
    engine = Depends(get_prediction_engine)
):
    """Predict price trend."""
    try:
        prediction = await engine.predict_trend(request.symbol, request.time_horizon)
        return {"success": True, "data": prediction.model_dump()}
    except Exception as e:
        logger.exception("Error predicting trend")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regime")
async def get_market_regime(
    market_index: str = "SPY",
    service = Depends(get_ai_analytics_service)
):
    """Detect current market regime."""
    try:
        regime = await service.detect_market_regime(market_index)
        return {"success": True, "data": regime.model_dump()}
    except Exception as e:
        logger.exception("Error detecting market regime")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/news-impact")
async def predict_news_impact(
    request: NewsImpactRequest,
    service = Depends(get_ai_analytics_service)
):
    """Predict market impact from news sentiment."""
    try:
        impact = await service.predict_news_impact(request.symbol, request.news_sentiment)
        return {"success": True, "data": impact}
    except Exception as e:
        logger.exception("Error predicting news impact")
        raise HTTPException(status_code=500, detail=str(e))
