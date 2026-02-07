# Guardian Department Agents (`guardian/guardian_agents.py`)

The Guardian department is the "Financial Fortress," responsible for the automated treasury, cash flow management, and banking security.

## Bill Automator Agent (Agent 6.1)
### Description
The `BillAutomatorAgent` handles the ingestion and processing of utility and operational bills.
- **Acceptance Criteria**: 100% OCR accuracy on amounts and due dates.

### Integration
- **Treasury Service**: Uses specialized PDF OCR to extract line-item data.
- **Staging**: Bills are staged for payment after validation, ensuring no manual data entry.

---

## Flow Master Agent (Agent 6.2)
### Description
The `FlowMasterAgent` manages active cash flow and liquidity across multiple accounts.
- **Threshold**: Executes high-limit ACH sweeps (e.g., when checking > $5,000).

### Role
Acts as the "Liquidity Controller."

---

## Net Worth Auditor Agent (Agent 6.5)
### Description
The `NetWorthAuditorAgent` is the real-time truth-check for the total net worth.

### Integration
- **Reconciliation**: Reconciles the internal ledger with external external balances (discrepancies > $0.05 trigger alerts).
- **SLA**: Audits must be completed within 60 seconds of a sync request.
