from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID, uuid4

class FeeScheduleBase(BaseModel):
    client_id: UUID
    advisor_id: UUID
    fee_type: str # AUM, PERFORMANCE
    base_fee_pct: Optional[float] = 0.0
    tier_1_max: Optional[float] = 1000000.0
    tier_1_rate: Optional[float] = 0.0100
    tier_2_max: Optional[float] = 5000000.0
    tier_2_rate: Optional[float] = 0.0075
    tier_3_rate: Optional[float] = 0.0050
    billing_frequency: str = "QUARTERLY"
    effective_date: date

class FeeSchedule(FeeScheduleBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class BillingRecordBase(BaseModel):
    fee_schedule_id: UUID
    billing_period_start: date
    billing_period_end: date
    aum_at_billing: float
    gross_fee: float
    proration_factor: float = 1.0
    net_fee: float

class BillingRecord(BillingRecordBase):
    id: UUID = Field(default_factory=uuid4)
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
