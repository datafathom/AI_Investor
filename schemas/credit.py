"""
==============================================================================
FILE: models/credit.py
ROLE: Credit Monitoring Data Models
PURPOSE: Pydantic models for credit score monitoring and improvement.

INTEGRATION POINTS:
    - CreditMonitoringService: Credit score tracking
    - CreditImprovementService: Improvement recommendations
    - CreditAPI: API response models
    - FrontendCredit: Credit dashboard widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class CreditFactor(str, Enum):
    """Credit score factors."""
    PAYMENT_HISTORY = "payment_history"
    CREDIT_UTILIZATION = "credit_utilization"
    LENGTH_OF_HISTORY = "length_of_history"
    CREDIT_MIX = "credit_mix"
    NEW_CREDIT = "new_credit"


class CreditScore(BaseModel):
    """Credit score record."""
    score_id: str
    user_id: str
    score: int = Field(..., ge=300, le=850)
    score_type: str = "fico"  # FICO, VantageScore
    factors: Dict[str, float] = {}  # {factor: impact_score}
    report_date: datetime
    trend: str = "stable"  # "increasing", "decreasing", "stable"


class CreditRecommendation(BaseModel):
    """Credit improvement recommendation."""
    recommendation_id: str
    factor: CreditFactor
    title: str
    description: str
    impact_score: int  # Estimated points improvement
    difficulty: str  # "easy", "medium", "hard"
    estimated_time: str  # "1 month", "3 months", etc.
    action_items: List[str]


class CreditProjection(BaseModel):
    """Credit score projection."""
    projection_id: str
    current_score: int
    projected_score: int
    projected_date: datetime
    assumptions: Dict
    confidence_level: float
