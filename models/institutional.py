"""
==============================================================================
FILE: models/institutional.py
ROLE: Institutional Data Models
PURPOSE: Pydantic models for institutional features, multi-client management,
         and professional tools.

INTEGRATION POINTS:
    - InstitutionalService: Multi-client management
    - ProfessionalToolsService: Professional tools
    - InstitutionalAPI: Institutional endpoints
    - FrontendInstitutional: Institutional dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional


class Client(BaseModel):
    """Client definition for institutional use."""
    client_id: str
    advisor_id: str
    client_name: str
    portfolio_ids: List[str] = []
    created_date: datetime
    updated_date: datetime


class WhiteLabelConfig(BaseModel):
    """White-label configuration."""
    config_id: str
    organization_id: str
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    custom_domain: Optional[str] = None
    branding_name: Optional[str] = None
    created_date: datetime
    updated_date: datetime


class ProfessionalReport(BaseModel):
    """Professional report definition."""
    report_id: str
    advisor_id: str
    client_id: str
    report_type: str
    content: Dict = {}
    generated_date: datetime
