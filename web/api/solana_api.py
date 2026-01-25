"""
==============================================================================
FILE: web/api/solana_api.py
ROLE: Solana API REST Endpoints
PURPOSE: RESTful endpoints for Solana wallet balance and SPL token queries.

INTEGRATION POINTS:
    - SolanaClient: Wallet balance retrieval
    - SolanaTokenRegistry: Token metadata lookup
    - WalletService: Portfolio sync

ENDPOINTS:
    GET /api/v1/solana/balance/{address} - Get SOL balance
    GET /api/v1/solana/tokens/{address} - Get SPL token balances
    GET /api/v1/solana/transactions/{address} - Get transaction history
    GET /api/v1/solana/token-info/{mint} - Get token metadata

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio

logger = logging.getLogger(__name__)

solana_bp = Blueprint('solana', __name__, url_prefix='/api/v1/solana')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# =============================================================================
# Get SOL Balance Endpoint
# =============================================================================

@solana_bp.route('/balance/<address>', methods=['GET'])
def get_balance(address: str):
    """
    Get SOL balance for an address.
    
    Returns:
        JSON with balance
    """
    try:
        from services.crypto.solana_client import get_solana_client
        client = get_solana_client()
        
        balance = _run_async(client.get_sol_balance(address))
        
        return jsonify({
            "address": address,
            "balance_sol": balance,
            "balance_lamports": int(balance * 1e9) if balance else 0
        })
        
    except Exception as e:
        logger.error(f"Failed to get SOL balance: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get balance",
            "message": str(e)
        }), 500


# =============================================================================
# Get SPL Tokens Endpoint
# =============================================================================

@solana_bp.route('/tokens/<address>', methods=['GET'])
def get_tokens(address: str):
    """
    Get SPL token balances for an address.
    
    Returns:
        JSON array of token balances
    """
    try:
        from services.crypto.solana_client import get_solana_client
        client = get_solana_client()
        
        tokens = _run_async(client.get_spl_tokens(address))
        
        return jsonify({
            "address": address,
            "tokens": tokens,
            "count": len(tokens)
        })
        
    except Exception as e:
        logger.error(f"Failed to get SPL tokens: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get tokens",
            "message": str(e)
        }), 500


# =============================================================================
# Get Transaction History Endpoint
# =============================================================================

@solana_bp.route('/transactions/<address>', methods=['GET'])
def get_transactions(address: str):
    """
    Get transaction history with parsed instructions.
    
    Query Params:
        limit: Maximum transactions (default 50)
        
    Returns:
        JSON array of transactions
    """
    try:
        limit = int(request.args.get('limit', 50))
        
        from services.crypto.solana_client import get_solana_client
        client = get_solana_client()
        
        transactions = _run_async(client.get_transaction_history(address, limit=limit))
        
        return jsonify({
            "address": address,
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
# Get Token Info Endpoint
# =============================================================================

@solana_bp.route('/token-info/<mint>', methods=['GET'])
def get_token_info(mint: str):
    """
    Get token metadata from registry.
    
    Returns:
        JSON with token info
    """
    try:
        from services.crypto.solana_token_registry import get_token_registry
        registry = get_token_registry()
        
        token_info = registry.get_token_info(mint)
        
        return jsonify({
            "mint": mint,
            "token_info": token_info
        })
        
    except Exception as e:
        logger.error(f"Failed to get token info: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get token info",
            "message": str(e)
        }), 500
