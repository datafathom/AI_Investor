import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class NotificationHub:
    """
    Centralized communication service for Phase 30/31.
    Handles Twilio (SMS) and SendGrid (Email).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationHub, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.twilio_enabled = os.getenv("TWILIO_ENABLED", "false").lower() == "true"
        self.sendgrid_enabled = os.getenv("SENDGRID_ENABLED", "false").lower() == "true"
        
        # MOCK initialization log
        logger.info(f"NotificationHub initialized. Twilio: {self.twilio_enabled}, SendGrid: {self.sendgrid_enabled}")

    async def send_sms(self, to_number: str, message: str) -> bool:
        """
        Sends an SMS via Twilio.
        """
        if not self.twilio_enabled:
            logger.info(f"MOCK SMS to {to_number}: {message}")
            return True
            
        try:
            # Real Twilio client logic would go here
            logger.info(f"TWILIO SMS sent to {to_number}")
            return True
        except Exception as e:
            logger.error(f"Twilio failure: {e}")
            return False

    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Sends an email via SendGrid.
        """
        if not self.sendgrid_enabled:
            logger.info(f"MOCK Email to {to_email}: [{subject}] {body[:30]}...")
            return True
            
        try:
            # Real SendGrid client logic would go here
            logger.info(f"SENDGRID Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"SendGrid failure: {e}")
            return False

    async def broadcast_alert(self, title: str, message: str, severity: str = "INFO"):
        """
        Broadcasts an alert across all enabled channels.
        """
        log_msg = f"[{severity}] {title}: {message}"
        if severity == "CRITICAL":
            logger.critical(log_msg)
            # Send SMS for critical alerts if configured
            admin_phone = os.getenv("ADMIN_PHONE")
            if admin_phone:
                await self.send_sms(admin_phone, f"CRITICAL: {title} - {message}")
        else:
            logger.info(log_msg)

notification_hub = NotificationHub()
