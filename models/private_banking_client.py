from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID, uuid4

class PrivateBankingClientBase(BaseModel):
    user_id: UUID
    verified_net_worth: float
    qualification_date: date
    verification_method: str = "DOCUMENT"
    tier: str # PRIVATE, ULTRA, FAMILY_OFFICE
    service_level: str = "WHITE_GLOVE"
    relationship_manager_id: Optional[UUID] = None

class PrivateBankingClient(PrivateBankingClientBase):
    id: UUID = Field(default_factory=uuid4)
    onboarded_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

    class Config:
        from_attributes = True

class TaxDeferralStrategyBase(BaseModel):
    client_id: UUID
    strategy_type: str # INSTALLMENT_SALE, OPPORTUNITY_ZONE, 1031_EXCHANGE
    gain_deferred: float
    tax_savings_estimate: Optional[float] = 0.0
    initiation_date: date
    expiration_date: Optional[date] = None

class TaxDeferralStrategy(TaxDeferralStrategyBase):
    id: UUID = Field(default_factory=uuid4)
    days_remaining: Optional[int] = 0
    status: str = "ACTIVE"
    compliance_verified: bool = False

    class Config:
        from_attributes = True
