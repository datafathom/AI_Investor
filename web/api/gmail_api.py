"""
==============================================================================
FILE: web/api/gmail_api.py
ROLE: Gmail API REST Endpoints
PURPOSE: RESTful endpoints for sending emails via Gmail API and managing
         email preferences.

INTEGRATION POINTS:
    - GmailService: Email sending
    - EmailTemplateEngine: Template rendering
    - GoogleAuthService: Token management

ENDPOINTS:
    POST /api/v1/gmail/send - Send email via Gmail
    POST /api/v1/gmail/send-template - Send templated email
    GET /api/v1/gmail/preview - Preview email template
    GET /api/v1/gmail/stats - Get sending statistics

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

gmail_bp = Blueprint('gmail', __name__, url_prefix='/api/v1/gmail')


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
    """Get Google access token from request or user storage."""
    # In production, retrieve from encrypted storage using user_id
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    
    # Fallback: get from request body or session
    data = request.json or {}
    return data.get('access_token')


# =============================================================================
# Send Email Endpoint
# =============================================================================

@gmail_bp.route('/send', methods=['POST'])
def send_email():
    """
    Send email via Gmail API.
    
    Request Body:
        {
            "to": "recipient@example.com",
            "subject": "Email Subject",
            "body_text": "Plain text body",
            "body_html": "<html>...</html>",  // optional
            "access_token": "google_access_token"  // optional if in header
        }
        
    Returns:
        JSON with message_id and status
    """
    try:
        data = request.json or {}
        
        to = data.get('to')
        subject = data.get('subject')
        body_text = data.get('body_text')
        body_html = data.get('body_html')
        access_token = _get_access_token()
        
        if not to or not subject or not body_text:
            return jsonify({
                "error": "Missing required fields: to, subject, body_text"
            }), 400
        
        if not access_token:
            return jsonify({
                "error": "Missing Google access token"
            }), 401
        
        user_id = _get_user_id()
        
        from services.communication.gmail_service import get_gmail_service
        gmail_service = get_gmail_service()
        
        result = _run_async(gmail_service.send_email(
            user_id=user_id,
            access_token=access_token,
            to=to,
            subject=subject,
            body_text=body_text,
            body_html=body_html
        ))
        
        return jsonify({
            "success": True,
            "message_id": result.get("message_id"),
            "status": result.get("status"),
            "provider": result.get("provider")
        })
        
    except RuntimeError as e:
        if "quota" in str(e).lower():
            return jsonify({
                "error": "Gmail quota exceeded",
                "message": str(e),
                "suggestion": "Use SendGrid fallback"
            }), 429
        return jsonify({
            "error": str(e)
        }), 500
    except Exception as e:
        logger.error(f"Gmail send failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to send email",
            "message": str(e)
        }), 500


# =============================================================================
# Send Templated Email Endpoint
# =============================================================================

@gmail_bp.route('/send-template', methods=['POST'])
def send_templated_email():
    """
    Send email using template.
    
    Request Body:
        {
            "to": "recipient@example.com",
            "template_name": "daily_summary",
            "template_context": {
                "starting_value": 100000,
                "ending_value": 105000,
                ...
            },
            "access_token": "google_access_token"
        }
        
    Returns:
        JSON with message_id and status
    """
    try:
        data = request.json or {}
        
        to = data.get('to')
        template_name = data.get('template_name')
        template_context = data.get('template_context', {})
        access_token = _get_access_token()
        
        if not to or not template_name:
            return jsonify({
                "error": "Missing required fields: to, template_name"
            }), 400
        
        if not access_token:
            return jsonify({
                "error": "Missing Google access token"
            }), 401
        
        user_id = _get_user_id()
        
        # Render template
        from services.communication.email_templates import get_email_template_engine
        template_engine = get_email_template_engine()
        body_text, body_html = template_engine.render_template(
            template_name=template_name,
            context=template_context
        )
        
        # Get subject from template context or use default
        subject = template_context.get('subject', f"Notification: {template_name}")
        
        # Send email
        from services.communication.gmail_service import get_gmail_service
        gmail_service = get_gmail_service()
        
        result = _run_async(gmail_service.send_email(
            user_id=user_id,
            access_token=access_token,
            to=to,
            subject=subject,
            body_text=body_text,
            body_html=body_html
        ))
        
        return jsonify({
            "success": True,
            "message_id": result.get("message_id"),
            "status": result.get("status"),
            "provider": result.get("provider"),
            "template": template_name
        })
        
    except Exception as e:
        logger.error(f"Templated email send failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to send templated email",
            "message": str(e)
        }), 500


# =============================================================================
# Preview Template Endpoint
# =============================================================================

@gmail_bp.route('/preview', methods=['GET'])
def preview_template():
    """
    Preview email template without sending.
    
    Query Params:
        template_name: Template to preview
        context: JSON string of template context (optional)
        
    Returns:
        JSON with rendered HTML and text
    """
    try:
        template_name = request.args.get('template_name')
        context_json = request.args.get('context', '{}')
        
        if not template_name:
            return jsonify({
                "error": "Missing template_name parameter"
            }), 400
        
        import json
        try:
            context = json.loads(context_json)
        except:
            context = {}
        
        from services.communication.email_templates import get_email_template_engine
        template_engine = get_email_template_engine()
        
        body_text, body_html = template_engine.render_template(
            template_name=template_name,
            context=context
        )
        
        return jsonify({
            "template_name": template_name,
            "body_text": body_text,
            "body_html": body_html,
            "context": context
        })
        
    except Exception as e:
        logger.error(f"Template preview failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to preview template",
            "message": str(e)
        }), 500


# =============================================================================
# Statistics Endpoint
# =============================================================================

@gmail_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get Gmail sending statistics for current user.
    
    Returns:
        JSON with send count and quota info
    """
    try:
        user_id = _get_user_id()
        
        from services.communication.gmail_service import get_gmail_service
        gmail_service = get_gmail_service()
        
        stats = _run_async(gmail_service.get_send_statistics(user_id))
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get statistics",
            "message": str(e)
        }), 500
