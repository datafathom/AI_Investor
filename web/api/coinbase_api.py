"""
==============================================================================
FILE: web/api/coinbase_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes Coinbase wallet capabilities to the frontend.
==============================================================================
"""

from flask import Blueprint, jsonify, request
import asyncio
import logging

from services.payments.coinbase_service import get_coinbase_client

logger = logging.getLogger(__name__)

coinbase_bp = Blueprint('coinbase_bp', __name__)

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@coinbase_bp.route('/wallet/coinbase/connect', methods=['POST'])
def connect_wallet():
    """
    Connect Coinbase Wallet (Mock).
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    user_id = "user_mock_123"
    
    client = get_coinbase_client(mock=use_mock)
    
    try:
        result = _run_async(client.connect_wallet(user_id))
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to connect wallet: {e}")
        return jsonify({"error": str(e)}), 500

@coinbase_bp.route('/wallet/coinbase/balance', methods=['GET'])
def get_balance():
    """
    Get wallet balance.
    Query: ?mock=true
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_coinbase_client(mock=use_mock)
    
    try:
        result = _run_async(client.get_wallet_balance())
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to fetch balance: {e}")
        return jsonify({"error": str(e)}), 500

@coinbase_bp.route('/wallet/coinbase/transactions', methods=['GET'])
def get_transactions():
    """
    Get wallet transactions.
    Query: ?mock=true
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_coinbase_client(mock=use_mock)
    
    try:
        result = _run_async(client.get_transactions())
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to fetch transactions: {e}")
        return jsonify({"error": str(e)}), 500
