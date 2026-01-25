"""
Tests for Integration Framework
Comprehensive test coverage for OAuth, connectors, and data mapping
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.integration.integration_framework import IntegrationFramework
from models.integration import Integration, IntegrationStatus


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.integration.integration_framework.get_cache_service'):
        return IntegrationFramework()


@pytest.mark.asyncio
async def test_create_integration(service):
    """Test integration creation."""
    service._save_integration = AsyncMock()
    
    result = await service.create_integration(
        user_id="user_123",
        app_name="mint",
        oauth_token="token_123"
    )
    
    assert result is not None
    assert isinstance(result, Integration)
    assert result.user_id == "user_123"
    assert result.app_name == "mint"
    assert result.status == IntegrationStatus.CONNECTED


@pytest.mark.asyncio
async def test_create_integration_unsupported_app(service):
    """Test integration creation with unsupported app."""
    with pytest.raises(ValueError, match="not supported"):
        await service.create_integration(
            user_id="user_123",
            app_name="unsupported_app"
        )


@pytest.mark.asyncio
async def test_get_supported_apps(service):
    """Test getting supported apps."""
    apps = service.get_supported_apps()
    
    assert apps is not None
    assert len(apps) > 0
    assert "mint" in apps
