"""
==============================================================================
FILE: services/notifications/sendgrid_service.py
ROLE: Email Notification Service
PURPOSE: Interfaces with SendGrid for sending reports and alerts.
         
INTEGRATION POINTS:
    - EmailAPI: Primary consumer.
    - ReportScheduler: Future consumer for automated reports.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import uuid
import datetime
from datetime import timezone
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class SendGridClient:
    """
    Client for SendGrid API.
    Currently defaults to MOCK MODE as per Phase 21 requirements.
    """
    
    def __init__(self, api_key: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.api_key = api_key
        # TODO: Initialize live SendGrid client here

    async def send_email(self, to_email: str, subject: str, content: str, content_type: str = "text/html") -> Dict[str, Any]:
        """
        Send an email message.
        """
        if self.mock:
            await asyncio.sleep(0.8) # Simulate processing time
            
            message_id = str(uuid.uuid4())
            logger.info(f"[SendGrid Mock] Sending Email to {to_email} | Subject: {subject}")
            
            return {
                "id": message_id,
                "to": to_email,
                "from": "reports@ai-investor.com",
                "subject": subject,
                "status": "sent",
                "timestamp": datetime.datetime.now(timezone.utc).isoformat()
            }
        return {}
    
    async def update_subscriptions(self, email: str, preferences: Dict[str, bool]) -> Dict[str, Any]:
        """
        Update user email subscription preferences.
        """
        if self.mock:
            await asyncio.sleep(0.3)
            return {
                "email": email,
                "preferences": preferences,
                "status": "updated"
            }
        return {}

_instance = None

def get_sendgrid_client(mock: bool = True) -> SendGridClient:
    global _instance
    if _instance is None:
        _instance = SendGridClient(mock=mock)
    return _instance
