"""
==============================================================================
FILE: web/api/square_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes Square merchant capabilities to the frontend.
==============================================================================
"""

import asyncio
import logging
from datetime import datetime
from flask import Blueprint, jsonify, request

from services.payments.square_service import get_square_client

logger = logging.getLogger(__name__)

square_bp = Blueprint('square_bp', __name__, url_prefix='/api/v1/square')

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@square_bp.route('/merchant/square/stats', methods=['GET'])
def get_stats():
    """
    Get merchant stats.
    Query: ?mock=true
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_square_client(mock=use_mock)
    
    try:
        result = _run_async(client.get_merchant_stats())
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to fetch Square stats: %s", e)
        return jsonify({"error": str(e)}), 500

@square_bp.route('/merchant/square/catalog', methods=['GET'])
def get_catalog():
    """
    Get merchant catalog.
    Query: ?mock=true
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_square_client(mock=use_mock)
    
    try:
        result = _run_async(client.get_catalog())
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to fetch Square catalog: %s", e)
        return jsonify({"error": str(e)}), 500


@square_bp.route('/api/v1/square/stats', methods=['GET'])
def get_stats_v1():
    """
    Get merchant stats (v1 API).
    Query: ?range=daily|weekly|monthly
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_square_client(mock=use_mock)
    
    try:
        result = _run_async(client.get_merchant_stats())
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to fetch Square stats: {e}")
        return jsonify({"error": str(e)}), 500


@square_bp.route('/api/v1/square/transactions', methods=['GET'])
def get_transactions():
    """Get transaction history."""
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_square_client(mock=use_mock)

    try:
        
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        location_id = request.args.get('location_id')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        transactions = _run_async(client.get_transactions(
            start_date=start_date,
            end_date=end_date,
            location_id=location_id
        ))
        
        return jsonify({
            "transactions": transactions,
            "count": len(transactions)
        })
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to get transactions: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500


@square_bp.route('/api/v1/square/refunds', methods=['GET'])
def get_refunds():
    """Get refund history."""
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_square_client(mock=use_mock)

    try:
        
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        refunds = _run_async(client.get_refunds(
            start_date=start_date,
            end_date=end_date
        ))
        
        return jsonify({
            "refunds": refunds,
            "count": len(refunds)
        })
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to get refunds: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500