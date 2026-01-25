"""
==============================================================================
FILE: web/api/robinhood_api.py
ROLE: Robinhood API REST Endpoints
PURPOSE: RESTful endpoints for Robinhood portfolio sync and connection management.

INTEGRATION POINTS:
    - RobinhoodClient: Portfolio data retrieval
    - PortfolioAggregator: Unified portfolio aggregation

ENDPOINTS:
    POST /api/v1/robinhood/connect - Connect Robinhood account
    GET /api/v1/robinhood/holdings - Get portfolio holdings
    GET /api/v1/robinhood/orders - Get order history
    GET /api/v1/robinhood/transactions - Get historical transactions
    GET /api/v1/robinhood/cost-basis - Calculate cost basis

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

robinhood_bp = Blueprint('robinhood', __name__, url_prefix='/api/v1/robinhood')


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


# =============================================================================
# Connect Account Endpoint
# =============================================================================

@robinhood_bp.route('/connect', methods=['POST'])
def connect_account():
    """
    Connect Robinhood account with credentials.
    
    Request Body:
        {
            "username": "robinhood_username",
            "password": "robinhood_password",
            "mfa_code": "123456"  // optional if MFA required
        }
        
    Returns:
        JSON with connection status
    """
    try:
        data = request.json or {}
        username = data.get('username')
        password = data.get('password')
        mfa_code = data.get('mfa_code')
        
        if not username or not password:
            return jsonify({
                "error": "Missing username or password"
            }), 400
        
        from services.brokerage.robinhood_client import get_robinhood_client
        client = get_robinhood_client()
        
        success = _run_async(client.login(username, password, mfa_code))
        
        if success:
            # In production: Store encrypted credentials securely
            return jsonify({
                "success": True,
                "message": "Robinhood account connected successfully",
                "connected_at": asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0
            })
        else:
            return jsonify({
                "error": "Authentication failed",
                "message": "Invalid credentials or MFA code"
            }), 401
        
    except Exception as e:
        logger.error(f"Robinhood connection failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to connect Robinhood account",
            "message": str(e)
        }), 500


# =============================================================================
# Get Holdings Endpoint
# =============================================================================

@robinhood_bp.route('/holdings', methods=['GET'])
def get_holdings():
    """
    Get portfolio holdings.
    
    Returns:
        JSON array of holdings
    """
    try:
        from services.brokerage.robinhood_client import get_robinhood_client
        client = get_robinhood_client()
        
        holdings = _run_async(client.get_holdings())
        
        return jsonify({
            "holdings": holdings,
            "count": len(holdings)
        })
        
    except Exception as e:
        logger.error(f"Failed to get holdings: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get holdings",
            "message": str(e)
        }), 500


# =============================================================================
# Get Orders Endpoint
# =============================================================================

@robinhood_bp.route('/orders', methods=['GET'])
def get_orders():
    """
    Get order history.
    
    Query Params:
        limit: Maximum orders to return (default 100)
        
    Returns:
        JSON array of orders
    """
    try:
        limit = int(request.args.get('limit', 100))
        
        from services.brokerage.robinhood_client import get_robinhood_client
        client = get_robinhood_client()
        
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
# Get Transactions Endpoint
# =============================================================================

@robinhood_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Get historical transactions for tax reporting.
    
    Query Params:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        
    Returns:
        JSON array of transactions
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        from services.brokerage.robinhood_client import get_robinhood_client
        client = get_robinhood_client()
        
        transactions = _run_async(client.get_historical_transactions(
            start_date=start_date,
            end_date=end_date
        ))
        
        return jsonify({
            "transactions": transactions,
            "count": len(transactions)
        })
        
    except Exception as e:
        logger.error(f"Failed to get transactions: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get transactions",
            "message": str(e)
        }), 500


# =============================================================================
# Calculate Cost Basis Endpoint
# =============================================================================

@robinhood_bp.route('/cost-basis', methods=['GET'])
def calculate_cost_basis():
    """
    Calculate cost basis and gains for a position.
    
    Query Params:
        symbol: Stock or crypto symbol
        
    Returns:
        JSON with cost basis calculation
    """
    try:
        symbol = request.args.get('symbol')
        
        if not symbol:
            return jsonify({
                "error": "Missing symbol parameter"
            }), 400
        
        from services.brokerage.robinhood_client import get_robinhood_client
        client = get_robinhood_client()
        
        result = _run_async(client.calculate_cost_basis(symbol))
        
        if "error" in result:
            return jsonify(result), 404
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Failed to calculate cost basis: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to calculate cost basis",
            "message": str(e)
        }), 500
