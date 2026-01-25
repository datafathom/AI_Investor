"""
==============================================================================
FILE: web/api/ethereum_api.py
ROLE: Ethereum API REST Endpoints
PURPOSE: RESTful endpoints for Ethereum wallet balance and token queries.

INTEGRATION POINTS:
    - EthereumClient: Wallet balance retrieval
    - WalletService: Portfolio sync

ENDPOINTS:
    GET /api/v1/ethereum/balance/{address} - Get ETH balance
    GET /api/v1/ethereum/tokens/{address} - Get ERC-20 token balances
    GET /api/v1/ethereum/gas-price - Get current gas price
    POST /api/v1/ethereum/validate-address - Validate address format

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio

logger = logging.getLogger(__name__)

ethereum_bp = Blueprint('ethereum', __name__, url_prefix='/api/v1/ethereum')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# =============================================================================
# Get ETH Balance Endpoint
# =============================================================================

@ethereum_bp.route('/balance/<address>', methods=['GET'])
def get_balance(address: str):
    """
    Get ETH balance for an address.
    
    Returns:
        JSON with balance
    """
    try:
        from services.crypto.ethereum_client import get_eth_client
        client = get_eth_client()
        
        balance = _run_async(client.get_eth_balance(address))
        
        return jsonify({
            "address": address,
            "balance_eth": balance,
            "balance_wei": int(balance * 1e18) if balance else 0
        })
        
    except Exception as e:
        logger.error(f"Failed to get ETH balance: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get balance",
            "message": str(e)
        }), 500


# =============================================================================
# Get Token Balances Endpoint
# =============================================================================

@ethereum_bp.route('/tokens/<address>', methods=['GET'])
def get_tokens(address: str):
    """
    Get all ERC-20 token balances for an address.
    
    Returns:
        JSON array of token balances
    """
    try:
        from services.crypto.ethereum_client import get_eth_client
        client = get_eth_client()
        
        tokens = _run_async(client.get_all_token_balances(address))
        
        return jsonify({
            "address": address,
            "tokens": tokens,
            "count": len(tokens)
        })
        
    except Exception as e:
        logger.error(f"Failed to get token balances: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get token balances",
            "message": str(e)
        }), 500


# =============================================================================
# Get Gas Price Endpoint
# =============================================================================

@ethereum_bp.route('/gas-price', methods=['GET'])
def get_gas_price():
    """
    Get current gas price estimate.
    
    Returns:
        JSON with gas price in Gwei
    """
    try:
        from services.crypto.ethereum_client import get_eth_client
        client = get_eth_client()
        
        gas_price = _run_async(client.get_gas_price())
        
        return jsonify({
            "gas_price_gwei": gas_price,
            "gas_price_wei": gas_price * 1e9
        })
        
    except Exception as e:
        logger.error(f"Failed to get gas price: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get gas price",
            "message": str(e)
        }), 500


# =============================================================================
# Validate Address Endpoint
# =============================================================================

@ethereum_bp.route('/validate-address', methods=['POST'])
def validate_address():
    """
    Validate Ethereum address format.
    
    Request Body:
        {
            "address": "0x..."
        }
        
    Returns:
        JSON with validation result
    """
    try:
        data = request.json or {}
        address = data.get('address')
        
        if not address:
            return jsonify({
                "error": "Missing address"
            }), 400
        
        from services.crypto.ethereum_client import get_eth_client
        client = get_eth_client()
        
        is_valid = client.validate_address(address)
        
        return jsonify({
            "address": address,
            "valid": is_valid
        })
        
    except Exception as e:
        logger.error(f"Address validation failed: {e}", exc_info=True)
        return jsonify({
            "error": "Validation failed",
            "message": str(e)
        }), 500
