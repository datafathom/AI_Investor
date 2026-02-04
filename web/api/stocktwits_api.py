"""
==============================================================================
FILE: web/api/stocktwits_api.py
ROLE: StockTwits API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for StockTwits sentiment and message streams.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import logging

from services.social.stocktwits_client import get_stocktwits_client
from services.analysis.stocktwits_sentiment import get_stocktwits_sentiment


def get_stocktwits_provider():
    return get_stocktwits_client()


def get_sentiment_provider():
    return get_stocktwits_sentiment()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/stocktwits", tags=["StockTwits"])


@router.get("/stream/{symbol}")
async def get_stream(symbol: str, client=Depends(get_stocktwits_provider)):
    """Get message stream for a symbol."""
    try:
        data = await client.get_symbol_stream(symbol)
        
        return {
            "success": True,
            "data": {
                "symbol": symbol,
                "messages": data,
                "count": len(data)
            }
        }
    except Exception as e:
        logger.exception("Failed to get stream")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/trending")
async def get_trending(client=Depends(get_stocktwits_provider)):
    """Get trending symbols."""
    try:
        data = await client.get_trending_symbols()
        
        return {
            "success": True,
            "data": {
                "trending": data,
                "count": len(data)
            }
        }
    except Exception as e:
        logger.exception("Failed to get trending")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/sentiment/{symbol}")
async def analyze_sentiment(symbol: str, analyzer=Depends(get_sentiment_provider)):
    """Analyze sentiment for a symbol."""
    try:
        data = await analyzer.analyze_symbol(symbol)
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Failed to analyze sentiment")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/volume-spike/{symbol}")
async def detect_volume_spike(
    symbol: str, 
    threshold: int = Query(50, description="Volume spike threshold percentage"),
    analyzer=Depends(get_sentiment_provider)
):
    """Detect volume spikes."""
    try:
        data = await analyzer.detect_volume_spikes(symbol, threshold)
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Failed to detect volume spike")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
