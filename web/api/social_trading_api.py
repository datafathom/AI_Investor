"""
==============================================================================
FILE: web/api/social_trading_api.py
ROLE: Social Trading API Endpoints
PURPOSE: REST endpoints for social trading and copy trading.

INTEGRATION POINTS:
    - SocialTradingService: Trader discovery
    - CopyTradingService: Copy trading execution
    - FrontendSocial: Social trading dashboard

ENDPOINTS:
    - POST /api/social-trading/profile/create
    - GET /api/social-trading/traders/top
    - POST /api/social-trading/follow
    - POST /api/social-trading/copy/create
    - POST /api/social-trading/copy/execute

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.social_trading.social_trading_service import get_social_trading_service
from services.social_trading.copy_trading_service import get_copy_trading_service

logger = logging.getLogger(__name__)

social_trading_bp = Blueprint('social_trading', __name__, url_prefix='/api/social-trading')


@social_trading_bp.route('/profile/create', methods=['POST'])
async def create_trader_profile():
    """
    Create trader profile.
    
    Request body:
        user_id: User identifier
        display_name: Display name
        bio: Optional bio
        is_public: Whether profile is public
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        display_name = data.get('display_name')
        bio = data.get('bio')
        is_public = data.get('is_public', True)
        
        if not user_id or not display_name:
            return jsonify({
                'success': False,
                'error': 'user_id and display_name are required'
            }), 400
        
        service = get_social_trading_service()
        profile = await service.create_trader_profile(
            user_id=user_id,
            display_name=display_name,
            bio=bio,
            is_public=is_public
        )
        
        return jsonify({
            'success': True,
            'data': profile.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating trader profile: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@social_trading_bp.route('/traders/top', methods=['GET'])
async def get_top_traders():
    """
    Get top traders.
    
    Query params:
        limit: Maximum number of traders (default: 20)
        metric: Ranking metric (default: total_return)
    """
    try:
        limit = int(request.args.get('limit', 20))
        metric = request.args.get('metric', 'total_return')
        
        service = get_social_trading_service()
        traders = await service.get_top_traders(limit, metric)
        
        return jsonify({
            'success': True,
            'data': [t.dict() for t in traders]
        })
        
    except Exception as e:
        logger.error(f"Error getting top traders: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@social_trading_bp.route('/follow', methods=['POST'])
async def follow_trader():
    """
    Follow a trader.
    
    Request body:
        follower_id: Follower user identifier
        trader_id: Trader identifier
    """
    try:
        data = request.get_json() or {}
        follower_id = data.get('follower_id')
        trader_id = data.get('trader_id')
        
        if not follower_id or not trader_id:
            return jsonify({
                'success': False,
                'error': 'follower_id and trader_id are required'
            }), 400
        
        service = get_social_trading_service()
        follow = await service.follow_trader(follower_id, trader_id)
        
        return jsonify({
            'success': True,
            'data': follow
        })
        
    except Exception as e:
        logger.error(f"Error following trader: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@social_trading_bp.route('/copy/create', methods=['POST'])
async def create_copy_config():
    """
    Create copy trading configuration.
    
    Request body:
        follower_id: Follower user identifier
        trader_id: Trader identifier
        allocation_percentage: Percentage of capital to allocate
        risk_multiplier: Risk adjustment factor
    """
    try:
        data = request.get_json() or {}
        follower_id = data.get('follower_id')
        trader_id = data.get('trader_id')
        allocation_percentage = float(data.get('allocation_percentage', 0))
        risk_multiplier = float(data.get('risk_multiplier', 1.0))
        
        if not follower_id or not trader_id or not allocation_percentage:
            return jsonify({
                'success': False,
                'error': 'follower_id, trader_id, and allocation_percentage are required'
            }), 400
        
        service = get_copy_trading_service()
        config = await service.create_copy_config(
            follower_id=follower_id,
            trader_id=trader_id,
            allocation_percentage=allocation_percentage,
            risk_multiplier=risk_multiplier
        )
        
        return jsonify({
            'success': True,
            'data': config.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating copy config: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@social_trading_bp.route('/copy/execute', methods=['POST'])
async def execute_copy_trade():
    """
    Execute copy trades for a trader's followers.
    
    Request body:
        trader_id: Trader identifier
        original_trade: Original trade details
    """
    try:
        data = request.get_json() or {}
        trader_id = data.get('trader_id')
        original_trade = data.get('original_trade')
        
        if not trader_id or not original_trade:
            return jsonify({
                'success': False,
                'error': 'trader_id and original_trade are required'
            }), 400
        
        service = get_copy_trading_service()
        copy_trades = await service.execute_copy_trade(trader_id, original_trade)
        
        return jsonify({
            'success': True,
            'data': [ct.dict() for ct in copy_trades]
        })
        
    except Exception as e:
        logger.error(f"Error executing copy trade: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
