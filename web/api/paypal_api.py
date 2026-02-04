"""
==============================================================================
FILE: web/api/paypal_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes PayPal payment capabilities to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

from services.payments.paypal_service import get_paypal_client


def get_paypal_provider(mock: bool = True):
    return get_paypal_client(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/paypal", tags=["PayPal"])


class CreateOrderRequest(BaseModel):
    amount: float = 29.00
    currency: str = "USD"


class CaptureOrderRequest(BaseModel):
    order_id: str


@router.post("/payment/paypal/create-order")
async def create_order(
    request: CreateOrderRequest,
    client=Depends(get_paypal_provider)
):
    """
    Create a PayPal order.
    Body: { "amount": 29.00, "currency": "USD" }
    """
    
    try:
        result = await client.create_order(request.amount, request.currency)
        return {"success": True, "data": result}
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to create PayPal order: %s", e)
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/payment/paypal/capture-order")
async def capture_order(
    request: CaptureOrderRequest,
    client=Depends(get_paypal_provider)
):
    """
    Capture a PayPal order.
    Body: { "order_id": "PAYPAL_..." }
    """
    if not request.order_id:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Order ID required"})
    
    try:
        result = await client.capture_order(request.order_id)
        return {"success": True, "data": result}
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to capture PayPal order: %s", e)
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
