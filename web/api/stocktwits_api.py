"""
==============================================================================
FILE: web/api/stocktwits_api.py
ROLE: StockTwits API REST Endpoints
PURPOSE: RESTful endpoints for StockTwits sentiment and message streams.

INTEGRATION POINTS:
    - StockTwitsClient: Message retrieval
    - StockTwitsSentimentAnalyzer: Sentiment analysis

ENDPOINTS:
    GET /api/v1/stocktwits/stream/{symbol} - Get symbol stream
    GET /api/v1/stocktwits/trending - Get trending symbols
    GET /api/v1/stocktwits/sentiment/{symbol} - Analyze sentiment
    GET /api/v1/stocktwits/volume-spike/{symbol} - Detect volume spikes

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio

logger = logging.getLogger(__name__)

stocktwits_bp = Blueprint('stocktwits', __name__, url_prefix='/api/v1/stocktwits')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@stocktwits_bp.route('/stream/<symbol>', methods=['GET'])
def get_stream(symbol: str):
    """Get message stream for a symbol."""
    try:
        from services.social.stocktwits_client import get_stocktwits_client
        client = get_stocktwits_client()
        
        stream = _run_async(client.get_symbol_stream(symbol))
        
        return jsonify({
            "symbol": symbol,
            "messages": stream,
            "count": len(stream)
        })
    except Exception as e:
        logger.error(f"Failed to get stream: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@stocktwits_bp.route('/trending', methods=['GET'])
def get_trending():
    """Get trending symbols."""
    try:
        from services.social.stocktwits_client import get_stocktwits_client
        client = get_stocktwits_client()
        
        trending = _run_async(client.get_trending_symbols())
        
        return jsonify({
            "trending": trending,
            "count": len(trending)
        })
    except Exception as e:
        logger.error(f"Failed to get trending: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@stocktwits_bp.route('/sentiment/<symbol>', methods=['GET'])
def analyze_sentiment(symbol: str):
    """Analyze sentiment for a symbol."""
    try:
        from services.analysis.stocktwits_sentiment import get_stocktwits_sentiment
        analyzer = get_stocktwits_sentiment()
        
        result = _run_async(analyzer.analyze_symbol(symbol))
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to analyze sentiment: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@stocktwits_bp.route('/volume-spike/<symbol>', methods=['GET'])
def detect_volume_spike(symbol: str):
    """Detect volume spikes."""
    try:
        threshold = int(request.args.get('threshold', 50))
        
        from services.analysis.stocktwits_sentiment import get_stocktwits_sentiment
        analyzer = get_stocktwits_sentiment()
        
        result = _run_async(analyzer.detect_volume_spikes(symbol, threshold))
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to detect volume spike: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
