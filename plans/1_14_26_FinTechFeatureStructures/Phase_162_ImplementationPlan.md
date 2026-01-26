# Phase 162: Multi-Family Office (MFO) Shared-Cost Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Family Office Team

---

## 📋 Overview

**Description**: Architect the Multi-Family Office (MFO) model. Allows multiple wealthy families ($20M-$100M) to share the cost of top-tier investment talent and infrastructure, achieving SFO-level capabilities at a fraction of the price (e.g., splitting a CIO's salary 5 ways).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 2

---

## 🎯 Sub-Deliverables

### 162.1 5-Family Shared Cost Logic (20% each) `[ ]`

**Acceptance Criteria**: Cost allocation engine. Split overhead (Rent, Tech, CIO Salary) among participating families based on either AUM%, fixed share (1/N), or usage-based keys.

#### Backend Implementation

```python
class ExpenseAllocator:
    """
    Allocate MFO operating expenses to participating families.
    
    Methods:
    - Fixed Split: Equal share (1/N).
    - Pro-Rata AUM: Share based on assets.
    - Usage Based: Share based on billable hours/tickets.
    """
    
    def allocate_expenses(
        self,
        expenses: list[Expense],
        families: list[Family],
        method: str = 'PRO_RATA_AUM'
    ) -> AllocationReport:
        """
        Calculate each family's share of the monthly burn.
        """
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Allocator Service | `services/mfo/expense_allocator.py` | `[ ]` |
| Billing Generator | `services/mfo/billing_gen.py` | `[ ]` |

---

### 162.2 Postgres MFO Trade Priority Schema `[ ]`

**Acceptance Criteria**: Handle trade aggregation and allocation. Block trades are executed at the MFO level and allocated pro-rata to family accounts. Ensure fair pricing (average price) for all, preventing "cherry-picking" of good fills.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE trade_blocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    total_quantity DECIMAL(20, 6) NOT NULL,
    average_price DECIMAL(20, 4),
    execution_time TIMESTAMPTZ,
    broker_order_id VARCHAR(100),
    
    -- Status
    status VARCHAR(20),                -- PENDING, FILLED, ALLOCATED, PARTIAL
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE block_allocations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    block_id UUID REFERENCES trade_blocks(id),
    family_account_id UUID NOT NULL,
    allocated_quantity DECIMAL(20, 6),
    allocated_price DECIMAL(20, 4),    -- Should match average_price
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/162_trade_allocation.sql` | `[ ]` |
| Trade Aggregator | `services/trading/trade_aggregator.py` | `[ ]` |

---

### 162.3 Neo4j Shared Professionals ↔ Multiple Families `[ ]`

**Acceptance Criteria**: Graph modeling of the MFO structure. One Professional node serves multiple Family nodes, but strict privacy firewalls must exist between Families (Family A cannot see Family B's data).

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:MFO_FIRM {name: "Summit Rock"})-[:EMPLOYS]->(:PROFESSIONAL:CIO {name: "Jane Doe"})

(:FAMILY_OFFICE:MEMBER {name: "Family A"})<-[:ADVISES]-(:PROFESSIONAL:CIO)
(:FAMILY_OFFICE:MEMBER {name: "Family B"})<-[:ADVISES]-(:PROFESSIONAL:CIO)

// Privacy Constraint
// No direct link between Family A and Family B
// MATCH (f1:FAMILY)-[:CAN_VIEW]->(f2:FAMILY) -> Must be 0
```

| Component | File Path | Status |
|-----------|-----------|--------|
| MFO Graph Service | `services/neo4j/mfo_graph.py` | `[ ]` |
| Privacy Firewall | `services/security/family_firewall.py` | `[ ]` |

---

### 162.4 Privacy Risk Disclosure Service `[ ]`

**Acceptance Criteria**: Automated generation of privacy disclosures. Families must acknowledge that while costs are shared, there is a theoretical risk of data leakage (mitigated by system controls).

| Component | File Path | Status |
|-----------|-----------|--------|
| Disclosure Manager | `services/compliance/privacy_disclosure.py` | `[ ]` |

---

### 162.5 MFO vs. Private Banker Comparison ($50M+) `[ ]`

**Acceptance Criteria**: Comparison tool showing MFO (Fiduciary, Open Architecture, Buy-Side) vs. Private Bank (Sales-driven, Proprietary Products, Sell-Side).

| Component | File Path | Status |
|-----------|-----------|--------|
| Comparison Tool | `services/reporting/mfo_vs_bank.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| MFO Dashboard | `frontend2/src/components/MFO/Dashboard.jsx` | `[ ]` |
| Cost Split View | `frontend2/src/components/MFO/CostSplit.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py mfo allocate-costs` | Run expense allocation | `[ ]` |
| `python cli.py mfo create-block` | Aggregate trades | `[ ]` |

---

*Last verified: 2026-01-25*
