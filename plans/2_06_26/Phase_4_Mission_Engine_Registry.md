# Phase 4: Mission Engine & Registry

## Overview
This phase transitions the OS from a collection of scripts into a true Mission Orchestrator. We are building the registry for the 200+ mission templates and the engine that translates these templates into active, multi-agent squads. Missions here are "Agency Perimeters"—strict containers for the rules of engagement.

## Deliverables

### 1. The 200-Mission Master Manifesto
**Description**: A comprehensive JSON/SQL library of all mission directives, sectors, and logic requirements.
- **Acceptance Criteria**:
  - All 200 missions from the `missionModulePlanning.txt` are normalized into the `mission_templates` table.
  - Each mission includes a `sector` (Finance, Security, etc.) and a `required_depts` list.
  - JSON schema validation ensures no template is missing its `goal` or `logic_hash`.

### 2. Hierarchical Mission Registry (React)
**Description**: A searchable library interface for operators to browse and select mission templates.
- **Acceptance Criteria**:
  - Filterable by Sector (Wealth, Shadow, Intelligence, etc.).
  - Displays "Est. ROI" and "Risk Level" (High/Medium/Low) for each template based on historical data.
  - "Quick Deploy" button initiates the configuration modal.

### 3. Mission "Agency Perimeter" Configurator
**Description**: A modal for setting strict operational constraints (Budget, TTL, Max Steps).
- **Acceptance Criteria**:
  - "Smart Sliders" enforce hard-caps on budget that cannot be overridden by the agent.
  - "Approval Mode" toggle (Strict/Threshold/Auto) is clearly defined and visualized.
  - Save button persists the configuration as a unique `active_mission` instance.

### 4. Squad Assembly Engine (Backend)
**Description**: The logic that maps a mission mission template to specific sub-agent invocations across multiple departments.
- **Acceptance Criteria**:
  - Successfully spawns the required Kafka consumers/producers for a multi-dept mission.
  - Correctly assigns `job_id` and `mission_id` to every outbound event.
  - "Context Injection" logic provides the agent with the specific mission ruleset on startup.

### 5. Sector-Based Resource Isolation
**Description**: Ensuring that a "Wealth" mission cannot access the "Shadow" department's tools unless explicitly connected.
- **Acceptance Criteria**:
  - Permission checks are enforced at the API gateway level for all tool calls.
  - Cross-sector data leak test (negative test) confirms isolation.
  - Audit logs clearly mark which sector authorized a specific tool execution.

### 6. Automated Mission ROI Batching
**Description**: Background process to aggregate historical mission performance into the template library.
- **Acceptance Criteria**:
  - Job runs every 24 hours to update "Avg Profit" and "Avg Gas" in the `mission_templates` table.
  - "Top Performance" badges are automatically applied to the most efficient missions in the UI.
  - Failed mission patterns are flagged for Dept 1 (Orchestrator) review.

## Proposed Changes

### [Backend] [Registry]
- [NEW] [mission_templates.json](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/config/mission_templates.json): The full 200 list.
- [NEW] [mission_service.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/mission_service.py): Deployment and lifecycle logic.

### [Frontend] [HUD]
- [NEW] [MissionLibrary.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/MissionLibrary.jsx): The browser.
- [NEW] [MissionConfigModal.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/MissionConfigModal.jsx): The configurator.

## Verification Plan

### Automated Tests
- `pytest tests/core/test_mission_deployment.py`
- `pytest tests/infra/test_sector_isolation.py`

### Manual Verification
- Deploy a "Security" mission and attempt to call a "Trading" tool (verify rejection).
- Search for a specific niche mission (e.g., "Burnout Recruiter") and verify template loads.
