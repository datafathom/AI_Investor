"""
Tests for Institutional Service
Comprehensive test coverage for client management and white-labeling
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.institutional.institutional_service import InstitutionalService
from models.institutional import Client, WhiteLabelConfig, ClientAnalytics


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
async def test_get_clients_for_advisor(service):
    """Test fetching clients for advisor."""
    result = await service.get_clients_for_advisor("advisor_123")
    
    assert len(result) >= 2
    assert result[0].client_name == "Family Office Alpha"
    assert result[0].aum == 120000000.0


@pytest.mark.asyncio
async def test_get_client_analytics(service):
    """Test calculating client analytics."""
    result = await service.get_client_analytics("client_123")
    
    assert result.client_id == "client_123"
    assert result.fee_forecast > 0
    assert result.churn_probability == 0.08
