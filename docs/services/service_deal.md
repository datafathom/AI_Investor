# Backend Service: Deal

## Overview
The **Deal Service** manages the lifecycle of private investment opportunities, specifically focusing on private equity syndication and "Club Deals." It is the platform's mechanism for handling oversubscribed investment capacity, ensuring that scarce deal flow is distributed according to institutional priorities and regulatory tiers.

## Core Components

### 1. Deal Allocation Engine (`deal_allocation_srv.py`)
The platform's priority enforcement layer for investment capacity.
- **Priority Tiering**: Implements a strict allocation policy:
    1. **SFO (Single Family Office)**: Receives first-priority full-fill where possible.
    2. **UHNW (Ultra-High-Net-Worth)**: Receives pro-rata allocation of the remaining capacity.
    3. **HNW (High-Net-Worth)**: Allocated only if capacity remains, otherwise moved to the waitlist.
- **Pro-Rata Logic**: Automatically calculates fractional allocations when total client demand exceeds available deal capacity.

### 2. Club Deal Manager (`club_deal_manager.py`)
A tool for formation and syndication of private investment groups.
- **Syndication Calculations**: Determines the "Syndication Gap" (Total Deal Size vs. Core Platform Commitment).
- **Private Tease Dispatch**: Automates the distribution of deal "teasers" to a selected circle of private participants via the platform's messaging/Kafka bus.

### 3. Waitlist & Interest Manager (`waitlist_manager.py`)
Captures and ranks early-stage interest.
- **First-Look Timestamping**: Logs client interest with high-precision timestamps to maintain a fair "First-Look" order within priority buckets.
- **Priority Bucketing**: Automatically sorts waitlisted participants by client tier (e.g., placing SFOs at the head of the queue regardless of arrival time).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Private Deal Center** | Opportunities List | `club_deal_manager.create_club_deal()` (View deals) |
| **Deal Detail View** | Commitment Button | `waitlist_manager.log_interest()` |
| **Deal Detail View** | My Allocation Card | `deal_allocation_srv.allocate_oversubscribed_deal()` |
| **Admin Panel** | Allocation Resolver | `deal_allocation_srv.allocate_oversubscribed_deal()` |
| **SFO Dashboard** | Exclusive Access Ribbons | `waitlist_manager.log_interest()` (Priority status) |

## Dependencies
- `uuid`: Generates unique identifiers for deals, participants, and transfer tickets.
- `decimal`: Used for precision financial calculations in volume-based allocations.

## Usage Examples

### Resolving an Oversubscribed Deal Allocation
```python
from services.deal.deal_allocation_srv import DealAllocationService
from decimal import Decimal

alloc_svc = DealAllocationService()

# 10M Capacity, 15M Demand
commitments = [
    {"user_id": "sfo_1", "tier": "SFO", "amount": Decimal("8,000,000")},
    {"user_id": "uhnw_1", "tier": "UHNW", "amount": Decimal("5,000,000")},
    {"user_id": "uhnw_2", "tier": "UHNW", "amount": Decimal("2,000,000")},
]

results = alloc_svc.allocate_oversubscribed_deal(
    total_capacity=Decimal("10,000,000"),
    commitments=commitments
)

for res in results:
    print(f"User: {res['user_id']} | Status: {res['status']} | Allocated: ${res['allocated']:,.2f}")
```

### Logging Waitlist Interest
```python
from services.deal.waitlist_manager import WaitlistManager

wm = WaitlistManager()

# Log interest for a highly anticipated deal
result = wm.log_interest(
    deal_id="PE-SERIES-B-AI",
    user_id="client_uhnw_88",
    amount=500_000,
    tier="UHNW"
)

print(f"Waitlist Status: {result['status']} (Position: {result['waitlist_position']})")
```
