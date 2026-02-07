# Backend Service: Audit

## Overview
The **Audit Service** provides high-integrity "Forensic Vault" capabilities designed for institutional-grade post-incident analysis. It is triggered during extreme ("nuclear-level") market risk events to capture full-state snapshots of the environment, system health, and agent activity.

## Core Components

### Forensic Vault (`forensic_vault.py`)
A specialized recorder for documenting critical system failure or extreme market drawdowns.

#### Classes

##### `ForensicVault`
Acts as a cold-storage auditor for preserving evidence and data during high-volatility regimes.

**Methods:**
- `capture_incident(symbol: str, drawdown: float, market_context: Dict[str, Any])`
    - **Purpose**: Packages the current system state, asset performance, and drawdown metrics into an immutable forensic record.
    - **Logic**: Logs a `CRITICAL` severity event and prepares a data package for permanent preservation.
    - **Returns**: A structured "incident package" containing timestamps, severity levels, and market snapshots.
- `get_market_context() -> Dict[str, Any]`
    - **Purpose**: Gathers a multi-layered snapshot of market conditions (VIX levels, asset correlations, active agent list) to provide context for the audit.

## Dependencies
- `logging`: Uses `logger.critical` for immediate visibility of forensic capture events.
- `datetime`: Provides high-resolution ISO timestamps for audit trails.

## Usage Example

### Manually Recording a Risk Incident
```python
from services.audit.forensic_vault import ForensicVault

vault = ForensicVault()
context = vault.get_market_context()

# Simulated extreme drawdown event on ETH
incident = vault.capture_incident(
    symbol="ETH", 
    drawdown=0.25, 
    market_context=context
)

print(f"Incident recorded: {incident['timestamp']} | Severity: {incident['severity']}")
```
