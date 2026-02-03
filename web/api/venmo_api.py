"""
==============================================================================
FILE: web/api/venmo_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes Venmo payment capabilities to the frontend.
==============================================================================
"""

import asyncio
import logging
from flask import Blueprint, jsonify, request

from services.payments.venmo_service import get_venmo_client

logger = logging.getLogger(__name__)

venmo_bp = Blueprint('venmo_bp', __name__, url_prefix='/api/v1/venmo')

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@venmo_bp.route('/payment/venmo/pay', methods=['POST'])
def pay():
    """
    Process Venmo payment.
    Body: { "amount": 29.00 }
    Query: ?mock=true
    """
    data = request.get_json() or {}
    amount = data.get('amount', 29.00)
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    
    # In real app, we might get username from session
    username = "mock_user_123"

    client = get_venmo_client(mock=use_mock)
    
    try:
        result = _run_async(client.process_payment(amount, username))
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to process Venmo payment: %s", e)
        return jsonify({"error": str(e)}), 500
