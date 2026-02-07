# Schema: Sovereign Ledger

## File Location
`schemas/sovereign_ledger.py`

## Purpose
Pydantic models for the sovereign ledger system used for tracking autonomous AI agent financial operations with cryptographic audit trails.

---

## Models

### SovereignLedgerEntry
**Sovereign ledger entry for AI agent operations.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `entry_id` | `str` | *required* | Unique entry ID | Primary key |
| `agent_id` | `str` | *required* | Operating agent | Attribution |
| `operation_type` | `str` | *required* | Type: `TRADE`, `TRANSFER`, `ALLOCATION` | Classification |
| `amount` | `Decimal` | *required* | Operation amount | Value |
| `currency` | `str` | `"USD"` | Currency code | Currency |
| `source_account` | `str` | *required* | Source account | Audit |
| `destination_account` | `str` | *required* | Destination account | Audit |
| `justification` | `str` | *required* | Agent's reasoning | Transparency |
| `confidence_score` | `float` | *required* | Agent confidence | Quality |
| `timestamp` | `datetime` | `datetime.utcnow` | Operation time | Ordering |
| `previous_hash` | `Optional[str]` | `None` | Prior entry hash | Chain |
| `entry_hash` | `str` | *computed* | Current entry hash | Integrity |

---

### AgentAllocation
**Budget allocation to an AI agent.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `allocation_id` | `str` | *required* | Allocation ID | Primary key |
| `agent_id` | `str` | *required* | Receiving agent | Attribution |
| `allocated_amount` | `float` | *required* | Amount allocated | Budget |
| `remaining_amount` | `float` | *required* | Unspent amount | Tracking |
| `allocation_date` | `datetime` | *required* | Allocation date | Timing |
| `expiration_date` | `Optional[datetime]` | `None` | Budget expiration | Lifecycle |

---

### OperationApproval
**Human approval for agent operations.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `approval_id` | `str` | *required* | Approval ID | Primary key |
| `entry_id` | `str` | *required* | Related ledger entry | Linking |
| `approver_id` | `str` | *required* | Human approver | Attribution |
| `approval_status` | `str` | *required* | Status: `PENDING`, `APPROVED`, `REJECTED` | Workflow |
| `approval_date` | `Optional[datetime]` | `None` | Approval timestamp | Timing |
| `comments` | `Optional[str]` | `None` | Approver comments | Context |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `SovereignLedgerService` | Entry management |
| `AgentBudgetService` | Allocation tracking |
| `ApprovalWorkflowService` | Human oversight |
