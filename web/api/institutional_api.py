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

import math
from typing import Dict, List, Optional
from flask import Blueprint, jsonify, request
import logging
from web.auth_utils import login_required
from services.institutional.institutional_service import get_institutional_service
from services.institutional.professional_tools_service import get_professional_tools_service

logger = logging.getLogger(__name__)

institutional_bp = Blueprint('institutional', __name__, url_prefix='/api/v1/institutional')


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
        jurisdiction = data.get('jurisdiction', 'US')
        funding_source = data.get('funding_source')
        strategy = data.get('strategy', 'Aggressive AI')
        
        if not advisor_id or not client_name:
            return jsonify({
                'success': False,
                'error': 'advisor_id and client_name are required'
            }), 400
        
        service = get_institutional_service()
        client = await service.create_client(
            advisor_id=advisor_id, 
            client_name=client_name,
            jurisdiction=jurisdiction,
            funding_source=funding_source,
            strategy=strategy
        )
        
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


@institutional_bp.route('/clients', methods=['GET'])
@login_required
async def get_clients():
    """Get all clients for the logged-in advisor."""
    try:
        # Assuming advisor_id is linked to the user_id in the auth session
        from flask import g
        advisor_id = g.user_id
        
        service = get_institutional_service()
        clients = await service.get_clients_for_advisor(advisor_id)
        
        return jsonify({
            'success': True,
            'data': [c.dict() for c in clients]
        })
    except Exception as e:
        logger.error(f"Error fetching clients: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@institutional_bp.route('/analytics/fees', methods=['GET'])
@login_required
async def get_fee_analytics():
    """Get fee analytics for an advisor or specific client."""
    try:
        client_id = request.args.get('client_id')
        service = get_institutional_service()
        data = await service.get_revenue_forecast(client_id)
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"Error fetching fee analytics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@institutional_bp.route('/analytics/risk/<client_id>', methods=['GET'])
@login_required
async def get_risk_analytics(client_id):
    """Get risk analytics for a specific client."""
    try:
        service = get_institutional_service()
        data = await service.get_client_risk_profile(client_id)
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"Error fetching risk analytics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@institutional_bp.route('/analytics/signatures/<client_id>', methods=['GET'])
@login_required
async def get_signatures(client_id):
    """Get signature status for a specific client."""
    try:
        service = get_institutional_service()
        data = await service.get_signature_status(client_id)
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"Error fetching signatures: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@institutional_bp.route('/analytics/allocation/<client_id>', methods=['GET'])
@login_required
async def get_allocation(client_id):
    """Get asset allocation for a specific client."""
    try:
        service = get_institutional_service()
        data = await service.get_asset_allocation(client_id)
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"Error fetching allocation: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@institutional_bp.route('/analytics/rebalance/<client_id>', methods=['POST'])
@login_required
async def calculate_drift_and_rebalance(client_id):
    """
    Calculate portfolio drift and trigger auto-rebalance for a client.
    
    Returns:
        drift_percentage: Current drift from target allocation
        actions: List of rebalance actions taken
        new_allocation: Updated allocation after rebalance
    """
    try:
        service = get_institutional_service()
        allocation_data = await service.get_asset_allocation(client_id)
        
        # Calculate total drift
        total_drift = sum(
            abs(alloc.get('drift', 0)) 
            for alloc in allocation_data.get('allocations', [])
        )
        
        # Simulate rebalance actions
        actions = []
        for alloc in allocation_data.get('allocations', []):
            drift = alloc.get('drift', 0)
            if abs(drift) > 1:  # Only act on significant drift
                action = 'BUY' if drift < 0 else 'SELL'
                actions.append({
                    'category': alloc.get('category'),
                    'action': action,
                    'adjustment_pct': abs(drift)
                })
        
        return jsonify({
            'success': True,
            'data': {
                'client_id': client_id,
                'drift_percentage': total_drift,
                'actions': actions,
                'rebalanced': len(actions) > 0,
                'message': f'Rebalanced {len(actions)} positions' if actions else 'No rebalancing needed'
            }
        })
    except Exception as e:
        logger.error(f"Error calculating drift: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


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
