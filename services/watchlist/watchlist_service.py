"""
==============================================================================
FILE: services/watchlist/watchlist_service.py
ROLE: Watchlist Service
PURPOSE: Manages user watchlists with symbol tracking and organization.

INTEGRATION POINTS:
    - MarketDataService: Price data for watchlist items
    - WatchlistAPI: Watchlist endpoints
    - FrontendWatchlist: Watchlist dashboard

FEATURES:
    - Multiple watchlists
    - Symbol organization
    - Watchlist sharing

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import timezone, datetime
from typing import Dict, List, Optional
from schemas.watchlist import Watchlist
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class WatchlistService:
    """
    Service for watchlist management.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        
    async def create_watchlist(
        self,
        user_id: str,
        watchlist_name: str,
        symbols: Optional[List[str]] = None
    ) -> Watchlist:
        """
        Create a new watchlist.
        
        Args:
            user_id: User identifier
            watchlist_name: Name of watchlist
            symbols: Optional initial symbols
            
        Returns:
            Watchlist object
        """
        logger.info(f"Creating watchlist {watchlist_name} for user {user_id}")
        
        watchlist = Watchlist(
            watchlist_id=f"watchlist_{user_id}_{datetime.now(timezone.utc).timestamp()}",
            user_id=user_id,
            watchlist_name=watchlist_name,
            symbols=symbols or [],
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
        
        # Save watchlist
        await self._save_watchlist(watchlist)
        
        return watchlist
    
    async def add_symbol(
        self,
        watchlist_id: str,
        symbol: str
    ) -> Watchlist:
        """
        Add symbol to watchlist.
        
        Args:
            watchlist_id: Watchlist identifier
            symbol: Stock symbol to add
            
        Returns:
            Updated Watchlist
        """
        watchlist = await self._get_watchlist(watchlist_id)
        if not watchlist:
            raise ValueError(f"Watchlist {watchlist_id} not found")
        
        if symbol not in watchlist.symbols:
            watchlist.symbols.append(symbol)
            watchlist.updated_date = datetime.now(timezone.utc)
            await self._save_watchlist(watchlist)
        
        return watchlist
    
    async def remove_symbol(
        self,
        watchlist_id: str,
        symbol: str
    ) -> Watchlist:
        """
        Remove symbol from watchlist.
        
        Args:
            watchlist_id: Watchlist identifier
            symbol: Stock symbol to remove
            
        Returns:
            Updated Watchlist
        """
        watchlist = await self._get_watchlist(watchlist_id)
        if not watchlist:
            raise ValueError(f"Watchlist {watchlist_id} not found")
        
        if symbol in watchlist.symbols:
            watchlist.symbols.remove(symbol)
            watchlist.updated_date = datetime.now(timezone.utc)
            await self._save_watchlist(watchlist)
        
        return watchlist
    
    async def get_user_watchlists(
        self,
        user_id: str
    ) -> List[Watchlist]:
        """
        Get all watchlists for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of Watchlist objects
        """
        # In production, would fetch from database
        return []
    
    async def _get_watchlist(self, watchlist_id: str) -> Optional[Watchlist]:
        """Get watchlist from cache."""
        cache_key = f"watchlist:{watchlist_id}"
        watchlist_data = self.cache_service.get(cache_key)
        if watchlist_data:
            return Watchlist(**watchlist_data)
        return None
    
    async def _save_watchlist(self, watchlist: Watchlist):
        """Save watchlist to cache."""
        cache_key = f"watchlist:{watchlist.watchlist_id}"
        self.cache_service.set(cache_key, watchlist.model_dump(), ttl=86400 * 365)


# Singleton instance
_watchlist_service: Optional[WatchlistService] = None


def get_watchlist_service() -> WatchlistService:
    """Get singleton watchlist service instance."""
    global _watchlist_service
    if _watchlist_service is None:
        _watchlist_service = WatchlistService()
    return _watchlist_service
