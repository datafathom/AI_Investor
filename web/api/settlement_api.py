"""
Settlement API - FastAPI Router
 (web/api/settlement_api.py)
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Any
import logging

from services.brokerage.settlement_service import get_settlement_service
from services.system.cache_service import get_cache_service


def get_settlement_provider():
    return get_settlement_service()


def get_cache_provider():
    return get_cache_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/settlement", tags=["Settlement"])

@router.get("/balances")
async def get_balances(service=Depends(get_settlement_provider)):
    """Retrieve settlement balance summary."""
    try:
        data = service.get_balance_summary()
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Failed to fetch balances")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/rates")
async def get_rates(
    service=Depends(get_settlement_provider),
    cache=Depends(get_cache_provider)
):
    """Retrieve current currency conversion rates."""
    try:
        cache_key = "settlement:rates"
        cached_rates = cache.get(cache_key)
        if cached_rates:
            return {"success": True, "data": cached_rates}
            
        rates = service.get_rates()
        
        # Cache for 60 seconds
        cache.set(cache_key, rates, ttl=60)
        return {"success": True, "data": rates}
    except Exception as e:
        logger.exception("Failed to fetch rates")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post("/convert")
async def convert_currency(
    data: Dict[str, Any] = Body(...),
    service=Depends(get_settlement_provider)
):
    try:
        from_curr = data.get('from')
        to_curr = data.get('to')
        amount = data.get('amount')
        
        if not from_curr or not to_curr or amount is None:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Missing conversion parameters"})
            
        result = service.convert_currency(from_curr, to_curr, float(amount))
        
        if result.get('status') == 'ERROR':
            return JSONResponse(status_code=400, content={"success": False, "detail": result.get('message', 'Conversion failed')})
            
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Currency conversion failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

