"""
Sovereign Ledger Schema - Double-Entry Accounting Core
Phase 1 Implementation: The Sovereign Kernel

This module defines the Pydantic schemas for the immutable double-entry ledger.
Every financial mutation is recorded as a balanced journal entry.

ACCEPTANCE CRITERIA from ROADMAP_AGENT_DEPT.md:
- Relational Integrity: Neo4j Graph must match Postgres Ledger with zero variance.
- Auditability: Every agent decision has a hashed audit trail.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import hashlib


class AccountType(str, Enum):
    """Double-entry account classification."""
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"


class TransactionStatus(str, Enum):
    """Lifecycle states for ledger transactions."""
    PENDING = "PENDING"           # Awaiting signature
    SIGNED = "SIGNED"             # User signature verified
    EXECUTED = "EXECUTED"         # Broker/bank confirmed
    RECONCILED = "RECONCILED"     # Matched with external source
    VOIDED = "VOIDED"             # Cancelled (audit trail preserved)


class LedgerAccount(BaseModel):
    """
    A double-entry account in the Chart of Accounts.
    
    Examples:
    - ASSET: "Brokerage:Schwab:Cash"
    - LIABILITY: "CreditCard:Chase:Balance"
    - EQUITY: "RetainedEarnings:2026"
    """
    id: str = Field(..., description="Unique account identifier")
    name: str = Field(..., description="Human-readable account name")
    account_type: AccountType
    parent_id: Optional[str] = Field(None, description="Parent account for hierarchy")
    currency: str = Field(default="USD", description="ISO 4217 currency code")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True


class JournalLine(BaseModel):
    """
    A single line in a journal entry (one side of the double-entry).
    
    The fundamental accounting equation must always balance:
    Assets = Liabilities + Equity
    """
    account_id: str = Field(..., description="Reference to LedgerAccount.id")
    debit: Decimal = Field(default=Decimal("0.00"))
    credit: Decimal = Field(default=Decimal("0.00"))
    memo: Optional[str] = None
    
    @field_validator("debit", "credit")
    @classmethod
    def validate_non_negative(cls, v: Decimal) -> Decimal:
        if v < Decimal("0"):
            raise ValueError("Debit/Credit amounts must be non-negative")
        return v.quantize(Decimal("0.0001"))  # 4 decimal precision


class JournalEntry(BaseModel):
    """
    An immutable journal entry representing a complete transaction.
    
    Double-entry invariant: sum(debits) == sum(credits)
    
    The entry includes a cryptographic hash of its contents for
    audit trail integrity, forming a hash-chain with the previous entry.
    """
    id: str = Field(..., description="Unique journal entry ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    description: str = Field(..., description="Transaction description")
    lines: List[JournalLine] = Field(..., min_length=2)
    status: TransactionStatus = TransactionStatus.PENDING
    
    # Cryptographic audit trail
    previous_hash: Optional[str] = Field(
        None, 
        description="SHA-256 hash of the previous entry (hash-chain)"
    )
    entry_hash: Optional[str] = Field(
        None, 
        description="SHA-256 hash of this entry's contents"
    )
    
    # Sovereign signature binding
    sovereign_signature_id: Optional[str] = Field(
        None,
        description="Reference to the WebAuthn challenge that authorized this entry"
    )
    signed_by_user_id: Optional[str] = None
    signed_at: Optional[datetime] = None
    
    # Agent provenance
    created_by_agent: Optional[str] = Field(
        None,
        description="Agent ID that proposed this entry (e.g., 'trader.4.1')"
    )
    
    @field_validator("lines")
    @classmethod
    def validate_balance(cls, lines: List[JournalLine]) -> List[JournalLine]:
        """Enforce the fundamental accounting equation."""
        total_debits = sum(line.debit for line in lines)
        total_credits = sum(line.credit for line in lines)
        if total_debits != total_credits:
            raise ValueError(
                f"Journal entry must balance. "
                f"Debits: {total_debits}, Credits: {total_credits}"
            )
        return lines

    def compute_hash(self) -> str:
        """
        Compute the SHA-256 hash of this entry for the immutable audit chain.
        
        The hash includes:
        - Entry ID, timestamp, description
        - All journal lines
        - Previous entry's hash (chain linkage)
        - Signature ID (non-repudiation)
        """
        content = (
            f"{self.id}|{self.timestamp.isoformat()}|{self.description}|"
            f"{self.previous_hash or 'GENESIS'}|{self.sovereign_signature_id or ''}|"
        )
        for line in self.lines:
            content += f"{line.account_id}:{line.debit}:{line.credit}|"
        
        return hashlib.sha256(content.encode()).hexdigest()


class LedgerSummary(BaseModel):
    """Aggregated view of account balances for reporting."""
    account_id: str
    account_name: str
    account_type: AccountType
    balance: Decimal = Field(description="Debit - Credit for the account")
    as_of: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True
