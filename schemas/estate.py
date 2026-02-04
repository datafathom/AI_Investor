"""
==============================================================================
FILE: models/estate.py
ROLE: Estate Planning Data Models
PURPOSE: Pydantic models for estate planning, beneficiary management, and
         inheritance simulation.

INTEGRATION POINTS:
    - EstatePlanningService: Estate planning calculations
    - InheritanceSimulator: Inheritance projections
    - EstateAPI: API response models
    - FrontendEstate: Estate dashboard widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class BeneficiaryType(str, Enum):
    """Beneficiary relationship types."""
    SPOUSE = "spouse"
    CHILD = "child"
    PARENT = "parent"
    SIBLING = "sibling"
    OTHER = "other"
    TRUST = "trust"
    CHARITY = "charity"


class Beneficiary(BaseModel):
    """Beneficiary definition."""
    beneficiary_id: str
    user_id: str
    name: str
    relationship: BeneficiaryType
    allocation_percentage: float = Field(..., ge=0, le=100)
    allocation_amount: Optional[float] = None
    tax_implications: Optional[Dict] = None
    created_date: datetime
    updated_date: datetime


class EstatePlan(BaseModel):
    """Estate plan definition."""
    plan_id: str
    user_id: str
    total_estate_value: float
    beneficiaries: List[Beneficiary]
    trust_accounts: List[Dict] = []
    tax_exempt_amount: float = 12000000.0  # 2024 estate tax exemption
    estimated_estate_tax: float = 0.0
    created_date: datetime
    updated_date: datetime


class InheritanceProjection(BaseModel):
    """Inheritance projection result."""
    projection_id: str
    beneficiary_id: str
    projected_inheritance: float
    projected_tax_liability: float
    after_tax_inheritance: float
    projected_date: datetime
    assumptions: Dict


class EstateScenario(BaseModel):
    """Estate planning scenario."""
    scenario_name: str
    estate_value: float
    beneficiaries: List[Dict]
    tax_strategies: List[str] = []  # e.g., "gifting", "trust", "charitable"
    projection_years: int = 10
