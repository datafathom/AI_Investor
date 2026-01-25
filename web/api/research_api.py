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

research_bp = Blueprint('research', __name__, url_prefix='/api/research')


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


@research_bp.route('/report/<report_id>', methods=['GET'])
async def get_report(report_id: str):
    """
    Get report details.
    """
    try:
        service = get_research_service()
        report = await service._get_report(report_id)
        
        if not report:
            return jsonify({
                'success': False,
                'error': 'Report not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': report.dict()
        })
        
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Error getting report: %s", e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@research_bp.route('/report/<report_id>/pdf', methods=['GET'])
async def download_pdf(report_id: str):
    """
    Download report as PDF.
    """
    try:
        generator = get_report_generator()
        pdf_bytes = await generator.generate_pdf(report_id)
        
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=report_{report_id}.pdf'
            }
        )
        
    except (ValueError, KeyError, RuntimeError, IOError) as e:
        logger.error("Error generating PDF: %s", e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@research_bp.route('/report/<report_id>/html', methods=['GET'])
async def download_html(report_id: str):
    """
    Download report as HTML.
    """
    try:
        generator = get_report_generator()
        html = await generator.generate_html(report_id)
        
        return Response(
            html,
            mimetype='text/html',
            headers={
                'Content-Disposition': f'attachment; filename=report_{report_id}.html'
            }
        )
        
    except (ValueError, KeyError, RuntimeError, IOError) as e:
        logger.error("Error generating HTML: %s", e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@research_bp.route('/report/<report_id>/excel', methods=['GET'])
async def download_excel(report_id: str):
    """
    Download report as Excel.
    """
    try:
        generator = get_report_generator()
        excel_bytes = await generator.generate_excel(report_id)
        
        return Response(
            excel_bytes,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                'Content-Disposition': f'attachment; filename=report_{report_id}.xlsx'
            }
        )
        
    except (ValueError, KeyError, RuntimeError, IOError) as e:
        logger.error("Error generating Excel: %s", e)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
