# Phase 67: Restricted Stock & Founder Liquidity Planning (10b5-1)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Legal & Wealth Team

---

## 📋 Overview

**Description**: Manage Restricted Stock Units (RSUs) and Founder Stock. These are illiquid assets until they vest. We need to track Vesting Schedules and plan 10b5-1 automated selling plans for diversification.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 67

---

## 🎯 Sub-Deliverables

### 67.1 Vesting Schedule Tracker `[ ]`

**Acceptance Criteria**: Dashboard showing "Upcoming Vesting Events". (e.g., 5000 shares unlock on Nov 15). Integrate effectively into Net Worth projections.

| Component | File Path | Status |
|-----------|-----------|--------|
| Vest Tracker | `services/planning/vesting_schedule.py` | `[ ]` |

---

### 67.2 Concentration Risk Projector `[ ]`

**Acceptance Criteria**: Project future concentration. "If you keep all vested RSUs, in 4 years, 80% of your net worth will be in one stock."

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Projector | `services/risk/rsu_concentration.py` | `[ ]` |

---

### 67.3 10b5-1 Plan Generator `[ ]`

**Acceptance Criteria**: Generate a legally compliant 10b5-1 trading plan template. "Sell 10% of vested shares on the 1st of each month to diversify."

| Component | File Path | Status |
|-----------|-----------|--------|
| Plan Gen | `services/legal/plan_generator.py` | `[ ]` |

---

### 67.4 Tax Withholding Optimizer (Sell-to-Cover) `[ ]`

**Acceptance Criteria**: Calculate the optimal withholding method. "Sell-to-Cover" (Sell enough shares to pay tax) vs "Cash Transfer".

| Component | File Path | Status |
|-----------|-----------|--------|
| Tax Opt | `services/tax/rsu_tax.py` | `[ ]` |

### 67.5 'Golden Handcuff' visualizer `[ ]`

**Acceptance Criteria**: Visualize "Unvested Value" as a Golden Handcuff metric. "You walk away from $2M if you quit today."

| Component | File Path | Status |
|-----------|-----------|--------|
| Handcuff Viz | `frontend2/src/components/Dashboard/UnvestedValue.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py rsu add-grant` | Input grant details | `[ ]` |
| `python cli.py rsu simulate-exit` | Check 10b5-1 | `[ ]` |

---

*Last verified: 2026-01-25*
