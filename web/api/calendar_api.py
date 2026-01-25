"""
==============================================================================
FILE: web/api/calendar_api.py
ROLE: Google Calendar API REST Endpoints
PURPOSE: RESTful endpoints for managing calendar events and syncing earnings.

INTEGRATION POINTS:
    - GoogleCalendarService: Event management
    - EarningsSyncService: Earnings calendar sync

ENDPOINTS:
    POST /api/v1/calendar/events - Create calendar event
    GET /api/v1/calendar/events - List calendar events
    PUT /api/v1/calendar/events/{id} - Update event
    DELETE /api/v1/calendar/events/{id} - Delete event
    POST /api/v1/calendar/sync/earnings - Sync earnings calendar

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/v1/calendar')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def _get_user_id():
    """Get current user ID from session/token."""
    return request.headers.get('X-User-ID', 'demo-user')


def _get_access_token():
    """Get Google access token from request."""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    data = request.json or {}
    return data.get('access_token')


# =============================================================================
# Create Event Endpoint
# =============================================================================

@calendar_bp.route('/events', methods=['POST'])
def create_event():
    """
    Create calendar event.
    
    Request Body:
        {
            "title": "Event Title",
            "description": "Event Description",
            "start_time": "2026-01-22T09:30:00",
            "end_time": "2026-01-22T10:30:00",  // optional
            "location": "Location",  // optional
            "event_type": "earnings",  // earnings, dividend, rebalance
            "access_token": "google_access_token"
        }
        
    Returns:
        JSON with event_id and details
    """
    try:
        data = request.json or {}
        
        title = data.get('title')
        description = data.get('description', '')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        location = data.get('location')
        event_type = data.get('event_type', 'default')
        access_token = _get_access_token()
        
        if not title or not start_time_str:
            return jsonify({
                "error": "Missing required fields: title, start_time"
            }), 400
        
        if not access_token:
            return jsonify({
                "error": "Missing Google access token"
            }), 401
        
        # Parse datetime
        try:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00')) if end_time_str else None
        except Exception as e:
            return jsonify({
                "error": f"Invalid datetime format: {str(e)}"
            }), 400
        
        from services.calendar.google_calendar_service import get_calendar_service
        calendar_service = get_calendar_service()
        
        result = _run_async(calendar_service.create_event(
            access_token=access_token,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            event_type=event_type
        ))
        
        return jsonify({
            "success": True,
            "event": result
        }), 201
        
    except Exception as e:
        logger.error(f"Create event failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to create event",
            "message": str(e)
        }), 500


# =============================================================================
# List Events Endpoint
# =============================================================================

@calendar_bp.route('/events', methods=['GET'])
def list_events():
    """
    List calendar events.
    
    Query Params:
        start_time: Start of time range (ISO format)
        end_time: End of time range (ISO format)
        max_results: Maximum events to return (default 50)
        
    Returns:
        JSON array of events
    """
    try:
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')
        max_results = int(request.args.get('max_results', 50))
        access_token = _get_access_token()
        
        if not access_token:
            return jsonify({
                "error": "Missing Google access token"
            }), 401
        
        start_time = None
        end_time = None
        
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        if end_time_str:
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        
        from services.calendar.google_calendar_service import get_calendar_service
        calendar_service = get_calendar_service()
        
        events = _run_async(calendar_service.list_events(
            access_token=access_token,
            start_time=start_time,
            end_time=end_time,
            max_results=max_results
        ))
        
        return jsonify({
            "events": events,
            "count": len(events)
        })
        
    except Exception as e:
        logger.error(f"List events failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to list events",
            "message": str(e)
        }), 500


# =============================================================================
# Update Event Endpoint
# =============================================================================

@calendar_bp.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id: str):
    """
    Update calendar event.
    
    Request Body:
        {
            "title": "New Title",  // optional
            "description": "New Description",  // optional
            "start_time": "2026-01-22T09:30:00",  // optional
            "end_time": "2026-01-22T10:30:00",  // optional
            "location": "New Location",  // optional
            "access_token": "google_access_token"
        }
        
    Returns:
        JSON with updated event details
    """
    try:
        data = request.json or {}
        access_token = _get_access_token()
        
        if not access_token:
            return jsonify({
                "error": "Missing Google access token"
            }), 401
        
        # Parse datetime if provided
        start_time = None
        end_time = None
        
        if data.get('start_time'):
            start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
        if data.get('end_time'):
            end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
        
        from services.calendar.google_calendar_service import get_calendar_service
        calendar_service = get_calendar_service()
        
        result = _run_async(calendar_service.update_event(
            access_token=access_token,
            event_id=event_id,
            title=data.get('title'),
            description=data.get('description'),
            start_time=start_time,
            end_time=end_time,
            location=data.get('location')
        ))
        
        return jsonify({
            "success": True,
            "event": result
        })
        
    except Exception as e:
        logger.error(f"Update event failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to update event",
            "message": str(e)
        }), 500


# =============================================================================
# Delete Event Endpoint
# =============================================================================

@calendar_bp.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id: str):
    """
    Delete calendar event.
    
    Returns:
        JSON confirmation
    """
    try:
        access_token = _get_access_token()
        
        if not access_token:
            return jsonify({
                "error": "Missing Google access token"
            }), 401
        
        from services.calendar.google_calendar_service import get_calendar_service
        calendar_service = get_calendar_service()
        
        deleted = _run_async(calendar_service.delete_event(
            access_token=access_token,
            event_id=event_id
        ))
        
        if deleted:
            return jsonify({
                "success": True,
                "message": "Event deleted"
            })
        else:
            return jsonify({
                "error": "Event not found"
            }), 404
        
    except Exception as e:
        logger.error(f"Delete event failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to delete event",
            "message": str(e)
        }), 500


# =============================================================================
# Sync Earnings Endpoint
# =============================================================================

@calendar_bp.route('/sync/earnings', methods=['POST'])
def sync_earnings():
    """
    Sync earnings calendar for user's holdings.
    
    Request Body:
        {
            "holdings": ["AAPL", "MSFT", ...],  // optional, defaults to user's portfolio
            "days_ahead": 90,  // optional
            "access_token": "google_access_token"
        }
        
    Returns:
        JSON with sync statistics
    """
    try:
        data = request.json or {}
        user_id = _get_user_id()
        access_token = _get_access_token()
        
        if not access_token:
            return jsonify({
                "error": "Missing Google access token"
            }), 401
        
        holdings = data.get('holdings', [])
        days_ahead = int(data.get('days_ahead', 90))
        
        # If no holdings provided, get from user's portfolio
        if not holdings:
            # TODO: Fetch from PortfolioService
            holdings = ["AAPL", "MSFT", "GOOGL"]  # Mock for now
        
        from services.calendar.earnings_sync import get_earnings_sync_service
        sync_service = get_earnings_sync_service()
        
        result = _run_async(sync_service.sync_earnings_for_user(
            user_id=user_id,
            access_token=access_token,
            holdings=holdings,
            days_ahead=days_ahead
        ))
        
        return jsonify({
            "success": True,
            "sync_result": result
        })
        
    except Exception as e:
        logger.error(f"Earnings sync failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to sync earnings",
            "message": str(e)
        }), 500
