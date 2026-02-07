# Backend Service: Core

## Overview
The **Core Service** houses the platform's highest level of system abstraction and unification. Its primary role is to serve as the "Ghost in the Machine," aggregating various specialized modules—Finance, Sovereignty, Singularity, and Space—into a single, unified system status and directive interface.

## Core Components

### 1. OmegaGeist Unification Engine (`omega_geist.py`)
The final aggregation layer of the Sovereign OS implementation (Phase 215.3).
- **Epoch Monitoring**: Performs deep-health checks across all major architectural "Epochs" (e.g., FinTech, Sovereignty, Singularity).
- **System Awareness**: Monitors the high-level operational state and "Awareness" level of the collective AI workforce.
- **Master Directive**: Ensures all sub-systems are aligned with the core system directive: `PRESERVE_AND_GROW`.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **System BIOS** | Initialization Console | `omega_geist.awaken()` |
| **Mission Control** | System Health Matrix | `omega_geist.awaken()` (Status fields) |
| **Warden / Security** | Epoch Pulse Monitor | `omega_geist.awaken()` |
| **Developer Sandbox** | Unification Trace | `omega_geist.modules` registry |

## Dependencies
- `logging`: Standard system logging for master system event tracking.
- `time`: Used for simulated system hardware spin-up and synchronization during initialization.

## Usage Examples

### Initializing System Unification
```python
from services.core.omega_geist import OmegaGeistService

geist = OmegaGeistService()

# Perform master system check
sys_status = geist.awaken()

if sys_status["Awareness"] == "HIGH":
    print(f"System Unification Successful. Directive: {sys_status['Directive']}")
```
