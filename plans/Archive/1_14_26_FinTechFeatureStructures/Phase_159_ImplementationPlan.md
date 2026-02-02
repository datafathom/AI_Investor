# Phase 159: Performance-Based Fee Carry & Hurdle Engine

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Billing & Accounting Team

---

## 📋 Overview

**Description**: Institutional billing for Alternative Investments: "2 and 20", Hurdle Rates, and High Water Marks.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 19

---

## 🎯 Sub-Deliverables

### 159.1 20% Carry Calculator (Above Hurdle) `[x]`

**Acceptance Criteria**: Calculate Carried Interest accurately.

| Component | File Path | Status |
|-----------|-----------|--------|
| Carry Calculator | `services/billing/carry_calculator.py` | `[x]` |

---

### 159.2 Postgres 2% Management Fee Table `[x]`

**Acceptance Criteria**: Track base management fee accruals.

| Component | File Path | Status |
|-----------|-----------|--------|
| Daily Accrual Svc | `services/billing/fee_service.py` | `[x]` |

---

### 159.3 High Water Mark Logic Service `[x]`

**Acceptance Criteria**: No performance fees during drawdown recovery.

| Component | File Path | Status |
|-----------|-----------|--------|
| HWM Tracker | `services/billing/carry_calculator.py` | `[x]` (Integrated) |

---

### 159.4 Neo4j Accredited Investor Verification Node `[x]`

**Acceptance Criteria**: Verify Accredited Investor / Qualified Client status.

| Component | File Path | Status |
|-----------|-----------|--------|
| Accreditation Service | `services/neo4j/accreditation.py` | `[x]` |

---

### 159.5 Incentive Alignment Aggression Flag `[x]`

**Acceptance Criteria**: Monitor for excessive risk-taking near billing periods.

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Taking Monitor | `services/risk/risk_monitor.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py billing calc-carry` | Estimate performance fee | `[x]` |
| `python cli.py billing check-hwm` | Show distance to HWM | `[x]` |

---

*Last verified: 2026-01-30*

