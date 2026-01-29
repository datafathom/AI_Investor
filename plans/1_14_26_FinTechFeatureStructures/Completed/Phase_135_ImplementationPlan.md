# Phase 135: Target Date & Glide-Path Automator

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Retirement Team

---

## 📋 Overview

**Description**: Implement an algorithmic glide-path engine similar to Target Date Funds (TDFs) but personalized. Automatically shift asset allocation from equities to fixed income as the user approaches their target retirement or education funding date.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 15

---

## 🎯 Sub-Deliverables

### 135.1 Glide-Path Equity → Bond Shift Service `[x]`

**Acceptance Criteria**: Build a service that calculates and executes the optimal asset allocation shift based on "years to target".

#### Backend Implementation

```python
class GlidePathEngine:
    """
    Calculate target allocation based on years to goal.
    
    Standard Glide Path:
    - 20+ Years: 90/10 Equity/Bond
    - 15 Years: 85/15
    - 10 Years: 75/25
    - 5 Years: 60/40
    - 0 Years: 40/60
    """
    
    def calculate_target_allocation(
        self,
        years_to_target: int,
        risk_tolerance: str = 'MODERATE'
    ) -> AllocationTargets:
        pass
    
    def generate_shift_trades(
        self,
        current_portfolio: Portfolio,
        target_allocation: AllocationTargets
    ) -> list[Trade]:
        """Generate trades to align with glide path."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Glide Path Engine | `services/retirement/glide_path_engine.py` | `[x]` |
| Shift Executor | `services/trading/shift_executor.py` | `[x]` |
| API Endpoint | `web/api/retirement/glide_path.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Glide Path Visualizer | `frontend2/src/components/Charts/GlidePathVisualizer.jsx` | `[x]` |
| Allocation Shift Preview | `frontend2/src/components/Portfolio/ShiftPreview.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Glide Path Engine | `tests/unit/test_glide_path_engine.py` | `[x]` |
| Integration: Shift Execution | `tests/integration/test_shift_execution.py` | `[x]` |

---

### 135.2 Postgres Target Year Milestone Schema `[x]`

**Acceptance Criteria**: Store target dates and milestones for all goals (Retirement, College, House Purchase) to drive the glide path logic.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE goal_milestones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    goal_type VARCHAR(50) NOT NULL,        -- RETIREMENT, EDUCATION, MAJOR_PURCHASE
    target_date DATE NOT NULL,
    
    -- Glide Path Config
    glide_path_strategy VARCHAR(50),       -- AGGRESSIVE, MODERATE, CONSERVATIVE, CUSTOM
    equity_landing_point DECIMAL(5, 2),    -- Equity % at target date (e.g. 0.40)
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    current_years_to_target DECIMAL(5, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_goal_user ON goal_milestones(user_id);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/135_goal_milestones.sql` | `[x]` |
| Goal Model | `models/goal_milestone.py` | `[x]` |

---

### 135.3 Neo4j 529 Plan Allocation Relationships `[x]`

**Acceptance Criteria**: Map 529 plans specifically to their glide paths in Neo4j, acknowledging that education goals have a harder deadline than retirement.

#### Neo4j Schema

```cypher
(:GOAL:EDUCATION {
    id: "uuid",
    beneficiary: "Child Name",
    matriculation_year: 2035
})

(:GLIDE_PATH {
    id: "uuid",
    name: "Age-Based Aggressive",
    current_equity_pct: 0.85
})

(:GOAL)-[:FOLLOWS_PATH {
    rebalance_frequency: "QUARTERLY",
    next_shift_date: date("2026-01-01")
}]->(:GLIDE_PATH)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Goal Graph Service | `services/neo4j/goal_graph.py` | `[x]` |

---

### 135.4 Kafka 12-Month Risk Reduction Trigger `[x]`

**Acceptance Criteria**: Kafka stream that triggers specific risk reduction actions (moving to cash/short-term bonds) 12 months before a major goal deadline.

#### Kafka Topic

```json
{
    "topic": "goal-deadline-alerts",
    "schema": {
        "goal_id": "uuid",
        "user_id": "uuid",
        "goal_type": "string",
        "months_remaining": "integer",
        "action_required": "RISK_REDUCTION",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Deadline Monitor | `services/kafka/deadline_monitor.py` | `[x]` |
| Risk Reducer | `services/risk/risk_reducer.py` | `[x]` |

---

### 135.5 State-Specific 529 Glide-Path Validator `[x]`

**Acceptance Criteria**: Validate that custom glide paths created for 529 plans comply with state rules (some states restrict custom allocations to ensure tax benefits).

| Component | File Path | Status |
|-----------|-----------|--------|
| State Validator | `services/compliance/state_529_validator.py` | `[x]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py glide-path target <years>` | Calculate target alloc | `[x]` |
| `python cli.py glide-path shift` | Execute allocation shifts | `[x]` |

---

*Last verified: 2026-01-25*
