"""
==============================================================================
FILE: services/notifications/twilio_service.py
ROLE: SMS Notification Service
PURPOSE: Interfaces with Twilio for sending high-priority alerts.
         
INTEGRATION POINTS:
    - TwilioAPI: Primary consumer.
    - AlertManager: Future consumer for system-wide alerts.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import random
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class TwilioClient:
    """
    Client for Twilio API.
    Currently defaults to MOCK MODE as per Phase 20 requirements.
    """
    
    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.account_sid = account_sid
        self.auth_token = auth_token
        # TODO: Initialize live Twilio client here

    async def send_sms(self, to_number: str, body: str) -> Dict[str, Any]:
        """
        Send an SMS message.
        """
        if self.mock:
            await asyncio.sleep(0.5) # Simulate network latency
            
            message_sid = f"SM{random.randint(1000000000, 9999999999)}"
            logger.info(f"[Twilio Mock] Sending SMS to {to_number}: {body}")
            
            return {
                "sid": message_sid,
                "to": to_number,
                "from": "+15550109999", # Mock Twilio number
                "body": body,
                "status": "delivered",
                "date_created": datetime.datetime.utcnow().isoformat(),
                "price": "0.0075",
                "direction": "outbound-api"
            }
        return {"status": "failed", "error": "Not in mock mode and credentials missing"}

    async def send_critical_alert(self, to_number: str, alert_type: str, details: str) -> Dict[str, Any]:
        """Send high-priority critical alerts."""
        emoji = "⚠️" if "margin" in alert_type.lower() else "🔥"
        body = f"{emoji} AI INVESTOR ALERT: {alert_type.upper()}! {details}"
        return await self.send_sms(to_number, body)

    async def send_verification_otp(self, to_number: str) -> str:
        """Send 6-digit OTP for phone verification."""
        code = str(random.randint(100000, 999999))
        body = f"Your AI Investor verification code is: {code}. It expires in 5 minutes."
        await self.send_sms(to_number, body)
        return code


_instance = None

def get_twilio_client(mock: bool = True) -> TwilioClient:
    global _instance
    if _instance is None:
        _instance = TwilioClient(mock=mock)
    return _instance
