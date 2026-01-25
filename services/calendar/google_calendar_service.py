"""
==============================================================================
FILE: services/calendar/google_calendar_service.py
ROLE: Google Calendar API Client Service
PURPOSE: Creates, updates, and deletes calendar events on user's Google Calendar.
         Used for earnings reminders, dividend dates, and rebalancing schedules.

INTEGRATION POINTS:
    - GoogleAuthService: Retrieves access tokens for Calendar API
    - EarningsSyncService: Syncs earnings calendar events
    - PortfolioService: Creates rebalancing reminders

SCOPES REQUIRED:
    - https://www.googleapis.com/auth/calendar

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.oauth2.credentials import Credentials
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    logger.warning("Google API client not installed. Install with: pip install google-api-python-client")


@dataclass
class CalendarEvent:
    """Calendar event data structure"""
    event_id: Optional[str] = None
    title: str = ""
    description: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    color_id: Optional[str] = None  # Google Calendar color ID
    reminders: Optional[List[Dict[str, Any]]] = None


class GoogleCalendarService:
    """
    Google Calendar API service for managing calendar events.
    """
    
    # Default reminder times (in minutes before event)
    DEFAULT_REMINDERS = [
        {"method": "email", "minutes": 1440},  # 1 day before
        {"method": "popup", "minutes": 60}    # 1 hour before
    ]
    
    # Color IDs for different event types
    COLOR_IDS = {
        "earnings": "9",      # Blue
        "dividend": "10",     # Green
        "rebalance": "5",     # Yellow
        "default": "1"        # Lavender
    }
    
    def __init__(self, mock: bool = False):
        """
        Initialize Google Calendar service.
        
        Args:
            mock: Use mock mode if True
        """
        self.mock = mock
    
    def _get_calendar_service(self, access_token: str):
        """
        Build Google Calendar API service client.
        
        Args:
            access_token: Google OAuth access token
            
        Returns:
            Calendar API service object
        """
        if self.mock or not GOOGLE_API_AVAILABLE:
            return None
        
        try:
            credentials = Credentials(token=access_token)
            service = build('calendar', 'v3', credentials=credentials)
            return service
        except Exception as e:
            logger.error(f"Failed to build Calendar service: {e}")
            raise
    
    async def create_event(
        self,
        access_token: str,
        title: str,
        description: str,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        location: Optional[str] = None,
        event_type: str = "default",
        reminders: Optional[List[Dict[str, Any]]] = None,
        calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """
        Create calendar event.
        
        Args:
            access_token: Google OAuth access token
            title: Event title
            description: Event description
            start_time: Event start time
            end_time: Event end time (defaults to start_time + 1 hour)
            location: Event location (optional)
            event_type: Event type for color coding (earnings, dividend, rebalance)
            reminders: Custom reminders (uses defaults if None)
            calendar_id: Calendar ID (defaults to "primary")
            
        Returns:
            Dict with event_id and event details
        """
        if self.mock:
            await asyncio.sleep(0.2)  # Simulate API call
            event_id = f"mock_event_{datetime.now().timestamp()}"
            logger.info(f"[MOCK Calendar] Created event: {title} at {start_time}")
            return {
                "event_id": event_id,
                "title": title,
                "start_time": start_time.isoformat(),
                "end_time": (end_time or start_time + timedelta(hours=1)).isoformat(),
                "status": "created",
                "provider": "google_calendar_mock"
            }
        
        try:
            service = self._get_calendar_service(access_token)
            if not service:
                raise RuntimeError("Calendar service not available")
            
            # Set end time if not provided
            if not end_time:
                end_time = start_time + timedelta(hours=1)
            
            # Build event body
            event_body = {
                "summary": title,
                "description": description,
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": "America/New_York"  # Default to ET
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "America/New_York"
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": reminders or self.DEFAULT_REMINDERS
                }
            }
            
            # Add location if provided
            if location:
                event_body["location"] = location
            
            # Add color if event type specified
            if event_type in self.COLOR_IDS:
                event_body["colorId"] = self.COLOR_IDS[event_type]
            
            # Create event
            created_event = service.events().insert(
                calendarId=calendar_id,
                body=event_body
            ).execute()
            
            logger.info(f"Calendar event created: {created_event.get('id')} - {title}")
            
            return {
                "event_id": created_event.get('id'),
                "title": created_event.get('summary'),
                "start_time": created_event.get('start', {}).get('dateTime'),
                "end_time": created_event.get('end', {}).get('dateTime'),
                "status": created_event.get('status'),
                "provider": "google_calendar",
                "html_link": created_event.get('htmlLink')
            }
            
        except HttpError as e:
            error_details = e.content.decode('utf-8') if e.content else str(e)
            logger.error(f"Calendar API error: {error_details}")
            raise RuntimeError(f"Failed to create calendar event: {error_details}")
        except Exception as e:
            logger.error(f"Unexpected error creating calendar event: {e}")
            raise
    
    async def update_event(
        self,
        access_token: str,
        event_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        location: Optional[str] = None,
        calendar_id: str = "primary"
    ) -> Dict[str, Any]:
        """
        Update existing calendar event.
        
        Args:
            access_token: Google OAuth access token
            event_id: Event ID to update
            title: New title (optional)
            description: New description (optional)
            start_time: New start time (optional)
            end_time: New end time (optional)
            location: New location (optional)
            calendar_id: Calendar ID
            
        Returns:
            Updated event details
        """
        if self.mock:
            await asyncio.sleep(0.2)
            logger.info(f"[MOCK Calendar] Updated event: {event_id}")
            return {
                "event_id": event_id,
                "status": "updated",
                "provider": "google_calendar_mock"
            }
        
        try:
            service = self._get_calendar_service(access_token)
            if not service:
                raise RuntimeError("Calendar service not available")
            
            # Get existing event
            event = service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            # Update fields
            if title:
                event['summary'] = title
            if description:
                event['description'] = description
            if start_time:
                event['start'] = {
                    "dateTime": start_time.isoformat(),
                    "timeZone": "America/New_York"
                }
            if end_time:
                event['end'] = {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "America/New_York"
                }
            if location:
                event['location'] = location
            
            # Update event
            updated_event = service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            logger.info(f"Calendar event updated: {event_id}")
            
            return {
                "event_id": updated_event.get('id'),
                "status": updated_event.get('status'),
                "provider": "google_calendar"
            }
            
        except HttpError as e:
            logger.error(f"Failed to update calendar event: {e}")
            raise RuntimeError(f"Failed to update calendar event: {str(e)}")
    
    async def delete_event(
        self,
        access_token: str,
        event_id: str,
        calendar_id: str = "primary"
    ) -> bool:
        """
        Delete calendar event.
        
        Args:
            access_token: Google OAuth access token
            event_id: Event ID to delete
            calendar_id: Calendar ID
            
        Returns:
            True if deleted successfully
        """
        if self.mock:
            await asyncio.sleep(0.1)
            logger.info(f"[MOCK Calendar] Deleted event: {event_id}")
            return True
        
        try:
            service = self._get_calendar_service(access_token)
            if not service:
                raise RuntimeError("Calendar service not available")
            
            service.events().delete(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            logger.info(f"Calendar event deleted: {event_id}")
            return True
            
        except HttpError as e:
            if e.resp.status == 404:
                logger.warning(f"Event {event_id} not found")
                return False
            logger.error(f"Failed to delete calendar event: {e}")
            raise RuntimeError(f"Failed to delete calendar event: {str(e)}")
    
    async def list_events(
        self,
        access_token: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        max_results: int = 50,
        calendar_id: str = "primary"
    ) -> List[Dict[str, Any]]:
        """
        List calendar events in date range.
        
        Args:
            access_token: Google OAuth access token
            start_time: Start of time range (defaults to now)
            end_time: End of time range (defaults to now + 30 days)
            max_results: Maximum number of events to return
            calendar_id: Calendar ID
            
        Returns:
            List of event dictionaries
        """
        if self.mock:
            await asyncio.sleep(0.2)
            return []
        
        try:
            service = self._get_calendar_service(access_token)
            if not service:
                raise RuntimeError("Calendar service not available")
            
            # Set defaults
            if not start_time:
                start_time = datetime.now()
            if not end_time:
                end_time = start_time + timedelta(days=30)
            
            # List events
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=start_time.isoformat() + 'Z',
                timeMax=end_time.isoformat() + 'Z',
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Format events
            formatted_events = []
            for event in events:
                formatted_events.append({
                    "event_id": event.get('id'),
                    "title": event.get('summary'),
                    "description": event.get('description'),
                    "start_time": event.get('start', {}).get('dateTime'),
                    "end_time": event.get('end', {}).get('dateTime'),
                    "location": event.get('location'),
                    "color_id": event.get('colorId'),
                    "html_link": event.get('htmlLink')
                })
            
            return formatted_events
            
        except HttpError as e:
            logger.error(f"Failed to list calendar events: {e}")
            raise RuntimeError(f"Failed to list calendar events: {str(e)}")


# Singleton instance
_calendar_service: Optional[GoogleCalendarService] = None


def get_calendar_service(mock: bool = True) -> GoogleCalendarService:
    """
    Get singleton Google Calendar service instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        GoogleCalendarService instance
    """
    global _calendar_service
    
    if _calendar_service is None:
        _calendar_service = GoogleCalendarService(mock=mock)
        logger.info(f"Google Calendar service initialized (mock={mock})")
    
    return _calendar_service
