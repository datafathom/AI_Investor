"""
==============================================================================
FILE: web/api/credit_api.py
ROLE: Credit Monitoring API Endpoints (FastAPI)
PURPOSE: REST endpoints for credit score monitoring and improvement.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Path, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict, Any

from services.credit.credit_monitoring_service import get_credit_monitoring_service as _get_credit_monitoring_service
from services.credit.credit_improvement_service import get_credit_improvement_service as _get_credit_improvement_service

def get_credit_monitoring_provider():
    return _get_credit_monitoring_service()

def get_credit_improvement_provider():
    return _get_credit_improvement_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/credit", tags=["Credit"])


class TrackCreditScoreRequest(BaseModel):
    user_id: str
    score: int
    score_type: str = "fico"
    factors: Optional[Dict[str, float]] = None


class SimulateImprovementRequest(BaseModel):
    recommendations: List[str] = []


@router.post("/score/track")
async def track_credit_score(
    request: TrackCreditScoreRequest,
    service = Depends(get_credit_monitoring_provider)
):
    """Track credit score update."""
    try:
        if not request.user_id or not request.score:
            raise HTTPException(status_code=400, detail="user_id and score are required")
        
        credit_score = await service.track_credit_score(
            user_id=request.user_id,
            score=request.score,
            score_type=request.score_type,
            factors=request.factors
        )
        
        return {
            'success': True,
            'data': credit_score.model_dump()
        }
    except Exception as e:
        logger.exception("Error tracking credit score")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/score/history/{user_id}")
async def get_credit_history(
    user_id: str = Path(...),
    months: int = Query(12, ge=1, le=120),
    service = Depends(get_credit_monitoring_provider)
):
    """Get credit score history."""
    try:
        history = await service.get_credit_history(user_id, months)
        
        return {
            'success': True,
            'data': [h.model_dump() for h in history]
        }
    except Exception as e:
        logger.exception("Error getting credit history")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/factors/{user_id}")
async def get_credit_factors(
    user_id: str = Path(...),
    service = Depends(get_credit_monitoring_provider)
):
    """Analyze credit score factors."""
    try:
        factors = await service.analyze_credit_factors(user_id)
        
        return {
            'success': True,
            'data': factors
        }
    except Exception as e:
        logger.exception("Error analyzing credit factors")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/recommendations/{user_id}")
async def get_recommendations(
    user_id: str = Path(...),
    service = Depends(get_credit_improvement_provider)
):
    """Get credit improvement recommendations."""
    try:
        recommendations = await service.generate_recommendations(user_id)
        
        return {
            'success': True,
            'data': [r.model_dump() for r in recommendations]
        }
    except Exception as e:
        logger.exception("Error getting recommendations")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/simulate/{user_id}")
async def simulate_improvement(
    user_id: str = Path(...),
    request: SimulateImprovementRequest = Body(...),
    improvement_service = Depends(get_credit_improvement_provider)
):
    """Simulate credit score improvement."""
    try:
        all_recommendations = await improvement_service.generate_recommendations(user_id)
        
        if request.recommendations:
            recommendations = [r for r in all_recommendations if r.recommendation_id in request.recommendations]
        else:
            recommendations = all_recommendations
        
        projection = await improvement_service.simulate_score_improvement(
            user_id=user_id,
            recommendations=recommendations
        )
        
        return {
            'success': True,
            'data': projection.model_dump()
        }
    except Exception as e:
        logger.exception("Error simulating improvement")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
