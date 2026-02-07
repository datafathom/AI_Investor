# Auditor Department Agents (`auditor/auditor_agents.py`)

This folder contains agents responsible for verifying the integrity of the system's financial and decision-making processes.

## Reconciliation Bot Agent (Agent 9.5)
### Description
The `ReconciliationBotAgent` is an automated accountant that ensures the internal ledger precisely matches the reality of external bank balances.

### Role
Acts as the "Truth Verifier" for all cash positions.

### Integration
- **Treasury Service**: Fetches real-time bank balances.
- **Ledger System**: Compares balances against Postgres entries.
- **Alerting**: Discrepancies > $0.05 trigger an immediate high-priority audit event.

---

## Mistake Classifier Agent (Agent 9.6)
### Description
The `MistakeClassifierAgent` performs "Post-Mortem" analysis on losing trades to determine if they were the result of a bad strategy or emotional "Tilt."

### Role
Acts as the "Psychologist" and "Compliance Officer" for the trading engine.

### Integration
- **Trade History**: Analyzes closed positions with negative P&L.
- **Scoring**: Assigns a "Tilt Score" (0.0 - 1.0). High tilt scores result in automatic circuit breaker triggers by the `ProtectorAgent`.
