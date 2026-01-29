from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID, uuid4

class Plan529Base(BaseModel):
    user_id: UUID
    beneficiary_id: UUID
    plan_name: str
    state: str
    is_resident_plan: bool = False
    custodian: Optional[str] = None
    beneficiary_name: str
    beneficiary_birth_date: date
    current_balance: float = 0.0
    monthly_contribution: float = 0.0
    target_college: Optional[str] = None
    estimated_cost: Optional[float] = 0.0
    portfolio_type: str = "AGE_BASED" # AGE_BASED, STATIC, CUSTOM

class Plan529(Plan529Base):
    id: UUID = Field(default_factory=uuid4)
    target_college_year: int = 0
    years_to_enrollment: Optional[int] = 0
    current_equity_allocation: float = 0.0
    target_equity_allocation: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class GlidePath529(BaseModel):
    plan_id: UUID
    years_to_enrollment: int
    equity_allocation: float
    fixed_income_allocation: float
    money_market_allocation: float
