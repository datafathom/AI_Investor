"""
==============================================================================
FILE: web/api/square_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes Square merchant capabilities to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
import logging

from services.payments.square_service import get_square_client


def get_square_provider(mock: bool = Query(True)):
    return get_square_client(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/square", tags=["Square"])


@router.get("/merchant/square/stats")
async def get_stats(client=Depends(get_square_provider)):
    """Get merchant stats."""
    try:
        data = await client.get_merchant_stats()
        return {"success": True, "data": data}
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to fetch Square stats: %s", e)
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/merchant/square/catalog")
async def get_catalog(client=Depends(get_square_provider)):
    """Get merchant catalog."""
    try:
        data = await client.get_catalog()
        return {"success": True, "data": data}
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to fetch Square catalog: %s", e)
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/stats")
async def get_stats_v1(
    range_type: str = Query("daily", alias="range", description="daily|weekly|monthly"),
    client=Depends(get_square_provider)
):
    """Get merchant stats (v1 API)."""
    try:
        data = await client.get_merchant_stats()
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Failed to fetch Square stats")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/transactions")
async def get_transactions(
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD"),
    location_id: Optional[str] = Query(None),
    client=Depends(get_square_provider)
):
    """Get transaction history."""

    try:
        start = None
        end = None
        
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        transactions = await client.get_transactions(
            start_date=start,
            end_date=end,
            location_id=location_id
        )
        
        return {
            "success": True,
            "data": {
                "transactions": transactions,
                "count": len(transactions)
            }
        }
    except (ValueError, KeyError, RuntimeError) as e:
        logger.exception("Failed to get transactions")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/refunds")
async def get_refunds(
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD"),
    client=Depends(get_square_provider)
):
    """Get refund history."""

    try:
        start = None
        end = None
        
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        refunds = await client.get_refunds(
            start_date=start,
            end_date=end
        )
        
        return {
            "success": True,
            "data": {
                "refunds": refunds,
                "count": len(refunds)
            }
        }
    except (ValueError, KeyError, RuntimeError) as e:
        logger.exception("Failed to get refunds")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})