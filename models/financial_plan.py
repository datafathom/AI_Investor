from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

class FinancialPlanBase(BaseModel):
    user_id: UUID
    plan_type: str = "STANDARD" # STANDARD, UHNW, SPECIALIZED
    complexity_score: float = 0.0
    status: str = "GENERATING"

class FinancialPlan(FinancialPlanBase):
    id: UUID = Field(default_factory=uuid4)
    price: float = 2500.0
    requires_human_review: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
