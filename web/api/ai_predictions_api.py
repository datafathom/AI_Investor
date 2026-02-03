"""
==============================================================================
FILE: web/api/ai_predictions_api.py
ROLE: AI Predictions API Endpoints
PURPOSE: REST endpoints for price predictions and market forecasting.

INTEGRATION POINTS:
    - PredictionEngine: Price forecasting
    - AIAnalyticsService: Market analysis
    - FrontendAI: Prediction dashboard

ENDPOINTS:
    - POST /api/ai-predictions/price
    - POST /api/ai-predictions/trend
    - GET /api/ai-predictions/regime
    - POST /api/ai-predictions/news-impact

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.ai_predictions.prediction_engine import get_prediction_engine
from services.ai_predictions.ai_analytics_service import get_ai_analytics_service

logger = logging.getLogger(__name__)

ai_predictions_bp = Blueprint('ai_predictions', __name__, url_prefix='/api/v1/ai_predictions')


@ai_predictions_bp.route('/price', methods=['POST'])
async def predict_price():
    """
    Predict future price.
    
    Request body:
        symbol: Stock symbol
        time_horizon: Prediction horizon (default: 1m)
        model_version: Model version (default: v1.0)
    """
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        time_horizon = data.get('time_horizon', '1m')
        model_version = data.get('model_version', 'v1.0')
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': 'symbol is required'
            }), 400
        
        engine = get_prediction_engine()
        prediction = await engine.predict_price(symbol, time_horizon, model_version)
        
        return jsonify({
            'success': True,
            'data': prediction.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error predicting price: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_predictions_bp.route('/trend', methods=['POST'])
async def predict_trend():
    """
    Predict price trend.
    
    Request body:
        symbol: Stock symbol
        time_horizon: Prediction horizon (default: 1m)
    """
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        time_horizon = data.get('time_horizon', '1m')
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': 'symbol is required'
            }), 400
        
        engine = get_prediction_engine()
        prediction = await engine.predict_trend(symbol, time_horizon)
        
        return jsonify({
            'success': True,
            'data': prediction.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error predicting trend: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_predictions_bp.route('/regime', methods=['GET'])
async def get_market_regime():
    """
    Detect current market regime.
    
    Query params:
        market_index: Market index symbol (default: SPY)
    """
    try:
        market_index = request.args.get('market_index', 'SPY')
        
        service = get_ai_analytics_service()
        regime = await service.detect_market_regime(market_index)
        
        return jsonify({
            'success': True,
            'data': regime.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error detecting market regime: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_predictions_bp.route('/news-impact', methods=['POST'])
async def predict_news_impact():
    """
    Predict market impact from news sentiment.
    
    Request body:
        symbol: Stock symbol
        news_sentiment: News sentiment score (-1 to 1)
    """
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        news_sentiment = float(data.get('news_sentiment', 0))
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': 'symbol is required'
            }), 400
        
        service = get_ai_analytics_service()
        impact = await service.predict_news_impact(symbol, news_sentiment)
        
        return jsonify({
            'success': True,
            'data': impact
        })
        
    except Exception as e:
        logger.error(f"Error predicting news impact: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
