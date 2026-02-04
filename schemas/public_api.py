"""
==============================================================================
FILE: models/public_api.py
ROLE: Public API Data Models
PURPOSE: Pydantic models for public API, API keys, and developer platform.

INTEGRATION POINTS:
    - PublicAPIService: API management
    - DeveloperPortalService: Developer resources
    - PublicAPI: Public API endpoints
    - FrontendDeveloper: Developer portal

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class APITier(str, Enum):
    """API tier levels."""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class APIKey(BaseModel):
    """API key definition."""
    api_key_id: str
    user_id: str
    api_key: str
    tier: APITier = APITier.FREE
    rate_limit: int = 100  # Requests per hour
    usage_count: int = 0
    created_date: datetime
    last_used_date: Optional[datetime] = None
    is_active: bool = True


class APIUsage(BaseModel):
    """API usage record."""
    usage_id: str
    api_key_id: str
    endpoint: str
    timestamp: datetime
    response_time_ms: float
    status_code: int
