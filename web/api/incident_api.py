"""
==============================================================================
FILE: web/api/incident_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes PagerDuty incident management to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

from services.notifications.pagerduty_service import get_pagerduty_client


def get_pagerduty_provider():
    # Note: the endpoint had a 'mock' query param that was passed to get_pagerduty_client.
    # We will keep that logic but use a provider for standard dependency injection.
    return get_pagerduty_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/incident", tags=["Incident"])


class TriggerIncidentRequest(BaseModel):
    title: str
    urgency: str = "high"


@router.post("/ops/incidents/trigger")
async def trigger_incident(
    request: TriggerIncidentRequest,
    mock: bool = Query(True, description="Use mock mode"),
    pagerduty_factory = Depends(get_pagerduty_provider)
):
    """
    Trigger an incident manually.
    Body: { "title": "System Down", "urgency": "high" }
    """
    if not request.title:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Missing 'title'"})

    client = pagerduty_factory(mock=mock)
    
    try:
        result = await client.trigger_incident(request.title, request.urgency)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to trigger incident")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/ops/incidents")
async def get_incidents(
    mock: bool = Query(True, description="Use mock mode"),
    pagerduty_factory = Depends(get_pagerduty_provider)
):
    """Get list of active incidents."""
    client = pagerduty_factory(mock=mock)
    
    try:
        result = await client.get_incidents()
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to fetch incidents")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
