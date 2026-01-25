"""
==============================================================================
FILE: web/api/paypal_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes PayPal payment capabilities to the frontend.
==============================================================================
"""

import asyncio
import logging
from flask import Blueprint, jsonify, request

from services.payments.paypal_service import get_paypal_client

logger = logging.getLogger(__name__)

paypal_bp = Blueprint('paypal_bp', __name__)

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@paypal_bp.route('/payment/paypal/create-order', methods=['POST'])
def create_order():
    """
    Create a PayPal order.
    Body: { "amount": 29.00, "currency": "USD" }
    Query: ?mock=true
    """
    data = request.get_json() or {}
    amount = data.get('amount', 29.00)
    currency = data.get('currency', 'USD')
    use_mock = request.args.get('mock', 'true').lower() == 'true'

    client = get_paypal_client(mock=use_mock)
    
    try:
        result = _run_async(client.create_order(amount, currency))
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to create PayPal order: %s", e)
        return jsonify({"error": str(e)}), 500

@paypal_bp.route('/payment/paypal/capture-order', methods=['POST'])
def capture_order():
    """
    Capture a PayPal order.
    Body: { "order_id": "PAYPAL_..." }
    """
    data = request.get_json() or {}
    order_id = data.get('order_id')
    use_mock = request.args.get('mock', 'true').lower() == 'true'

    if not order_id:
        return jsonify({"error": "Order ID required"}), 400
        
    client = get_paypal_client(mock=use_mock)
    
    try:
        result = _run_async(client.capture_order(order_id))
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to capture PayPal order: %s", e)
        return jsonify({"error": str(e)}), 500
