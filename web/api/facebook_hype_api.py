"""
==============================================================================
FILE: web/api/facebook_hype_api.py
ROLE: Facebook Hype API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for monitoring Facebook pages for stock mentions.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Header, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/facebook_hype", tags=["Facebook Hype"])


def get_facebook_hype_provider():
    from services.social.facebook_hype_service import get_facebook_hype_service
    return get_facebook_hype_service()


class MonitorPageRequest(BaseModel):
    page_id: str
    tickers: Optional[List[str]] = None
    access_token: Optional[str] = None


class CheckSpikeRequest(BaseModel):
    page_id: str
    ticker: str
    threshold_multiplier: float = 2.0


def _get_access_token(authorization: Optional[str], body_token: Optional[str]):
    """Helper to get access token from header or body."""
    if authorization and authorization.startswith('Bearer '):
        return authorization[7:]
    return body_token


@router.post("/monitor")
async def monitor_page(
    request: MonitorPageRequest,
    authorization: Optional[str] = Header(None)
):
    """Monitor a Facebook page for stock ticker mentions."""
    try:
        access_token = _get_access_token(authorization, request.access_token)
        
        if not access_token:
            raise HTTPException(status_code=401, detail="Missing Facebook access token")
        
        from services.social.facebook_hype_service import get_facebook_hype_service
        hype_service = get_facebook_hype_service()
        
        result = await hype_service.monitor_page(
            page_id=request.page_id,
            access_token=access_token,
            tickers=request.tickers
        )
        
        return {"success": True, "data": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Page monitoring failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/aggregates")
async def get_aggregates(
    page_id: Optional[str] = Query(None),
    ticker: Optional[str] = Query(None)
):
    """Get hourly aggregated mention counts."""
    try:
        from services.social.facebook_hype_service import get_facebook_hype_service
        hype_service = get_facebook_hype_service()
        
        result = await hype_service.get_hourly_aggregates(
            page_id=page_id,
            ticker=ticker
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to get aggregates")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/check-spike")
async def check_spike(request: CheckSpikeRequest):
    """Check if mention count has spiked above threshold."""
    try:
        from services.social.facebook_hype_service import get_facebook_hype_service
        hype_service = get_facebook_hype_service()
        
        result = await hype_service.check_for_spikes(
            page_id=request.page_id,
            ticker=request.ticker,
            threshold_multiplier=request.threshold_multiplier
        )
        
        if result:
            return {
                "success": True,
                "data": {
                    "spike_detected": True,
                    "alert": result
                }
            }
        else:
            return {
                "success": True,
                "data": {
                    "spike_detected": False
                }
            }
    except Exception as e:
        logger.exception("Spike check failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
