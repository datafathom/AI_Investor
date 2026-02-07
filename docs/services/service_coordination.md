# Backend Service: Coordination

## Overview
The **Coordination Service** is the platform's inter-departmental orchestration layer. It is designed to align the actions of diverse stakeholders—such as Financial Advisors, CPAs, Attorneys, and AI Agents—around a unified set of client objectives, ensuring that complex financial strategies (like estate planning or tax-loss harvesting) are executed in sync.

## Core Components

### 1. Shared Goals Manager (`shared_goals.py`)
A centralized registry for multi-stakeholder objectives.
- **Stakeholder Mapping**: Explicitly tracks which entities (e.g., `ADVISOR`, `CPA`, `ATTORNEY`) are responsible for portions of a top-level goal.
- **Atomic Goal Tracking**: Maintains the lifecycle of coordinated tasks from `OPEN` to completion.
- **Audit Logging**: Emits `COORDINATION_LOG` events to the system's observability stack, capturing exactly when and how goals are modified across different departments.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Mission Control** | Coordinated Timeline | `shared_goals_service.goals` (filtered by client) |
| **Collaboration Hub** | Shared Objectives Feed | `shared_goals_service.add_coordinated_goal()` |
| **Advisor Workstation** | Stakeholder Progress Panel | `shared_goals_service.goals` |
| **Client Portal** | Unified Roadmap | `shared_goals_service.goals` |

## Dependencies
- `logging`: Standard system logging for cross-stakeholder audit trails.

## Usage Examples

### Adding a Coordinated Tax Strategy Goal
```python
from services.coordination.shared_goals import SharedGoalsService

coord_svc = SharedGoalsService()

# Coordinate a ROTH conversion between the Advisor and CPA
goal = coord_svc.add_coordinated_goal(
    client_id="client_vanguard_88",
    goal_desc="Execute $50k ROTH Conversion for 2026 Tax Year",
    stakeholders=["ADVISOR", "CPA"]
)

print(f"Goal Coordinated: {goal['description']} with status {goal['status']}")
```
