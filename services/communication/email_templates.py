"""
==============================================================================
FILE: services/communication/email_templates.py
ROLE: Email Template Engine
PURPOSE: Renders HTML email templates using Jinja2 for portfolio alerts,
         trade confirmations, daily summaries, and system notifications.

INTEGRATION POINTS:
    - GmailService: Sends rendered templates
    - SendGridService: Fallback email provider
    - NotificationService: Triggers template rendering

TEMPLATES:
    - margin_alert: Margin call warnings
    - daily_summary: Portfolio performance summary
    - trade_confirmation: Trade execution confirmations
    - password_reset: Password reset links
    - earnings_reminder: Upcoming earnings notifications
    - dividend_notification: Dividend payment alerts

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from jinja2 import Environment, FileSystemLoader, Template
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    logger.warning("Jinja2 not installed. Install with: pip install jinja2")


class EmailTemplateEngine:
    """
    Email template engine using Jinja2 for rendering HTML emails.
    """
    
    # Template directory (relative to this file)
    TEMPLATE_DIR = Path(__file__).parent / "templates" / "email"
    
    def __init__(self, mock: bool = False):
        """
        Initialize template engine.
        
        Args:
            mock: Use mock mode if True
        """
        self.mock = mock
        
        if JINJA2_AVAILABLE and not mock:
            try:
                self.env = Environment(
                    loader=FileSystemLoader(str(self.TEMPLATE_DIR)),
                    autoescape=True
                )
            except Exception as e:
                logger.warning(f"Failed to load template directory: {e}")
                self.env = None
        else:
            self.env = None
    
    def render_template(
        self,
        template_name: str,
        context: Dict[str, Any],
        plain_text: bool = False
    ) -> tuple[str, str]:
        """
        Render email template.
        
        Args:
            template_name: Template filename (without extension)
            context: Template variables
            plain_text: If True, return plain text version only
            
        Returns:
            Tuple of (plain_text, html_text) or (plain_text, "") if plain_text=True
        """
        if self.mock or not self.env:
            return self._render_mock_template(template_name, context, plain_text)
        
        try:
            # Load template
            html_template = self.env.get_template(f"{template_name}.html")
            text_template = self.env.get_template(f"{template_name}.txt")
            
            # Render templates
            html_content = html_template.render(**context)
            text_content = text_template.render(**context)
            
            if plain_text:
                return text_content, ""
            
            return text_content, html_content
            
        except Exception as e:
            logger.error(f"Template rendering failed: {e}")
            # Fallback to mock
            return self._render_mock_template(template_name, context, plain_text)
    
    def _render_mock_template(
        self,
        template_name: str,
        context: Dict[str, Any],
        plain_text: bool
    ) -> tuple[str, str]:
        """Render mock template for testing."""
        templates = {
            "email_verification": {
                "subject": "Verify Your Email - AI Investor",
                "text": f"Please verify your email by clicking here: {context.get('verification_url', '#')}",
                "html": f"<h2>Verify Your Email</h2><p>Click <a href='{context.get('verification_url', '#')}'>here</a> to verify your account.</p>"
            },
            "margin_alert": {
                "subject": "Margin Alert - Action Required",
                "text": f"""
Margin Alert

Your portfolio margin level has dropped below the maintenance threshold.

Portfolio Value: ${context.get('portfolio_value', 'N/A')}
Margin Used: ${context.get('margin_used', 'N/A')}
Margin Level: {context.get('margin_level', 'N/A')}%

Please deposit funds or close positions to meet margin requirements.

View Portfolio: {context.get('portfolio_url', '#')}
                """,
                "html": f"""
<h2>Margin Alert</h2>
<p>Your portfolio margin level has dropped below the maintenance threshold.</p>
<ul>
    <li><strong>Portfolio Value:</strong> ${context.get('portfolio_value', 'N/A')}</li>
    <li><strong>Margin Used:</strong> ${context.get('margin_used', 'N/A')}</li>
    <li><strong>Margin Level:</strong> {context.get('margin_level', 'N/A')}%</li>
</ul>
<p>Please deposit funds or close positions to meet margin requirements.</p>
<a href="{context.get('portfolio_url', '#')}">View Portfolio</a>
                """
            },
            "daily_summary": {
                "subject": f"Daily Portfolio Summary - {datetime.now().strftime('%Y-%m-%d')}",
                "text": f"""
Daily Portfolio Summary

Portfolio Performance:
- Starting Value: ${context.get('starting_value', 'N/A')}
- Ending Value: ${context.get('ending_value', 'N/A')}
- Daily Change: {context.get('daily_change_pct', 'N/A')}%

Top Performers:
{self._format_list(context.get('top_performers', []))}

Top Losers:
{self._format_list(context.get('top_losers', []))}

View Full Report: {context.get('report_url', '#')}
                """,
                "html": f"""
<h2>Daily Portfolio Summary</h2>
<h3>Portfolio Performance</h3>
<ul>
    <li><strong>Starting Value:</strong> ${context.get('starting_value', 'N/A')}</li>
    <li><strong>Ending Value:</strong> ${context.get('ending_value', 'N/A')}</li>
    <li><strong>Daily Change:</strong> {context.get('daily_change_pct', 'N/A')}%</li>
</ul>
<h3>Top Performers</h3>
{self._format_html_list(context.get('top_performers', []))}
<h3>Top Losers</h3>
{self._format_html_list(context.get('top_losers', []))}
<a href="{context.get('report_url', '#')}">View Full Report</a>
                """
            },
            "trade_confirmation": {
                "subject": f"Trade Confirmation - {context.get('symbol', 'N/A')}",
                "text": f"""
Trade Confirmation

Your order has been executed:

Symbol: {context.get('symbol', 'N/A')}
Side: {context.get('side', 'N/A')}
Quantity: {context.get('quantity', 'N/A')}
Price: ${context.get('price', 'N/A')}
Total: ${context.get('total', 'N/A')}
Execution Time: {context.get('execution_time', 'N/A')}

View Trade Details: {context.get('trade_url', '#')}
                """,
                "html": f"""
<h2>Trade Confirmation</h2>
<p>Your order has been executed:</p>
<ul>
    <li><strong>Symbol:</strong> {context.get('symbol', 'N/A')}</li>
    <li><strong>Side:</strong> {context.get('side', 'N/A')}</li>
    <li><strong>Quantity:</strong> {context.get('quantity', 'N/A')}</li>
    <li><strong>Price:</strong> ${context.get('price', 'N/A')}</li>
    <li><strong>Total:</strong> ${context.get('total', 'N/A')}</li>
    <li><strong>Execution Time:</strong> {context.get('execution_time', 'N/A')}</li>
</ul>
<a href="{context.get('trade_url', '#')}">View Trade Details</a>
                """
            },
            "password_reset": {
                "subject": "Password Reset Request",
                "text": f"""
Password Reset Request

You requested to reset your password. Click the link below to reset:

{context.get('reset_url', '#')}

This link expires in 1 hour.

If you didn't request this, please ignore this email.
                """,
                "html": f"""
<h2>Password Reset Request</h2>
<p>You requested to reset your password. Click the link below to reset:</p>
<a href="{context.get('reset_url', '#')}">Reset Password</a>
<p>This link expires in 1 hour.</p>
<p><small>If you didn't request this, please ignore this email.</small></p>
                """
            },
            "earnings_reminder": {
                "subject": f"Earnings Reminder - {context.get('symbol', 'N/A')}",
                "text": f"""
Earnings Reminder

{context.get('symbol', 'N/A')} is reporting earnings on {context.get('earnings_date', 'N/A')}.

Expected EPS: ${context.get('expected_eps', 'N/A')}
Previous EPS: ${context.get('previous_eps', 'N/A')}

View Company Research: {context.get('research_url', '#')}
                """,
                "html": f"""
<h2>Earnings Reminder</h2>
<p><strong>{context.get('symbol', 'N/A')}</strong> is reporting earnings on <strong>{context.get('earnings_date', 'N/A')}</strong>.</p>
<ul>
    <li><strong>Expected EPS:</strong> ${context.get('expected_eps', 'N/A')}</li>
    <li><strong>Previous EPS:</strong> ${context.get('previous_eps', 'N/A')}</li>
</ul>
<a href="{context.get('research_url', '#')}">View Company Research</a>
                """
            },
            "dividend_notification": {
                "subject": f"Dividend Payment - {context.get('symbol', 'N/A')}",
                "text": f"""
Dividend Payment Notification

You received a dividend payment:

Symbol: {context.get('symbol', 'N/A')}
Amount per Share: ${context.get('dividend_per_share', 'N/A')}
Shares Owned: {context.get('shares', 'N/A')}
Total Payment: ${context.get('total_payment', 'N/A')}
Payment Date: {context.get('payment_date', 'N/A')}

View Portfolio: {context.get('portfolio_url', '#')}
                """,
                "html": f"""
<h2>Dividend Payment Notification</h2>
<p>You received a dividend payment:</p>
<ul>
    <li><strong>Symbol:</strong> {context.get('symbol', 'N/A')}</li>
    <li><strong>Amount per Share:</strong> ${context.get('dividend_per_share', 'N/A')}</li>
    <li><strong>Shares Owned:</strong> {context.get('shares', 'N/A')}</li>
    <li><strong>Total Payment:</strong> ${context.get('total_payment', 'N/A')}</li>
    <li><strong>Payment Date:</strong> {context.get('payment_date', 'N/A')}</li>
</ul>
<a href="{context.get('portfolio_url', '#')}">View Portfolio</a>
                """
            }
        }
        
        template = templates.get(template_name, {
            "subject": "Notification",
            "text": str(context),
            "html": f"<p>{str(context)}</p>"
        })
        
        if plain_text:
            return template["text"], ""
        
        return template["text"], template["html"]
    
    def _format_list(self, items: list) -> str:
        """Format list for plain text."""
        if not items:
            return "None"
        return "\n".join(f"- {item}" for item in items[:5])
    
    def _format_html_list(self, items: list) -> str:
        """Format list for HTML."""
        if not items:
            return "<p>None</p>"
        return "<ul>" + "".join(f"<li>{item}</li>" for item in items[:5]) + "</ul>"


# Singleton instance
_template_engine: Optional[EmailTemplateEngine] = None


def get_email_template_engine(mock: bool = True) -> EmailTemplateEngine:
    """
    Get singleton email template engine instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        EmailTemplateEngine instance
    """
    global _template_engine
    
    if _template_engine is None:
        _template_engine = EmailTemplateEngine(mock=mock)
        logger.info(f"Email template engine initialized (mock={mock})")
    
    return _template_engine
