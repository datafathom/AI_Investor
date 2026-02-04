"""
==============================================================================
FILE: services/social/youtube_client.py
ROLE: Visual Macro Intelligence
PURPOSE: Searches YouTube for macro strategy videos and retrieves captions.
         Mocks functionality for Phase 29.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import random
from typing import Dict, Any, List, Optional
from datetime import timezone, datetime
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class YouTubeClient:
    """
    Client for YouTube Data API v3.
    Defaults to MOCK MODE for Phase 29.
    """
    
    def __init__(self, api_key: Optional[str] = None, mock: bool = True):
        self.mock = mock
        sm = get_secret_manager()
        self.api_key = api_key or sm.get_secret('YOUTUBE_API_KEY')

    async def search_videos(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for videos based on macro keywords."""
        if self.mock:
            await asyncio.sleep(0.5)
            # Representative institutional content
            channels = ["MacroVoices", "RealVision", "Blockworks Macro", "Bloomberg Finance"]
            return [
                {
                    "video_id": f"vid_{random.randint(1000, 9999)}",
                    "title": f"Institutional View: {query} for 2026",
                    "channel": random.choice(channels),
                    "published_at": datetime.now(timezone.utc).isoformat(),
                    "thumbnail": "https://i.ytimg.com/vi/mock/hqdefault.jpg"
                } for _ in range(limit)
            ]
        return []

    async def get_video_transcript(self, video_id: str) -> str:
        """Fetch plain text transcript for a video."""
        if self.mock:
            return (
                "Today we are looking at the liquidity cycle. We expect $BTC to outperform "
                "equities due to the softening dollar. The historical precedent for this "
                "setup suggests institutional allocation will accelerate through Q3. "
                "However, risks remain in the credit markets as rates stay higher for longer."
            )
        return ""

    async def get_channel_statistics(self, channel_id: str) -> Dict[str, Any]:
        """Fetch statistics for a channel."""
        if self.mock:
            return {
                "viewCount": str(random.randint(1000000, 100000000)),
                "subscriberCount": str(random.randint(10000, 5000000)),
                "hiddenSubscriberCount": False,
                "videoCount": str(random.randint(100, 5000))
            }
        return {}

_instance = None

def get_youtube_client(mock: bool = True) -> YouTubeClient:
    global _instance
    if _instance is None:
        _instance = YouTubeClient(mock=mock)
    return _instance
