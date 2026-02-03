"""
==============================================================================
FILE: web/api/enterprise_api.py
ROLE: Enterprise API Endpoints
PURPOSE: REST endpoints for enterprise features and multi-user support.

INTEGRATION POINTS:
    - EnterpriseService: Team management
    - MultiUserService: Collaboration
    - FrontendEnterprise: Enterprise dashboard

ENDPOINTS:
    - POST /api/enterprise/organization/create
    - POST /api/enterprise/team/create
    - POST /api/enterprise/team/:team_id/member
    - POST /api/enterprise/resource/share

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.enterprise.enterprise_service import get_enterprise_service
from services.enterprise.multi_user_service import get_multi_user_service

logger = logging.getLogger(__name__)

enterprise_bp = Blueprint('enterprise', __name__, url_prefix='/api/v1/enterprise')


@enterprise_bp.route('/organization/create', methods=['POST'])
async def create_organization():
    """
    Create organization.
    
    Request body:
        name: Organization name
        parent_organization_id: Optional parent organization
    """
    try:
        data = request.get_json() or {}
        name = data.get('name')
        parent_organization_id = data.get('parent_organization_id')
        
        if not name:
            return jsonify({
                'success': False,
                'error': 'name is required'
            }), 400
        
        service = get_enterprise_service()
        organization = await service.create_organization(name, parent_organization_id)
        
        return jsonify({
            'success': True,
            'data': organization.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating organization: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@enterprise_bp.route('/team/create', methods=['POST'])
async def create_team():
    """
    Create team.
    
    Request body:
        organization_id: Organization identifier
        team_name: Team name
    """
    try:
        data = request.get_json() or {}
        organization_id = data.get('organization_id')
        team_name = data.get('team_name')
        
        if not organization_id or not team_name:
            return jsonify({
                'success': False,
                'error': 'organization_id and team_name are required'
            }), 400
        
        service = get_enterprise_service()
        team = await service.create_team(organization_id, team_name)
        
        return jsonify({
            'success': True,
            'data': team.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating team: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@enterprise_bp.route('/team/<team_id>/member', methods=['POST'])
async def add_team_member(team_id: str):
    """
    Add member to team.
    
    Request body:
        user_id: User identifier
        role: Team role
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        role = data.get('role')
        
        if not user_id or not role:
            return jsonify({
                'success': False,
                'error': 'user_id and role are required'
            }), 400
        
        service = get_enterprise_service()
        team = await service.add_team_member(team_id, user_id, role)
        
        return jsonify({
            'success': True,
            'data': team.dict()
        })
        
    except Exception as e:
        logger.error(f"Error adding team member: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@enterprise_bp.route('/resource/share', methods=['POST'])
async def share_resource():
    """
    Share resource with team.
    
    Request body:
        resource_type: Resource type
        resource_id: Resource identifier
        team_id: Team identifier
        permissions: Permission dictionary
    """
    try:
        data = request.get_json() or {}
        resource_type = data.get('resource_type')
        resource_id = data.get('resource_id')
        team_id = data.get('team_id')
        permissions = data.get('permissions', {})
        
        if not all([resource_type, resource_id, team_id]):
            return jsonify({
                'success': False,
                'error': 'resource_type, resource_id, and team_id are required'
            }), 400
        
        service = get_multi_user_service()
        shared_resource = await service.share_resource(
            resource_type=resource_type,
            resource_id=resource_id,
            team_id=team_id,
            permissions=permissions
        )
        
        return jsonify({
            'success': True,
            'data': shared_resource.dict()
        })
        
    except Exception as e:
        logger.error(f"Error sharing resource: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
