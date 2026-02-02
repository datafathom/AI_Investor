"""
==============================================================================
FILE: web/api/research_api.py
ROLE: Research & Reports API Endpoints
PURPOSE: REST endpoints for research report generation and download.

INTEGRATION POINTS:
    - ResearchService: Report generation
    - ReportGenerator: Format conversion
    - FrontendResearch: Research dashboard

ENDPOINTS:
    - POST /api/research/portfolio-report
    - POST /api/research/company-research
    - GET /api/research/report/:report_id
    - GET /api/research/report/:report_id/pdf
    - GET /api/research/report/:report_id/html
    - GET /api/research/report/:report_id/excel

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from flask import Blueprint, jsonify, request, Response

from services.research.research_service import get_research_service
from services.research.report_generator import get_report_generator

logger = logging.getLogger(__name__)

research_bp = Blueprint('research', __name__, url_prefix='/api/v1/research')


@research_bp.route('/portfolio-report', methods=['POST'])
async def generate_portfolio_report():
    """
    Generate portfolio analysis report.
    
    Request body:
        user_id: User identifier
        portfolio_id: Portfolio identifier
        title: Optional report title
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        portfolio_id = data.get('portfolio_id')
        title = data.get('title')
        
        if not user_id or not portfolio_id:
            return jsonify({
                'success': False,
                'error': 'user_id and portfolio_id are required'
            }), 400
        
        service = get_research_service()
        report = await service.generate_portfolio_report(
            user_id=user_id,
            portfolio_id=portfolio_id,
            title=title
        )
        
        return jsonify({
            'success': True,
            'data': report.dict()
        })
        
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Error generating portfolio report: %s", e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@research_bp.route('/company-research', methods=['POST'])
async def generate_company_research():
    """
    Generate company research report.
    
    Request body:
        user_id: User identifier
        symbol: Stock symbol
        title: Optional report title
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        symbol = data.get('symbol')
        title = data.get('title')
        
        if not user_id or not symbol:
            return jsonify({
                'success': False,
                'error': 'user_id and symbol are required'
            }), 400
        
        service = get_research_service()
        report = await service.generate_company_research(
            user_id=user_id,
            symbol=symbol,
            title=title
        )
        
        return jsonify({
            'success': True,
            'data': report.dict()
        })
        
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Error generating company research: %s", e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@research_bp.route('/reports', methods=['GET'])
async def get_user_reports():
    """
    Get all reports for a user.
    """
    try:
        user_id = request.args.get('user_id', 'default_user')
        service = get_research_service()
        reports = await service._get_reports_from_db(user_id) # Using the method expected by store
        return jsonify({
            'success': True,
            'data': [r.dict() for r in reports]
        })
    except Exception as e:
        logger.error(f"Error getting reports list: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@research_bp.route('/templates', methods=['GET'])
async def get_templates():
    """
    Get available report templates.
    """
    return jsonify({
        'success': True,
        'data': [
            {"template_id": "equity_deep_dive", "template_name": "Equity Deep Dive", "description": "Fundamental analysis for stocks.", "category": "Equities"},
            {"template_id": "macro_regime_shift", "template_name": "Macro Regime Shift", "description": "Analysis of regime changes.", "category": "Macro"},
            {"template_id": "risk_contagion", "template_name": "Risk Contagion", "description": "Network-based risk propagation.", "category": "Risk"}
        ]
    })

@research_bp.route('/generate', methods=['POST'])
async def generate_report():
    """
    Generate a new report.
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 'default_user')
        template_id = data.get('template_id')
        title = data.get('report_title')
        
        service = get_research_service()
        # For now, all templates map to company research for the demo
        # (In real app, we'd use template_id to choose logic)
        report = await service.generate_company_research(
            user_id=user_id,
            symbol="SPY", # Placeholder
            title=title
        )
        
        return jsonify({
            'success': True,
            'data': report.dict()
        })
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@research_bp.route('/report/<report_id>/pdf', methods=['GET'])
async def download_pdf(report_id: str):
    """Download report as PDF."""
    try:
        generator = get_report_generator()
        pdf_bytes = await generator.generate_pdf(report_id)
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment; filename=report_{report_id}.pdf'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@research_bp.route('/report/<report_id>/html', methods=['GET'])
async def download_html(report_id: str):
    """Download report as HTML."""
    try:
        generator = get_report_generator()
        html = await generator.generate_html(report_id)
        return Response(html, mimetype='text/html', headers={'Content-Disposition': f'attachment; filename=report_{report_id}.html'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@research_bp.route('/report/<report_id>/excel', methods=['GET'])
async def download_excel(report_id: str):
    """Download report as Excel."""
    try:
        generator = get_report_generator()
        excel_bytes = await generator.generate_excel(report_id)
        return Response(excel_bytes, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={'Content-Disposition': f'attachment; filename=report_{report_id}.xlsx'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
