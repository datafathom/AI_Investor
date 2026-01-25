"""
==============================================================================
FILE: models/enterprise.py
ROLE: Enterprise Data Models
PURPOSE: Pydantic models for enterprise features, teams, and organizations.

INTEGRATION POINTS:
    - EnterpriseService: Team management
    - MultiUserService: Shared resources
    - EnterpriseAPI: Enterprise endpoints
    - FrontendEnterprise: Enterprise dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class TeamRole(str, Enum):
    """Team member roles."""
    ADMIN = "admin"
    MANAGER = "manager"
    ANALYST = "analyst"
    VIEWER = "viewer"


class Organization(BaseModel):
    """Organization definition."""
    organization_id: str
    name: str
    parent_organization_id: Optional[str] = None
    created_date: datetime
    updated_date: datetime


class Team(BaseModel):
    """Team definition."""
    team_id: str
    organization_id: str
    team_name: str
    members: List[Dict] = []  # {user_id, role}
    created_date: datetime
    updated_date: datetime


class SharedResource(BaseModel):
    """Shared resource definition."""
    resource_id: str
    resource_type: str  # portfolio, report, watchlist, etc.
    team_id: str
    permissions: Dict = {}  # {user_id: permission_level}
    created_date: datetime
    updated_date: datetime
