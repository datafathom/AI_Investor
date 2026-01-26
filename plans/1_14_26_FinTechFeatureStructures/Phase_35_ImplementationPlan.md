# Phase 35: Portfolio Equilibrium Monitor

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Architecture Team

---

## 📋 Overview

**Description**: Maintain the disciplined balance between aggressive alpha-seeking and defensive capital shielding. The "Equilibrium Monitor" ensures the system doesn't accidentally become 100% Risk On or 100% Risk Off without cause.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 35

---

## 🎯 Sub-Deliverables

### 35.1 Real-Time 'Equilibrium Gauge' Widget `[ ]`

**Acceptance Criteria**: Visualization. Left = "Shielding" (Cash/Bonds). Right = "Hunting" (Crypto/FX). Center = Equilibrium.

| Component | File Path | Status |
|-----------|-----------|--------|
| Gauge Widget | `frontend2/src/components/Dashboard/EquilibriumGauge.jsx` | `[ ]` |

---

### 35.2 Volatility-Based Searcher Throttling `[ ]`

**Acceptance Criteria**: Verify that the system automatically reduces SearcherAgent activity when VIX volatility exceeds 25. (Throttle trade frequency).

| Component | File Path | Status |
|-----------|-----------|--------|
| Throttler | `services/agents/searcher/throttler.py` | `[ ]` |

---

### 35.3 Maximum Alpha Allocation Cap (50%) `[ ]`

**Acceptance Criteria**: Ensure that total alpha-seeking capital never exceeds the 50% allocation of total liquid equity. The other 50% must be Moat/Passive.

| Component | File Path | Status |
|-----------|-----------|--------|
| Allocation Guard | `services/risk/allocation_guard.py` | `[ ]` |

---

### 35.4 Neo4j 'Equilibrium Shift' Events `[ ]`

**Acceptance Criteria**: Map 'Equilibrium Shifts' to the Neo4j graph. Correlate shifts with macro events (e.g., "Fed Meeting" -> "Shift to Shielding").

```cypher
(:MACRO_EVENT {name: "FOMC Rate Hike"})-[:CAUSED_SHIFT]->(:SYSTEM_STATE {mode: "DEFENSIVE"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Shift Logger | `services/neo4j/shift_logger.py` | `[ ]` |

---

### 35.5 'System Harmony' Status Check `[ ]`

**Acceptance Criteria**: Trigger a 'System Harmony' status (Green Light) only if R-Multiple expectancy and drawdown are within set parameters.

| Component | File Path | Status |
|-----------|-----------|--------|
| Harmony Check | `services/monitoring/harmony_check.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py equil status` | Show balance | `[ ]` |
| `python cli.py equil force-rebalance` | Trigger shift | `[ ]` |

---

*Last verified: 2026-01-25*
