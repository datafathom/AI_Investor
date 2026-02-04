"""
==============================================================================
FILE: models/research.py
ROLE: Research & Reports Data Models
PURPOSE: Pydantic models for research reports, analysis, and document
         generation.

INTEGRATION POINTS:
    - ResearchService: Report generation
    - ReportGenerator: Document creation
    - ResearchAPI: Research endpoints
    - FrontendResearch: Research dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class ReportType(str, Enum):
    """Report types."""
    PORTFOLIO_ANALYSIS = "portfolio_analysis"
    COMPANY_RESEARCH = "company_research"
    MARKET_OUTLOOK = "market_outlook"
    PERFORMANCE_REPORT = "performance_report"
    TAX_REPORT = "tax_report"
    CUSTOM = "custom"


class ReportStatus(str, Enum):
    """Report generation status."""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchReport(BaseModel):
    """Research report definition."""
    report_id: str
    user_id: str
    report_type: ReportType
    title: str
    content: str
    sections: List[Dict] = []
    charts: List[Dict] = []
    data: Dict = {}
    status: ReportStatus = ReportStatus.PENDING
    generated_date: Optional[datetime] = None
    created_date: datetime
    updated_date: datetime


class ReportTemplate(BaseModel):
    """Report template definition."""
    template_id: str
    template_name: str
    report_type: ReportType
    sections: List[Dict] = []
    default_settings: Dict = {}
