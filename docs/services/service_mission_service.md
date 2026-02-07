# Backend Service: Mission Service (Autonomous Squads)

## Overview
The **Mission Service** is the platform's operational commander. It transforms high-level user objectives (e.g., "Find M&A Targets" or "Liquidate Crypto Assets") into executable, multi-agent workflows. By utilizing a "Template Registry," the service allows users to deploy pre-configured squads of agents with specific roles, budgets, and risk parameters. It orchestrates the lifecycle of these missions—from configuration and budget allocation to the asynchronous dispatch of jobs via the ARQ task queue.

## Core Components

### 1. Mission Template Registry (`mission_service.py`)
The catalog of available autonomous operations.
- **Template Loading**: Ingests mission definitions from `config/mission_templates.json`. Each template defines the mission's goal, required departments (e.g., Wealth + Intelligence), outcome logic hash, and default constraints.
- **Example Missions**:
    - **M&A Scout**: Deploys Wealth and Intelligence agents to find acquisition targets.
    - **Crash Protocol**: Triggers Security and Finance agents for emergency asset liquidation.
    - **Shadow Mirror**: Runs a red-team security audit on internal infrastructure.

### 2. Autonomous Deployment Engine (`mission_service.py`)
Instantiates and dispatches mission squads.
- **Squad Configuration**: Merges the static template with dynamic user overrides (e.g., "Increase budget to $5,000" or "Set Time-to-Live to 2 hours").
- **ARQ Job Dispatch**: Converts the mission parameters into asynchronous jobs (`run_agent_logic`) and pushes them to the Redis-backed ARQ worker pool. This ensures that agents execute in parallel, non-blocking processes.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mission Control** | Mission Library Grid | `mission_service.get_all_templates()` | **Implemented** |
| **Mission Control** | Launch Configuration Modal| `mission_service.deploy_mission()` | **Implemented** |
| **Mission Overview** | Active Mission Tracker | `mission_service` (Job Status) | **Implemented** |
| **Orchestrator** | Visual Mission Flow | `mission_service` (Dept Dependencies) | **Implemented** |

> [!NOTE]
> **Integration Status**: The Mission Service is deeply integrated into the frontend. The `MissionControl.jsx` page provides a full UI for browsing the template library, configuring parameters, and visually monitoring the real-time status of deployed agent squads.

## Dependencies
- `config.mission_templates.json`: The source of truth for all available mission definitions.
- `arq`: The asynchronous task queue used to dispatch agent jobs to background workers.
- `uuid`: Generates unique Mission IDs (`mssn_...`) for tracking execution across the distributed system.

## Usage Examples

### Listing Available Missions for a Specific Sector
```python
from services.mission_service import get_mission_service

svc = get_mission_service()

# specific templates for 'Security' sector missions
security_missions = svc.get_all_templates(sector="Security")

for m in security_missions:
    print(f"ID: {m['id']} | Name: {m['name']}")
    print(f"Goal: {m['goal']}")
```

### Deploying a 'Crash Protocol' Mission via Code
```python
from services.mission_service import get_mission_service

svc = get_mission_service()

# Deploy emergency liquidation with elevated budget
result = await svc.deploy_mission(
    template_id="mission_002", # Crash Protocol
    config={
        "budget": 5000, # Override default $1000
        "ttl": 300 # 5 minutes max execution time
    },
    arq_pool=redis_pool_connection
)

print(f"Mission Launched: {result['mission_id']}")
print(f"Active Jobs: {len(result['jobs'])}")
```
