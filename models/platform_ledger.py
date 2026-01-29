from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class PlatformLedgerBase(BaseModel):
    transaction_type: str # DEPOSIT, WITHDRAWAL, TRADE, TRANSFER, FEE
    account_id: UUID
    custodian_id: UUID
    amount: float
    currency: str = "USD"
    from_account: Optional[str] = None
    to_account: Optional[str] = None
    counterparty_name: Optional[str] = None

class PlatformLedger(PlatformLedgerBase):
    id: UUID = Field(default_factory=uuid4)
    entry_timestamp: datetime = Field(default_factory=datetime.now)
    custodian_confirmation_id: Optional[str] = None
    is_reconciled: bool = False
    previous_hash: Optional[str] = None
    entry_hash: str
    hash_verified: bool = False

    class Config:
        from_attributes = True
