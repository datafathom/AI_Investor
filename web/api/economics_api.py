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
        index = float(service.calculate_current_index())
        inflation = float(service.get_uhnwi_inflation_rate())
        
        return jsonify({
            "current_index": index,
            "inflation_rate": inflation,
            "components": {
                "tuition": 0.12,
                "staff": 0.05,
                "travel": 0.09,
                "real_estate": 0.06
            },
            "status": "success"
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
