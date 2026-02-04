"""
==============================================================================
FILE: web/api/email_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes Email capabilities to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from services.notifications.sendgrid_service import get_sendgrid_client as _get_sendgrid_client

def get_sendgrid_provider(mock: bool = True):
    return _get_sendgrid_client(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/email", tags=["Email"])


class SendEmailRequest(BaseModel):
    to: str
    subject: str = "Test Email"
    content: str = "This is a test email."


class SubscriptionRequest(BaseModel):
    email: str
    preferences: Dict[str, Any] = {}


@router.post("/notifications/email/send")
async def send_test_email(
    request: SendEmailRequest,
    mock: bool = Query(True, description="Use mock mode"),
    client = Depends(get_sendgrid_provider)
):
    """
    Send a test email.
    Body: { "to": "user@example.com", "subject": "Test", "content": "Hello" }
    """
    if not request.to:
        raise HTTPException(status_code=400, detail="Missing 'to' email address")
    
    try:
        result = await client.send_email(request.to, request.subject, request.content)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to send email")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/notifications/email/subscribe")
async def update_subscriptions(
    request: SubscriptionRequest,
    mock: bool = Query(True, description="Use mock mode"),
    client = Depends(get_sendgrid_provider)
):
    """
    Update email subscriptions.
    Body: { "email": "...", "preferences": { "daily": true, ... } }
    """
    if not request.email:
        raise HTTPException(status_code=400, detail="Missing 'email'")
    
    try:
        result = await client.update_subscriptions(request.email, request.preferences)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to update subscriptions")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
