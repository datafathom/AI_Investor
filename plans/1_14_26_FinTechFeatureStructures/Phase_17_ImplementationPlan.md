# Phase 17: TimescaleDB Balance & Equity Tracker

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Database Team

---

## 📋 Overview

**Description**: Develop the real-time balance and equity tracking service with sub-second state hydration for the portfolio dashboard.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 17.1 Postgres Equity Triggers `[ ]`

**Acceptance Criteria**: Implement Postgres triggers that update equity values on every price tick received from the `fx-stream-global` topic.

| Component | File Path | Status |
|-----------|-----------|--------|
| Equity Trigger | `migrations/017_equity_triggers.sql` | `[ ]` |
| Trigger Handler | `services/portfolio/equity_trigger_handler.py` | `[ ]` |

---

### 17.2 Portfolio Store Hydration `[ ]`

**Acceptance Criteria**: Configure the `usePortfolioStore` to reflect balance changes across the GUI within 50ms of a trade event.

| Component | File Path | Status |
|-----------|-----------|--------|
| Portfolio Store | `frontend2/src/stores/portfolioStore.js` | `[ ]` |
| WebSocket Handler | `frontend2/src/services/portfolioSocket.js` | `[ ]` |

---

### 17.3 Unrealized P&L Aggregation `[ ]`

**Acceptance Criteria**: Ensure the tracker accounts for unrealized P&L by aggregating all open position valuations in real-time.

| Component | File Path | Status |
|-----------|-----------|--------|
| PnL Aggregator | `services/portfolio/pnl_aggregator.py` | `[ ]` |
| Position Valuator | `services/portfolio/position_valuator.py` | `[ ]` |

---

### 17.4 Historical Equity Curves `[ ]`

**Acceptance Criteria**: Log historical equity curves to a TimescaleDB hypertable for rolling drawdown and recovery analysis.

| Component | File Path | Status |
|-----------|-----------|--------|
| Equity Curve Logger | `services/portfolio/equity_curve_logger.py` | `[ ]` |
| Migration | `migrations/017_equity_curves.sql` | `[ ]` |

---

### 17.5 Brokerage Consistency Check `[ ]`

**Acceptance Criteria**: Verify data consistency between the brokerage API and the internal ledger every 30 seconds.

| Component | File Path | Status |
|-----------|-----------|--------|
| Consistency Checker | `services/reconciliation/consistency_checker.py` | `[ ]` |
| Alert Service | `services/alerts/reconciliation_alert.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 17.1 Equity Triggers | `[ ]` | `[ ]` |
| 17.2 Store Hydration | `[ ]` | `[ ]` |
| 17.3 Unrealized P&L | `[ ]` | `[ ]` |
| 17.4 Equity Curves | `[ ]` | `[ ]` |
| 17.5 Consistency Check | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

*Last verified: 2026-01-25*
