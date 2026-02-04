"""
==============================================================================
FILE: web/api/venmo_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes Venmo payment capabilities to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging

from services.payments.venmo_service import get_venmo_client


def get_venmo_provider(mock: bool = Query(True)):
    return get_venmo_client(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/venmo", tags=["Venmo"])


class VenmoPaymentRequest(BaseModel):
    amount: float = 29.00


@router.post("/payment/venmo/pay")
async def pay(
    request: VenmoPaymentRequest,
    client=Depends(get_venmo_provider)
):
    """
    Process Venmo payment.
    Body: { "amount": 29.00 }
    Query: ?mock=true
    """
    # In real app, we might get username from session
    username = "mock_user_123"

    try:
        data = await client.process_payment(request.amount, username)
        return {"success": True, "data": data}
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to process Venmo payment: %s", e)
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
