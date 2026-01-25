"""
Tests for Marketplace Service
Comprehensive test coverage for extension reviews, ratings, and installation
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.marketplace.marketplace_service import MarketplaceService
from models.marketplace import ExtensionReview


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.marketplace.marketplace_service.get_extension_framework'), \
         patch('services.marketplace.marketplace_service.get_cache_service'):
        return MarketplaceService()


@pytest.mark.asyncio
async def test_add_review(service):
    """Test adding extension review."""
    service._save_review = AsyncMock()
    
    result = await service.add_review(
        extension_id="ext_123",
        user_id="user_123",
        rating=5,
        comment="Great extension!"
    )
    
    assert result is not None
    assert isinstance(result, ExtensionReview)
    assert result.extension_id == "ext_123"
    assert result.rating == 5


@pytest.mark.asyncio
async def test_get_extension_reviews(service):
    """Test getting extension reviews."""
    service._get_reviews_from_db = AsyncMock(return_value=[
        ExtensionReview(
            review_id="review_1",
            extension_id="ext_123",
            user_id="user_1",
            rating=5,
            comment="Great!",
            created_date=datetime.utcnow()
        ),
        ExtensionReview(
            review_id="review_2",
            extension_id="ext_123",
            user_id="user_2",
            rating=4,
            comment="Good extension",
            created_date=datetime.utcnow()
        ),
    ])
    
    result = await service.get_extension_reviews("ext_123")
    
    assert result is not None
    assert len(result) == 2


@pytest.mark.asyncio
async def test_install_extension(service):
    """Test extension installation."""
    service.framework._get_extension = AsyncMock(return_value={
        'extension_id': 'ext_123',
        'status': 'approved'
    })
    service._save_installation = AsyncMock(return_value=True)
    
    result = await service.install_extension(
        user_id="user_123",
        extension_id="ext_123"
    )
    
    assert result is True
