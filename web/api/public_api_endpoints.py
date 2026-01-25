"""
==============================================================================
FILE: web/api/public_api_endpoints.py
ROLE: Public API Endpoints
PURPOSE: REST endpoints for public API and developer platform.

INTEGRATION POINTS:
    - PublicAPIService: API management
    - DeveloperPortalService: Developer resources
    - FrontendDeveloper: Developer portal

ENDPOINTS:
    - POST /api/public/api-key/create
    - GET /api/public/api-key/:api_key_id
    - GET /api/public/documentation
    - GET /api/public/sdks

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.public_api.public_api_service import get_public_api_service
from services.public_api.developer_portal_service import get_developer_portal_service

logger = logging.getLogger(__name__)

public_api_bp = Blueprint('public_api', __name__, url_prefix='/api/public')


@public_api_bp.route('/api-key/create', methods=['POST'])
async def create_api_key():
    """
    Create API key.
    
    Request body:
        user_id: User identifier
        tier: API tier (default: free)
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        tier = data.get('tier', 'free')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id is required'
            }), 400
        
        service = get_public_api_service()
        api_key = await service.create_api_key(user_id, tier)
        
        return jsonify({
            'success': True,
            'data': api_key.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating API key: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@public_api_bp.route('/api-key/<api_key_id>', methods=['GET'])
async def get_api_key(api_key_id: str):
    """
    Get API key details.
    """
    try:
        service = get_public_api_service()
        api_key = await service._get_api_key(api_key_id)
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': api_key.dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting API key: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@public_api_bp.route('/documentation', methods=['GET'])
async def get_documentation():
    """
    Get API documentation.
    """
    try:
        service = get_developer_portal_service()
        docs = await service.get_api_documentation()
        
        return jsonify({
            'success': True,
            'data': docs
        })
        
    except Exception as e:
        logger.error(f"Error getting documentation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@public_api_bp.route('/sdks', methods=['GET'])
async def get_sdks():
    """
    Get available SDKs.
    """
    try:
        service = get_developer_portal_service()
        sdks = await service.get_sdks()
        
        return jsonify({
            'success': True,
            'data': sdks
        })
        
    except Exception as e:
        logger.error(f"Error getting SDKs: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
