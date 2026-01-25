"""
==============================================================================
FILE: services/marketplace/marketplace_service.py
ROLE: Marketplace Service
PURPOSE: Provides extension listing, reviews, ratings, and installation
         management.

INTEGRATION POINTS:
    - ExtensionFramework: Extension infrastructure
    - PaymentService: Payment processing
    - MarketplaceAPI: Marketplace endpoints
    - FrontendMarketplace: Marketplace dashboard

FEATURES:
    - Extension listing
    - Reviews and ratings
    - Installation management
    - Payment processing

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from models.marketplace import ExtensionReview
from services.marketplace.extension_framework import get_extension_framework
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class MarketplaceService:
    """
    Service for marketplace management.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.framework = get_extension_framework()
        self.cache_service = get_cache_service()
        
    async def add_review(
        self,
        extension_id: str,
        user_id: str,
        rating: int,
        comment: Optional[str] = None
    ) -> ExtensionReview:
        """
        Add review for extension.
        
        Args:
            extension_id: Extension identifier
            user_id: User identifier
            rating: Rating (1-5)
            comment: Optional comment
            
        Returns:
            ExtensionReview object
        """
        logger.info(f"Adding review for extension {extension_id}")
        
        review = ExtensionReview(
            review_id=f"review_{extension_id}_{user_id}_{datetime.utcnow().timestamp()}",
            extension_id=extension_id,
            user_id=user_id,
            rating=rating,
            comment=comment,
            created_date=datetime.utcnow()
        )
        
        # Save review
        await self._save_review(review)
        
        return review
    
    async def install_extension(
        self,
        extension_id: str,
        user_id: str
    ) -> Dict:
        """
        Install extension for user.
        
        Args:
            extension_id: Extension identifier
            user_id: User identifier
            
        Returns:
            Installation dictionary
        """
        logger.info(f"Installing extension {extension_id} for user {user_id}")
        
        installation = {
            "installation_id": f"install_{user_id}_{extension_id}_{datetime.utcnow().timestamp()}",
            "extension_id": extension_id,
            "user_id": user_id,
            "installed_date": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        # Save installation
        cache_key = f"installation:{installation['installation_id']}"
        self.cache_service.set(cache_key, installation, ttl=86400 * 365)
        
        return installation
    
    async def _save_review(self, review: ExtensionReview):
        """Save review to cache."""
        cache_key = f"review:{review.review_id}"
        self.cache_service.set(cache_key, review.dict(), ttl=86400 * 365)


# Singleton instance
_marketplace_service: Optional[MarketplaceService] = None


def get_marketplace_service() -> MarketplaceService:
    """Get singleton marketplace service instance."""
    global _marketplace_service
    if _marketplace_service is None:
        _marketplace_service = MarketplaceService()
    return _marketplace_service
