"""
==============================================================================
FILE: web/api/integration_api.py
ROLE: Integration API Endpoints
PURPOSE: REST endpoints for third-party app integrations.

INTEGRATION POINTS:
    - IntegrationFramework: Integration infrastructure
    - IntegrationService: Integration management
    - FrontendIntegration: Integration dashboard

ENDPOINTS:
    - POST /api/integration/create
    - GET /api/integration/user/:user_id
    - POST /api/integration/:integration_id/sync

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.integration.integration_framework import get_integration_framework
from services.integration.integration_service import get_integration_service

logger = logging.getLogger(__name__)

integration_bp = Blueprint('integration', __name__, url_prefix='/api/v1/integration')


@integration_bp.route('/create', methods=['POST'])
async def create_integration():
    """
    Create integration connection.
    
    Request body:
        user_id: User identifier
        app_name: App name
        oauth_token: Optional OAuth token
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        app_name = data.get('app_name')
        oauth_token = data.get('oauth_token')
        
        if not user_id or not app_name:
            return jsonify({
                'success': False,
                'error': 'user_id and app_name are required'
            }), 400
        
        framework = get_integration_framework()
        integration = await framework.create_integration(user_id, app_name, oauth_token)
        
        return jsonify({
            'success': True,
            'data': integration.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error creating integration: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@integration_bp.route('/user/<user_id>', methods=['GET'])
async def get_user_integrations(user_id: str):
    """
    Get integrations for user.
    """
    try:
        # In production, would fetch from database
        return jsonify({
            'success': True,
            'data': []
        })
        
    except Exception as e:
        logger.error(f"Error getting integrations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@integration_bp.route('/<integration_id>/sync', methods=['POST'])
async def sync_integration(integration_id: str):
    """
    Sync data from integration.
    
    Request body:
        sync_type: Sync type (default: incremental)
    """
    try:
        data = request.get_json() or {}
        sync_type = data.get('sync_type', 'incremental')
        
        service = get_integration_service()
        job = await service.sync_data(integration_id, sync_type)
        
        return jsonify({
            'success': True,
            'data': job.model_dump() if hasattr(job, 'model_dump') else job
        })
        
    except Exception as e:
        logger.error(f"Error syncing integration: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
