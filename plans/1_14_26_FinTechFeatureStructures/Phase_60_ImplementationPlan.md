# Phase 60: Scenario Modeling & 'What-If' Impact Simulator

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: Stress-test the Yellowstone equilibrium by simulating extreme macro shocks and black swan events. "What if Oil hits $150?" "What if the Fed hikes to 8%?"

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 60

---

## 🎯 Sub-Deliverables

### 60.1 Macro Shock Propagator `[ ]`

**Acceptance Criteria**: Implement Drag-and-Drop Macro Event Triggers (e.g., 'Oil to $150'). Use Neo4j correlations to propagate the shock. Oil Up -> Transportation Stocks Down -> Inflation Up -> Bonds Down.

| Component | File Path | Status |
|-----------|-----------|--------|
| Propagator | `services/simulation/shock_propagator.py` | `[ ]` |

---

### 60.2 Portfolio Revaluation Forecast `[ ]`

**Acceptance Criteria**: Develop a Portfolio Revaluation Forecast Chart showing expected shock trajectory and recovery paths.

| Component | File Path | Status |
|-----------|-----------|--------|
| Forecast Chart | `frontend2/src/components/Charts/ShockForecast.jsx` | `[ ]` |

---

### 60.3 Liquidity 'Bank Run' Simulator `[ ]`

**Acceptance Criteria**: Deploy a Liquidity Stress Test. If everyone sells at once, calculate slippage and bid-ask spread widening. Can we exit?

| Component | File Path | Status |
|-----------|-----------|--------|
| Run Sim | `services/simulation/liquidity_crisis.py` | `[ ]` |

---

### 60.4 Time-to-Breakeven Estimator `[ ]`

**Acceptance Criteria**: Calculate 'Time-to-Break-even' based on current hedges and historical recovery averages. "It will take 18 months to recover from this crash."

| Component | File Path | Status |
|-----------|-----------|--------|
| Breakeven Calc | `services/analysis/recovery_time.py` | `[ ]` |

### 60.5 Scenario Saver (Preset Library) `[ ]`

**Acceptance Criteria**: Allow users to save custom scenarios ("My Zombie Apocalypse") and re-run them against the portfolio weekly.

| Component | File Path | Status |
|-----------|-----------|--------|
| Scenario Library | `services/storage/scenarios.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py sim run-shock --oil=150` | Execute shock | `[ ]` |
| `python cli.py sim list-presets` | Show scenarios | `[ ]` |

---

*Last verified: 2026-01-25*
