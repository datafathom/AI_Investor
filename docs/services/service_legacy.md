# Backend Service: Legacy (Generational Stewardship)

## Overview
The **Legacy (Generational Stewardship) Service** is the platform's engine for ultra-long-term wealth preservation and multi-generational data archival. Unlike traditional portfolio services that focus on 5-10 year horizons, the Legacy service operates on a **100-year timescale**. It manages the hyper-durable asset allocations required for inter-generational survival and provides specialized tools like "Digital Time Capsules" to preserve family wisdom and institutional state for descendants through the next century.

## Core Components

### 1. Century Planner (`century_planner.py`)
The 100-year strategic allocator.
- **Hyper-Durable Allocation**: Focuses on assets with extreme longevity: physical gold, arable land, clean water rights, and Bitcoin (Cold Storage). It generates a "Century Plan" that prioritizes core wealth preservation over short-term market alpha.
- **Inter-Generational Horizon**: Sets a dynamic target (e.g., Year 2126) and provides rebalancing prescriptions meant to be followed across multiple generations.

### 2. Digital Time Capsule (`time_capsule.py`)
Long-term data archival on resilient physical media.
- **Archival Hashing**: Hashes and prepares critical family or institutional data for etching on high-durability media such as **Quartz Glass (5D memory)** or M-DISC.
- **Unlock Protocols**: Establishes "Sealed" archival states with specific unlock dates, effectively creating a cryptographically-secured bridge to the future.

### 3. Perpetual System Monitor (`perpetual.py`)
Stewardship of the Sovereign OS state across the system's lifecycle.
- **System Post-Mortem & Perpetual State**: Tracks the entire operational history of the AI Investor system. It maintains a ledger of major milestones and phases, ensuring that the "Ancestral State" of the system is preserved for future operators.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Legacy Station** | 100-Year Century Planner | `century_planner.generate_100_year_plan()` |
| **Legacy Station** | Digital Time Capsule Seal | `time_capsule.seal_capsule()` |
| **Governance Hub** | Perpetual System Status | `perpetual.generate_post_mortem()` |
| **Legacy Station** | Durable Asset Heatmap | `century_planner.target_allocation` |
| **Admin Panel** | System Milestone Ledger | `perpetual.record_milestone()` |

## Dependencies
- `hashlib`: Used for generating archival hashes for time capsules.
- `datetime`: Tracks system inception and generational target dates.
- `logging`: Records the sealing of capsules and the generation of multi-century plans.

## Usage Examples

### Generating a 100-Year Wealth Preservation Plan
```python
from services.legacy.century_planner import CenturyPlannerService

planner = CenturyPlannerService()

# Generate a plan for a $100M Family Office AUM
plan = planner.generate_100_year_plan(current_wealth=100_000_000.0)

print(f"Plan Horizon: {plan['horizon']}")
print(f"Goal: {plan['primary_goal']}")
for asset, amount in plan['allocation_usd'].items():
    print(f"{asset}: ${amount:,.2f}")
```

### Sealing a Generational Time Capsule
```python
from services.legacy.time_capsule import TimeCapsuleService

capsule_svc = TimeCapsuleService()

# Prepare family council mission statement for the year 2076
capsule = capsule_svc.seal_capsule(
    content_description="Family Constitution & Mission Statement",
    unlock_date="2076-01-01"
)

print(f"Capsule ID: {capsule['capsule_id']}")
print(f"Storage Medium: {capsule['media_type']}")
print(f"Physical Target: {capsule['location']}")
```

### Recording an Institutional Milestone for Perpetual History
```python
from services.legacy.perpetual import PerpetualLegacy

legacy = PerpetualLegacy()

# Record the completion of Phase 100 Deployment
legacy.record_milestone("Sovereign OS reached Perpetual Operation state.")
status = legacy.generate_post_mortem()

print(f"System Legacy Mode: {status['legacy_mode']}")
print(f"Total Captured Milestones: {status['total_milestones']}")
```
