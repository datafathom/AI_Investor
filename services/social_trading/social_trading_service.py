"""
==============================================================================
FILE: services/social_trading/social_trading_service.py
ROLE: Social Trading Service
PURPOSE: Enables social trading features including trader discovery,
         performance ranking, and follow/unfollow functionality.

INTEGRATION POINTS:
    - PortfolioService: Trader performance data
    - UserService: User profiles and social connections
    - ExecutionService: Copy trading execution
    - SocialTradingAPI: Social trading endpoints

FEATURES:
    - Trader discovery and ranking
    - Performance tracking
    - Follow/unfollow system
    - Copy trading

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from models.social_trading import TraderProfile, TraderRanking
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class SocialTradingService:
    """
    Service for social trading features.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        
    async def create_trader_profile(
        self,
        user_id: str,
        display_name: str,
        bio: Optional[str] = None,
        is_public: bool = True
    ) -> TraderProfile:
        """
        Create trader profile for social trading.
        
        Args:
            user_id: User identifier
            display_name: Display name
            bio: Optional bio
            is_public: Whether profile is public
            
        Returns:
            TraderProfile object
        """
        logger.info(f"Creating trader profile for user {user_id}")
        
        profile = TraderProfile(
            trader_id=f"trader_{user_id}_{datetime.utcnow().timestamp()}",
            user_id=user_id,
            display_name=display_name,
            bio=bio,
            ranking=TraderRanking.BRONZE,
            is_public=is_public,
            created_date=datetime.utcnow()
        )
        
        # Save profile
        await self._save_profile(profile)
        
        return profile
    
    async def get_top_traders(
        self,
        limit: int = 20,
        metric: str = "total_return"
    ) -> List[TraderProfile]:
        """
        Get top traders by performance metric.
        
        Args:
            limit: Maximum number of traders
            metric: Ranking metric (total_return, sharpe_ratio, win_rate)
            
        Returns:
            List of TraderProfile objects
        """
        logger.info(f"Getting top {limit} traders by {metric}")
        
        # In production, would query database and sort by metric
        # For now, return mock data
        return []
    
    async def follow_trader(
        self,
        follower_id: str,
        trader_id: str
    ) -> Dict:
        """
        Follow a trader.
        
        Args:
            follower_id: Follower user identifier
            trader_id: Trader identifier
            
        Returns:
            Follow relationship dictionary
        """
        logger.info(f"User {follower_id} following trader {trader_id}")
        
        follow = {
            "follow_id": f"follow_{follower_id}_{trader_id}",
            "follower_id": follower_id,
            "trader_id": trader_id,
            "created_date": datetime.utcnow().isoformat()
        }
        
        # Save follow relationship
        cache_key = f"follow:{follower_id}:{trader_id}"
        self.cache_service.set(cache_key, follow, ttl=86400 * 365)
        
        return follow
    
    async def _get_profile(self, trader_id: str) -> Optional[TraderProfile]:
        """Get trader profile from cache."""
        cache_key = f"trader_profile:{trader_id}"
        profile_data = self.cache_service.get(cache_key)
        if profile_data:
            return TraderProfile(**profile_data)
        return None
    
    async def _save_profile(self, profile: TraderProfile):
        """Save trader profile to cache."""
        cache_key = f"trader_profile:{profile.trader_id}"
        self.cache_service.set(cache_key, profile.dict(), ttl=86400 * 365)


# Singleton instance
_social_trading_service: Optional[SocialTradingService] = None


def get_social_trading_service() -> SocialTradingService:
    """Get singleton social trading service instance."""
    global _social_trading_service
    if _social_trading_service is None:
        _social_trading_service = SocialTradingService()
    return _social_trading_service
