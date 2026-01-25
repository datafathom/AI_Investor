"""
==============================================================================
FILE: web/api/paper_trading_api.py
ROLE: Paper Trading API Endpoints
PURPOSE: REST endpoints for paper trading and simulation.

INTEGRATION POINTS:
    - PaperTradingService: Virtual portfolio management
    - SimulationService: Historical replay
    - FrontendPaperTrading: Paper trading dashboard

ENDPOINTS:
    - POST /api/paper-trading/portfolio/create
    - GET /api/paper-trading/portfolio/:portfolio_id
    - POST /api/paper-trading/order/execute
    - GET /api/paper-trading/portfolio/:portfolio_id/performance
    - POST /api/paper-trading/simulation/run

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from services.trading.paper_trading_service import get_paper_trading_service
from services.trading.simulation_service import get_simulation_service

logger = logging.getLogger(__name__)

paper_trading_bp = Blueprint('paper_trading', __name__, url_prefix='/api/paper-trading')
simulation_bp = Blueprint('simulation', __name__, url_prefix='/api/simulation')


@paper_trading_bp.route('/portfolio/create', methods=['POST'])
async def create_virtual_portfolio():
    """
    Create virtual portfolio for paper trading.
    
    Request body:
        user_id: User identifier
        portfolio_name: Name of portfolio
        initial_cash: Initial cash amount (default: 100000)
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        portfolio_name = data.get('portfolio_name', 'Paper Trading Portfolio')
        initial_cash = float(data.get('initial_cash', 100000.0))
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id is required'
            }), 400
        
        service = get_paper_trading_service()
        portfolio = await service.create_virtual_portfolio(
            user_id=user_id,
            portfolio_name=portfolio_name,
            initial_cash=initial_cash
        )
        
        return jsonify({
            'success': True,
            'data': portfolio.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating virtual portfolio: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@paper_trading_bp.route('/portfolio/<portfolio_id>', methods=['GET'])
async def get_portfolio(portfolio_id: str):
    """
    Get virtual portfolio details.
    """
    try:
        service = get_paper_trading_service()
        portfolio = await service._get_portfolio(portfolio_id)
        
        if not portfolio:
            return jsonify({
                'success': False,
                'error': 'Portfolio not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': portfolio.dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting portfolio: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@paper_trading_bp.route('/order/execute', methods=['POST'])
async def execute_paper_order():
    """
    Execute paper trading order.
    
    Request body:
        portfolio_id: Virtual portfolio identifier
        symbol: Stock symbol
        quantity: Number of shares
        order_type: Order type (market, limit, stop)
        price: Optional limit/stop price
    """
    try:
        data = request.get_json() or {}
        portfolio_id = data.get('portfolio_id')
        symbol = data.get('symbol')
        quantity = int(data.get('quantity', 0))
        order_type = data.get('order_type', 'market')
        price = data.get('price')
        
        if not portfolio_id or not symbol or not quantity:
            return jsonify({
                'success': False,
                'error': 'portfolio_id, symbol, and quantity are required'
            }), 400
        
        service = get_paper_trading_service()
        order = await service.execute_paper_order(
            portfolio_id=portfolio_id,
            symbol=symbol,
            quantity=quantity,
            order_type=order_type,
            price=price
        )
        
        return jsonify({
            'success': True,
            'data': order.dict()
        })
        
    except Exception as e:
        logger.error(f"Error executing paper order: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@paper_trading_bp.route('/portfolio/<portfolio_id>/performance', methods=['GET'])
async def get_portfolio_performance(portfolio_id: str):
    """
    Get portfolio performance metrics.
    """
    try:
        service = get_paper_trading_service()
        performance = await service.get_portfolio_performance(portfolio_id)
        
        return jsonify({
            'success': True,
            'data': performance
        })
        
    except Exception as e:
        logger.error(f"Error getting portfolio performance: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@simulation_bp.route('/run', methods=['POST'])
async def run_simulation():
    """
    Run historical simulation/backtest.
    
    Request body:
        strategy_name: Name of strategy
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        initial_capital: Initial capital (default: 100000)
        strategy_config: Optional strategy configuration
    """
    try:
        data = request.get_json() or {}
        strategy_name = data.get('strategy_name')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        initial_capital = float(data.get('initial_capital', 100000.0))
        strategy_config = data.get('strategy_config')
        
        if not strategy_name or not start_date_str or not end_date_str:
            return jsonify({
                'success': False,
                'error': 'strategy_name, start_date, and end_date are required'
            }), 400
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        service = get_simulation_service()
        result = await service.run_historical_simulation(
            strategy_name=strategy_name,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            strategy_config=strategy_config
        )
        
        return jsonify({
            'success': True,
            'data': result.dict()
        })
        
    except Exception as e:
        logger.error(f"Error running simulation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
