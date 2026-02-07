# Backend Service: Mobile (Quick Actions)

## Overview
The **Mobile Service** is a lightweight compatibility layer designed to optimize the Sovereign OS experience for smaller screens. Its primary function is to expose **Quick Actions**—high-leverage, macro commands that allow a user to perform complex portfolio operations with a single tap. This is crucial for "on-the-go" management, where full dashboard interactivity is limited.

## Core Components

### 1. Quick Action Executor (`quick_actions.py`)
The command hub for mobile inputs.
- **Macro Command Logic**: Maps simple string commands (e.g., `CLOSE_ALL`) to complex backend workflows.
- **Defined Actions**:
    - **CLOSE_ALL**: Emergency liquidation of all open speculative positions.
    - **HEDGE**: Immediately buys OTM puts or short futures to delta-neutralize the portfolio.
    - **REDUCE_50**: Halves the size of every active position to reduce risk exposure.
    - **STOP_TRADING**: Activates "Zen Mode," halting all algorithmic trading bots.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mobile Layout** | Floating Action Button (FAB) | `quick_actions.execute()` | **Partial / Disconnected** |

> [!WARNING]
> **Integration Gap**: A `QuickActions.jsx` component exists in the frontend codebase, but it currently relies on hardcoded default actions (`Quick Trade`, `Deposit`) rather than the backend's defined macros (`CLOSE_ALL`, `HEDGE`). The wiring to the backend `execute()` endpoint is **not yet implemented**.

## Dependencies
- `typing`: Standard library for type safety.
- `logging`: Records mobile command execution for audit trails.

## Usage Examples

### Executing a 'Panic' Hedge Command
```python
from services.mobile.quick_actions import QuickActions

# User taps "HEDGE" on mobile app
action_result = QuickActions.execute("HEDGE")

if action_result["success"]:
    print(f"Command Executed: {action_result['description']}")
else:
    print("Invalid Mobile Command")
```

### Flattening the Portfolio (Emergency Close)
```python
from services.mobile.quick_actions import QuickActions

# User taps "CLOSE ALL"
result = QuickActions.execute("CLOSE_ALL")
# Backend would trigger OrderExecutionService to send liquidating market orders
print(result) 
# Output: {'success': True, 'action': 'CLOSE_ALL', 'description': 'Close all positions'}
```
