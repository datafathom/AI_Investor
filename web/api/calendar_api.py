"""
==============================================================================
FILE: web/api/calendar_api.py
ROLE: Google Calendar API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for managing calendar events and syncing earnings.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Header, Query, Path, Body, Depends
from pydantic import BaseModel
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

from services.calendar.google_calendar_service import get_calendar_service as _get_calendar_service
from services.calendar.earnings_sync import get_earnings_sync_service as _get_earnings_sync_service

def get_calendar_service():
    """Dependency for getting the Google calendar service."""
    return _get_calendar_service()

def get_earnings_sync_service():
    """Dependency for getting the earnings sync service."""
    return _get_earnings_sync_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/calendar", tags=["Calendar"])


class CreateEventRequest(BaseModel):
    title: str
    description: str = ""
    start_time: str
    end_time: Optional[str] = None
    location: Optional[str] = None
    event_type: str = "default"
    access_token: Optional[str] = None


class UpdateEventRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    access_token: Optional[str] = None


class SyncEarningsRequest(BaseModel):
    holdings: Optional[List[str]] = None
    days_ahead: int = 90
    access_token: Optional[str] = None


def _get_access_token(authorization: Optional[str], body_token: Optional[str]):
    """Helper to get access token from header or body."""
    if authorization and authorization.startswith('Bearer '):
        return authorization[7:]
    return body_token


@router.post("/events")
async def create_event(
    request: CreateEventRequest,
    service = Depends(get_calendar_service),
    authorization: Optional[str] = Header(None)
):
    """Create calendar event."""
    try:
        access_token = _get_access_token(authorization, request.access_token)
        if not access_token:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=401, content={"success": False, "detail": "Missing Google access token"})
        
        # Parse datetime
        try:
            start_time = datetime.fromisoformat(request.start_time.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(request.end_time.replace('Z', '+00:00')) if request.end_time else None
        except Exception as e:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=400, content={"success": False, "detail": f"Invalid datetime format: {str(e)}"})
        
        result = await service.create_event(
            access_token=access_token,
            title=request.title,
            description=request.description,
            start_time=start_time,
            end_time=end_time,
            location=request.location,
            event_type=request.event_type
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Create event failed")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/events")
async def list_events(
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    max_results: int = Query(50, ge=1, le=250),
    service = Depends(get_calendar_service),
    authorization: Optional[str] = Header(None)
):
    """List calendar events."""
    try:
        access_token = _get_access_token(authorization, None)
        if not access_token:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=401, content={"success": False, "detail": "Missing Google access token"})
        
        t_start = None
        t_end = None
        if start_time:
            t_start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        if end_time:
            t_end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        events = await service.list_events(
            access_token=access_token,
            start_time=t_start,
            end_time=t_end,
            max_results=max_results
        )
        
        return {"success": True, "data": events, "count": len(events)}
    except Exception as e:
        logger.exception("List events failed")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.put("/events/{event_id}")
async def update_event(
    event_id: str = Path(...),
    request: UpdateEventRequest = Body(...),
    service = Depends(get_calendar_service),
    authorization: Optional[str] = Header(None)
):
    """Update calendar event."""
    try:
        access_token = _get_access_token(authorization, request.access_token)
        if not access_token:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=401, content={"success": False, "detail": "Missing Google access token"})
        
        t_start = None
        t_end = None
        if request.start_time:
            t_start = datetime.fromisoformat(request.start_time.replace('Z', '+00:00'))
        if request.end_time:
            t_end = datetime.fromisoformat(request.end_time.replace('Z', '+00:00'))
        
        result = await service.update_event(
            access_token=access_token,
            event_id=event_id,
            title=request.title,
            description=request.description,
            start_time=t_start,
            end_time=t_end,
            location=request.location
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Update event failed")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.delete("/events/{event_id}")
async def delete_event(
    event_id: str = Path(...),
    service = Depends(get_calendar_service),
    authorization: Optional[str] = Header(None)
):
    """Delete calendar event."""
    try:
        access_token = _get_access_token(authorization, None)
        if not access_token:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=401, content={"success": False, "detail": "Missing Google access token"})
        
        deleted = await service.delete_event(
            access_token=access_token,
            event_id=event_id
        )
        
        if deleted:
            return {"success": True, "data": {"message": "Event deleted"}}
        else:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=404, content={"success": False, "detail": "Event not found"})
    except Exception as e:
        logger.exception("Delete event failed")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/sync/earnings")
async def sync_earnings(
    request: SyncEarningsRequest,
    service = Depends(get_earnings_sync_service),
    authorization: Optional[str] = Header(None),
    x_user_id: str = Header("demo-user")
):
    """Sync earnings calendar for user's holdings."""
    try:
        access_token = _get_access_token(authorization, request.access_token)
        if not access_token:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=401, content={"success": False, "detail": "Missing Google access token"})
        
        holdings = request.holdings or ["AAPL", "MSFT", "GOOGL"]
        
        result = await service.sync_earnings_for_user(
            user_id=x_user_id,
            access_token=access_token,
            holdings=holdings,
            days_ahead=request.days_ahead
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Earnings sync failed")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
