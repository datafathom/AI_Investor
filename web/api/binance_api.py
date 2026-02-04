"""
==============================================================================
FILE: web/api/binance_api.py
ROLE: REST API for Binance Data (FastAPI)
PURPOSE: Exposes Binance Service functionality to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Path, Body, Depends
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict, Any

from services.data.binance_service import get_binance_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/binance", tags=["Binance"])

# TODO: Get mock status from config/env
MOCK_MODE = True 

def get_binance_service():
    """Dependency for getting the binance client."""
    return get_binance_client(mock=MOCK_MODE)


class OrderRequest(BaseModel):
    symbol: str
    side: str
    quantity: float
    price: Optional[float] = None


@router.get("/ticker/{symbol}")
async def get_ticker(
    symbol: str = Path(...),
    client = Depends(get_binance_service)
):
    """Get 24hr ticker price change statistics."""
    try:
        data = await client.get_ticker(symbol.upper())
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception(f"Error getting ticker for {symbol}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/depth/{symbol}")
async def get_order_book(
    symbol: str = Path(...),
    limit: int = Query(5, ge=1, le=500),
    client = Depends(get_binance_service)
):
    """Get order book depth."""
    try:
        data = await client.get_order_book(symbol.upper(), limit=limit)
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception(f"Error getting order book for {symbol}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/order")
async def place_order(
    request_data: OrderRequest,
    client = Depends(get_binance_service)
):
    """Place a new order."""
    try:
        result = await client.place_order(
            request_data.symbol.upper(), 
            request_data.side, 
            request_data.quantity, 
            request_data.price
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Error placing order")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
