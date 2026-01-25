"""
==============================================================================
FILE: web/api/ibkr_api.py
ROLE: Interactive Brokers API REST Endpoints
PURPOSE: RESTful endpoints for IBKR account management and order execution.

INTEGRATION POINTS:
    - IBKRClient: Order execution and account data
    - IBKRGatewayManager: Gateway lifecycle management

ENDPOINTS:
    GET /api/v1/ibkr/account-summary - Get account summary
    GET /api/v1/ibkr/positions - Get all positions
    GET /api/v1/ibkr/orders - Get order history
    POST /api/v1/ibkr/orders - Place order
    DELETE /api/v1/ibkr/orders/{id} - Cancel order
    GET /api/v1/ibkr/margin - Get margin requirements
    GET /api/v1/ibkr/currency-exposure - Get currency exposure
    GET /api/v1/ibkr/gateway/status - Get gateway status

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

ibkr_bp = Blueprint('ibkr', __name__, url_prefix='/api/v1/ibkr')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# =============================================================================
# Account Summary Endpoint
# =============================================================================

@ibkr_bp.route('/account-summary', methods=['GET'])
def get_account_summary():
    """
    Get comprehensive account summary.
    
    Query Params:
        account_id: Optional account ID filter
        
    Returns:
        JSON with account summary
    """
    try:
        account_id = request.args.get('account_id')
        
        from services.brokerage.ibkr_client import get_ibkr_client
        client = get_ibkr_client()
        
        # Ensure connected
        if not client.connected:
            _run_async(client.connect())
        
        summary = _run_async(client.get_account_summary())
        
        return jsonify(summary)
        
    except Exception as e:
        logger.error(f"Failed to get account summary: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get account summary",
            "message": str(e)
        }), 500


# =============================================================================
# Positions Endpoint
# =============================================================================

@ibkr_bp.route('/positions', methods=['GET'])
def get_positions():
    """
    Get all open positions across asset classes.
    
    Returns:
        JSON array of positions
    """
    try:
        from services.brokerage.ibkr_client import get_ibkr_client
        client = get_ibkr_client()
        
        if not client.connected:
            _run_async(client.connect())
        
        positions = _run_async(client.get_positions())
        
        return jsonify({
            "positions": positions,
            "count": len(positions)
        })
        
    except Exception as e:
        logger.error(f"Failed to get positions: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get positions",
            "message": str(e)
        }), 500


# =============================================================================
# Orders Endpoints
# =============================================================================

@ibkr_bp.route('/orders', methods=['GET'])
def get_orders():
    """
    Get order history.
    
    Query Params:
        account_id: Optional account filter
        
    Returns:
        JSON array of orders
    """
    try:
        account_id = request.args.get('account_id')
        
        from services.brokerage.ibkr_client import get_ibkr_client
        client = get_ibkr_client()
        
        if not client.connected:
            _run_async(client.connect())
        
        orders = _run_async(client.get_orders(account_id=account_id))
        
        return jsonify({
            "orders": orders,
            "count": len(orders)
        })
        
    except Exception as e:
        logger.error(f"Failed to get orders: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get orders",
            "message": str(e)
        }), 500


@ibkr_bp.route('/orders', methods=['POST'])
def place_order():
    """
    Place an order.
    
    Request Body:
        {
            "contract": "AAPL",
            "action": "BUY",
            "quantity": 100,
            "order_type": "MKT",
            "price": 150.00,  // optional for limit orders
            "account_id": "U12345678"  // optional
        }
        
    Returns:
        JSON with order confirmation
    """
    try:
        data = request.json or {}
        
        contract = data.get('contract')
        action = data.get('action')
        quantity = data.get('quantity')
        order_type = data.get('order_type', 'MKT')
        price = data.get('price')
        account_id = data.get('account_id')
        
        if not contract or not action or not quantity:
            return jsonify({
                "error": "Missing required fields: contract, action, quantity"
            }), 400
        
        from services.brokerage.ibkr_client import get_ibkr_client
        client = get_ibkr_client()
        
        if not client.connected:
            _run_async(client.connect())
        
        result = _run_async(client.place_order(
            contract=contract,
            action=action,
            quantity=quantity,
            order_type=order_type,
            price=price,
            account_id=account_id
        ))
        
        return jsonify({
            "success": True,
            "order": result
        }), 201
        
    except Exception as e:
        logger.error(f"Failed to place order: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to place order",
            "message": str(e)
        }), 500


@ibkr_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id: int):
    """
    Cancel an order.
    
    Returns:
        JSON confirmation
    """
    try:
        from services.brokerage.ibkr_client import get_ibkr_client
        client = get_ibkr_client()
        
        if not client.connected:
            _run_async(client.connect())
        
        cancelled = _run_async(client.cancel_order(order_id))
        
        if cancelled:
            return jsonify({
                "success": True,
                "message": f"Order {order_id} cancelled"
            })
        else:
            return jsonify({
                "error": "Failed to cancel order"
            }), 500
        
    except Exception as e:
        logger.error(f"Failed to cancel order: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to cancel order",
            "message": str(e)
        }), 500


# =============================================================================
# Margin Endpoint
# =============================================================================

@ibkr_bp.route('/margin', methods=['GET'])
def get_margin():
    """
    Get margin requirements and utilization.
    
    Query Params:
        account_id: Optional account filter
        
    Returns:
        JSON with margin information
    """
    try:
        account_id = request.args.get('account_id')
        
        from services.brokerage.ibkr_client import get_ibkr_client
        client = get_ibkr_client()
        
        if not client.connected:
            _run_async(client.connect())
        
        margin = _run_async(client.get_margin_requirements(account_id=account_id))
        
        return jsonify(margin)
        
    except Exception as e:
        logger.error(f"Failed to get margin: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get margin requirements",
            "message": str(e)
        }), 500


# =============================================================================
# Currency Exposure Endpoint
# =============================================================================

@ibkr_bp.route('/currency-exposure', methods=['GET'])
def get_currency_exposure():
    """
    Get currency exposure across all positions.
    
    Query Params:
        account_id: Optional account filter
        
    Returns:
        JSON array of currency exposures
    """
    try:
        account_id = request.args.get('account_id')
        
        from services.brokerage.ibkr_client import get_ibkr_client
        client = get_ibkr_client()
        
        if not client.connected:
            _run_async(client.connect())
        
        exposure = _run_async(client.get_currency_exposure(account_id=account_id))
        
        return jsonify({
            "currency_exposure": exposure
        })
        
    except Exception as e:
        logger.error(f"Failed to get currency exposure: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get currency exposure",
            "message": str(e)
        }), 500


# =============================================================================
# Gateway Status Endpoint
# =============================================================================

@ibkr_bp.route('/gateway/status', methods=['GET'])
def get_gateway_status():
    """
    Get IBKR Gateway status.
    
    Returns:
        JSON with gateway status
    """
    try:
        from services.brokerage.ibkr_gateway_manager import get_ibkr_gateway
        gateway = get_ibkr_gateway()
        
        status = _run_async(gateway.get_session_status())
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Failed to get gateway status: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get gateway status",
            "message": str(e)
        }), 500
