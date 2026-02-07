# Lawyer Department Agents (`lawyer/lawyer_agents.py`)

The Lawyer department is the "Compliance Shield," ensuring that all system actions remain within regulatory and tax-efficient boundaries.

## Wash-Sale Watchdog Agent (Agent 8.1)
### Description
The `WashSaleWatchdogAgent` specifically monitors trade requests for potential IRS "Wash-Sale" rule violations.

### Role
Acts as a "Compliance Gatekeeper" for tax efficiency.

### Logic & Integration
- **Compliance Service**: Audits ticker trade history over the preceding and succeeding 30-day windows.
- **Blocking**: Automatically blocks trades that would trigger a violation, providing a detailed reason to the `ProtectorAgent`.
- **SLA**: Determines compliance status in real-time during the order creation pipeline.
