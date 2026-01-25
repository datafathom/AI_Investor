"""
Tests for Institutional Service
Comprehensive test coverage for client management and white-labeling
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.institutional.institutional_service import InstitutionalService
from models.institutional import Client, WhiteLabelConfig


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.institutional.institutional_service.get_cache_service'):
        return InstitutionalService()


@pytest.mark.asyncio
async def test_create_client(service):
    """Test client creation."""
    service._save_client = AsyncMock()
    
    result = await service.create_client(
        advisor_id="advisor_123",
        client_name="John Doe"
    )
    
    assert result is not None
    assert isinstance(result, Client)
    assert result.advisor_id == "advisor_123"
    assert result.client_name == "John Doe"


@pytest.mark.asyncio
async def test_configure_white_label(service):
    """Test white-label configuration."""
    service._save_white_label_config = AsyncMock()
    
    result = await service.configure_white_label(
        organization_id="org_123",
        logo_url="https://example.com/logo.png",
        primary_color="#0066CC",
        secondary_color="#FFFFFF",
        custom_domain="invest.example.com"
    )
    
    assert result is not None
    assert isinstance(result, WhiteLabelConfig)
    assert result.organization_id == "org_123"
    assert result.logo_url == "https://example.com/logo.png"
