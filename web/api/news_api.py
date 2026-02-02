"""
==============================================================================
FILE: web/api/news_api.py
ROLE: News & Sentiment API Endpoints
PURPOSE: REST endpoints for news aggregation and sentiment analysis.

INTEGRATION POINTS:
    - NewsAggregationService: News collection
    - SentimentAnalysisService: Sentiment scoring
    - FrontendNews: News dashboard widgets

ENDPOINTS:
    - GET /api/news/articles
    - GET /api/news/symbol/:symbol
    - GET /api/news/trending
    - GET /api/news/sentiment/:symbol
    - GET /api/news/impact/:symbol

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.news.news_aggregation_service import get_news_aggregation_service
from services.news.sentiment_analysis_service import get_sentiment_analysis_service

logger = logging.getLogger(__name__)

news_bp = Blueprint('news', __name__, url_prefix='/api/news')


@news_bp.route('/articles', methods=['GET'])
async def get_news_articles():
    """
    Get news articles.
    
    Query params:
        symbols: Comma-separated list of symbols
        limit: Maximum number of articles (default: 50)
        hours_back: Hours to look back (default: 24)
    """
    try:
        symbols_str = request.args.get('symbols')
        symbols = symbols_str.split(',') if symbols_str else None
        limit = int(request.args.get('limit', 50))
        hours_back = int(request.args.get('hours_back', 24))
        
        service = get_news_aggregation_service()
        articles = await service.fetch_news(
            symbols=symbols,
            limit=limit,
            hours_back=hours_back
        )
        
        return jsonify({
            'success': True,
            'data': [a.dict() for a in articles]
        })
        
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/symbol/<symbol>', methods=['GET'])
async def get_news_for_symbol(symbol: str):
    """
    Get news articles for a specific symbol.
    
    Query params:
        limit: Maximum number of articles (default: 20)
    """
    try:
        limit = int(request.args.get('limit', 20))
        
        service = get_news_aggregation_service()
        articles = await service.get_news_for_symbol(symbol, limit)
        
        return jsonify({
            'success': True,
            'data': [a.dict() for a in articles]
        })
        
    except Exception as e:
        logger.error(f"Error fetching news for symbol: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/trending', methods=['GET'])
async def get_trending_news():
    """
    Get trending news articles.
    
    Query params:
        limit: Maximum number of articles (default: 20)
    """
    try:
        limit = int(request.args.get('limit', 20))
        
        service = get_news_aggregation_service()
        articles = await service.get_trending_news(limit)
        
        return jsonify({
            'success': True,
            'data': [a.dict() for a in articles]
        })
        
    except Exception as e:
        logger.error(f"Error fetching trending news: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/sentiment/<symbol>', methods=['GET'])
async def get_sentiment(symbol: str):
    """
    Get sentiment analysis for a symbol.
    
    Query params:
        hours_back: Hours to look back (default: 24)
    """
    try:
        hours_back = int(request.args.get('hours_back', 24))
        
        service = get_sentiment_analysis_service()
        sentiment = await service.get_symbol_sentiment(symbol, hours_back)
        
        return jsonify({
            'success': True,
            'data': sentiment.dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting sentiment: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/impact/<symbol>', methods=['GET'])
async def get_market_impact(symbol: str):
    """
    Assess market impact from news sentiment.
    """
    try:
        service = get_sentiment_analysis_service()
        impact = await service.assess_market_impact(symbol)
        
        return jsonify({
            'success': True,
            'data': impact.dict()
        })
        
    except Exception as e:
        logger.error(f"Error assessing market impact: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/sectors', methods=['GET'])
async def get_sector_sentiment():
    """
    Get sentiment across all market sectors for the Flow Radar.
    """
    try:
        service = get_sentiment_analysis_service()
        sectors = await service.get_all_sectors_sentiment()
        
        return jsonify({
            'success': True,
            'data': [s.dict() for s in sectors]
        })
    except Exception as e:
        logger.error(f"Error getting sector sentiment: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
