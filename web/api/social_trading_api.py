from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict
from pydantic import BaseModel
import logging

from services.social_trading.feed import SocialTradingFeed
from services.social_trading.influencer_tracker import InfluencerTracker

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/social-trading", tags=["Social Trading"])

@router.get("/feed")
async def get_feed(limit: int = 20):
    service = SocialTradingFeed()
    return await service.get_feed(limit)

@router.get("/influencers")
async def list_influencers():
    service = InfluencerTracker()
    return await service.list_influencers()

@router.post("/influencers/{id}/follow")
async def follow_influencer(id: str):
    service = InfluencerTracker()
    is_following = await service.follow(id)
    return {"success": True, "is_following": is_following}
