# Phase 89: Monte Carlo FIRE Simulator

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Wealth Planning Team

---

## 📋 Overview

**Description**: Specialized Monte Carlo for FIRE (Financial Independence, Retire Early). Accounts for "Sequence of Returns Risk" in the first 5 years of retirement.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 89

---

## 🎯 Sub-Deliverables

### 89.1 Sequence of Returns Risk Visualizer `[ ]`

**Acceptance Criteria**: Visualize the "Danger Zone" (first 5 years). Show failure rates if a 2008-style crash happens immediately after retiring.

| Component | File Path | Status |
|-----------|-----------|--------|
| Seq Risk Viz | `frontend2/src/components/Charts/SeqRisk.jsx` | `[ ]` |

---

### 89.2 Variable Spending Rules (Flex) `[ ]`

**Acceptance Criteria**: Sim with rules: "If market drops 20%, I cut spending by 10%". Shows how flexibility increases success rate to 100%.

| Component | File Path | Status |
|-----------|-----------|--------|
| Flex Rules | `services/simulation/flex_spending.py` | `[ ]` |

---

### 89.3 Health Care Cost Inflator `[ ]`

**Acceptance Criteria**: Model Healthcare inflation (higher than CPI) specifically for US users pre-Medicare.

| Component | File Path | Status |
|-----------|-----------|--------|
| Health Inf | `services/planning/health_cost.py` | `[ ]` |

---

### 89.4 Social Security Optimization `[ ]`

**Acceptance Criteria**: Optimize claiming strategy. "Delay until 70 gives an 8% guaranteed return increase/year."

| Component | File Path | Status |
|-----------|-----------|--------|
| SS Opt | `services/planning/ss_claim.py` | `[ ]` |

### 89.5 Legacy Goal Input `[ ]`

**Acceptance Criteria**: "Die With Zero" vs "Leave $5M". Adjust the success probability based on residual capital goal.

| Component | File Path | Status |
|-----------|-----------|--------|
| Legacy Param | `services/simulation/legacy_goal.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py fire run-sim` | Execute | `[ ]` |
| `python cli.py fire check-safety` | Safe to quit? | `[ ]` |

---

*Last verified: 2026-01-25*
