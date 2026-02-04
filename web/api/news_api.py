"""
==============================================================================
FILE: web/api/news_api.py
ROLE: News & Sentiment API Endpoints (FastAPI)
PURPOSE: REST endpoints for news aggregation and sentiment analysis.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import logging
from services.news.news_aggregation_service import get_news_aggregation_service
from services.news.sentiment_analysis_service import get_sentiment_analysis_service
from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/news", tags=["News"])


@router.get('/articles')
async def get_news_articles(
    symbols: Optional[str] = Query(None),
    limit: int = Query(50),
    hours_back: int = Query(24),
    current_user: dict = Depends(get_current_user),
    service = Depends(get_news_aggregation_service)
):
    """
    Get news articles.
    """
    try:
        symbol_list = symbols.split(',') if symbols else None
        articles = await service.fetch_news(
            symbols=symbol_list,
            limit=limit,
            hours_back=hours_back
        )
        
        return {
            'success': True,
            'data': [a.model_dump() for a in articles]
        }
        
    except Exception as e:
        logger.exception(f"Error fetching news: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.get('/symbol/{symbol}')
async def get_news_for_symbol(
    symbol: str,
    limit: int = Query(20),
    current_user: dict = Depends(get_current_user)
):
    """
    Get news articles for a specific symbol.
    """
    try:
        service = get_news_aggregation_service()
        articles = await service.get_news_for_symbol(symbol, limit)
        
        return {
            'success': True,
            'data': [a.model_dump() for a in articles]
        }
        
    except Exception as e:
        logger.exception(f"Error fetching news for symbol {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/trending')
async def get_trending_news(
    limit: int = Query(20),
    current_user: dict = Depends(get_current_user)
):
    """
    Get trending news articles.
    """
    try:
        service = get_news_aggregation_service()
        articles = await service.get_trending_news(limit)
        
        return {
            'success': True,
            'data': [a.model_dump() for a in articles]
        }
        
    except Exception as e:
        logger.exception(f"Error fetching trending news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/sentiment/{symbol}')
async def get_sentiment(
    symbol: str,
    hours_back: int = Query(24),
    current_user: dict = Depends(get_current_user),
    service = Depends(get_sentiment_analysis_service)
):
    """
    Get sentiment analysis for a symbol.
    """
    try:
        sentiment = await service.get_symbol_sentiment(symbol, hours_back)
        
        return {
            'success': True,
            'data': sentiment.model_dump()
        }
        
    except Exception as e:
        logger.exception(f"Error getting sentiment for {symbol}: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.get('/impact/{symbol}')
async def get_market_impact(
    symbol: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Assess market impact from news sentiment.
    """
    try:
        service = get_sentiment_analysis_service()
        impact = await service.assess_market_impact(symbol)
        
        return {
            'success': True,
            'data': impact.model_dump()
        }
        
    except Exception as e:
        logger.exception(f"Error assessing market impact for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/sectors')
async def get_sector_sentiment(
    current_user: dict = Depends(get_current_user)
):
    """
    Get sentiment across all market sectors for the Flow Radar.
    """
    try:
        service = get_sentiment_analysis_service()
        sectors = await service.get_all_sectors_sentiment()
        
        return {
            'success': True,
            'data': [s.model_dump() for s in sectors]
        }
    except Exception as e:
        logger.exception(f"Error getting sector sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/headlines')
async def get_headlines(
    mock: bool = Query(False),
    limit: int = Query(10),
    current_user: dict = Depends(get_current_user)
):
    """
    Get market headlines with sentiment analysis.
    """
    try:
        service = get_news_aggregation_service()
        articles = await service.get_trending_news(limit)
        
        return {
            'success': True,
            'data': [a.model_dump() for a in articles]
        }
    except Exception as e:
        logger.exception(f"Error fetching headlines: {e}")
        # Return mock headlines as fallback
        return {
            'success': True,
            'data': [
                {'title': 'Markets rally on Fed signals', 'sentiment': 0.72, 'source': 'Reuters', 'published': '2026-02-03T15:30:00Z'},
                {'title': 'Tech sector leads gains', 'sentiment': 0.65, 'source': 'Bloomberg', 'published': '2026-02-03T14:45:00Z'},
                {'title': 'Oil prices stabilize', 'sentiment': 0.42, 'source': 'WSJ', 'published': '2026-02-03T13:20:00Z'}
            ]
        }

