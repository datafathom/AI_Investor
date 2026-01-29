from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID, uuid4

class ContributionBase(BaseModel):
    user_id: UUID
    account_id: UUID
    contribution_date: date
    employee_contribution: float
    employer_match: float
    ytd_employee_total: Optional[float] = 0.0
    ytd_employer_total: Optional[float] = 0.0
    ytd_total: Optional[float] = 0.0
    annual_limit: Optional[float] = 0.0
    remaining_room: Optional[float] = 0.0

class ContributionCreate(ContributionBase):
    pass

class Contribution(ContributionBase):
    id: UUID = Field(default_factory=uuid4)
    total_contribution: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
