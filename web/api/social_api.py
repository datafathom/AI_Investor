"""
==============================================================================
FILE: web/api/social_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes social sentiment data (Reddit) to the frontend.
==============================================================================
"""

import asyncio
import logging
from flask import Blueprint, jsonify, request

from services.social.reddit_service import get_reddit_client

logger = logging.getLogger(__name__)

social_bp = Blueprint('social_bp', __name__)

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@social_bp.route('/reddit/posts', methods=['GET'])
def get_reddit_posts():
    """
    Get top posts from a subreddit.
    Query: ?subreddit=wallstreetbets&limit=10&mock=true
    """
    subreddit = request.args.get('subreddit', 'wallstreetbets')
    limit = int(request.args.get('limit', 10))
    # Phase 8 defaults to mock=True unless specified otherwise, but service defaults to mock=True anyway
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    
    client = get_reddit_client(mock=use_mock)
    
    try:
        posts = _run_async(client.get_subreddit_posts(subreddit, limit))
        return jsonify([p.model_dump() for p in posts])
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to fetch reddit posts: %s", e)
        return jsonify({"error": str(e)}), 500

@social_bp.route('/reddit/analyze/<ticker>', methods=['GET'])
def analyze_ticker_sentiment(ticker: str):
    """
    Get sentiment analysis for a ticker.
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_reddit_client(mock=use_mock)
    
    try:
        result = _run_async(client.analyze_sentiment(ticker))
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to analyze sentiment for %s: %s", ticker, e)
        return jsonify({"error": str(e)}), 500

@social_bp.route('/sentiment/heatmap', methods=['GET'])
def get_sentiment_heatmap():
    """
    Get sentiment heatmap data (aggregated by sector/topic).
    """
    # Mock data for demonstration
    heatmap = [
        {"id": "Technology", "value": 0.85, "count": 150, "color": "hsl(var(--success-h), 70%, 50%)"},
        {"id": "Finance", "value": 0.45, "count": 120, "color": "hsl(var(--primary-h), 70%, 50%)"},
        {"id": "Healthcare", "value": -0.25, "count": 80, "color": "hsl(var(--danger-h), 70%, 50%)"},
        {"id": "Energy", "value": 0.15, "count": 60, "color": "hsl(var(--primary-h), 50%, 40%)"},
        {"id": "Consumer", "value": 0.65, "count": 200, "color": "hsl(var(--success-h), 60%, 40%)"},
        {"id": "Crypto", "value": 0.95, "count": 450, "color": "hsl(var(--accent-h), 80%, 60%)"},
    ]
    return jsonify({
        "status": "success",
        "data": heatmap
    })
