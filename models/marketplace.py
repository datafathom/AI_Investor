"""
==============================================================================
FILE: models/marketplace.py
ROLE: Marketplace Data Models
PURPOSE: Pydantic models for extension marketplace, plugins, and reviews.

INTEGRATION POINTS:
    - ExtensionFramework: Extension infrastructure
    - MarketplaceService: Marketplace management
    - MarketplaceAPI: Marketplace endpoints
    - FrontendMarketplace: Marketplace dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class ExtensionStatus(str, Enum):
    """Extension status."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Extension(BaseModel):
    """Extension definition."""
    extension_id: str
    developer_id: str
    extension_name: str
    description: str
    version: str
    status: ExtensionStatus = ExtensionStatus.DRAFT
    price: float = 0.0  # 0 for free
    category: str
    install_count: int = 0
    rating: float = 0.0
    review_count: int = 0
    created_date: datetime
    updated_date: datetime


class ExtensionReview(BaseModel):
    """Extension review."""
    review_id: str
    extension_id: str
    user_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    created_date: datetime
