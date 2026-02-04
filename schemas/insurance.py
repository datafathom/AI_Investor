from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID, uuid4

class InsuranceProviderBase(BaseModel):
    name: str
    provider_type: str
    am_best_rating: Optional[str] = None
    specializations: List[str] = []
    licensed_states: List[str] = []

class InsuranceProvider(InsuranceProviderBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class InsurancePolicyBase(BaseModel):
    client_id: UUID
    provider_id: UUID
    policy_type: str # TERM_LIFE, WHOLE_LIFE, PPLI, UMBRELLA
    policy_number: str
    death_benefit: Optional[float] = 0.0
    cash_value: Optional[float] = 0.0
    annual_premium: float
    effective_date: date
    expiration_date: Optional[date] = None

class InsurancePolicy(InsurancePolicyBase):
    id: UUID = Field(default_factory=uuid4)
    status: str = "ACTIVE"
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
