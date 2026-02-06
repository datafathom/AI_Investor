"""
Politics API - FastAPI Router
 (web/api/politics_api.py)
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Any
import logging

from services.analysis.congress_tracker import get_congress_tracker


def get_congress_provider():
    return get_congress_tracker()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/politics", tags=["Politics"])

@router.get("/disclosures")
async def get_disclosures(service=Depends(get_congress_provider)):
    """Fetch latest congressional trades."""
    try:
        disclosures = service.fetch_latest_disclosures()
        return {
            "success": True,
            "data": {
                "count": len(disclosures),
                "disclosures": disclosures
            }
        }
    except Exception as e:
        logger.exception("Failed to fetch disclosures")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/alpha/{ticker}")
async def get_alpha_score(ticker: str, service=Depends(get_congress_provider)):
    """Get alpha score for a specific ticker."""
    try:
        score = service.get_political_alpha_signal(ticker)
        correlation = service.correlate_with_lobbying(ticker)
        
        return {
            "success": True,
            "data": {
                "ticker": ticker,
                "alpha_score": score,
                "lobbying_intensity": correlation["lobbying_intensity"],
                "confidence": correlation["confidence"]
            }
        }
    except Exception as e:
        logger.exception(f"Failed to fetch alpha score for {ticker}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

