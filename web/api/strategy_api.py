"""
==============================================================================
FILE: web/api/strategy_api.py
ROLE: Strategy API Endpoints
PURPOSE: REST endpoints for strategy builder and execution.

INTEGRATION POINTS:
    - StrategyBuilderService: Strategy creation
    - StrategyExecutionService: Live execution
    - FrontendStrategy: Strategy builder widgets

ENDPOINTS:
    - POST /api/strategy/create
    - GET /api/strategy/:strategy_id
    - POST /api/strategy/:strategy_id/rule
    - GET /api/strategy/templates
    - POST /api/strategy/:strategy_id/validate
    - POST /api/strategy/:strategy_id/start
    - POST /api/strategy/:strategy_id/stop
    - POST /api/strategy/:strategy_id/pause
    - GET /api/strategy/:strategy_id/performance

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.strategy.strategy_builder_service import get_strategy_builder_service
from services.strategy.strategy_execution_service import get_strategy_execution_service

logger = logging.getLogger(__name__)

strategy_bp = Blueprint('strategy', __name__, url_prefix='/api/v1/strategy')


@strategy_bp.route('/create', methods=['POST'])
async def create_strategy():
    """
    Create a new trading strategy.
    
    Request body:
        user_id: User identifier
        strategy_name: Name of strategy
        description: Optional description
        rules: Optional list of rule dictionaries
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        strategy_name = data.get('strategy_name')
        description = data.get('description')
        rules = data.get('rules')
        
        if not user_id or not strategy_name:
            return jsonify({
                'success': False,
                'error': 'user_id and strategy_name are required'
            }), 400
        
        service = get_strategy_builder_service()
        strategy = await service.create_strategy(
            user_id=user_id,
            strategy_name=strategy_name,
            description=description,
            rules=rules
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


@strategy_bp.route('/<strategy_id>', methods=['GET'])
async def get_strategy(strategy_id: str):
    """
    Get strategy details.
    """
    try:
        service = get_strategy_builder_service()
        strategy = await service._get_strategy(strategy_id)
        
        if not strategy:
            return jsonify({
                'success': False,
                'error': 'Strategy not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': strategy.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error getting strategy: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@strategy_bp.route('/<strategy_id>/rule', methods=['POST'])
async def add_rule(strategy_id: str):
    """
    Add rule to strategy.
    
    Request body:
        condition_type: Condition type
        condition: Condition parameters
        action: Action to take
        priority: Rule priority
    """
    try:
        data = request.get_json() or {}
        condition_type = data.get('condition_type')
        condition = data.get('condition')
        action = data.get('action')
        priority = int(data.get('priority', 0))
        
        if not condition_type or not condition or not action:
            return jsonify({
                'success': False,
                'error': 'condition_type, condition, and action are required'
            }), 400
        
        service = get_strategy_builder_service()
        rule = await service.add_rule(
            strategy_id=strategy_id,
            condition_type=condition_type,
            condition=condition,
            action=action,
            priority=priority
        )
        
        return jsonify({
            'success': True,
            'data': rule.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error adding rule: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@strategy_bp.route('/templates', methods=['GET'])
async def get_templates():
    """
    Get strategy templates.
    """
    try:
        service = get_strategy_builder_service()
        templates = await service.get_strategy_templates()
        
        return jsonify({
            'success': True,
            'data': templates
        })
        
    except Exception as e:
        logger.error(f"Error getting templates: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@strategy_bp.route('/<strategy_id>/validate', methods=['POST'])
async def validate_strategy(strategy_id: str):
    """
    Validate strategy.
    """
    try:
        service = get_strategy_builder_service()
        validation = await service.validate_strategy(strategy_id)
        
        return jsonify({
            'success': True,
            'data': validation
        })
        
    except Exception as e:
        logger.error(f"Error validating strategy: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@strategy_bp.route('/<strategy_id>/start', methods=['POST'])
async def start_strategy(strategy_id: str):
    """
    Start strategy execution.
    
    Request body:
        portfolio_id: Portfolio identifier
    """
    try:
        data = request.get_json() or {}
        portfolio_id = data.get('portfolio_id')
        
        if not portfolio_id:
            return jsonify({
                'success': False,
                'error': 'portfolio_id is required'
            }), 400
        
        service = get_strategy_execution_service()
        strategy = await service.start_strategy(strategy_id, portfolio_id)
        
        return jsonify({
            'success': True,
            'data': strategy.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error starting strategy: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@strategy_bp.route('/<strategy_id>/stop', methods=['POST'])
async def stop_strategy(strategy_id: str):
    """
    Stop strategy execution.
    """
    try:
        service = get_strategy_execution_service()
        strategy = await service.stop_strategy(strategy_id)
        
        return jsonify({
            'success': True,
            'data': strategy.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error stopping strategy: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@strategy_bp.route('/<strategy_id>/pause', methods=['POST'])
async def pause_strategy(strategy_id: str):
    """
    Pause strategy execution.
    """
    try:
        service = get_strategy_execution_service()
        strategy = await service.pause_strategy(strategy_id)
        
        return jsonify({
            'success': True,
            'data': strategy.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error pausing strategy: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@strategy_bp.route('/<strategy_id>/performance', methods=['GET'])
async def get_strategy_performance(strategy_id: str):
    """
    Get strategy performance metrics.
    """
    try:
        service = get_strategy_execution_service()
        performance = await service.get_strategy_performance(strategy_id)
        
        return jsonify({
            'success': True,
            'data': performance.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error getting performance: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@strategy_bp.route('/<strategy_id>/drift', methods=['GET'])
async def get_strategy_drift(strategy_id: str):
    """
    Get model drift metrics for a strategy.
    """
    try:
        service = get_strategy_execution_service()
        drift = await service.calculate_model_drift(strategy_id)
        
        return jsonify({
            'success': True,
            'data': drift.model_dump()
        })
    except Exception as e:
        logger.error(f"Error getting drift: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
