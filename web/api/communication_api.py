"""
==============================================================================
FILE: web/api/communication_api.py
ROLE: Communication Gateway (FastAPI)
PURPOSE: Expose Notification and Personalization services to the frontend.
==============================================================================
"""

import logging
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from services.analysis.morning_briefing import get_briefing_service as _get_briefing_service
from services.communication.notification_manager import get_notification_manager as _get_notification_manager, AlertPriority

from fastapi import APIRouter, HTTPException, Query, Body, Depends

def get_briefing_provider():
    """Dependency for getting the briefing service."""
    return _get_briefing_service()

def get_notification_provider():
    """Dependency for getting the notification manager."""
    return _get_notification_manager()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/communication", tags=["Communication"])


class TestAlertRequest(BaseModel):
    message: str = "Test Alert from Dashboard"
    priority: str = "INFO"


@router.get("/briefing")
async def get_morning_briefing(
    name: str = Query("Commander"),
    value: float = Query(100000.0),
    fear: float = Query(50.0),
    sentiment: str = Query("NEUTRAL"),
    service = Depends(get_briefing_provider)
):
    """ Get the personalized morning briefing. """
    try:
        report = service.generate_briefing(name, value, fear, sentiment)
        
        return {
            "success": True,
            "data": {
                "briefing_text": report,
                "meta": {
                    "fear_used": fear,
                    "sentiment_used": sentiment
                }
            }
        }
    except Exception as e:
        logger.exception("Failed to generate briefing")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/test-alert")
async def trigger_test_alert(
    request: TestAlertRequest,
    manager = Depends(get_notification_provider)
):
    """ Trigger a test alert to verify notification channels. """
    try:
        priority_str = request.priority.upper()
        try:
            priority = AlertPriority[priority_str]
        except KeyError:
            priority = AlertPriority.INFO
            
        manager.send_alert(request.message, priority)
        
        return {
            "success": True,
            "data": {
                "status": "sent",
                "channel_count": len(manager.history[-1]['channels']),
                "channels": manager.history[-1]['channels']
            }
        }
    except Exception as e:
        logger.exception("Failed to send test alert")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
