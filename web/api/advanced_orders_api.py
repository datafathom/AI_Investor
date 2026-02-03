"""
==============================================================================
FILE: web/api/advanced_orders_api.py
ROLE: Advanced Orders API Endpoints
PURPOSE: REST endpoints for advanced order types and smart execution.

INTEGRATION POINTS:
    - AdvancedOrderService: Order type management
    - SmartExecutionService: Execution algorithms
    - FrontendTrading: Order entry widgets

ENDPOINTS:
    - POST /api/orders/trailing-stop
    - POST /api/orders/bracket
    - POST /api/orders/oco
    - POST /api/orders/conditional
    - PUT /api/orders/trailing-stop/:order_id/update
    - POST /api/execution/twap
    - POST /api/execution/vwap
    - POST /api/execution/implementation-shortfall

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from services.execution.advanced_order_service import get_advanced_order_service
from services.execution.smart_execution_service import get_smart_execution_service

logger = logging.getLogger(__name__)

advanced_orders_bp = Blueprint('advanced_orders', __name__, url_prefix='/api/v1/execution')
execution_bp = Blueprint('execution', __name__, url_prefix='/api/v1/execution')


@advanced_orders_bp.route('/trailing-stop', methods=['POST'])
async def create_trailing_stop():
    """
    Create trailing stop order.
    
    Request body:
        user_id: User identifier
        symbol: Stock symbol
        quantity: Number of shares
        trailing_type: "amount" or "percentage"
        trailing_value: Trailing amount or percentage
        initial_stop_price: Optional initial stop price
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        symbol = data.get('symbol')
        quantity = int(data.get('quantity', 0))
        trailing_type = data.get('trailing_type', 'percentage')
        trailing_value = float(data.get('trailing_value', 0))
        initial_stop_price = data.get('initial_stop_price')
        
        if not user_id or not symbol or not quantity or not trailing_value:
            return jsonify({
                'success': False,
                'error': 'user_id, symbol, quantity, and trailing_value are required'
            }), 400
        
        service = get_advanced_order_service()
        order = await service.create_trailing_stop(
            user_id=user_id,
            symbol=symbol,
            quantity=quantity,
            trailing_type=trailing_type,
            trailing_value=trailing_value,
            initial_stop_price=initial_stop_price
        )
        
        return jsonify({
            'success': True,
            'data': order.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error creating trailing stop: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@advanced_orders_bp.route('/bracket', methods=['POST'])
async def create_bracket_order():
    """
    Create bracket order.
    
    Request body:
        user_id: User identifier
        symbol: Stock symbol
        quantity: Number of shares
        entry_price: Entry price
        profit_target_price: Optional profit target price
        stop_loss_price: Optional stop loss price
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        symbol = data.get('symbol')
        quantity = int(data.get('quantity', 0))
        entry_price = float(data.get('entry_price', 0))
        profit_target_price = data.get('profit_target_price')
        stop_loss_price = data.get('stop_loss_price')
        
        if not user_id or not symbol or not quantity or not entry_price:
            return jsonify({
                'success': False,
                'error': 'user_id, symbol, quantity, and entry_price are required'
            }), 400
        
        service = get_advanced_order_service()
        bracket = await service.create_bracket_order(
            user_id=user_id,
            symbol=symbol,
            quantity=quantity,
            entry_price=entry_price,
            profit_target_price=profit_target_price,
            stop_loss_price=stop_loss_price
        )
        
        return jsonify({
            'success': True,
            'data': bracket.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error creating bracket order: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@advanced_orders_bp.route('/oco', methods=['POST'])
async def create_oco_order():
    """
    Create OCO (One-Cancels-Other) order.
    
    Request body:
        user_id: User identifier
        symbol: Stock symbol
        quantity: Number of shares
        order1: First order definition
        order2: Second order definition
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        symbol = data.get('symbol')
        quantity = int(data.get('quantity', 0))
        order1 = data.get('order1')
        order2 = data.get('order2')
        
        if not user_id or not symbol or not quantity or not order1 or not order2:
            return jsonify({
                'success': False,
                'error': 'user_id, symbol, quantity, order1, and order2 are required'
            }), 400
        
        service = get_advanced_order_service()
        oco = await service.create_oco_order(
            user_id=user_id,
            symbol=symbol,
            quantity=quantity,
            order1=order1,
            order2=order2
        )
        
        return jsonify({
            'success': True,
            'data': oco
        })
        
    except Exception as e:
        logger.error(f"Error creating OCO order: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@advanced_orders_bp.route('/conditional', methods=['POST'])
async def create_conditional_order():
    """
    Create conditional order.
    
    Request body:
        user_id: User identifier
        symbol: Stock symbol
        quantity: Number of shares
        order_type: Order type (market, limit, etc.)
        condition_type: Condition type (price, time, volume)
        condition_value: Condition trigger value
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        symbol = data.get('symbol')
        quantity = int(data.get('quantity', 0))
        order_type = data.get('order_type', 'market')
        condition_type = data.get('condition_type')
        condition_value = float(data.get('condition_value', 0))
        
        if not user_id or not symbol or not quantity or not condition_type or not condition_value:
            return jsonify({
                'success': False,
                'error': 'user_id, symbol, quantity, condition_type, and condition_value are required'
            }), 400
        
        service = get_advanced_order_service()
        order = await service.create_conditional_order(
            user_id=user_id,
            symbol=symbol,
            quantity=quantity,
            order_type=order_type,
            condition_type=condition_type,
            condition_value=condition_value
        )
        
        return jsonify({
            'success': True,
            'data': order.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error creating conditional order: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@advanced_orders_bp.route('/trailing-stop/<order_id>/update', methods=['PUT'])
async def update_trailing_stop(order_id: str):
    """
    Update trailing stop with current price.
    
    Request body:
        current_price: Current market price
    """
    try:
        data = request.get_json() or {}
        current_price = float(data.get('current_price', 0))
        
        if not current_price:
            return jsonify({
                'success': False,
                'error': 'current_price is required'
            }), 400
        
        service = get_advanced_order_service()
        updated_order = await service.update_trailing_stop(order_id, current_price)
        
        return jsonify({
            'success': True,
            'data': updated_order.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error updating trailing stop: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@execution_bp.route('/twap', methods=['POST'])
async def execute_twap():
    """
    Execute order using TWAP algorithm.
    
    Request body:
        symbol: Stock symbol
        total_quantity: Total quantity to execute
        time_window_minutes: Time window in minutes
        start_time: Optional start time (ISO format)
    """
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        total_quantity = int(data.get('total_quantity', 0))
        time_window_minutes = int(data.get('time_window_minutes', 60))
        start_time_str = data.get('start_time')
        
        if not symbol or not total_quantity:
            return jsonify({
                'success': False,
                'error': 'symbol and total_quantity are required'
            }), 400
        
        start_time = datetime.fromisoformat(start_time_str) if start_time_str else None
        
        service = get_smart_execution_service()
        executions = await service.execute_twap(
            symbol=symbol,
            total_quantity=total_quantity,
            time_window_minutes=time_window_minutes,
            start_time=start_time
        )
        
        return jsonify({
            'success': True,
            'data': [e.model_dump() for e in executions]
        })
        
    except Exception as e:
        logger.error(f"Error executing TWAP: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@execution_bp.route('/vwap', methods=['POST'])
async def execute_vwap():
    """
    Execute order using VWAP algorithm.
    
    Request body:
        symbol: Stock symbol
        total_quantity: Total quantity to execute
        time_window_minutes: Time window in minutes
        start_time: Optional start time (ISO format)
    """
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        total_quantity = int(data.get('total_quantity', 0))
        time_window_minutes = int(data.get('time_window_minutes', 60))
        start_time_str = data.get('start_time')
        
        if not symbol or not total_quantity:
            return jsonify({
                'success': False,
                'error': 'symbol and total_quantity are required'
            }), 400
        
        start_time = datetime.fromisoformat(start_time_str) if start_time_str else None
        
        service = get_smart_execution_service()
        executions = await service.execute_vwap(
            symbol=symbol,
            total_quantity=total_quantity,
            time_window_minutes=time_window_minutes,
            start_time=start_time
        )
        
        return jsonify({
            'success': True,
            'data': [e.model_dump() for e in executions]
        })
        
    except Exception as e:
        logger.error(f"Error executing VWAP: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@execution_bp.route('/implementation-shortfall', methods=['POST'])
async def execute_implementation_shortfall():
    """
    Execute order using Implementation Shortfall algorithm.
    
    Request body:
        symbol: Stock symbol
        total_quantity: Total quantity to execute
        urgency: Urgency factor (0.0-1.0, default: 0.5)
    """
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        total_quantity = int(data.get('total_quantity', 0))
        urgency = float(data.get('urgency', 0.5))
        
        if not symbol or not total_quantity:
            return jsonify({
                'success': False,
                'error': 'symbol and total_quantity are required'
            }), 400
        
        service = get_smart_execution_service()
        executions = await service.execute_implementation_shortfall(
            symbol=symbol,
            total_quantity=total_quantity,
            urgency=urgency
        )
        
        return jsonify({
            'success': True,
            'data': [e.model_dump() for e in executions]
        })
        
    except Exception as e:
        logger.error(f"Error executing Implementation Shortfall: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
