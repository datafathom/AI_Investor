# Phase 132: Active vs. Passive Operating Efficiency Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Operations/Analyst Team

---

## 📋 Overview

**Description**: Model and compare the operational efficiency of Active management vs. Passive indexing. This involves tracking fees, trading costs, tax drag, and the "human capital" cost of research for active strategies to determine the true net benefit.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 12

---

## 🎯 Sub-Deliverables

### 132.1 Fixed Passive Models Workload Tracker `[ ]`

**Acceptance Criteria**: Track the operational workload (rebalancing frequency, research hours) required for passive models versus active stock picking.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE operational_workload (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_type VARCHAR(20) NOT NULL,    -- ACTIVE, PASSIVE, HYBRID
    model_name VARCHAR(100),
    
    -- Resource Usage
    research_hours_monthly DECIMAL(10, 2),
    trading_minutes_monthly DECIMAL(10, 2),
    monitoring_hours_monthly DECIMAL(10, 2),
    
    -- Costs
    data_subscription_cost DECIMAL(10, 2),
    tool_cost DECIMAL(10, 2),
    
    log_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Workload Tracker | `services/operations/workload_tracker.py` | `[ ]` |
| Cost Allocator | `services/operations/cost_allocator.py` | `[ ]` |

---

### 132.2 Management Fee Margin Comparison `[ ]`

**Acceptance Criteria**: Calculate the margin pressure on advisors by comparing fee revenue against the commoditized cost of beta (0.03% ETFs).

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Margin Calc | `services/finance/fee_margin_calc.py` | `[ ]` |
| Beta Cost Baseline | `services/finance/beta_cost_baseline.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Margin Dashboard | `frontend2/src/components/Operations/MarginDashboard.jsx` | `[ ]` |
| Fee Compression Chart | `frontend2/src/components/Charts/FeeCompression.jsx` | `[ ]` |

---

### 132.3 Neo4j Advisor Focus Node (Gathering vs. Research) `[ ]`

**Acceptance Criteria**: Map how advisors spend their time in Neo4j to identify if they are "Asset Gatherers" (Sales) or "Investment Managers" (Research).

#### Neo4j Schema

```cypher
(:ADVISOR {id: "uuid", name: "John Doe"})

(:ACTIVITY:SALES {type: "CLIENT_MEETING", hours: 25})
(:ACTIVITY:RESEARCH {type: "STOCK_ANALYSIS", hours: 5})

(:ADVISOR)-[:SPENDS_TIME {pct: 0.80}]->(:ACTIVITY:SALES)
(:ADVISOR)-[:SPENDS_TIME {pct: 0.20}]->(:ACTIVITY:RESEARCH)

// Classification Node
(:ADVISOR)-[:CLASSIFIED_AS]->(:FOCUS_TYPE {category: "ASSET_GATHERER"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Advisor Focus Graph | `services/neo4j/advisor_focus_graph.py` | `[ ]` |
| Focus Classifier | `services/operations/focus_classifier.py` | `[ ]` |

---

### 132.4 Operational Cost Calculator `[ ]`

**Acceptance Criteria**: Calculator to sum all hidden costs of active management: spreads, commissions, tax drag, and cash drag.

```python
class OperationalCostCalculator:
    """
    Calculate Total Cost of Ownership (TCO) for strategies.
    
    Costs:
    1. Expense Ratio / Management Fee
    2. Transaction Costs (Bid-Ask Spread)
    3. Tax Cost (Capital Gains distributions)
    4. Cash Drag (Opportunity cost of uninvested cash)
    """
    
    def calculate_tco(self, strategy: Strategy) -> Decimal:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Op Cost Calculator | `services/finance/op_cost_calculator.py` | `[ ]` |
| Tax Drag Calc | `services/tax/tax_drag_calc.py` | `[ ]` |

---

### 132.5 Client Retention Model `[ ]`

**Acceptance Criteria**: Model correlation between performance/fees and client retention rates.

| Component | File Path | Status |
|-----------|-----------|--------|
| Retention Model | `services/analytics/retention_model.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py ops workload` | Show workload metrics | `[ ]` |
| `python cli.py ops calc-tco <strategy>` | Calculate total cost | `[ ]` |

---

*Last verified: 2026-01-25*
