"""
==============================================================================
FILE: web/api/youtube_api.py
ROLE: YouTube API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for searching trading videos and fetching channel stats.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Header, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict, Any

from services.social.youtube_client import get_youtube_client

logger = logging.getLogger(__name__)


def get_youtube_provider():
    return get_youtube_client()

router = APIRouter(prefix="/api/v1/youtube", tags=["YouTube"])


class VideoSearchRequest(BaseModel):
    query: str
    max_results: int = 10


@router.get("/search")
async def search_videos(
    q: str = Query(...),
    max_results: int = Query(10, ge=1, le=50),
    service=Depends(get_youtube_provider)
):
    """Search for trading and finance videos."""
    try:
        videos = await service.search_videos(q, max_results=max_results)
        return {
            "success": True,
            "data": {
                "query": q, 
                "videos": videos, 
                "count": len(videos)
            }
        }
    except Exception as e:
        logger.exception("YouTube search failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/channel/{channel_id}")
async def get_channel_stats(
    channel_id: str,
    service=Depends(get_youtube_provider)
):
    """Get statistics for a specific YouTube channel."""
    try:
        stats = await service.get_channel_statistics(channel_id)
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.exception("Failed to get channel stats")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
