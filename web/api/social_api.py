"""
==============================================================================
FILE: web/api/social_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes social sentiment data (Reddit) to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import logging

from services.social.reddit_service import get_reddit_client


def get_reddit_provider(mock: bool = Query(True)):
    return get_reddit_client(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/social", tags=["Social"])


@router.get("/reddit/posts")
async def get_reddit_posts(
    subreddit: str = Query("wallstreetbets"),
    limit: int = Query(10),
    client=Depends(get_reddit_provider)
):
    try:
        posts = await client.get_subreddit_posts(subreddit, limit)
        return {"success": True, "data": [p.model_dump() for p in posts]}
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to fetch reddit posts: %s", e)
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/reddit/analyze/{ticker}")
async def analyze_ticker_sentiment(
    ticker: str,
    client=Depends(get_reddit_provider)
):
    """Get sentiment analysis for a ticker."""
    try:
        data = await client.analyze_sentiment(ticker)
        return {"success": True, "data": data}
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to analyze sentiment for %s: %s", ticker, e)
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/sentiment/heatmap")
async def get_sentiment_heatmap():
    """Get sentiment heatmap data (aggregated by sector/topic)."""
    # Mock data for demonstration
    heatmap = [
        {"id": "Technology", "value": 0.85, "count": 150, "color": "hsl(var(--success-h), 70%, 50%)"},
        {"id": "Finance", "value": 0.45, "count": 120, "color": "hsl(var(--primary-h), 70%, 50%)"},
        {"id": "Healthcare", "value": -0.25, "count": 80, "color": "hsl(var(--danger-h), 70%, 50%)"},
        {"id": "Energy", "value": 0.15, "count": 60, "color": "hsl(var(--primary-h), 50%, 40%)"},
        {"id": "Consumer", "value": 0.65, "count": 200, "color": "hsl(var(--success-h), 60%, 40%)"},
        {"id": "Crypto", "value": 0.95, "count": 450, "color": "hsl(var(--accent-h), 80%, 60%)"},
    ]
    return {
        "success": True,
        "data": heatmap
    }
