"""
==============================================================================
FILE: apis/binance_api.py
ROLE: REST API for Binance Data
PURPOSE: Exposes Binance Service functionality to the frontend.
         
INTEGRATION POINTS:
    - BinanceService: Data source.
    - Frontend: Consumer.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

from flask import Blueprint, request, jsonify
from services.data.binance_service import get_binance_client
import logging

binance_bp = Blueprint('binance_api', __name__)
logger = logging.getLogger(__name__)

# TODO: Get mock status from config/env
MOCK_MODE = True 

@binance_bp.route('/api/binance/ticker/<symbol>', methods=['GET'])
async def get_ticker(symbol):
    """
    Get 24hr ticker price change statistics.
    """
    try:
        client = get_binance_client(mock=MOCK_MODE)
        data = await client.get_ticker(symbol.upper())
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting ticker for {symbol}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@binance_bp.route('/api/binance/depth/<symbol>', methods=['GET'])
async def get_order_book(symbol):
    """
    Get order book depth.
    Query Params: limit (default 5)
    """
    try:
        limit = int(request.args.get('limit', 5))
        client = get_binance_client(mock=MOCK_MODE)
        data = await client.get_order_book(symbol.upper(), limit=limit)
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting order book for {symbol}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@binance_bp.route('/api/binance/order', methods=['POST'])
async def place_order():
    """
    Place a new order.
    Body: {symbol, side, quantity, price(optional)}
    """
    try:
        data = request.json
        symbol = data.get('symbol')
        side = data.get('side')
        quantity = float(data.get('quantity'))
        price = float(data.get('price')) if 'price' in data else None
        
        if not all([symbol, side, quantity]):
            return jsonify({"error": "Missing required fields"}), 400
            
        client = get_binance_client(mock=MOCK_MODE)
        result = await client.place_order(symbol.upper(), side, quantity, price)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error placing order: {str(e)}")
        return jsonify({"error": str(e)}), 500
