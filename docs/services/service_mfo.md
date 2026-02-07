# Backend Service: MFO (Multi-Family Office)

## Overview
The **MFO (Multi-Family Office) Service** provides the administrative and lifestyle infrastructure required to manage multiple high-net-worth families within a single institutional framework. It enables shared office operations by automating the allocation of overhead costs (Staff, Tech, Rent), orchestrating professional concierge and expert network requests, and aggregating group spending to unlock institutional-grade vendor discounts and leverage that individual families could not achieve alone.

## Core Components

### 1. Shared Concierge & Expert Router (`concierge_srv.py`)
Centralized management of lifestyle and professional requests.
- **Lifestyle Ticketing**: Routes and prioritizes requests (from travel and jets to urgent security) into a shared MFO concierge queue. It identifies VIP priority based on the nature and urgency of the request.
- **Expert Network Access**: Interfaces with a vetted professional network (via Neo4j) to locate specialists in domains like legal, tax, or fine art, ensuring MFO-wide discount rates are applied.

### 2. Overhead Expense Allocator (`expense_allocator.py`)
Automates the splitting of MFO operational costs.
- **Pro-Rata AUM Allocation**: Default methodology that splits shared costs (e.g., Bloomberg terminals, shared office rent) proportionally based on each family's Assets Under Management (AUM).
- **Fixed Split Allocation**: Alternative methodology that applies an equal fixed-cost burden across all participating families regardless of size.

### 3. Vendor Leverage Aggregator (`spend_aggregator.py`)
Pools family spending to achieve institutional benefits.
- **Group Negotiation Power**: Aggregates the total spending of all member families with specific vendors. If the aggregate spend exceeds specific thresholds (e.g., >$1M), it automatically unlocks "Tier 1" institutional discounts, providing group leverage that benefits every participating family.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Concierge Hub** | Active Lifestyle Tickets | `concierge_service.create_lifestyle_request()` |
| **MFO Admin Panel** | Overhead Allocation Table | `mfo_expense_allocator.split_monthly_overhead()` |
| **MFO Admin Panel** | Vendor Leverage Tracker | `mfo_spend_aggregator.calculate_group_leverage()` |
| **Governance Hub** | Vetted Expert Directory | `concierge_service.fetch_expert_access()` |
| **System Settings** | MFO Billing Summary | `mfo_expense_allocator` (Allocation results) |

## Dependencies
- `decimal`: Used for all precision math involving overhead splits and aggregate spending.
- `uuid`: Generates unique identifiers for family accounts and concierge tickets.
- `logging`: Records structural MFO events like "Threshold Reached for Vendor Discount" or "Overhead Allocation Finalized."

## Usage Examples

### Creating a High-Priority Concierge Request
```python
from services.mfo.concierge_srv import ConciergeService
import uuid

concierge = ConciergeService()
family_id = uuid.uuid4()

# Client requests an urgent private jet charter
req = concierge.create_lifestyle_request(
    family_id=family_id,
    req_type="TRAVEL",
    detail="URGENT: Need private charter from London to Zurich for Family Council."
)

print(f"Ticket: {req['ticket_id']} | Priority: {req['priority']} | Team: {req['assigned_team']}")
```

### Allocating MFO Overhead via Pro-Rata AUM
```python
from services.mfo.expense_allocator import MFOExpenseAllocator
from decimal import Decimal

allocator = MFOExpenseAllocator()

# Shared office overhead for the month: $250k
overhead = Decimal("250000.00")

# Families and their current AUMs
aums = {
    "Family_Vanderbilt": Decimal("1200000000.00"),
    "Family_Astor": Decimal("800000000.00")
}

splits = allocator.split_monthly_overhead(total_overhead=overhead, family_aums=aums)

for s in splits:
    print(f"Family: {s['family_id']} | Share: ${s['amount']:,} (Method: {s['method']})")
```

### Unlocking Group Leverage via Spend Aggregation
```python
from services.mfo.spend_aggregator import MFOSpendAggregator

aggregator = MFOSpendAggregator()

# Total spends at a specific provider (e.g., Wheels Up) across all MFO families
provider_spends = [400000, 350000, 300000] # Total > $1M

leverage = aggregator.calculate_group_leverage(vendor_name="GlobalAero", family_spends=provider_spends)

print(f"Vendor: {leverage['vendor']} | Aggregate Spend: ${leverage['aggregate_spend']:,.2f}")
print(f"Discount Unlocked: {leverage['group_discount_pct']}% | Status: {leverage['status']}")
```
