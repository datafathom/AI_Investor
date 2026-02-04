"""
==============================================================================
FILE: web/api/crypto_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes real-time crypto prices and volume data.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
import logging

from services.data.crypto_compare_service import get_crypto_client as _get_crypto_client

def get_crypto_provider():
    return _get_crypto_client()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/market/crypto", tags=["Crypto"])


@router.get("/price")
async def get_crypto_price(
    symbols: str = Query("BTC,ETH", description="Comma-separated symbols"),
    currencies: str = Query("USD", description="Comma-separated currencies"),
    mock: bool = Query(False, description="Use mock mode"),
    service = Depends(get_crypto_provider)
):
    """
    Get real-time prices for multiple symbols.
    Query: ?symbols=BTC,ETH&currencies=USD,EUR&mock=false
    """
    symbol_list = symbols.split(',')
    currency_list = currencies.split(',')
    
    if mock:
        service.mock = True
        
    try:
        results = await service.get_price(symbol_list, currency_list)
        return {"success": True, "data": results}
    except Exception as e:
        logger.exception("Error fetching crypto prices")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/volume/{symbol}")
async def get_crypto_volume(
    symbol: str,
    mock: bool = Query(False, description="Use mock mode"),
    service = Depends(get_crypto_provider)
):
    """Get exchange volume data for a symbol."""
    if mock:
        service.mock = True
        
    try:
        results = await service.get_top_exchanges_volume(symbol)
        return {"success": True, "data": [r.model_dump() for r in results]}
    except Exception as e:
        logger.exception("Error fetching crypto volume for %s", symbol)
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
