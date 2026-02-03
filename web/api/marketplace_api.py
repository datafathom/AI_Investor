"""
==============================================================================
FILE: web/api/marketplace_api.py
ROLE: Marketplace API Endpoints
PURPOSE: REST endpoints for extension marketplace.

INTEGRATION POINTS:
    - ExtensionFramework: Extension infrastructure
    - MarketplaceService: Marketplace management
    - FrontendMarketplace: Marketplace dashboard

ENDPOINTS:
    - POST /api/marketplace/extension/create
    - GET /api/marketplace/extensions
    - POST /api/marketplace/extension/:extension_id/install
    - POST /api/marketplace/extension/:extension_id/review

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.marketplace.extension_framework import get_extension_framework
from services.marketplace.marketplace_service import get_marketplace_service

logger = logging.getLogger(__name__)

marketplace_bp = Blueprint('marketplace', __name__, url_prefix='/api/v1/marketplace')


@marketplace_bp.route('/extension/create', methods=['POST'])
async def create_extension():
    """
    Create extension.
    
    Request body:
        developer_id: Developer identifier
        extension_name: Extension name
        description: Extension description
        version: Extension version
        category: Extension category
    """
    try:
        data = request.get_json() or {}
        developer_id = data.get('developer_id')
        extension_name = data.get('extension_name')
        description = data.get('description')
        version = data.get('version')
        category = data.get('category')
        
        if not all([developer_id, extension_name, description, version, category]):
            return jsonify({
                'success': False,
                'error': 'developer_id, extension_name, description, version, and category are required'
            }), 400
        
        framework = get_extension_framework()
        extension = await framework.create_extension(
            developer_id=developer_id,
            extension_name=extension_name,
            description=description,
            version=version,
            category=category
        )
        
        return jsonify({
            'success': True,
            'data': extension.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating extension: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@marketplace_bp.route('/extensions', methods=['GET'])
async def get_extensions():
    """
    Get available extensions.
    
    Query params:
        category: Optional category filter
    """
    try:
        category = request.args.get('category')
        
        # In production, would query database
        return jsonify({
            'success': True,
            'data': []
        })
        
    except Exception as e:
        logger.error(f"Error getting extensions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@marketplace_bp.route('/extension/<extension_id>/install', methods=['POST'])
async def install_extension(extension_id: str):
    """
    Install extension.
    
    Request body:
        user_id: User identifier
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id is required'
            }), 400
        
        service = get_marketplace_service()
        installation = await service.install_extension(extension_id, user_id)
        
        return jsonify({
            'success': True,
            'data': installation
        })
        
    except Exception as e:
        logger.error(f"Error installing extension: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@marketplace_bp.route('/extension/<extension_id>/review', methods=['POST'])
async def add_review(extension_id: str):
    """
    Add review for extension.
    
    Request body:
        user_id: User identifier
        rating: Rating (1-5)
        comment: Optional comment
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        rating = int(data.get('rating', 0))
        comment = data.get('comment')
        
        if not user_id or not rating:
            return jsonify({
                'success': False,
                'error': 'user_id and rating are required'
            }), 400
        
        if rating < 1 or rating > 5:
            return jsonify({
                'success': False,
                'error': 'rating must be between 1 and 5'
            }), 400
        
        service = get_marketplace_service()
        review = await service.add_review(extension_id, user_id, rating, comment)
        
        return jsonify({
            'success': True,
            'data': review.dict()
        })
        
    except Exception as e:
        logger.error(f"Error adding review: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
