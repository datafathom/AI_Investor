"""
Tests for Public API Service
Comprehensive test coverage for API key management and usage tracking
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.public_api.public_api_service import PublicAPIService
from models.public_api import APIKey, APITier, APIUsage


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.public_api.public_api_service.get_cache_service'):
        return PublicAPIService()


@pytest.mark.asyncio
async def test_create_api_key(service):
    """Test API key creation."""
    service._save_api_key = AsyncMock()
    
    result = await service.create_api_key(
        user_id="user_123",
        tier="pro"
    )
    
    assert result is not None
    assert isinstance(result, APIKey)
    assert result.user_id == "user_123"
    assert result.tier == APITier.PRO
    assert result.rate_limit == 1000  # Pro tier limit
    assert result.api_key.startswith("sk_")


@pytest.mark.asyncio
async def test_create_api_key_different_tiers(service):
    """Test API key creation with different tiers."""
    service._save_api_key = AsyncMock()
    
    tiers = ["free", "pro", "enterprise"]
    expected_limits = [100, 1000, 10000]
    
    for tier, expected_limit in zip(tiers, expected_limits):
        result = await service.create_api_key(
            user_id="user_123",
            tier=tier
        )
        assert result.tier.value == tier
        assert result.rate_limit == expected_limit


@pytest.mark.asyncio
async def test_track_api_usage(service):
    """Test API usage tracking."""
    service._save_usage = AsyncMock()
    
    result = await service.track_api_usage(
        api_key_id="key_123",
        endpoint="/api/v1/portfolio",
        response_time_ms=50
    )
    
    assert result is not None
    assert isinstance(result, APIUsage) or isinstance(result, dict)


@pytest.mark.asyncio
async def test_get_api_usage(service):
    """Test getting API usage statistics."""
    service._get_usage_from_db = AsyncMock(return_value=[
        APIUsage(
            usage_id="usage_1",
            api_key_id="key_123",
            endpoint="/api/v1/portfolio",
            response_time_ms=50,
            timestamp=datetime.utcnow()
        )
    ])
    
    result = await service.get_api_usage("key_123", limit=100)
    
    assert result is not None
    assert len(result) == 1
