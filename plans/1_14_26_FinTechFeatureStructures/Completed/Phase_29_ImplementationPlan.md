# Phase 29: TimescaleDB Portfolio Drawdown History

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Performance & Reporting Team

---

## 📋 Overview

**Description**: Maintain high-resolution records of account drawdown for historical risk modeling and agent feedback loops. Instead of just "P&L", we track the *path* of the equity curve to detect volatility.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 29

---

## 🎯 Sub-Deliverables

### 29.1 High-Resolution Equity Hypertable `[x]`

**Acceptance Criteria**: Record account equity every 60 seconds into a TimescaleDB hypertable.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE equity_curve_1m (
    timestamp TIMESTAMPTZ NOT NULL,
    account_id UUID NOT NULL,
    equity DECIMAL(20, 2),
    balance DECIMAL(20, 2),
    open_pnl DECIMAL(20, 2)
);

SELECT create_hypertable('equity_curve_1m', 'timestamp');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/29_equity_curve.sql` | `[x]` |
| Recorder | `services/performance/equity_recorder.py` | `[x]` |

---

### 29.2 Rolling Drawdown Calculator (SQL) `[x]`

**Acceptance Criteria**: Calculate rolling Maximum Drawdown (MDD) across 1-day, 7-day, and 30-day windows via optimized SQL queries (using TimescaleDB window functions).

```sql
SELECT
    timestamp,
    equity,
    MAX(equity) OVER (ORDER BY timestamp ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as peak,
    (equity - MAX(equity) OVER (...)) / MAX(equity) OVER (...) as drawdown
FROM equity_curve_1m;
```

| Component | File Path | Status |
|-----------|-----------|--------|
| SQL Queries | `services/performance/drawdown_queries.sql` | `[x]` |

---

### 29.3 Risk Adjustment Feedback Loop `[x]`

**Acceptance Criteria**: Ensure drawdown data is used to dynamically adjust the system's Max Risk % for the following session. (High drawdown -> Reduce Risk).

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Adjuster | `services/risk/feedback_loop.py` | `[x]` |

---

### 29.4 D3.js 'Underwater' Chart `[x]`

**Acceptance Criteria**: Frontend visualization showing the "Underwater" depth (distance from High Water Mark) at 60 FPS using D3.js.

| Component | File Path | Status |
|-----------|-----------|--------|
| Chart | `frontend2/src/components/Charts/Underwater.jsx` | `[x]` |

---

### 29.5 Drawdown Acceleration Alert `[x]`

**Acceptance Criteria**: Trigger automated Kafka alerts to the ProtectorAgent if drawdown *velocity* accelerates (e.g., losing 1% in 5 minutes).

| Component | File Path | Status |
|-----------|-----------|--------|
| Acceleration Monitor | `services/alerts/dd_velocity.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py perf get-mdd` | Show max drawdown | `[x]` |
| `python cli.py perf underwater` | Show current depth | `[x]` |

---

*Last verified: 2026-01-25*
