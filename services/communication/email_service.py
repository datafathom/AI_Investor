"""
Email Service
Production-ready email sending service with multiple providers
"""

import os
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class EmailProvider(Enum):
    """Email service providers."""
    SENDGRID = "sendgrid"
    AWS_SES = "aws_ses"
    SMTP = "smtp"


class EmailService:
    """Email sending service with multiple provider support."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmailService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.provider = self._get_provider()
            self._client = None
            self._init_client()
    
    def _get_provider(self) -> EmailProvider:
        """Determine which email provider to use."""
        provider_str = os.getenv('EMAIL_PROVIDER', 'sendgrid').lower()
        
        if provider_str == 'sendgrid':
            return EmailProvider.SENDGRID
        elif provider_str == 'aws_ses':
            return EmailProvider.AWS_SES
        elif provider_str == 'smtp':
            return EmailProvider.SMTP
        else:
            logger.warning(f"Unknown email provider: {provider_str}, defaulting to SendGrid")
            return EmailProvider.SENDGRID
    
    def _init_client(self):
        """Initialize email client based on provider."""
        if self.provider == EmailProvider.SENDGRID:
            self._init_sendgrid()
        elif self.provider == EmailProvider.AWS_SES:
            self._init_aws_ses()
        elif self.provider == EmailProvider.SMTP:
            self._init_smtp()
    
    def _init_sendgrid(self):
        """Initialize SendGrid client."""
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail
            
            api_key = os.getenv('SENDGRID_API_KEY')
            if not api_key:
                logger.warning("SENDGRID_API_KEY not set, email sending disabled")
                return
            
            self._client = sendgrid.SendGridAPIClient(api_key=api_key)
            logger.info("SendGrid email service initialized")
        except ImportError:
            logger.warning("sendgrid library not installed. Install with: pip install sendgrid")
        except Exception as e:
            logger.error(f"Failed to initialize SendGrid: {e}")
    
    def _init_aws_ses(self):
        """Initialize AWS SES client."""
        try:
            import boto3
            
            region = os.getenv('AWS_REGION', 'us-east-1')
            self._client = boto3.client('ses', region_name=region)
            logger.info("AWS SES email service initialized")
        except ImportError:
            logger.warning("boto3 not installed. Install with: pip install boto3")
        except Exception as e:
            logger.error(f"Failed to initialize AWS SES: {e}")
    
    def _init_smtp(self):
        """Initialize SMTP client."""
        self.smtp_host = os.getenv('SMTP_HOST', 'localhost')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.smtp_use_tls = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
        
        logger.info(f"SMTP email service configured: {self.smtp_host}:{self.smtp_port}")
    
    def send_email(self, to: str, subject: str, body: str, 
                   html_body: Optional[str] = None, from_email: Optional[str] = None,
                   cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None,
                   reply_to: Optional[str] = None) -> bool:
        """
        Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Plain text body
            html_body: HTML body (optional)
            from_email: Sender email (defaults to configured sender)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)
            reply_to: Reply-to address (optional)
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self._client and self.provider != EmailProvider.SMTP:
            logger.error("Email client not initialized")
            return False
        
        try:
            if self.provider == EmailProvider.SENDGRID:
                return self._send_sendgrid(to, subject, body, html_body, from_email, cc, bcc, reply_to)
            elif self.provider == EmailProvider.AWS_SES:
                return self._send_aws_ses(to, subject, body, html_body, from_email, cc, bcc, reply_to)
            elif self.provider == EmailProvider.SMTP:
                return self._send_smtp(to, subject, body, html_body, from_email, cc, bcc, reply_to)
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
        
        return False
    
    def _send_sendgrid(self, to: str, subject: str, body: str, 
                      html_body: Optional[str] = None, from_email: Optional[str] = None,
                      cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None,
                      reply_to: Optional[str] = None) -> bool:
        """Send email via SendGrid."""
        from sendgrid.helpers.mail import Mail, Email, Content
        
        from_addr = from_email or os.getenv('EMAIL_FROM', 'noreply@ai-investor.com')
        
        message = Mail(
            from_email=Email(from_addr),
            to_emails=to,
            subject=subject,
            plain_text_content=body
        )
        
        if html_body:
            message.add_content(Content("text/html", html_body))
        
        if cc:
            for email in cc:
                message.add_cc(Email(email))
        
        if bcc:
            for email in bcc:
                message.add_bcc(Email(email))
        
        if reply_to:
            message.reply_to = Email(reply_to)
        
        try:
            response = self._client.send(message)
            logger.info(f"Email sent via SendGrid: {response.status_code}")
            return response.status_code in [200, 201, 202]
        except Exception as e:
            logger.error(f"SendGrid error: {e}")
            return False
    
    def _send_aws_ses(self, to: str, subject: str, body: str,
                     html_body: Optional[str] = None, from_email: Optional[str] = None,
                     cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None,
                     reply_to: Optional[str] = None) -> bool:
        """Send email via AWS SES."""
        from_addr = from_email or os.getenv('EMAIL_FROM', 'noreply@ai-investor.com')
        
        destination = {'ToAddresses': [to]}
        if cc:
            destination['CcAddresses'] = cc
        if bcc:
            destination['BccAddresses'] = bcc
        
        message = {
            'Subject': {'Data': subject, 'Charset': 'UTF-8'},
            'Body': {'Text': {'Data': body, 'Charset': 'UTF-8'}}
        }
        
        if html_body:
            message['Body']['Html'] = {'Data': html_body, 'Charset': 'UTF-8'}
        
        try:
            response = self._client.send_email(
                Source=from_addr,
                Destination=destination,
                Message=message,
                ReplyToAddresses=[reply_to] if reply_to else []
            )
            logger.info(f"Email sent via AWS SES: {response['MessageId']}")
            return True
        except Exception as e:
            logger.error(f"AWS SES error: {e}")
            return False
    
    def _send_smtp(self, to: str, subject: str, body: str,
                  html_body: Optional[str] = None, from_email: Optional[str] = None,
                  cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None,
                  reply_to: Optional[str] = None) -> bool:
        """Send email via SMTP."""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        from_addr = from_email or os.getenv('EMAIL_FROM', 'noreply@ai-investor.com')
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to
        
        if cc:
            msg['Cc'] = ', '.join(cc)
        if reply_to:
            msg['Reply-To'] = reply_to
        
        # Add plain text part
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML part if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Combine all recipients
        recipients = [to]
        if cc:
            recipients.extend(cc)
        if bcc:
            recipients.extend(bcc)
        
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.smtp_use_tls:
                server.starttls()
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg, from_addr, recipients)
            server.quit()
            logger.info(f"Email sent via SMTP to {to}")
            return True
        except Exception as e:
            logger.error(f"SMTP error: {e}")
            return False
    
    def send_transactional_email(self, to: str, template: str, context: Dict[str, Any]) -> bool:
        """
        Send a transactional email using a template.
        
        Args:
            to: Recipient email
            template: Template name (e.g., 'welcome', 'password_reset')
            context: Template context variables
        
        Returns:
            True if sent successfully
        """
        # Load template (in production, use Jinja2 or similar)
        subject, body, html_body = self._render_template(template, context)
        return self.send_email(to, subject, body, html_body)
    
    def _render_template(self, template: str, context: Dict[str, Any]) -> tuple:
        """Render email template."""
        templates = {
            'welcome': {
                'subject': 'Welcome to AI Investor!',
                'body': f"Welcome {context.get('name', 'User')}! Thank you for joining AI Investor.",
                'html': f"<h1>Welcome {context.get('name', 'User')}!</h1><p>Thank you for joining AI Investor.</p>"
            },
            'password_reset': {
                'subject': 'Reset Your Password',
                'body': f"Click here to reset your password: {context.get('reset_link', '')}",
                'html': f"<p>Click <a href='{context.get('reset_link', '')}'>here</a> to reset your password.</p>"
            },
            'onboarding_complete': {
                'subject': 'Onboarding Complete!',
                'body': f"Congratulations {context.get('name', 'User')}! Your onboarding is complete.",
                'html': f"<h1>Congratulations!</h1><p>Your onboarding is complete. Start investing!</p>"
            }
        }
        
        template_data = templates.get(template, {
            'subject': 'Notification from AI Investor',
            'body': 'You have a new notification.',
            'html': '<p>You have a new notification.</p>'
        })
        
        return template_data['subject'], template_data['body'], template_data['html']


def get_email_service() -> EmailService:
    """Get email service instance."""
    return EmailService()
