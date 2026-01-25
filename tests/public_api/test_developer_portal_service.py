"""
Tests for Developer Portal Service
Comprehensive test coverage for API documentation and SDKs
"""

import pytest
from unittest.mock import patch
from services.public_api.developer_portal_service import DeveloperPortalService, get_developer_portal_service


@pytest.fixture
def service():
    """Create service instance."""
    return DeveloperPortalService()


@pytest.mark.asyncio
async def test_get_api_documentation(service):
    """Test getting API documentation."""
    result = await service.get_api_documentation()
    
    assert result is not None
    assert 'version' in result
    assert 'endpoints' in result
    assert len(result['endpoints']) > 0


@pytest.mark.asyncio
async def test_get_sdks(service):
    """Test getting available SDKs."""
    result = await service.get_sdks()
    
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(sdk['language'] == 'Python' for sdk in result)


@pytest.mark.asyncio
async def test_get_developer_portal_service_singleton():
    """Test singleton pattern."""
    service1 = get_developer_portal_service()
    service2 = get_developer_portal_service()
    
    assert service1 is service2
