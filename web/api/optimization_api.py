"""
==============================================================================
FILE: web/api/optimization_api.py
ROLE: Optimization API Endpoints
PURPOSE: REST endpoints for portfolio optimization and rebalancing.

INTEGRATION POINTS:
    - PortfolioOptimizerService: Optimization calculations
    - RebalancingService: Rebalancing recommendations
    - FrontendOptimization: Dashboard widgets

ENDPOINTS:
    - POST /api/optimization/optimize/:portfolio_id
    - GET /api/optimization/rebalancing/check/:portfolio_id
    - POST /api/optimization/rebalancing/recommend/:portfolio_id
    - POST /api/optimization/rebalancing/execute/:portfolio_id
    - GET /api/optimization/rebalancing/history/:portfolio_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.optimization.portfolio_optimizer_service import get_optimizer_service
from services.optimization.rebalancing_service import get_rebalancing_service
from models.optimization import OptimizationConstraints

logger = logging.getLogger(__name__)

optimization_bp = Blueprint('optimization', __name__, url_prefix='/api/v1/optimization')


@optimization_bp.route('/optimize/<portfolio_id>', methods=['POST'])
async def optimize_portfolio(portfolio_id: str):
    """
    Optimize portfolio for given objective.
    
    Request body:
        objective: Optimization objective (maximize_sharpe, minimize_risk, etc.)
        method: Optimization method (mean_variance, risk_parity, etc.)
        constraints: Optional constraints object
        risk_model: Risk model (historical, factor, etc.)
        lookback_days: Lookback period in days
    """
    try:
        data = request.get_json() or {}
        objective = data.get('objective', 'maximize_sharpe')
        method = data.get('method', 'mean_variance')
        risk_model = data.get('risk_model', 'historical')
        lookback_days = int(data.get('lookback_days', 252))
        
        # Parse constraints if provided
        constraints = None
        if 'constraints' in data:
            constraints = OptimizationConstraints(**data['constraints'])
        
        service = get_optimizer_service()
        result = await service.optimize(
            portfolio_id=portfolio_id,
            objective=objective,
            method=method,
            constraints=constraints,
            risk_model=risk_model,
            lookback_days=lookback_days
        )
        
        return jsonify({
            'success': True,
            'data': result.dict()
        })
        
    except Exception as e:
        logger.error(f"Error optimizing portfolio: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@optimization_bp.route('/rebalancing/check/<portfolio_id>', methods=['GET'])
async def check_rebalancing(portfolio_id: str):
    """
    Check if portfolio needs rebalancing.
    
    Query params:
        threshold: Drift threshold (default: 0.05)
    """
    try:
        threshold = float(request.args.get('threshold', 0.05))
        
        service = get_rebalancing_service()
        needs_rebalancing = await service.check_rebalancing_needed(
            portfolio_id=portfolio_id,
            threshold=threshold
        )
        
        return jsonify({
            'success': True,
            'data': {
                'needs_rebalancing': needs_rebalancing,
                'threshold': threshold
            }
        })
        
    except Exception as e:
        logger.error(f"Error checking rebalancing: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@optimization_bp.route('/rebalancing/recommend/<portfolio_id>', methods=['POST'])
async def recommend_rebalancing(portfolio_id: str):
    """
    Generate rebalancing recommendation.
    
    Request body:
        strategy: Rebalancing strategy (full, threshold, cash_flow)
    """
    try:
        data = request.get_json() or {}
        strategy = data.get('strategy', 'threshold')
        
        service = get_rebalancing_service()
        recommendation = await service.generate_rebalancing_recommendation(
            portfolio_id=portfolio_id,
            strategy=strategy
        )
        
        return jsonify({
            'success': True,
            'data': recommendation.dict()
        })
        
    except Exception as e:
        logger.error(f"Error generating rebalancing recommendation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@optimization_bp.route('/rebalancing/execute/<portfolio_id>', methods=['POST'])
async def execute_rebalancing(portfolio_id: str):
    """
    Execute rebalancing trades.
    
    Request body:
        recommendation: RebalancingRecommendation object
        approved: Whether user has approved (required if recommendation.requires_approval)
    """
    try:
        data = request.get_json() or {}
        recommendation_data = data.get('recommendation')
        approved = data.get('approved', False)
        
        if not recommendation_data:
            return jsonify({
                'success': False,
                'error': 'Recommendation is required'
            }), 400
        
        from models.optimization import RebalancingRecommendation
        recommendation = RebalancingRecommendation(**recommendation_data)
        
        service = get_rebalancing_service()
        history = await service.execute_rebalancing(
            portfolio_id=portfolio_id,
            recommendation=recommendation,
            approved=approved
        )
        
        return jsonify({
            'success': True,
            'data': history.dict()
        })
        
    except Exception as e:
        logger.error(f"Error executing rebalancing: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@optimization_bp.route('/rebalancing/history/<portfolio_id>', methods=['GET'])
async def get_rebalancing_history(portfolio_id: str):
    """
    Get rebalancing history for portfolio.
    
    Query params:
        limit: Maximum number of records (default: 10)
    """
    try:
        limit = int(request.args.get('limit', 10))
        
        service = get_rebalancing_service()
        history = await service.get_rebalancing_history(
            portfolio_id=portfolio_id,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'data': [h.dict() for h in history]
        })
        
    except Exception as e:
        logger.error(f"Error getting rebalancing history: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
