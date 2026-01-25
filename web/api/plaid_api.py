"""
==============================================================================
FILE: web/api/plaid_api.py
ROLE: Plaid API REST Endpoints
PURPOSE: RESTful endpoints for Plaid bank account linking and balance checks.

INTEGRATION POINTS:
    - PlaidService: Bank account linking
    - PlaidLinkModal: Frontend Link initialization

ENDPOINTS:
    POST /api/v1/plaid/link-token - Create link token
    POST /api/v1/plaid/exchange-token - Exchange public token
    GET /api/v1/plaid/accounts - Get linked accounts
    GET /api/v1/plaid/balance - Get account balance
    POST /api/v1/plaid/check-overdraft - Check overdraft protection

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import asyncio
import logging
from typing import Optional
from flask import Blueprint, request, jsonify

logger = logging.getLogger(__name__)

plaid_bp = Blueprint('plaid', __name__, url_prefix='/api/v1/plaid')


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
# Create Link Token Endpoint
# =============================================================================

@plaid_bp.route('/link-token', methods=['POST'])
def create_link_token():
    """
    Create Plaid Link token for frontend initialization.
    
    Request Body:
        {
            "client_name": "AI Investor"  // optional
        }
        
    Returns:
        JSON with link_token
    """
    try:
        data = request.json or {}
        user_id = _get_user_id()
        client_name = data.get('client_name', 'AI Investor')
        
        from services.banking.plaid_service import get_plaid_service
        plaid_service = get_plaid_service()
        
        link_token = _run_async(plaid_service.create_link_token(
            user_id=user_id,
            client_name=client_name
        ))
        
        return jsonify({
            "link_token": link_token,
            "expiration": None  # Link tokens expire quickly
        })
        
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to create link token: %s", e, exc_info=True)
        return jsonify({
            "error": "Failed to create link token",
            "message": str(e)
        }), 500


# =============================================================================
# Exchange Public Token Endpoint
# =============================================================================

@plaid_bp.route('/exchange-token', methods=['POST'])
def exchange_token():
    """
    Exchange public token for access token.
    
    Request Body:
        {
            "public_token": "public-sandbox-..."
        }
        
    Returns:
        JSON with access_token and account metadata
    """
    try:
        data = request.json or {}
        public_token = data.get('public_token')
        user_id = _get_user_id()
        
        if not public_token:
            return jsonify({
                "error": "Missing public_token"
            }), 400
        
        from services.banking.plaid_service import get_plaid_service
        plaid_service = get_plaid_service()
        
        result = _run_async(plaid_service.exchange_public_token(
            public_token=public_token,
            user_id=user_id
        ))
        
        # In production: Store encrypted access_token in database
        # For now, return it (frontend should send it back for balance checks)
        
        return jsonify({
            "success": True,
            "item_id": result.get("item_id"),
            "accounts": result.get("accounts", []),
            # Note: In production, access_token should be stored server-side only
            "access_token": result.get("access_token")  # Remove in production
        })
        
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to exchange token: %s", e, exc_info=True)
        return jsonify({
            "error": "Failed to exchange token",
            "message": str(e)
        }), 500


# =============================================================================
# Get Accounts Endpoint
# =============================================================================

@plaid_bp.route('/accounts', methods=['GET'])
def get_accounts():
    """
    Get linked bank accounts.
    
    Headers:
        Authorization: Bearer {access_token}
        
    Returns:
        JSON with accounts list
    """
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "error": "Missing or invalid Authorization header"
            }), 401
        
        access_token = auth_header[7:]  # Remove "Bearer " prefix
        
        from services.banking.plaid_service import get_plaid_service
        plaid_service = get_plaid_service()
        
        accounts = _run_async(plaid_service.get_accounts(access_token))
        
        return jsonify({
            "accounts": accounts
        })
        
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to get accounts: %s", e, exc_info=True)
        return jsonify({
            "error": "Failed to get accounts",
            "message": str(e)
        }), 500


# =============================================================================
# Get Balance Endpoint
# =============================================================================

@plaid_bp.route('/balance', methods=['GET'])
def get_balance():
    """
    Get account balance(s).
    Rate-limited to 3 checks per hour per user.
    
    Query Params:
        account_id: Specific account ID (optional)
        
    Headers:
        Authorization: Bearer {access_token}
        X-User-ID: User ID for rate limiting
        
    Returns:
        JSON with balance information
    """
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "error": "Missing or invalid Authorization header"
            }), 401
        
        access_token = auth_header[7:]
        account_id = request.args.get('account_id')
        user_id = _get_user_id()
        
        from services.banking.plaid_service import get_plaid_service
        plaid_service = get_plaid_service()
        
        balance_data = _run_async(plaid_service.get_balance(
            access_token=access_token,
            account_id=account_id,
            user_id=user_id
        ))
        
        return jsonify(balance_data)
        
    except RuntimeError as e:
        if "rate limit" in str(e).lower():
            return jsonify({
                "error": "Rate limit exceeded",
                "message": str(e)
            }), 429
        raise
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to get balance: %s", e, exc_info=True)
        return jsonify({
            "error": "Failed to get balance",
            "message": str(e)
        }), 500


# =============================================================================
# Check Overdraft Protection Endpoint
# =============================================================================

@plaid_bp.route('/check-overdraft', methods=['POST'])
def check_overdraft():
    """
    Check if account has sufficient balance for deposit.
    
    Request Body:
        {
            "account_id": "acc-...",
            "deposit_amount": 1000.00
        }
        
    Headers:
        Authorization: Bearer {access_token}
        X-User-ID: User ID
        
    Returns:
        JSON with overdraft warning if applicable
    """
    try:
        data = request.json or {}
        account_id = data.get('account_id')
        deposit_amount = data.get('deposit_amount')
        
        if not account_id or deposit_amount is None:
            return jsonify({
                "error": "Missing account_id or deposit_amount"
            }), 400
        
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "error": "Missing or invalid Authorization header"
            }), 401
        
        access_token = auth_header[7:]
        user_id = _get_user_id()
        
        from services.banking.plaid_service import get_plaid_service
        plaid_service = get_plaid_service()
        
        result = _run_async(plaid_service.check_overdraft_protection(
            access_token=access_token,
            account_id=account_id,
            deposit_amount=deposit_amount,
            user_id=user_id
        ))
        
        return jsonify(result)
        
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to check overdraft: %s", e, exc_info=True)
        return jsonify({
            "error": "Failed to check overdraft protection",
            "message": str(e)
        }), 500
