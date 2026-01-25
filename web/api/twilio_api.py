"""
==============================================================================
FILE: web/api/twilio_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes Twilio SMS capabilities to the frontend.
==============================================================================
"""

from flask import Blueprint, jsonify, request
import asyncio
import logging

from services.notifications.twilio_service import get_twilio_client

logger = logging.getLogger(__name__)

twilio_api_bp = Blueprint('twilio_api_bp', __name__)

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@twilio_api_bp.route('/notifications/twilio/send', methods=['POST'])
def send_alert():
    """
    Send a test SMS alert.
    Body: { "to": "+1555...", "message": "Test Alert" }
    """
    data = request.get_json() or {}
    to_number = data.get('to')
    message = data.get('message')
    use_mock = request.args.get('mock', 'true').lower() == 'true'

    if not to_number or not message:
        return jsonify({"error": "Missing 'to' or 'message'"}), 400

    client = get_twilio_client(mock=use_mock)
    
    try:
        result = _run_async(client.send_sms(to_number, message))
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        return jsonify({"error": str(e)}), 500
