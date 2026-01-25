"""
==============================================================================
FILE: web/api/tax_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes TaxBit analysis to the frontend.
==============================================================================
"""

from flask import Blueprint, jsonify, request
import asyncio
import logging

from services.taxes.taxbit_service import get_taxbit_client

logger = logging.getLogger(__name__)

tax_api_bp = Blueprint('tax_api_bp', __name__)

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@tax_api_bp.route('/tax/harvesting/opportunities', methods=['GET'])
def get_opportunities():
    """
    Get tax loss harvesting opportunities.
    Query: ?mock=true
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    portfolio_id = "port_mock_001"
    
    client = get_taxbit_client(mock=use_mock)
    
    try:
        result = _run_async(client.get_harvesting_opportunities(portfolio_id))
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to fetch tax analysis: {e}")
        return jsonify({"error": str(e)}), 500
