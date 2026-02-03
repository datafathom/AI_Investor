"""
==============================================================================
FILE: web/api/options_api.py
ROLE: Options API Endpoints
PURPOSE: REST endpoints for options strategy building and analytics.

INTEGRATION POINTS:
    - OptionsStrategyBuilderService: Strategy construction
    - OptionsAnalyticsService: Greeks and P&L analysis
    - FrontendOptions: Options dashboard widgets

ENDPOINTS:
    - POST /api/options/strategy/create
    - POST /api/options/strategy/template
    - GET /api/options/strategy/:strategy_id/greeks
    - GET /api/options/strategy/:strategy_id/pnl
    - POST /api/options/strategy/:strategy_id/analyze

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from services.options.strategy_builder_service import get_strategy_builder_service
from services.options.options_analytics_service import get_options_analytics_service

logger = logging.getLogger(__name__)

options_bp = Blueprint('options', __name__, url_prefix='/api/v1/options')


@options_bp.route('/strategy/create', methods=['POST'])
async def create_strategy():
    """
    Create a new options strategy.
    
    Request body:
        strategy_name: Name of strategy
        underlying_symbol: Underlying stock symbol
        legs: List of leg objects
        strategy_type: Strategy type (default: "custom")
    """
    try:
        data = request.get_json() or {}
        strategy_name = data.get('strategy_name')
        underlying_symbol = data.get('underlying_symbol')
        legs = data.get('legs', [])
        strategy_type = data.get('strategy_type', 'custom')
        
        if not strategy_name or not underlying_symbol:
            return jsonify({
                'success': False,
                'error': 'strategy_name and underlying_symbol are required'
            }), 400
        
        service = get_strategy_builder_service()
        strategy = await service.create_strategy(
            strategy_name=strategy_name,
            underlying_symbol=underlying_symbol,
            legs=legs,
            strategy_type=strategy_type
        )
        
        return jsonify({
            'success': True,
            'data': strategy.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error creating strategy: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@options_bp.route('/strategy/template', methods=['POST'])
async def create_from_template():
    """
    Create strategy from template.
    
    Request body:
        template_name: Template name
        underlying_symbol: Underlying stock symbol
        current_price: Current stock price
        expiration: Expiration date (YYYY-MM-DD)
        **kwargs: Template-specific parameters
    """
    try:
        data = request.get_json() or {}
        template_name = data.get('template_name')
        underlying_symbol = data.get('underlying_symbol')
        current_price = float(data.get('current_price', 0))
        expiration_str = data.get('expiration')
        
        if not template_name or not underlying_symbol or not expiration_str:
            return jsonify({
                'success': False,
                'error': 'template_name, underlying_symbol, and expiration are required'
            }), 400
        
        expiration = datetime.strptime(expiration_str, '%Y-%m-%d')
        
        service = get_strategy_builder_service()
        strategy = await service.create_from_template(
            template_name=template_name,
            underlying_symbol=underlying_symbol,
            current_price=current_price,
            expiration=expiration,
            **{k: v for k, v in data.items() if k not in ['template_name', 'underlying_symbol', 'current_price', 'expiration']}
        )
        
        return jsonify({
            'success': True,
            'data': strategy.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error creating strategy from template: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@options_bp.route('/strategy/<strategy_id>/greeks', methods=['GET'])
async def get_greeks(strategy_id: str):
    """
    Calculate Greeks for strategy.
    
    Query params:
        underlying_price: Current underlying price
        days_to_expiration: Days until expiration
        volatility: Implied volatility (default: 0.20)
    """
    try:
        underlying_price = float(request.args.get('underlying_price', 0))
        days_to_expiration = int(request.args.get('days_to_expiration', 30))
        volatility = float(request.args.get('volatility', 0.20))
        
        if underlying_price == 0:
            return jsonify({
                'success': False,
                'error': 'underlying_price is required'
            }), 400
        
        # Get strategy from cache
        from services.system.cache_service import get_cache_service
        cache_service = get_cache_service()
        strategy_data = cache_service.get(f"strategy:{strategy_id}")
        
        if not strategy_data:
            return jsonify({
                'success': False,
                'error': 'Strategy not found'
            }), 404
        
        from models.options import OptionsStrategy
        strategy = OptionsStrategy(**strategy_data)
        
        analytics_service = get_options_analytics_service()
        greeks = await analytics_service.calculate_greeks(
            strategy=strategy,
            underlying_price=underlying_price,
            days_to_expiration=days_to_expiration,
            volatility=volatility
        )
        
        return jsonify({
            'success': True,
            'data': greeks.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error calculating Greeks: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@options_bp.route('/strategy/<strategy_id>/pnl', methods=['GET'])
async def get_pnl(strategy_id: str):
    """
    Calculate P&L for strategy.
    
    Query params:
        underlying_price: Underlying price to analyze
        days_to_expiration: Days until expiration
    """
    try:
        underlying_price = float(request.args.get('underlying_price', 0))
        days_to_expiration = int(request.args.get('days_to_expiration', 30))
        
        if underlying_price == 0:
            return jsonify({
                'success': False,
                'error': 'underlying_price is required'
            }), 400
        
        # Get strategy
        from services.system.cache_service import get_cache_service
        cache_service = get_cache_service()
        strategy_data = cache_service.get(f"strategy:{strategy_id}")
        
        if not strategy_data:
            return jsonify({
                'success': False,
                'error': 'Strategy not found'
            }), 404
        
        from models.options import OptionsStrategy
        strategy = OptionsStrategy(**strategy_data)
        
        analytics_service = get_options_analytics_service()
        pnl = await analytics_service.calculate_pnl(
            strategy=strategy,
            underlying_price=underlying_price,
            days_to_expiration=days_to_expiration
        )
        
        return jsonify({
            'success': True,
            'data': pnl.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error calculating P&L: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@options_bp.route('/strategy/<strategy_id>/analyze', methods=['POST'])
async def analyze_strategy(strategy_id: str):
    """
    Complete strategy analysis.
    
    Request body:
        underlying_price: Current underlying price
        days_to_expiration: Days until expiration
        volatility: Implied volatility (default: 0.20)
    """
    try:
        data = request.get_json() or {}
        underlying_price = float(data.get('underlying_price', 0))
        days_to_expiration = int(data.get('days_to_expiration', 30))
        volatility = float(data.get('volatility', 0.20))
        
        if underlying_price == 0:
            return jsonify({
                'success': False,
                'error': 'underlying_price is required'
            }), 400
        
        # Get strategy
        from services.system.cache_service import get_cache_service
        cache_service = get_cache_service()
        strategy_data = cache_service.get(f"strategy:{strategy_id}")
        
        if not strategy_data:
            return jsonify({
                'success': False,
                'error': 'Strategy not found'
            }), 404
        
        from models.options import OptionsStrategy
        strategy = OptionsStrategy(**strategy_data)
        
        analytics_service = get_options_analytics_service()
        analysis = await analytics_service.analyze_strategy(
            strategy=strategy,
            underlying_price=underlying_price,
            days_to_expiration=days_to_expiration,
            volatility=volatility
        )
        
        return jsonify({
            'success': True,
            'data': analysis.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error analyzing strategy: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@options_bp.route('/chain', methods=['GET'])
async def get_options_chain():
    """
    Get options chain for symbol.
    """
    try:
        symbol = request.args.get('symbol', 'AAPL')
        
        # Mock Data Generation
        import random
        strikes = [100 + i*5 for i in range(20)]
        chain = []
        for strike in strikes:
            chain.append({
                'strike': strike,
                'call_bid': round(random.uniform(1.0, 10.0), 2),
                'call_ask': round(random.uniform(1.1, 10.1), 2),
                'put_bid': round(random.uniform(1.0, 10.0), 2),
                'put_ask': round(random.uniform(1.1, 10.1), 2)
            })
            
        return jsonify({
            'success': True,
            'data': chain
        })
    except Exception as e:
        logger.error(f"Error getting options chain: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
