"""
==============================================================================
FILE: web/api/stripe_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes Billing/Stripe capabilities to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import logging

from services.payments.stripe_service import get_stripe_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/stripe", tags=["Stripe"])


class CheckoutRequest(BaseModel):
    plan_id: str


@router.get("/billing/subscription")
async def get_subscription(mock: bool = Query(True, description="Use mock mode")):
    """
    Get current user subscription.
    Query: ?mock=true
    """
    # In a real app, we'd get user_id from session/token
    user_id = "user_mock_123"
    
    client = get_stripe_client(mock=mock)
    
    try:
        result = await client.get_subscription(user_id)
        return result
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to fetch subscription: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/billing/checkout")
async def create_checkout(
    request: CheckoutRequest,
    mock: bool = Query(True, description="Use mock mode")
):
    """
    Create a checkout session.
    Body: { "plan_id": "price_pro_monthly" }
    """
    user_id = "user_mock_123"

    if not request.plan_id:
        raise HTTPException(status_code=400, detail="Plan ID required")
        
    client = get_stripe_client(mock=mock)
    
    try:
        result = await client.create_checkout_session(user_id, request.plan_id)
        return result
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to create checkout: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
