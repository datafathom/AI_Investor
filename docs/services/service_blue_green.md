# Backend Service: Blue-Green

## Overview
The **Blue-Green Service** provides the infrastructure for **Zero-Downtime Hot-Swapping** of agent logic and system components. It ensures that new code can be deployed, verified, and promoted to production without interrupting active financial operations or agent processing.

## Core Concepts

### 1. Environment Topology
- **GREEN (Production)**: The currently active and trusted version of the logic.
- **BLUE (Staging)**: The new version of the logic being prepared for cutover.

### 2. Hot-Swap Lifecycle (`deploy_hot_swap`)
The service automates a robust 4-stage deployment cycle:
1. **Backup Green**: Creates a timestamped snapshot of the current logic in the `backups/agents` directory before any changes are made.
2. **Deploy Blue**: Writes the new code to the target execution path.
3. **Verify Blue**: Performs a simulated verification phase (static analysis or startup check) to ensure the new logic is viable.
4. **Cutover**: Officially promotes the BLUE version to LIVE status and updates the internal version metadata registry.

### 3. Automated Rollback
If a deployment fails at any stage (verification error, runtime crash), the service can automatically or manually revert to the most recent GREEN backup. This maintains system stability and prevents "half-deployed" or broken states.

## Version Registry
The service maintains an in-memory `active_versions` registry that tracks:
- `deployment_id`: A unique identifies for the swap event.
- `timestamp`: When the deployment occurred.
- `backup_path`: The location of the previous version's snapshot.
- `status`: Current lifecycle state (`LIVE`, `ROLLED_BACK`, etc.).

## Usage Examples

### Executing a Logic Hot-Swap
```python
from services.blue_green_service import get_blue_green_service

bg_service = get_blue_green_service()

new_agent_logic = """
def process_event(event):
    print("New Optimized Logic V2")
    return True
"""

# Deploy and verify
result = await bg_service.deploy_hot_swap(
    agent_id="trading_agent_alpha",
    new_code=new_agent_logic,
    file_path="services/agents/trading_agent_alpha.py"
)

if result['status'] == "success":
    print(f"Hot-Swap Complete: Deployment ID {result['deployment_id']}")
```

### Performing a Manual Rollback
```python
from services.blue_green_service import get_blue_green_service

bg_service = get_blue_green_service()

success = bg_service.rollback(
    agent_id="trading_agent_alpha",
    file_path="services/agents/trading_agent_alpha.py"
)

if success:
    print("System restored to previous stable Green version.")
```
