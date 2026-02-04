"""
==============================================================================
FILE: web/api/robinhood_api.py
ROLE: Robinhood API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for Robinhood portfolio sync and connection management.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Header, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Any
import logging
import asyncio

from services.brokerage.robinhood_client import get_robinhood_client


def get_robinhood_provider():
    return get_robinhood_client()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/robinhood", tags=["Robinhood"])


class ConnectRequest(BaseModel):
    username: str
    password: str
    mfa_code: Optional[str] = None


@router.post("/connect")
async def connect_account(
    request: ConnectRequest,
    service=Depends(get_robinhood_provider)
):
    """
    Connect Robinhood account with credentials.
    """
    try:
        success = await service.login(request.username, request.password, request.mfa_code)
        
        if success:
            return {
                "success": True,
                "data": {
                    "message": "Robinhood account connected successfully",
                    "connected_at": asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0
                }
            }
        else:
            return JSONResponse(
                status_code=401, 
                content={"success": False, "detail": "Invalid credentials or MFA code"}
            )
            
    except Exception as e:
        logger.exception("Robinhood connection failed")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.get("/holdings")
async def get_holdings(service=Depends(get_robinhood_provider)):
    """Get portfolio holdings."""
    try:
        holdings = await service.get_holdings()
        
        return {
            "success": True,
            "data": {
                "holdings": holdings,
                "count": len(holdings)
            }
        }
    except Exception as e:
        logger.exception("Failed to get holdings")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.get("/orders")
async def get_orders(
    limit: int = Query(100, ge=1, le=500),
    service=Depends(get_robinhood_provider)
):
    """Get order history."""
    try:
        orders = await service.get_orders(limit=limit)
        
        return {
            "success": True,
            "data": {
                "orders": orders,
                "count": len(orders)
            }
        }
    except Exception as e:
        logger.exception("Failed to get orders")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.get("/transactions")
async def get_transactions(
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    service=Depends(get_robinhood_provider)
):
    """Get historical transactions for tax reporting."""
    try:
        transactions = await service.get_historical_transactions(
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            "success": True,
            "data": {
                "transactions": transactions,
                "count": len(transactions)
            }
        }
    except Exception as e:
        logger.exception("Failed to get transactions")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.get("/cost-basis")
async def calculate_cost_basis(
    symbol: str = Query(..., description="Stock or crypto symbol"),
    service=Depends(get_robinhood_provider)
):
    """Calculate cost basis and gains for a position."""
    try:
        result = await service.calculate_cost_basis(symbol)
        
        if "error" in result:
            return JSONResponse(status_code=404, content={"success": False, "detail": result.get("error")})
        
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to calculate cost basis")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )
