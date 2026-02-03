"""
==============================================================================
FILE: web/api/coinbase_crypto_api.py
ROLE: Coinbase Crypto API REST Endpoints
PURPOSE: RESTful endpoints for Coinbase trading and custody management.

INTEGRATION POINTS:
    - CoinbaseClient: Trading and account management
    - CoinbaseCustody: Vault balance management

ENDPOINTS:
    GET /api/v1/coinbase/accounts - Get trading accounts
    GET /api/v1/coinbase/trading-pairs - Get available trading pairs
    POST /api/v1/coinbase/orders - Place order
    GET /api/v1/coinbase/orders - Get order history
    GET /api/v1/coinbase/vaults - Get vault balances
    POST /api/v1/coinbase/vaults/withdraw - Request withdrawal

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio

logger = logging.getLogger(__name__)

coinbase_crypto_bp = Blueprint('coinbase_crypto', __name__, url_prefix='/api/v1/coinbase_crypto')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# =============================================================================
# Get Accounts Endpoint
# =============================================================================

@coinbase_crypto_bp.route('/accounts', methods=['GET'])
def get_accounts():
    """
    Get all trading accounts/balances.
    
    Returns:
        JSON array of accounts
    """
    try:
        from services.crypto.coinbase_client import get_coinbase_client
        client = get_coinbase_client()
        
        accounts = _run_async(client.get_accounts())
        
        return jsonify({
            "accounts": accounts,
            "count": len(accounts)
        })
        
    except Exception as e:
        logger.error(f"Failed to get accounts: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get accounts",
            "message": str(e)
        }), 500


# =============================================================================
# Get Trading Pairs Endpoint
# =============================================================================

@coinbase_crypto_bp.route('/trading-pairs', methods=['GET'])
def get_trading_pairs():
    """
    Get available trading pairs.
    
    Returns:
        JSON array of product IDs
    """
    try:
        from services.crypto.coinbase_client import get_coinbase_client
        client = get_coinbase_client()
        
        pairs = _run_async(client.get_trading_pairs())
        
        return jsonify({
            "trading_pairs": pairs,
            "count": len(pairs)
        })
        
    except Exception as e:
        logger.error(f"Failed to get trading pairs: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get trading pairs",
            "message": str(e)
        }), 500


# =============================================================================
# Place Order Endpoint
# =============================================================================

@coinbase_crypto_bp.route('/orders', methods=['POST'])
def place_order():
    """
    Place a trade order.
    
    Request Body:
        {
            "product_id": "BTC-USD",
            "side": "buy",
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": "100.00"
                }
            }
        }
        
    Returns:
        JSON with order confirmation
    """
    try:
        data = request.json or {}
        product_id = data.get('product_id')
        side = data.get('side')
        order_config = data.get('order_configuration')
        
        if not product_id or not side or not order_config:
            return jsonify({
                "error": "Missing required fields: product_id, side, order_configuration"
            }), 400
        
        from services.crypto.coinbase_client import get_coinbase_client
        client = get_coinbase_client()
        
        result = _run_async(client.place_order(
            product_id=product_id,
            side=side,
            order_configuration=order_config
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


# =============================================================================
# Get Orders Endpoint
# =============================================================================

@coinbase_crypto_bp.route('/orders', methods=['GET'])
def get_orders():
    """
    Get order history.
    
    Query Params:
        limit: Maximum orders (default 100)
        
    Returns:
        JSON array of orders
    """
    try:
        limit = int(request.args.get('limit', 100))
        
        from services.crypto.coinbase_client import get_coinbase_client
        client = get_coinbase_client()
        
        orders = _run_async(client.get_orders(limit=limit))
        
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


# =============================================================================
# Get Vault Balances Endpoint
# =============================================================================

@coinbase_crypto_bp.route('/vaults', methods=['GET'])
def get_vaults():
    """
    Get vault balances.
    
    Query Params:
        vault_id: Optional vault ID filter
        
    Returns:
        JSON array of vault balances
    """
    try:
        vault_id = request.args.get('vault_id')
        
        from services.crypto.coinbase_custody import get_coinbase_custody
        custody = get_coinbase_custody()
        
        balances = _run_async(custody.get_vault_balances(vault_id=vault_id))
        
        return jsonify({
            "vault_balances": balances,
            "count": len(balances)
        })
        
    except Exception as e:
        logger.error(f"Failed to get vault balances: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get vault balances",
            "message": str(e)
        }), 500


# =============================================================================
# Request Withdrawal Endpoint
# =============================================================================

@coinbase_crypto_bp.route('/vaults/withdraw', methods=['POST'])
def request_withdrawal():
    """
    Request withdrawal from vault (requires multi-party approval).
    
    Request Body:
        {
            "vault_id": "vault_primary",
            "currency": "BTC",
            "amount": 0.5,
            "destination": "bc1q..."
        }
        
    Returns:
        JSON with withdrawal request
    """
    try:
        data = request.json or {}
        vault_id = data.get('vault_id')
        currency = data.get('currency')
        amount = data.get('amount')
        destination = data.get('destination')
        
        if not all([vault_id, currency, amount, destination]):
            return jsonify({
                "error": "Missing required fields: vault_id, currency, amount, destination"
            }), 400
        
        from services.crypto.coinbase_custody import get_coinbase_custody
        custody = get_coinbase_custody()
        
        result = _run_async(custody.request_withdrawal(
            vault_id=vault_id,
            currency=currency,
            amount=amount,
            destination=destination
        ))
        
        return jsonify({
            "success": True,
            "withdrawal_request": result
        }), 201
        
    except Exception as e:
        logger.error(f"Failed to request withdrawal: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to request withdrawal",
            "message": str(e)
        }), 500
