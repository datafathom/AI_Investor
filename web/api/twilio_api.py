"""
==============================================================================
FILE: web/api/twilio_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes Twilio SMS capabilities to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging

from services.notifications.twilio_service import get_twilio_client


def get_twilio_provider(mock: bool = Query(True)):
    return get_twilio_client(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/twilio", tags=["Twilio"])


class TwilioSMSRequest(BaseModel):
    to: str
    message: str


@router.post("/notifications/twilio/send")
async def send_alert(
    request: TwilioSMSRequest,
    client=Depends(get_twilio_provider)
):
    """
    Send a test SMS alert.
    Body: { "to": "+1555...", "message": "Test Alert" }
    """
    if not request.to or not request.message:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Missing 'to' or 'message'"})

    try:
        data = await client.send_sms(request.to, request.message)
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Failed to send SMS")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
