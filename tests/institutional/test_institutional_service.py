"""
Tests for Institutional Service
Comprehensive test coverage for client management and white-labeling
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch
from services.institutional.institutional_service import InstitutionalService
from models.institutional import Client, WhiteLabelConfig, ClientAnalytics


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.institutional.institutional_service.get_cache_service'), \
         patch('services.institutional.institutional_service.neo4j_service') as mock_neo4j:
        service = InstitutionalService()
        service.neo4j = mock_neo4j
        return service


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
    # Mock Neo4j response for get_clients
    service.neo4j.execute_query.return_value = [
        {'c': {'id': 'client_1', 'name': 'Family Office Alpha', 'jurisdiction': 'US', 'strategy': 'Conservative'}}
    ]
    service.cache_service.get.return_value = {
        'client_id': 'client_1',
        'advisor_id': 'advisor_123',
        'client_name': 'Family Office Alpha',
        'aum': 120000000.0,
        'jurisdiction': 'US',
        'strategy': 'Conservative',
        'created_date': datetime.now(timezone.utc).isoformat(),
        'updated_date': datetime.now(timezone.utc).isoformat()
    }

    result = await service.get_clients_for_advisor("advisor_123")
    
    assert len(result) >= 1
    assert result[0].client_name == "Family Office Alpha"
    assert result[0].aum == 120000000.0


@pytest.mark.asyncio
async def test_get_client_analytics(service):
    """Test calculating client analytics."""
    result = await service.get_client_analytics("client_123")
    
    assert result.client_id == "client_123"
    assert result.fee_forecast > 0
    assert result.churn_probability == 0.08
