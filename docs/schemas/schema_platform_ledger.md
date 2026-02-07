# Schema: Platform Ledger

## File Location
`schemas/platform_ledger.py`

## Purpose
Pydantic models for the platform's internal ledger system with cryptographic hashing for auditability and WORM compliance.

---

## Enums

### AccountType
**Ledger account types.**

| Value | Description |
|-------|-------------|
| `ASSET` | Asset account |
| `LIABILITY` | Liability account |
| `EQUITY` | Equity account |
| `REVENUE` | Revenue account |
| `EXPENSE` | Expense account |

---

## Models

### PlatformLedgerBase
**Ledger entry base model.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `transaction_type` | `str` | *required* | Transaction category | Classification |
| `debit_account` | `str` | *required* | Debit account code | Double-entry |
| `credit_account` | `str` | *required* | Credit account code | Double-entry |
| `amount` | `Decimal` | *required* | Transaction amount | Value |
| `currency` | `str` | `"USD"` | Currency code | Currency handling |
| `reference_id` | `Optional[str]` | `None` | External reference | Linking |
| `description` | `Optional[str]` | `None` | Transaction description | Context |
| `timestamp` | `datetime` | `datetime.utcnow` | Transaction time | Ordering |

---

### PlatformLedger
**Full ledger entry with hash chain.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `sequence_number` | `int` | `0` | Monotonic sequence | Ordering |
| `previous_hash` | `Optional[str]` | `None` | Hash of previous entry | Chain integrity |
| `entry_hash` | `str` | *computed* | SHA-256 hash of entry | Tamper detection |

**Methods:**
- `compute_hash()`: Generates SHA-256 hash of entry data for WORM compliance

---

## Integration Points

| Service | Usage |
|---------|-------|
| `LedgerService` | Entry management |
| `AuditService` | Integrity verification |
| `ComplianceService` | WORM compliance |
