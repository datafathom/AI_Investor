"""
Tests for Integration Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.integration import (
    IntegrationStatus,
    Integration,
    SyncJob
)


class TestIntegrationStatusEnum:
    """Tests for IntegrationStatus enum."""
    
    def test_integration_status_enum(self):
        """Test integration status enum values."""
        assert IntegrationStatus.CONNECTED == "connected"
        assert IntegrationStatus.DISCONNECTED == "disconnected"
        assert IntegrationStatus.ERROR == "error"
        assert IntegrationStatus.SYNCING == "syncing"


class TestIntegration:
    """Tests for Integration model."""
    
    def test_valid_integration(self):
        """Test valid integration creation."""
        integration = Integration(
            integration_id='int_1',
            user_id='user_1',
            app_name='mint',
            status=IntegrationStatus.CONNECTED,
            oauth_token='token_123',
            last_sync_date=datetime.now(),
            sync_frequency='daily',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert integration.integration_id == 'int_1'
        assert integration.status == IntegrationStatus.CONNECTED
        assert integration.app_name == 'mint'
    
    def test_integration_defaults(self):
        """Test integration with default values."""
        integration = Integration(
            integration_id='int_1',
            user_id='user_1',
            app_name='ynab',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert integration.status == IntegrationStatus.DISCONNECTED
        assert integration.sync_frequency == 'daily'
        assert integration.oauth_token is None


class TestSyncJob:
    """Tests for SyncJob model."""
    
    def test_valid_sync_job(self):
        """Test valid sync job creation."""
        job = SyncJob(
            sync_job_id='job_1',
            integration_id='int_1',
            sync_type='full',
            status='completed',
            started_date=datetime.now(),
            completed_date=datetime.now(),
            records_synced=1000
        )
        assert job.sync_job_id == 'job_1'
        assert job.sync_type == 'full'
        assert job.records_synced == 1000
    
    def test_sync_job_defaults(self):
        """Test sync job with default values."""
        job = SyncJob(
            sync_job_id='job_1',
            integration_id='int_1',
            sync_type='incremental'
        )
        assert job.status == 'pending'
        assert job.records_synced == 0
        assert job.started_date is None
