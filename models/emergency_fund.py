from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class EmergencyFundBase(BaseModel):
    user_id: UUID
    total_liquid_cash: float
    checking_balance: Optional[float] = 0.0
    savings_balance: Optional[float] = 0.0
    money_market_balance: Optional[float] = 0.0
    monthly_expenses: float
    coverage_tier: Optional[str] = "ADEQUATE"
    income_stability_score: Optional[float] = 50.0
    career_risk_factor: Optional[float] = 50.0

class EmergencyFundCreate(EmergencyFundBase):
    pass

class EmergencyFund(EmergencyFundBase):
    id: UUID = Field(default_factory=uuid4)
    annual_expenses: float = 0.0
    months_of_coverage: float = 0.0
    last_calculated: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class EmergencyFundKafkaMessage(BaseModel):
    user_id: UUID
    liquid_cash: float
    monthly_expenses: float
    months_coverage: float
    coverage_tier: str
    alert_level: str
    timestamp: datetime = Field(default_factory=datetime.now)
