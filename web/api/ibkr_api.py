"""
==============================================================================
FILE: web/api/ibkr_api.py
ROLE: Interactive Brokers API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for IBKR account management and order execution.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Body, Path, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict, Any

from services.brokerage.ibkr_client import get_ibkr_client
from services.brokerage.ibkr_gateway_manager import get_ibkr_gateway


def get_ibkr_client_provider():
    return get_ibkr_client()


def get_ibkr_gateway_provider():
    return get_ibkr_gateway()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ibkr", tags=["IBKR"])


class OrderRequest(BaseModel):
    contract: str
    action: str
    quantity: float
    order_type: str = "MKT"
    price: Optional[float] = None
    account_id: Optional[str] = None


@router.get("/account-summary")
async def get_account_summary(
    account_id: Optional[str] = Query(None),
    client = Depends(get_ibkr_client_provider)
):
    """Get comprehensive account summary."""
    try:
        if not client.connected:
            await client.connect()
        
        summary = await client.get_account_summary()
        return {"success": True, "data": summary}
    except Exception as e:
        logger.exception("Failed to get account summary")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/positions")
async def get_positions(client = Depends(get_ibkr_client_provider)):
    """Get all open positions across asset classes."""
    try:
        if not client.connected:
            await client.connect()
        
        positions = await client.get_positions()
        return {
            "success": True,
            "data": {
                "positions": positions,
                "count": len(positions)
            }
        }
    except Exception as e:
        logger.exception("Failed to get positions")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/orders")
async def get_orders(
    account_id: Optional[str] = Query(None),
    client = Depends(get_ibkr_client_provider)
):
    """Get order history."""
    try:
        if not client.connected:
            await client.connect()
        
        orders = await client.get_orders(account_id=account_id)
        return {
            "success": True,
            "data": {
                "orders": orders,
                "count": len(orders)
            }
        }
    except Exception as e:
        logger.exception("Failed to get orders")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/orders", status_code=201)
async def place_order(
    request: OrderRequest,
    client = Depends(get_ibkr_client_provider)
):
    """Place an order."""
    try:
        if not client.connected:
            await client.connect()
        
        result = await client.place_order(
            contract=request.contract,
            action=request.action,
            quantity=request.quantity,
            order_type=request.order_type,
            price=request.price,
            account_id=request.account_id
        )
        
        return {
            "success": True,
            "data": {
                "order": result
            }
        }
    except Exception as e:
        logger.exception("Failed to place order")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.delete("/orders/{order_id}")
async def cancel_order(
    order_id: int = Path(...),
    client = Depends(get_ibkr_client_provider)
):
    """Cancel an order."""
    try:
        if not client.connected:
            await client.connect()
        
        cancelled = await client.cancel_order(order_id)
        
        if cancelled:
            return {
                "success": True,
                "data": {
                    "message": f"Order {order_id} cancelled"
                }
            }
        else:
            return JSONResponse(status_code=500, content={"success": False, "detail": "Failed to cancel order"})
    except Exception as e:
        logger.exception("Failed to cancel order")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/margin")
async def get_margin(
    account_id: Optional[str] = Query(None),
    client = Depends(get_ibkr_client_provider)
):
    """Get margin requirements and utilization."""
    try:
        if not client.connected:
            await client.connect()
        
        margin = await client.get_margin_requirements(account_id=account_id)
        return {"success": True, "data": margin}
    except Exception as e:
        logger.exception("Failed to get margin")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/currency-exposure")
async def get_currency_exposure(
    account_id: Optional[str] = Query(None),
    client = Depends(get_ibkr_client_provider)
):
    """Get currency exposure across all positions."""
    try:
        if not client.connected:
            await client.connect()
        
        exposure = await client.get_currency_exposure(account_id=account_id)
        return {
            "success": True,
            "data": {
                "currency_exposure": exposure
            }
        }
    except Exception as e:
        logger.exception("Failed to get currency exposure")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/gateway/status")
async def get_gateway_status(
    gateway = Depends(get_ibkr_gateway_provider)
):
    """Get IBKR Gateway status."""
    try:
        status = await gateway.get_session_status()
        return {"success": True, "data": status}
    except Exception as e:
        logger.exception("Failed to get gateway status")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
