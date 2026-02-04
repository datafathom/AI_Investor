from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID, uuid4

class EmployerMatchConfigBase(BaseModel):
    user_id: UUID
    employer_name: str
    match_type: str = "DOLLAR_FOR_DOLLAR" # DOLLAR_FOR_DOLLAR, PARTIAL, TIERED
    match_percentage: float
    max_match_percentage: Optional[float] = None
    annual_match_cap: Optional[float] = None
    tier_1_employee_pct: Optional[float] = None
    tier_1_employer_pct: Optional[float] = None
    tier_2_employee_pct: Optional[float] = None
    tier_2_employer_pct: Optional[float] = None
    vesting_type: Optional[str] = "IMMEDIATE" # IMMEDIATE, CLIFF, GRADED
    vesting_cliff_months: Optional[int] = 0
    vesting_schedule: Optional[Dict[str, float]] = None # {"12": 0.20, ...}
    effective_date: Optional[date] = None

class EmployerMatchConfigCreate(EmployerMatchConfigBase):
    pass

class EmployerMatchConfig(EmployerMatchConfigBase):
    id: UUID = Field(default_factory=uuid4)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
