# Phase 186: 10b5-1 Preset Selling Plan Framework

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Compliance Team

---

## 📋 Overview

**Description**: Automate SEC Rule 10b5-1 Plans. This "Safe Harbor" allows corporate insiders to sell stock without accusations of Insider Trading, provided the trades are pre-scheduled (e.g., "Sell 10,000 shares on the 1st of every month") and the plan is entered into when they have *no* material non-public information (MNPI).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 6

---

## 🎯 Sub-Deliverables

### 186.1 10b5-1 Non-Discretionary Execution Service `[ ]`

**Acceptance Criteria**: Execution engine that fires trade orders automatically based on the pre-set schedule. Crucially, the user *cannot* intervene to stop or change a trade once the plan is active (Non-Discretionary).

#### Backend Implementation

```python
class PlanExecutor:
    """
    Execute 10b5-1 trades blindly.
    """
    def execute_scheduled_trades(self, date: Date) -> ExecutionReport:
        trades = self.db.get_trades_for_date(date)
        for trade in trades:
            if trade.plan_agreed_period_active:
                self.broker.submit_order(trade) # NO USER CONFIRMATION ALLOWED
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Plan Executor | `services/compliance/plan_executor.py` | `[ ]` |
| Schedule Engine | `services/trading/schedule_engine.py` | `[ ]` |

---

### 186.2 Fiduciary Execution Layer (No Timing) `[ ]`

**Acceptance Criteria**: Verify that execution is "Best Execution" (VWAP/TWAP) and not "Timed" to benefit the insider.

| Component | File Path | Status |
|-----------|-----------|--------|
| VWAP Algo | `services/trading/vwap_algo.py` | `[ ]` |

---

### 186.3 Postgres Non-Timing Justification Record `[ ]`

**Acceptance Criteria**: Immutable log proving the trade plan was created during an "Open Window" (after earnings, before blackout).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE trading_plans_10b51 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    insider_id UUID NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    
    -- Creation
    creation_date DATE NOT NULL,
    cooling_off_days INTEGER DEFAULT 90, -- New SEC Rule (Feb 2023)
    first_trade_date DATE GENERATED ALWAYS AS (creation_date + cooling_off_days) STORED,
    
    -- Status
    status VARCHAR(20),                -- ACTIVE, TERMINATED, COMPLETED
    termination_date DATE,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    is_immutable BOOLEAN DEFAULT TRUE
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/186_trading_plans.sql` | `[ ]` |
| Plan Manager | `services/compliance/plan_manager.py` | `[ ]` |

---

### 186.4 Neo4j Executive ↔ Pre-Scripted Plan Relationship `[ ]`

**Acceptance Criteria**: Graph visibility. Executives can see *that* a plan exists, but the UI must block "Edit" buttons during active periods.

```cypher
(:EXECUTIVE)-[:ESTABLISHED_PLAN {
    date: date("2024-01-01"),
    broker: "Morgan Stanley"
}]->(:PLAN_10B51)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Plan Graph | `services/neo4j/plan_graph.py` | `[ ]` |

---

### 186.5 Revision Limit Gate (Prevent Changes with Knowledge) `[ ]`

**Acceptance Criteria**: Strict logic to prevent "Modifying a Plan" continuously. New SEC rules limit single-trade plans to 1 per year to prevent gaming the system.

| Component | File Path | Status |
|-----------|-----------|--------|
| Revision Gate | `services/compliance/revision_gate.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Plan Setup Wizard | `frontend2/src/components/Compliance/PlanWizard.jsx` | `[ ]` |
| Read-Only Schedule | `frontend2/src/components/Calendar/PlanSchedule.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py 10b51 create` | Draft new plan | `[ ]` |
| `python cli.py 10b51 execute-daily` | Run daily batch | `[ ]` |

---

*Last verified: 2026-01-25*
