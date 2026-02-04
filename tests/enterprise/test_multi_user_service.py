"""
Tests for Multi-User Service
Comprehensive test coverage for shared resources and collaboration
"""

import pytest
from datetime import timezone, datetime
from unittest.mock import Mock, AsyncMock, patch
from services.enterprise.multi_user_service import MultiUserService
from schemas.enterprise import SharedResource


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.enterprise.multi_user_service.get_cache_service'):
        return MultiUserService()


@pytest.mark.asyncio
async def test_share_resource(service):
    """Test sharing resource with team."""
    service._save_shared_resource = AsyncMock()
    
    result = await service.share_resource(
        resource_type="portfolio",
        resource_id="portfolio_123",
        team_id="team_456",
        permissions={'read': True, 'write': False}
    )
    
    assert result is not None
    assert isinstance(result, SharedResource)
    assert result.resource_type == "portfolio"
    assert result.team_id == "team_456"


@pytest.mark.asyncio
async def test_get_shared_resources(service):
    """Test getting shared resources for team."""
    service._get_shared_resources_from_db = AsyncMock(return_value=[
        SharedResource(
            resource_id="shared_1",
            resource_type="portfolio",
            team_id="team_123",
            permissions={'read': True},
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
    ])
    
    result = await service.get_shared_resources("team_123")
    
    assert result is not None
    assert len(result) == 1
