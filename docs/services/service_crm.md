# Backend Service: CRM

## Overview
The **CRM (Customer Relationship Management)** service provides the platform's relationship intelligence layer. It is responsible for categorizing the user's client base into distinct tiers based on Assets Under Management (AUM) and strategic institutional status, ensuring that high-value opportunities and support resources are allocated with maximum efficiency.

## Core Components

### 1. Priority Scorer (`client_priority.py`)
A policy-driven engine that determines client importance and service levels (Phase 173.1).
- **Tiering Logic**:
    - **TIER_1_SFO (Priority 1)**: Single Family Offices (SFOs) or clients with **$50M+** in AUM. These represent the highest strategic priority.
    - **TIER_2_UHNW (Priority 2)**: Ultra-High-Net-Worth individuals with **$5M+** in AUM. Includes "Qualified Purchaser" status flagging for regulatory access to private funds.
    - **TIER_3_RETAIL (Priority 3)**: Standard retail clients.
- **Regulatory Profiling**: Automatically determines if a client meets the SEC "Qualified Purchaser" threshold, which is critical for restricted investment participation.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **CRM Dashboard** | Client List | `priority_scorer.calculate_priority()` (Tier labels) |
| **CRM Dashboard** | AUM Distribution Plot | `priority_scorer.calculate_priority()` |
| **Deal Center** | Allocation Modal | `priority_scorer.calculate_priority()` (Priority sorting) |
| **Client Onboarding** | Eligibility Wizard | `priority_scorer.calculate_priority()` (QP Status) |

## Dependencies
- `logging`: Records CRM logic events for institutional relationship audit trails.

## Usage Examples

### Calculating Client Priority and QP Status
```python
from services.crm.client_priority import PriorityScorer

scorer = PriorityScorer()

# Calculate tier for an institutional prospect
client_profile = scorer.calculate_priority(
    aum=120_000_000, 
    is_sfo=True
)

print(f"Client Tier: {client_profile['tier']}")
print(f"Qualified Purchaser: {client_profile['is_qualified_purchaser']}")
```
