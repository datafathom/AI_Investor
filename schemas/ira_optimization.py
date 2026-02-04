from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class IRAOptimizationProfileBase(BaseModel):
    user_id: UUID
    current_marginal_rate: float
    current_effective_rate: Optional[float] = None
    current_agi: Optional[float] = 0.0
    filing_status: str # SINGLE, MARRIED_JOINT, HEAD_OF_HOUSEHOLD
    projected_retirement_rate: Optional[float] = None
    projected_retirement_income: Optional[float] = 0.0
    expected_social_security: Optional[float] = 0.0
    expected_pension_income: Optional[float] = 0.0
    current_age: int
    retirement_age: int
    life_expectancy: int = 90

class IRAOptimizationProfileCreate(IRAOptimizationProfileBase):
    pass

class IRAOptimizationProfile(IRAOptimizationProfileBase):
    id: UUID = Field(default_factory=uuid4)
    years_to_retirement: int = 0
    recommended_strategy: Optional[str] = None
    split_percentage_roth: Optional[float] = 0.0
    recommendation_confidence: Optional[float] = 0.0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class AnalysisResult(BaseModel):
    traditional_value: float
    roth_value: float
    breakeven_rate: float
    recommendation: str
