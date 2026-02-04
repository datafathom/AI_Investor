from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class AdvisorBase(BaseModel):
    name: str
    email: EmailStr
    fiduciary_status: bool = False
    fiduciary_type: Optional[str] = None # RIA, BROKER_DEALER, HYBRID
    registration_type: str # SEC, STATE
    registration_number: Optional[str] = None
    registration_state: Optional[str] = None
    sec_crd_number: Optional[str] = None
    firm_name: Optional[str] = None
    firm_type: Optional[str] = None # RIA, WIREHOUSE, INDEPENDENT
    aum_under_management: Optional[float] = 0.0
    fee_structure: Optional[str] = None # FEE_ONLY, COMMISSION, HYBRID

class AdvisorCreate(AdvisorBase):
    pass

class Advisor(AdvisorBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
