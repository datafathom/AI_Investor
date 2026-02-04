"""
Tests for Integration Service
Comprehensive test coverage for data synchronization and connectors
"""

import pytest
from datetime import timezone, datetime
from unittest.mock import Mock, AsyncMock, patch
from services.integration.integration_service import IntegrationService
from schemas.integration import SyncJob


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.integration.integration_service.get_integration_framework'), \
         patch('services.integration.integration_service.get_cache_service'):
        return IntegrationService()


@pytest.mark.asyncio
async def test_sync_data(service):
    """Test data synchronization."""
    service._save_sync_job = AsyncMock()
    
    result = await service.sync_data(
        integration_id="integration_123",
        sync_type="incremental"
    )
    
    assert result is not None
    assert isinstance(result, SyncJob)
    assert result.integration_id == "integration_123"
    assert result.sync_type == "incremental"
    assert result.status == "completed"


@pytest.mark.asyncio
async def test_sync_data_full(service):
    """Test full data synchronization."""
    service._save_sync_job = AsyncMock()
    
    result = await service.sync_data(
        integration_id="integration_123",
        sync_type="full"
    )
    
    assert result is not None
    assert result.sync_type == "full"


@pytest.mark.asyncio
async def test_get_sync_status(service):
    """Test getting sync job status."""
    service._get_sync_job = AsyncMock(return_value=SyncJob(
        sync_job_id="sync_123",
        integration_id="integration_123",
        sync_type="incremental",
        status="completed",
        started_date=datetime.now(timezone.utc),
        completed_date=datetime.now(timezone.utc),
        records_synced=100
    ))
    
    result = await service.get_sync_status("sync_123")
    
    assert result is not None
    assert result.status == "completed"
