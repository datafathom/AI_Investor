"""
==============================================================================
FILE: web/api/watchlist_api.py
ROLE: Watchlist & Alerts API Endpoints
PURPOSE: REST endpoints for watchlist management and alerts.

INTEGRATION POINTS:
    - WatchlistService: Watchlist management
    - AlertService: Alert system
    - FrontendWatchlist: Watchlist dashboard widgets

ENDPOINTS:
    - POST /api/watchlist/create
    - GET /api/watchlist/user/:user_id
    - POST /api/watchlist/:watchlist_id/add
    - POST /api/watchlist/:watchlist_id/remove
    - POST /api/alert/create
    - GET /api/alert/user/:user_id
    - POST /api/alert/:alert_id/cancel

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.watchlist.watchlist_service import get_watchlist_service
from services.watchlist.alert_service import get_alert_service

logger = logging.getLogger(__name__)

watchlist_bp = Blueprint('watchlist', __name__, url_prefix='/api/watchlist')
alert_bp = Blueprint('alert', __name__, url_prefix='/api/alert')


@watchlist_bp.route('/create', methods=['POST'])
async def create_watchlist():
    """
    Create a new watchlist.
    
    Request body:
        user_id: User identifier
        watchlist_name: Name of watchlist
        symbols: Optional initial symbols
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        watchlist_name = data.get('watchlist_name')
        symbols = data.get('symbols')
        
        if not user_id or not watchlist_name:
            return jsonify({
                'success': False,
                'error': 'user_id and watchlist_name are required'
            }), 400
        
        service = get_watchlist_service()
        watchlist = await service.create_watchlist(
            user_id=user_id,
            watchlist_name=watchlist_name,
            symbols=symbols
        )
        
        return jsonify({
            'success': True,
            'data': watchlist.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating watchlist: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@watchlist_bp.route('/user/<user_id>', methods=['GET'])
async def get_user_watchlists(user_id: str):
    """
    Get all watchlists for user.
    """
    try:
        service = get_watchlist_service()
        watchlists = await service.get_user_watchlists(user_id)
        
        return jsonify({
            'success': True,
            'data': [w.dict() for w in watchlists]
        })
        
    except Exception as e:
        logger.error(f"Error getting watchlists: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@watchlist_bp.route('/<watchlist_id>/add', methods=['POST'])
async def add_symbol(watchlist_id: str):
    """
    Add symbol to watchlist.
    
    Request body:
        symbol: Stock symbol to add
    """
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': 'symbol is required'
            }), 400
        
        service = get_watchlist_service()
        watchlist = await service.add_symbol(watchlist_id, symbol)
        
        return jsonify({
            'success': True,
            'data': watchlist.dict()
        })
        
    except Exception as e:
        logger.error(f"Error adding symbol: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@watchlist_bp.route('/<watchlist_id>/remove', methods=['POST'])
async def remove_symbol(watchlist_id: str):
    """
    Remove symbol from watchlist.
    
    Request body:
        symbol: Stock symbol to remove
    """
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': 'symbol is required'
            }), 400
        
        service = get_watchlist_service()
        watchlist = await service.remove_symbol(watchlist_id, symbol)
        
        return jsonify({
            'success': True,
            'data': watchlist.dict()
        })
        
    except Exception as e:
        logger.error(f"Error removing symbol: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@alert_bp.route('/create', methods=['POST'])
async def create_alert():
    """
    Create a price alert.
    
    Request body:
        user_id: User identifier
        symbol: Stock symbol
        alert_type: Alert type (price_above, price_below, price_change)
        threshold: Alert threshold
        notification_methods: Notification methods
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        symbol = data.get('symbol')
        alert_type = data.get('alert_type')
        threshold = float(data.get('threshold', 0))
        notification_methods = data.get('notification_methods', ['email'])
        
        if not user_id or not symbol or not alert_type or not threshold:
            return jsonify({
                'success': False,
                'error': 'user_id, symbol, alert_type, and threshold are required'
            }), 400
        
        service = get_alert_service()
        alert = await service.create_price_alert(
            user_id=user_id,
            symbol=symbol,
            alert_type=alert_type,
            threshold=threshold,
            notification_methods=notification_methods
        )
        
        return jsonify({
            'success': True,
            'data': alert.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@alert_bp.route('/user/<user_id>', methods=['GET'])
async def get_user_alerts(user_id: str):
    """
    Get all alerts for user.
    """
    try:
        service = get_alert_service()
        # In production, would fetch from database
        alerts = [a for a in service.active_alerts.values() if a.user_id == user_id]
        
        return jsonify({
            'success': True,
            'data': [a.dict() for a in alerts]
        })
        
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@alert_bp.route('/<alert_id>/cancel', methods=['POST'])
async def cancel_alert(alert_id: str):
    """
    Cancel an alert.
    """
    try:
        service = get_alert_service()
        alert = await service._get_alert(alert_id)
        
        if not alert:
            return jsonify({
                'success': False,
                'error': 'Alert not found'
            }), 404
        
        alert.status = AlertStatus.CANCELLED
        await service._save_alert(alert)
        
        if alert_id in service.active_alerts:
            del service.active_alerts[alert_id]
        
        return jsonify({
            'success': True,
            'data': alert.dict()
        })
        
    except Exception as e:
        logger.error(f"Error cancelling alert: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
