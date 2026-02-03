"""
==============================================================================
FILE: web/api/facebook_hype_api.py
ROLE: Facebook Hype API REST Endpoints
PURPOSE: RESTful endpoints for monitoring Facebook pages for stock mentions.

INTEGRATION POINTS:
    - FacebookHypeService: Page monitoring
    - HypeTrackerService: Spike alerts

ENDPOINTS:
    POST /api/v1/facebook/monitor - Monitor a page for ticker mentions
    GET /api/v1/facebook/aggregates - Get hourly aggregates
    POST /api/v1/facebook/check-spike - Check for mention spikes

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

facebook_hype_bp = Blueprint('facebook_hype', __name__, url_prefix='/api/v1/facebook_hype')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def _get_access_token():
    """Get Facebook access token from request."""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    data = request.json or {}
    return data.get('access_token')


# =============================================================================
# Monitor Page Endpoint
# =============================================================================

@facebook_hype_bp.route('/monitor', methods=['POST'])
def monitor_page():
    """
    Monitor a Facebook page for stock ticker mentions.
    
    Request Body:
        {
            "page_id": "page_id_or_username",
            "tickers": ["AAPL", "MSFT"],  // optional
            "access_token": "facebook_access_token"  // optional if in header
        }
        
    Returns:
        JSON with mention counts
    """
    try:
        data = request.json or {}
        page_id = data.get('page_id')
        tickers = data.get('tickers')
        access_token = _get_access_token()
        
        if not page_id:
            return jsonify({
                "error": "Missing page_id"
            }), 400
        
        if not access_token:
            return jsonify({
                "error": "Missing Facebook access token"
            }), 401
        
        from services.social.facebook_hype_service import get_facebook_hype_service
        hype_service = get_facebook_hype_service()
        
        result = _run_async(hype_service.monitor_page(
            page_id=page_id,
            access_token=access_token,
            tickers=tickers
        ))
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Page monitoring failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to monitor page",
            "message": str(e)
        }), 500


# =============================================================================
# Get Aggregates Endpoint
# =============================================================================

@facebook_hype_bp.route('/aggregates', methods=['GET'])
def get_aggregates():
    """
    Get hourly aggregated mention counts.
    
    Query Params:
        page_id: Optional page ID filter
        ticker: Optional ticker filter
        
    Returns:
        JSON with aggregated counts
    """
    try:
        page_id = request.args.get('page_id')
        ticker = request.args.get('ticker')
        
        from services.social.facebook_hype_service import get_facebook_hype_service
        hype_service = get_facebook_hype_service()
        
        result = _run_async(hype_service.get_hourly_aggregates(
            page_id=page_id,
            ticker=ticker
        ))
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Failed to get aggregates: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to get aggregates",
            "message": str(e)
        }), 500


# =============================================================================
# Check Spike Endpoint
# =============================================================================

@facebook_hype_bp.route('/check-spike', methods=['POST'])
def check_spike():
    """
    Check if mention count has spiked above threshold.
    
    Request Body:
        {
            "page_id": "page_id",
            "ticker": "AAPL",
            "threshold_multiplier": 2.0  // optional
        }
        
    Returns:
        JSON with spike alert if detected
    """
    try:
        data = request.json or {}
        page_id = data.get('page_id')
        ticker = data.get('ticker')
        threshold = float(data.get('threshold_multiplier', 2.0))
        
        if not page_id or not ticker:
            return jsonify({
                "error": "Missing page_id or ticker"
            }), 400
        
        from services.social.facebook_hype_service import get_facebook_hype_service
        hype_service = get_facebook_hype_service()
        
        result = _run_async(hype_service.check_for_spikes(
            page_id=page_id,
            ticker=ticker,
            threshold_multiplier=threshold
        ))
        
        if result:
            return jsonify({
                "spike_detected": True,
                "alert": result
            })
        else:
            return jsonify({
                "spike_detected": False
            })
        
    except Exception as e:
        logger.error(f"Spike check failed: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to check for spikes",
            "message": str(e)
        }), 500
