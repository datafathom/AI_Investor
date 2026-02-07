# Backend Service: Private Banking (The Velvet Rope)

## Overview
The **Private Banking Service** strictly manages the exclusivity of the platform. It acts as the "Bouncer," automatically upgrading users to higher tiers of service based on their Net Worth and assigning them human Relationship Managers (RMs) to handle complex manual needs. It distinguishes the platform from a retail brokerage by offering "White Glove" support logic.

## Core Components

### 1. Client Qualifier (`qualifier.py`)
The Gatekeeper.
- **Tier Logic**:
    - **PRIVATE**: > $10M Net Worth.
    - **ULTRA**: > $50M Net Worth.
    - **FAMILY_OFFICE**: > $100M Net Worth.
- **Automatic Upgrades**: Monitors net worth changes to trigger upgrade workflows (e.g., notifying the Concierge team).

### 2. RM Load Balancer (`rm_load_balancer.py`)
The Assigner.
- **Human Resource Management**: Assigns a human Relationship Manager to a new client based on capacity.
- **Capacity Limits**: Enforces hard caps (e.g., 50 clients per RM for Ultra High Net Worth) to ensure service quality remains high.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Settings** | Account Tier | `qualifier.qualify_client()` | **Implemented** (Implicit in `departmentRegistry.js`) |
| **Concierge** | Chat to RM | `rm_load_balancer.assign_next_available_rm()` | **Missing** (UI not found) |

## Dependencies
- `uuid`: For unique client and RM identification.

## Usage Examples

### Qualifying a Client
```python
from services.private_banking.qualifier import PrivateBankingQualifier

qualifier = PrivateBankingQualifier()

# User just hit $55M Net Worth
status = qualifier.qualify_client(
    user_id="user_whale_01",
    net_worth=55000000.00
)

print(f"Qualified Tier: {status['tier']}") # Should be ULTRA
print(f"Is Qualified: {status['qualified']}")
```

### Assigning a Relationship Manager
```python
from services.private_banking.rm_load_balancer import RMLoadBalancer

balancer = RMLoadBalancer()

managers = [
    {"id": "rm_alice", "current_count": 48},
    {"id": "rm_bob", "current_count": 12} # Bob is open
]

assigned_rm = balancer.assign_next_available_rm(
    client_tier="ULTRA",
    managers=managers
)

print(f"Assigned RM: {assigned_rm}")
```
