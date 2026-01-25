"""
==============================================================================
FILE: web/api/institutional_api.py
ROLE: Institutional API Endpoints
PURPOSE: REST endpoints for institutional features and professional tools.

INTEGRATION POINTS:
    - InstitutionalService: Multi-client management
    - ProfessionalToolsService: Professional tools
    - FrontendInstitutional: Institutional dashboard

ENDPOINTS:
    - POST /api/institutional/client/create
    - POST /api/institutional/whitelabel/configure
    - POST /api/institutional/report/generate

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.institutional.institutional_service import get_institutional_service
from services.institutional.professional_tools_service import get_professional_tools_service

logger = logging.getLogger(__name__)

institutional_bp = Blueprint('institutional', __name__, url_prefix='/api/institutional')


@institutional_bp.route('/client/create', methods=['POST'])
async def create_client():
    """
    Create client for advisor.
    
    Request body:
        advisor_id: Advisor identifier
        client_name: Client name
    """
    try:
        data = request.get_json() or {}
        advisor_id = data.get('advisor_id')
        client_name = data.get('client_name')
        
        if not advisor_id or not client_name:
            return jsonify({
                'success': False,
                'error': 'advisor_id and client_name are required'
            }), 400
        
        service = get_institutional_service()
        client = await service.create_client(advisor_id, client_name)
        
        return jsonify({
            'success': True,
            'data': client.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@institutional_bp.route('/whitelabel/configure', methods=['POST'])
async def configure_white_label():
    """
    Configure white-label branding.
    
    Request body:
        organization_id: Organization identifier
        logo_url: Optional logo URL
        primary_color: Optional primary color
        secondary_color: Optional secondary color
        custom_domain: Optional custom domain
        branding_name: Optional branding name
    """
    try:
        data = request.get_json() or {}
        organization_id = data.get('organization_id')
        logo_url = data.get('logo_url')
        primary_color = data.get('primary_color')
        secondary_color = data.get('secondary_color')
        custom_domain = data.get('custom_domain')
        branding_name = data.get('branding_name')
        
        if not organization_id:
            return jsonify({
                'success': False,
                'error': 'organization_id is required'
            }), 400
        
        service = get_institutional_service()
        config = await service.configure_white_label(
            organization_id=organization_id,
            logo_url=logo_url,
            primary_color=primary_color,
            secondary_color=secondary_color,
            custom_domain=custom_domain,
            branding_name=branding_name
        )
        
        return jsonify({
            'success': True,
            'data': config.dict()
        })
        
    except Exception as e:
        logger.error(f"Error configuring white-label: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@institutional_bp.route('/report/generate', methods=['POST'])
async def generate_professional_report():
    """
    Generate professional report.
    
    Request body:
        advisor_id: Advisor identifier
        client_id: Client identifier
        report_type: Report type
        content: Report content
    """
    try:
        data = request.get_json() or {}
        advisor_id = data.get('advisor_id')
        client_id = data.get('client_id')
        report_type = data.get('report_type')
        content = data.get('content', {})
        
        if not all([advisor_id, client_id, report_type]):
            return jsonify({
                'success': False,
                'error': 'advisor_id, client_id, and report_type are required'
            }), 400
        
        service = get_professional_tools_service()
        report = await service.generate_professional_report(
            advisor_id=advisor_id,
            client_id=client_id,
            report_type=report_type,
            content=content
        )
        
        return jsonify({
            'success': True,
            'data': report.dict()
        })
        
    except Exception as e:
        logger.error(f"Error generating professional report: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
