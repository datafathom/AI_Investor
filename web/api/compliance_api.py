"""
==============================================================================
FILE: web/api/compliance_api.py
ROLE: Compliance API Endpoints
PURPOSE: REST endpoints for compliance checking and reporting.

INTEGRATION POINTS:
    - ComplianceEngine: Rule checking
    - ReportingService: Report generation
    - FrontendCompliance: Compliance dashboard

ENDPOINTS:
    - POST /api/compliance/check
    - POST /api/compliance/report/generate
    - GET /api/compliance/violations/:user_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from datetime import datetime
from services.compliance.compliance_engine import get_compliance_engine
from services.compliance.reporting_service import get_reporting_service

logger = logging.getLogger(__name__)

compliance_bp = Blueprint('compliance', __name__, url_prefix='/api/compliance')


import asyncio

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@compliance_bp.route('/check', methods=['POST'])
def check_compliance():
    """
    Check transaction for compliance violations.
    
    Request body:
        user_id: User identifier
        transaction: Transaction details
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        transaction = data.get('transaction')
        
        if not user_id or not transaction:
            return jsonify({
                'success': False,
                'error': 'user_id and transaction are required'
            }), 400
        
        engine = get_compliance_engine()
        violations = _run_async(engine.check_compliance(user_id, transaction))
        
        return jsonify({
            'success': True,
            'data': [v.model_dump(mode='json') for v in violations]
        })
        
    except Exception as e:
        logger.error(f"Error checking compliance: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@compliance_bp.route('/report/generate', methods=['POST'])
def generate_report():
    """
    Generate compliance report.
    
    Request body:
        user_id: User identifier
        report_type: Report type
        period_start: Period start date (ISO format)
        period_end: Period end date (ISO format)
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        report_type = data.get('report_type')
        period_start = datetime.fromisoformat(data.get('period_start'))
        period_end = datetime.fromisoformat(data.get('period_end'))
        
        if not all([user_id, report_type, period_start, period_end]):
            return jsonify({
                'success': False,
                'error': 'user_id, report_type, period_start, and period_end are required'
            }), 400
        
        service = get_reporting_service()
        report = _run_async(service.generate_compliance_report(
            user_id=user_id,
            report_type=report_type,
            period_start=period_start,
            period_end=period_end
        ))
        
        return jsonify({
            'success': True,
            'data': report.model_dump(mode='json')
        })
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@compliance_bp.route('/violations/<user_id>', methods=['GET'])
def get_violations(user_id: str):
    """
    Get compliance violations for user.
    """
    try:
        # In production, would fetch from database
        return jsonify({
            'success': True,
            'data': []
        })
        
    except Exception as e:
        logger.error(f"Error getting violations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
