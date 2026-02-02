"""
==============================================================================
FILE: web/api/credit_api.py
ROLE: Credit Monitoring API Endpoints
PURPOSE: REST endpoints for credit score monitoring and improvement.

INTEGRATION POINTS:
    - CreditMonitoringService: Credit score tracking
    - CreditImprovementService: Improvement recommendations
    - FrontendCredit: Credit dashboard widgets

ENDPOINTS:
    - POST /api/credit/score/track
    - GET /api/credit/score/history/:user_id
    - GET /api/credit/factors/:user_id
    - GET /api/credit/recommendations/:user_id
    - POST /api/credit/simulate/:user_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.credit.credit_monitoring_service import get_credit_monitoring_service
from services.credit.credit_improvement_service import get_credit_improvement_service

logger = logging.getLogger(__name__)

credit_bp = Blueprint('credit', __name__, url_prefix='/api/credit')


@credit_bp.route('/score/track', methods=['POST'])
async def track_credit_score():
    """
    Track credit score update.
    
    Request body:
        user_id: User identifier
        score: Credit score (300-850)
        score_type: Score type (default: fico)
        factors: Optional factor impact scores
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        score = int(data.get('score', 0))
        score_type = data.get('score_type', 'fico')
        factors = data.get('factors')
        
        if not user_id or not score:
            return jsonify({
                'success': False,
                'error': 'user_id and score are required'
            }), 400
        
        service = get_credit_monitoring_service()
        credit_score = await service.track_credit_score(
            user_id=user_id,
            score=score,
            score_type=score_type,
            factors=factors
        )
        
        return jsonify({
            'success': True,
            'data': credit_score.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error tracking credit score: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@credit_bp.route('/score/history/<user_id>', methods=['GET'])
async def get_credit_history(user_id: str):
    """
    Get credit score history.
    
    Query params:
        months: Number of months of history (default: 12)
    """
    try:
        months = int(request.args.get('months', 12))
        
        service = get_credit_monitoring_service()
        history = await service.get_credit_history(user_id, months)
        
        return jsonify({
            'success': True,
            'data': [h.model_dump() for h in history]
        })
        
    except Exception as e:
        logger.error(f"Error getting credit history: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@credit_bp.route('/factors/<user_id>', methods=['GET'])
async def get_credit_factors(user_id: str):
    """
    Analyze credit score factors.
    """
    try:
        service = get_credit_monitoring_service()
        factors = await service.analyze_credit_factors(user_id)
        
        return jsonify({
            'success': True,
            'data': factors
        })
        
    except Exception as e:
        logger.error(f"Error analyzing credit factors: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@credit_bp.route('/recommendations/<user_id>', methods=['GET'])
async def get_recommendations(user_id: str):
    """
    Get credit improvement recommendations.
    """
    try:
        service = get_credit_improvement_service()
        recommendations = await service.generate_recommendations(user_id)
        
        return jsonify({
            'success': True,
            'data': [r.model_dump() for r in recommendations]
        })
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@credit_bp.route('/simulate/<user_id>', methods=['POST'])
async def simulate_improvement(user_id: str):
    """
    Simulate credit score improvement.
    
    Request body:
        recommendations: Optional list of recommendation IDs to apply
    """
    try:
        data = request.get_json() or {}
        recommendation_ids = data.get('recommendations', [])
        
        # Get all recommendations
        improvement_service = get_credit_improvement_service()
        all_recommendations = await improvement_service.generate_recommendations(user_id)
        
        # Filter if specific recommendations provided
        if recommendation_ids:
            recommendations = [r for r in all_recommendations if r.recommendation_id in recommendation_ids]
        else:
            recommendations = all_recommendations
        
        # Simulate improvement
        projection = await improvement_service.simulate_score_improvement(
            user_id=user_id,
            recommendations=recommendations
        )
        
        return jsonify({
            'success': True,
            'data': projection.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error simulating improvement: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
