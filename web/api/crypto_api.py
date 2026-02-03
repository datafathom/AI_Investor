"""
==============================================================================
FILE: web/api/crypto_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes real-time crypto prices and volume data.
==============================================================================
"""

import asyncio
import logging
from flask import Blueprint, jsonify, request

from services.data.crypto_compare_service import get_crypto_client

logger = logging.getLogger(__name__)

crypto_api_bp = Blueprint('crypto_api_bp', __name__, url_prefix='/api/v1/crypto')

def _run_async(coro):
    return asyncio.run(coro)

@crypto_api_bp.route('/api/v1/market/crypto/price', methods=['GET'])
def get_crypto_price():
    """
    Get real-time prices for multiple symbols.
    Query: ?symbols=BTC,ETH&currencies=USD,EUR&mock=false
    """
    symbols = request.args.get('symbols', 'BTC,ETH').split(',')
    currencies = request.args.get('currencies', 'USD').split(',')
    use_mock = request.args.get('mock', 'false').lower() == 'true'
    
    client = get_crypto_client()
    if use_mock:
        client.mock = True
        
    try:
        results = _run_async(client.get_price(symbols, currencies))
        return jsonify(results)
    except (RuntimeError, ValueError) as e:
        logger.error("Failed to fetch crypto prices: %s", e)
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.exception("Unexpected error fetching crypto prices: %s", e)
        return jsonify({"error": "An unexpected error occurred"}), 500

@crypto_api_bp.route('/api/v1/market/crypto/volume/<symbol>', methods=['GET'])
def get_crypto_volume(symbol: str):
    """
    Get exchange volume data for a symbol.
    """
    use_mock = request.args.get('mock', 'false').lower() == 'true'
    client = get_crypto_client()
    if use_mock:
        client.mock = True
        
    try:
        results = _run_async(client.get_top_exchanges_volume(symbol))
        return jsonify([r.model_dump() for r in results])
    except (RuntimeError, ValueError) as e:
        logger.error("Failed to fetch volume for %s: %s", symbol, e)
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.exception("Unexpected error fetching volume for %s: %s", symbol, e)
        return jsonify({"error": "An unexpected error occurred"}), 500
