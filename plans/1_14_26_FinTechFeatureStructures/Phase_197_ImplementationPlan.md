# Phase 197: Social Class Maintenance (SCM) Ultimate KPI

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Core Strategy Team

---

## 📋 Overview

**Description**: The ultimate metric for UHNW clients. "Return on Lifestyle" (ROL).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 17

---

## 🎯 Sub-Deliverables

### 197.1 "Cost of Living Extremely Well" (CLEW) Index `[x]`

**Acceptance Criteria**: Create a custom inflation index.

| Component | File Path | Status |
|-----------|-----------|--------|
| Index Calculator | `services/economics/clew_index_svc.py` | `[x]` |

---

### 197.2 Lifestyle Burn Rate Projector `[x]`

**Acceptance Criteria**: Project current burn rate forward 30 years.

| Component | File Path | Status |
|-----------|-----------|--------|
| Burn Projector | `services/planning/lifestyle_burn_svc.py` | `[x]` |

---

### 197.3 "Drop in Class" Probability Simulator (Monte Carlo) `[x]`

**Acceptance Criteria**: Risk of ruin.

| Component | File Path | Status |
|-----------|-----------|--------|
| Class Risk Sim | `services/simulation/class_risk_sim.py` | `[x]` |

---

### 197.4 Sustainable Withdrawal Rate (SWR) for UHNW `[x]`

**Acceptance Criteria**: Adjust the "4% Rule" for UHNW.

| Component | File Path | Status |
|-----------|-----------|--------|
| SWR Adjuster | `services/planning/swr_adjuster.py` | `[x]` |

---

### 197.5 Inter-Generational Dilution Tracker `[x]`

**Acceptance Criteria**: Model the dilution of wealth.

| Component | File Path | Status |
|-----------|-----------|--------|
| Dilution Tracker | `services/estate/dilution_tracker.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py sfc calc-clew` | Show lifestyle inflation | `[x]` |
| `python cli.py sfc check-dilution` | Project per-capita wealth | `[x]` |

---

*Last verified: 2026-01-30*


---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py sfc calc-clew` | Show lifestyle inflation | `[ ]` |
| `python cli.py sfc check-dilution` | Project per-capita wealth | `[ ]` |

---

*Last verified: 2026-01-25*
