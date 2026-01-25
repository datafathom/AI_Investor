"""
==============================================================================
FILE: services/communication/gmail_service.py
ROLE: Gmail API Client Service
PURPOSE: Sends emails through authenticated user's Gmail account using Gmail API.
         Provides personalized email notifications for portfolio alerts, trade
         confirmations, and daily summaries.

INTEGRATION POINTS:
    - GoogleAuthService: Retrieves access tokens for Gmail API
    - EmailTemplateEngine: Renders HTML email templates
    - NotificationService: Triggers email sending
    - SendGridService: Fallback if Gmail quota exceeded

SCOPES REQUIRED:
    - https://www.googleapis.com/auth/gmail.send

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import base64
import json
import asyncio
from typing import Dict, Any, Optional, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.oauth2.credentials import Credentials
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    logger.warning("Google API client not installed. Install with: pip install google-api-python-client")


class GmailService:
    """
    Gmail API service for sending emails through authenticated user's Gmail account.
    """
    
    # Gmail API quota limits
    DAILY_SEND_LIMIT = 500  # Per user per day
    RATE_LIMIT_PER_SECOND = 10
    
    def __init__(self, mock: bool = False):
        """
        Initialize Gmail service.
        
        Args:
            mock: Use mock mode if True
        """
        self.mock = mock
        self._send_count = {}  # Track sends per user (in production, use Redis)
        self._last_send_time = {}  # Rate limiting
        
    def _get_gmail_service(self, access_token: str):
        """
        Build Gmail API service client.
        
        Args:
            access_token: Google OAuth access token
            
        Returns:
            Gmail API service object
        """
        if self.mock or not GOOGLE_API_AVAILABLE:
            return None
        
        try:
            credentials = Credentials(token=access_token)
            service = build('gmail', 'v1', credentials=credentials)
            return service
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
            raise
    
    def _create_message(
        self,
        sender: str,
        to: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, str]:
        """
        Create email message in Gmail API format.
        
        Args:
            sender: Sender email address
            to: Recipient email address
            subject: Email subject
            body_text: Plain text body
            body_html: HTML body (optional)
            attachments: List of attachments with 'filename' and 'content' keys
            
        Returns:
            Message dict with 'raw' field containing base64-encoded message
        """
        if body_html:
            message = MIMEMultipart('alternative')
            message['to'] = to
            message['from'] = sender
            message['subject'] = subject
            
            part1 = MIMEText(body_text, 'plain')
            part2 = MIMEText(body_html, 'html')
            
            message.attach(part1)
            message.attach(part2)
        else:
            message = MIMEText(body_text)
            message['to'] = to
            message['from'] = sender
            message['subject'] = subject
        
        # Add attachments if provided
        if attachments:
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment['content'])
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {attachment["filename"]}'
                )
                message.attach(part)
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}
    
    async def send_email(
        self,
        user_id: str,
        access_token: str,
        to: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        sender: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Send email via Gmail API.
        
        Args:
            user_id: User ID for quota tracking
            access_token: Google OAuth access token
            to: Recipient email address
            subject: Email subject
            body_text: Plain text body
            body_html: HTML body (optional)
            sender: Sender email (defaults to authenticated user's email)
            attachments: List of attachments
            
        Returns:
            Dict with message_id and status
        """
        if self.mock:
            await asyncio.sleep(0.2)  # Simulate API call
            logger.info(f"[MOCK Gmail] Sent email to {to}: {subject}")
            return {
                "message_id": f"mock_message_{datetime.now().timestamp()}",
                "status": "sent",
                "provider": "gmail_mock"
            }
        
        # Check quota
        if not self._check_quota(user_id):
            raise RuntimeError(f"Daily send limit exceeded for user {user_id}")
        
        # Rate limiting
        await self._rate_limit(user_id)
        
        try:
            # Get Gmail service
            service = self._get_gmail_service(access_token)
            if not service:
                raise RuntimeError("Gmail service not available")
            
            # Get user's email if sender not provided
            if not sender:
                profile = service.users().getProfile(userId='me').execute()
                sender = profile.get('emailAddress', 'noreply@aiinvestor.com')
            
            # Create message
            message = self._create_message(
                sender=sender,
                to=to,
                subject=subject,
                body_text=body_text,
                body_html=body_html,
                attachments=attachments
            )
            
            # Send message
            sent_message = service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            # Track send
            self._track_send(user_id)
            
            logger.info(f"Gmail email sent: {sent_message.get('id')} to {to}")
            
            return {
                "message_id": sent_message.get('id'),
                "status": "sent",
                "provider": "gmail",
                "thread_id": sent_message.get('threadId')
            }
            
        except HttpError as e:
            error_details = json.loads(e.content.decode('utf-8'))
            error_message = error_details.get('error', {}).get('message', str(e))
            logger.error(f"Gmail API error: {error_message}")
            
            # Check if quota exceeded
            if 'quota' in error_message.lower() or e.resp.status == 429:
                raise RuntimeError("Gmail quota exceeded. Consider using SendGrid fallback.")
            
            raise RuntimeError(f"Failed to send email via Gmail: {error_message}")
        
        except Exception as e:
            logger.error(f"Unexpected error sending Gmail email: {e}")
            raise
    
    def _check_quota(self, user_id: str) -> bool:
        """Check if user has remaining daily quota."""
        count = self._send_count.get(user_id, 0)
        return count < self.DAILY_SEND_LIMIT
    
    def _track_send(self, user_id: str):
        """Track email send for quota management."""
        if user_id not in self._send_count:
            self._send_count[user_id] = 0
        self._send_count[user_id] += 1
    
    async def _rate_limit(self, user_id: str):
        """Rate limit sends to avoid hitting API limits."""
        if user_id in self._last_send_time:
            elapsed = asyncio.get_event_loop().time() - self._last_send_time[user_id]
            if elapsed < (1.0 / self.RATE_LIMIT_PER_SECOND):
                await asyncio.sleep((1.0 / self.RATE_LIMIT_PER_SECOND) - elapsed)
        
        self._last_send_time[user_id] = asyncio.get_event_loop().time()
    
    async def get_send_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get email sending statistics for user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with send count and quota info
        """
        count = self._send_count.get(user_id, 0)
        return {
            "sends_today": count,
            "quota_limit": self.DAILY_SEND_LIMIT,
            "remaining": max(0, self.DAILY_SEND_LIMIT - count),
            "provider": "gmail"
        }


# Singleton instance
_gmail_service: Optional[GmailService] = None


def get_gmail_service(mock: bool = True) -> GmailService:
    """
    Get singleton Gmail service instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        GmailService instance
    """
    global _gmail_service
    
    if _gmail_service is None:
        _gmail_service = GmailService(mock=mock)
        logger.info(f"Gmail service initialized (mock={mock})")
    
    return _gmail_service
