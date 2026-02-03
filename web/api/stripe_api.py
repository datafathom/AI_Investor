"""
==============================================================================
FILE: web/api/stripe_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes Billing/Stripe capabilities to the frontend.
==============================================================================
"""

import asyncio
import logging
from flask import Blueprint, jsonify, request

from services.payments.stripe_service import get_stripe_client

logger = logging.getLogger(__name__)

stripe_bp = Blueprint('stripe_bp', __name__, url_prefix='/api/v1/stripe')

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@stripe_bp.route('/billing/subscription', methods=['GET'])
def get_subscription():
    """
    Get current user subscription.
    Query: ?mock=true
    """
    # In a real app, we'd get user_id from session/token
    user_id = "user_mock_123" 
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    
    client = get_stripe_client(mock=use_mock)
    
    try:
        result = _run_async(client.get_subscription(user_id))
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to fetch subscription: %s", e)
        return jsonify({"error": str(e)}), 500

@stripe_bp.route('/billing/checkout', methods=['POST'])
def create_checkout():
    """
    Create a checkout session.
    Body: { "plan_id": "price_pro_monthly" }
    """
    data = request.get_json()
    plan_id = data.get('plan_id')
    user_id = "user_mock_123"
    use_mock = request.args.get('mock', 'true').lower() == 'true'

    if not plan_id:
        return jsonify({"error": "Plan ID required"}), 400
        
    client = get_stripe_client(mock=use_mock)
    
    try:
        result = _run_async(client.create_checkout_session(user_id, plan_id))
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to create checkout: %s", e)
        return jsonify({"error": str(e)}), 500
