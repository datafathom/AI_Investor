"""
==============================================================================
FILE: web/api/analytics_api.py
ROLE: Analytics API Endpoints
PURPOSE: REST endpoints for portfolio analytics including performance
         attribution and risk decomposition.

INTEGRATION POINTS:
    - PerformanceAttributionService: Attribution calculations
    - RiskDecompositionService: Risk analysis
    - FrontendAnalytics: Dashboard widgets

ENDPOINTS:
    - GET /api/analytics/attribution/:portfolio_id
    - GET /api/analytics/contribution/:portfolio_id
    - GET /api/analytics/risk/factor/:portfolio_id
    - GET /api/analytics/risk/concentration/:portfolio_id
    - GET /api/analytics/risk/correlation/:portfolio_id
    - GET /api/analytics/risk/tail/:portfolio_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from services.analytics.performance_attribution_service import get_attribution_service
from services.analytics.risk_decomposition_service import get_risk_decomposition_service

logger = logging.getLogger(__name__)

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/attribution/<portfolio_id>', methods=['GET'])
async def get_attribution(portfolio_id: str):
    """
    Get performance attribution for a portfolio.
    
    Query params:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        benchmark: Optional benchmark symbol (e.g., SPY)
        attribution_type: Type of attribution (multi_factor, hierarchical, simple)
    """
    try:
        start_date_str = request.args.get('start_date', '2024-01-01')
        end_date_str = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        benchmark = request.args.get('benchmark')
        attribution_type = request.args.get('attribution_type', 'multi_factor')
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        service = get_attribution_service()
        attribution = await service.calculate_attribution(
            portfolio_id=portfolio_id,
            start_date=start_date,
            end_date=end_date,
            benchmark=benchmark,
            attribution_type=attribution_type
        )
        
        return jsonify({
            'success': True,
            'data': attribution.dict()
        })
        
    except Exception as e:
        logger.error(f"Error calculating attribution: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analytics_bp.route('/contribution/<portfolio_id>', methods=['GET'])
async def get_contribution(portfolio_id: str):
    """
    Get contribution analysis for a portfolio.
    
    Query params:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    try:
        start_date_str = request.args.get('start_date', '2024-01-01')
        end_date_str = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        service = get_attribution_service()
        contributions = await service.calculate_contribution(
            portfolio_id=portfolio_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify({
            'success': True,
            'data': [c.dict() for c in contributions]
        })
        
    except Exception as e:
        logger.error(f"Error calculating contribution: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analytics_bp.route('/risk/factor/<portfolio_id>', methods=['GET'])
async def get_factor_risk(portfolio_id: str):
    """
    Get factor risk decomposition for a portfolio.
    
    Query params:
        factor_model: Factor model (fama_french, barra, custom)
        lookback_days: Lookback period in days (default: 252)
    """
    try:
        factor_model = request.args.get('factor_model', 'fama_french')
        lookback_days = int(request.args.get('lookback_days', 252))
        
        service = get_risk_decomposition_service()
        risk_analysis = await service.decompose_factor_risk(
            portfolio_id=portfolio_id,
            factor_model=factor_model,
            lookback_days=lookback_days
        )
        
        return jsonify({
            'success': True,
            'data': risk_analysis.dict()
        })
        
    except Exception as e:
        logger.error(f"Error calculating factor risk: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analytics_bp.route('/risk/concentration/<portfolio_id>', methods=['GET'])
async def get_concentration_risk(portfolio_id: str):
    """
    Get concentration risk analysis for a portfolio.
    
    Query params:
        dimensions: Comma-separated list of dimensions (holding, sector, geography, asset_class)
    """
    try:
        dimensions_str = request.args.get('dimensions', 'holding,sector,geography')
        dimensions = [d.strip() for d in dimensions_str.split(',')]
        
        service = get_risk_decomposition_service()
        concentration = await service.calculate_concentration_risk(
            portfolio_id=portfolio_id,
            dimensions=dimensions
        )
        
        return jsonify({
            'success': True,
            'data': concentration.dict()
        })
        
    except Exception as e:
        logger.error(f"Error calculating concentration risk: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analytics_bp.route('/risk/correlation/<portfolio_id>', methods=['GET'])
async def get_correlation(portfolio_id: str):
    """
    Get correlation analysis for a portfolio.
    
    Query params:
        lookback_days: Lookback period in days (default: 252)
    """
    try:
        lookback_days = int(request.args.get('lookback_days', 252))
        
        service = get_risk_decomposition_service()
        correlation = await service.analyze_correlation(
            portfolio_id=portfolio_id,
            lookback_days=lookback_days
        )
        
        return jsonify({
            'success': True,
            'data': correlation.dict()
        })
        
    except Exception as e:
        logger.error(f"Error calculating correlation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@analytics_bp.route('/risk/tail/<portfolio_id>', methods=['GET'])
async def get_tail_risk(portfolio_id: str):
    """
    Get tail risk contributions for a portfolio.
    
    Query params:
        confidence_level: Confidence level (default: 0.95)
        method: Calculation method (historical, monte_carlo, parametric)
    """
    try:
        confidence_level = float(request.args.get('confidence_level', 0.95))
        method = request.args.get('method', 'historical')
        
        service = get_risk_decomposition_service()
        tail_risk = await service.calculate_tail_risk_contributions(
            portfolio_id=portfolio_id,
            confidence_level=confidence_level,
            method=method
        )
        
        return jsonify({
            'success': True,
            'data': tail_risk.dict()
        })
        
    except Exception as e:
        logger.error(f"Error calculating tail risk: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
