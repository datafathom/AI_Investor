from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

class ProfessionalRoleBase(BaseModel):
    role_code: str
    role_name: str
    role_category: str # FIDUCIARY, NON_FIDUCIARY
    fiduciary_standard: bool
    can_earn_commissions: bool = False
    can_earn_aum_fees: bool = True
    exclusive_with: List[str] = []

class ProfessionalRole(ProfessionalRoleBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class RoleAssignmentBase(BaseModel):
    user_id: UUID
    role_id: UUID
    client_id: Optional[UUID] = None
    is_active: bool = True

class RoleAssignment(RoleAssignmentBase):
    id: UUID = Field(default_factory=uuid4)
    conflict_check_passed: bool
    assigned_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
