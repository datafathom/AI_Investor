"""
==============================================================================
FILE: models/integration.py
ROLE: Integration Data Models
PURPOSE: Pydantic models for third-party app integrations and data
         synchronization.

INTEGRATION POINTS:
    - IntegrationFramework: Integration infrastructure
    - IntegrationService: Integration management
    - IntegrationAPI: Integration endpoints
    - FrontendIntegration: Integration dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class IntegrationStatus(str, Enum):
    """Integration status."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    SYNCING = "syncing"


class Integration(BaseModel):
    """Integration definition."""
    integration_id: str
    user_id: str
    app_name: str  # mint, ynab, personal_capital, etc.
    status: IntegrationStatus = IntegrationStatus.DISCONNECTED
    oauth_token: Optional[str] = None
    last_sync_date: Optional[datetime] = None
    sync_frequency: str = "daily"  # realtime, hourly, daily, manual
    created_date: datetime
    updated_date: datetime


class SyncJob(BaseModel):
    """Data synchronization job."""
    sync_job_id: str
    integration_id: str
    sync_type: str  # full, incremental
    status: str = "pending"  # pending, running, completed, failed
    started_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    records_synced: int = 0
