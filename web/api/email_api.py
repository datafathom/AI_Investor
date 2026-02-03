"""
==============================================================================
FILE: web/api/email_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes Email capabilities to the frontend.
==============================================================================
"""

from flask import Blueprint, jsonify, request
import asyncio
import logging

from services.notifications.sendgrid_service import get_sendgrid_client

logger = logging.getLogger(__name__)

email_api_bp = Blueprint('email_api_bp', __name__, url_prefix='/api/v1/email')

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@email_api_bp.route('/notifications/email/send', methods=['POST'])
def send_test_email():
    """
    Send a test email.
    Body: { "to": "user@example.com", "subject": "Test", "content": "Hello" }
    """
    data = request.get_json() or {}
    to_email = data.get('to')
    subject = data.get('subject', 'Test Email')
    content = data.get('content', 'This is a test email.')
    use_mock = request.args.get('mock', 'true').lower() == 'true'

    if not to_email:
        return jsonify({"error": "Missing 'to' email address"}), 400

    client = get_sendgrid_client(mock=use_mock)
    
    try:
        result = _run_async(client.send_email(to_email, subject, content))
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return jsonify({"error": str(e)}), 500

@email_api_bp.route('/notifications/email/subscribe', methods=['POST'])
def update_subscriptions():
    """
    Update email subscriptions.
    Body: { "email": "...", "preferences": { "daily": true, ... } }
    """
    data = request.get_json() or {}
    email = data.get('email')
    preferences = data.get('preferences', {})
    use_mock = request.args.get('mock', 'true').lower() == 'true'

    if not email:
        return jsonify({"error": "Missing 'email'"}), 400

    client = get_sendgrid_client(mock=use_mock)
    
    try:
        result = _run_async(client.update_subscriptions(email, preferences))
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to update subscriptions: {e}")
        return jsonify({"error": str(e)}), 500
