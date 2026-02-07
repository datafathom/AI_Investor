# Backend Service: Admin

## Overview
The **Admin Service** provides administrative and overarching control capabilities for the AI Investor platform. It includes high-level system monitoring through a "God Mode" dashboard and intelligent communication management via automated email triage.

## Components

### Command Center Service (`command_center_svc.py`)
This service acts as the backend for the platform's central command dashboard. It aggregates status reports and performance metrics from all 200 phases of the system.

#### Classes

##### `CommandCenterService`
A singleton service that provides a unified view of system health.

**Methods:**
- `get_system_status() -> Dict[str, Any]`
    - **Purpose**: Polls key subsystems (tax engine, risk engine, trading bots, etc.) for their current operational status.
    - **Returns**: A dictionary containing:
        - `orchestrator_status`: Current status of the master orchestrator.
        - `active_phases`: Number of active operational phases.
        - `global_risk_level`: Current system-wide risk assessment.
        - `subsystems`: Individual RAG (Red/Amber/Green) statuses for core engines.

---

### Inbox Service (`inbox_service.py`)
Part of the Phase 8 (Global HQ) implementation, this service handles the intelligent triage of the executive inbox to minimize noise and surface actionable communication.

#### Classes

##### `InboxService`
A singleton service that leverages Local LLMs for email classification.

**Methods:**
- `classify_email(subject: str, sender: str, snippet: str) -> Dict[str, Any]` (Async)
    - **Purpose**: Triages an incoming email into actionable categories.
    - **Arguments**:
        - `subject`: Email subject line.
        - `sender`: Sender's email address.
        - `snippet`: A short snippet of the email content.
    - **Logic**: Uses a local Llama3 model (via Ollama) to classify the email as `ACTIONABLE`, `PROMO`, or `NOISE`.
    - **Returns**: A JSON object containing the `classification`, the `reason` for the triage, and an `urgency` score (1-10).

## Dependencies
- `services.system.model_manager`: Used by `InboxService` to interact with local LLMs.
- `json` & `re`: Used for parsing LLM outputs.
- `logging`: Standard system logging.

## Usage Example

### Checking System Status
```python
from services.admin.command_center_svc import CommandCenterService

admin_svc = CommandCenterService()
status = admin_svc.get_system_status()
print(f"Global Risk: {status['global_risk_level']}")
```

### Triaging Emails
```python
from services.admin.inbox_service import get_inbox_service

inbox = get_inbox_service()
result = await inbox.classify_email(
    subject="Urgent: Margin Call on TSLA",
    sender="broker@example.com",
    snippet="TSLA has dropped below..."
)
print(f"Priority: {result['urgency']} | Action: {result['classification']}")
```
