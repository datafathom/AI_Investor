# Phase 7: Mission Rollout & Analytics

## Overview
This is the final phase of the Mission Module upgrade. We are scaling the OS to handle the full 200-mission fleet simultaneously and providing the web-based IDE for "Hot-Swapping" agent behavior. We move from building parts to optimizing the entire machine for maximum Alpha extraction.

## Deliverables

### 1. Web-Based Agent Logic IDE
**Description**: A full-featured editor in the React UI for modifying agent Python/JS code on the fly.
- **Acceptance Criteria**:
  - Features syntax highlighting, line numbering, and simple code folding (via PrismJS).
  - "Pre-Save Audit" runs the code through a static analyzer for safety violations.
  - IDE displays the "Last Successful Execution" log for the selected sub-agent.

### 2. "Hot-Reload" Deployment Bridge
**Description**: The mechanism that allows Dept 1 to inject new code into running containers without downtime.
- **Acceptance Criteria**:
  - "Zero-Downtime" cutover: New worker starts on the latest Kafka offset while the old one gracefully shuts down.
  - Deployment history with "One-Click Rollback" is operational in the IDE.
  - Success signal is received by the UI only after the new worker completes its first task.

### 3. Agent Log-Replay Debugger
**Description**: A tool to "Replay" past mission failures through the IDE to test new code against real historical data.
- **Acceptance Criteria**:
  - Operator can select a `FAILED` job ID and "Feed" its input Kafka messages into the Logic Editor.
  - "Step-through" mode allows the operator to see the agent's internal state at each message.
  - Fixes can be verified against the historical input before live deployment.

### 4. Fleet-Scale Orchestration Dashboard
**Description**: A high-density monitoring view for managing > 50 simultaneous active missions.
- **Acceptance Criteria**:
  - Dashboard handles high-frequency updates (PnL/Logs) without dropping browser frames.
  - "Batch Actions" (Pause Selected, Terminate Sector) are implemented and verified.
  - Visual density is optimized for a 4K "War Room" display.

### 5. Automated Alpha-Profitability Reporting
**Description**: End-of-day (EOD) reports synthesized by the Historian (Dept 15).
- **Acceptance Criteria**:
  - Generates a PDF/JSON report showing "Most Profitable Sector" and "Weakest Sub-Agent."
  - Reports are PGP-encrypted and pushed to the Sovereign Archive.
  - Historical ROI trends are used to "Self-Adjust" mission weights for the next 24 hours.

### 6. The "Sovereign Singularity" Meta-Mission
**Description**: Mission 200: A self-optimizing directive where the OS analyzes all other 199 missions and suggests new directives.
- **Acceptance Criteria**:
  - Successfully identifies the top 5% earning missions and auto-allocates 80% of idle resources to them.
  - Generates "Mission 201-300" JSON schema based on current market inefficiencies.
  - Presents meta-strategies to the human operator via a dedicated "Strategy Proposal" HUD.

## Proposed Changes

### [Frontend] [IDE]
- [NEW] [AgentLogicEditor.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/AgentLogicEditor.jsx): The development environment.
- [NEW] [HistoryReplay.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/HistoryReplay.jsx): The debugger.

### [Backend] [Orchestration]
- [MODIFY] [blue_green_service.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/blue_green_service.py): Deployment logic.
- [NEW] [meta_optimizer.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/meta_optimizer.py): Mission 200 logic.

## Verification Plan

### Automated Tests
- `pytest tests/core/test_hot_reload_persistence.py`
- `pytest tests/analytics/test_alpha_reporting.py`

### Manual Verification
- Edit the logic for a "Scraper" agent in the IDE and hit **Hot Reload**.
- Verify that a past failure can be "Replayed" and results in a "Success" with the new code.
- Generate a daily report and confirm data accuracy against the DB.
