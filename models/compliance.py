"""
==============================================================================
FILE: models/compliance.py
ROLE: Compliance Data Models
PURPOSE: Pydantic models for compliance checking, reporting, and violations.

INTEGRATION POINTS:
    - ComplianceEngine: Rule checking
    - ReportingService: Report generation
    - ComplianceAPI: Compliance endpoints
    - FrontendCompliance: Compliance dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class ViolationSeverity(str, Enum):
    """Violation severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceRule(BaseModel):
    """Compliance rule definition."""
    rule_id: str
    regulation: str  # SEC, FINRA, etc.
    rule_name: str
    description: str
    rule_logic: Dict = {}  # Rule evaluation logic


class ComplianceViolation(BaseModel):
    """Compliance violation."""
    violation_id: str
    rule_id: str
    user_id: str
    severity: ViolationSeverity
    description: str
    detected_date: datetime
    resolved_date: Optional[datetime] = None
    status: str = "open"  # open, resolved, false_positive


class ComplianceReport(BaseModel):
    """Compliance report."""
    report_id: str
    user_id: str
    report_type: str  # regulatory, custom, etc.
    period_start: datetime
    period_end: datetime
    violations: List[str] = []
    generated_date: datetime
