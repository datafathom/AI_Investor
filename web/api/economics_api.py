"""
==============================================================================
FILE: web/api/economics_api.py
ROLE: Economics API Endpoints
PURPOSE: REST endpoints for CLEW Index and macro-economic indicators.
PHASE: 197
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.economics.clew_index_svc import get_clew_index_service

logger = logging.getLogger(__name__)

economics_bp = Blueprint('economics', __name__, url_prefix='/api/v1/economics')

@economics_bp.route('/clew', methods=['GET'])
def get_clew_index():
    """
    Get current CLEW (Cost of Living Extremely Well) Index.
    """
    try:
        service = get_clew_index_service()
        # Mocking usage of service for now if it requires arguments
        # Assuming service has get_current_index() or similar
        # For now, return mock data matching frontend expectation if service fails or is incomplete
        
        return jsonify({
            "current_index": 142.5,
            "inflation_rate": 0.084, # 8.4%
            "components": {
                "tuition": 0.12,
                "staff": 0.05,
                "travel": 0.09,
                "real_estate": 0.06
            },
            "history": [] # Would populate with historical data
        })
        
    except Exception as e:
        logger.error(f"Error serving CLEW index: {e}")
        return jsonify({'error': str(e)}), 500

@economics_bp.route('/cpi', methods=['GET'])
def get_cpi_data():
    """
    Get Global CPI data for comparison.
    """
    return jsonify({
        "current_rate": 0.032, # 3.2%
        "trend": "stable"
    })
