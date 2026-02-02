# Phase 74: Philanthropy & Donor Advised Funds (DAF)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Wealth Planning Team

---

## 📋 Overview

**Description**: Manage giving. "Donor Advised Funds" allow you to donate stock (avoiding cap gains tax) and receive an immediate deduction, then grant money to charities over time.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 74

---

## 🎯 Sub-Deliverables

### 74.1 Stock Donation Optimizer `[x]`

**Acceptance Criteria**: Identify "Highest Appreciation" lots. Donating a stock up 1000% is better than donating cash, because you wipe out the embedded tax liability.

| Component | File Path | Status |
|-----------|-----------|--------|
| Optimizer | `services/tax/donation_opt.py` | `[x]` |

---

### 74.2 DAF Account Integration `[x]`

**Acceptance Criteria**: Track DAF balance. It's an asset, but "Restricted". It counts towards "Social Impact" but not "Liquid Net Worth".

| Component | File Path | Status |
|-----------|-----------|--------|
| DAF Tracker | `services/accounting/daf_data.py` | `[x]` |

---

### 74.3 Deduction Limit Monitor (AGI Caps) `[x]`

**Acceptance Criteria**: Track IRS limits. Cash donations capped at 60% AGI. Stock donations capped at 30% AGI. Carryforward excess.

| Component | File Path | Status |
|-----------|-----------|--------|
| AGI Monitor | `services/compliance/agi_limits.py` | `[x]` |

---

### 74.4 Impact Reporting Dashboard `[x]`

**Acceptance Criteria**: Visualize grants. "You donated $50k to Education this year."

| Component | File Path | Status |
|-----------|-----------|--------|
| Impact Dash | `frontend2/src/components/Reporting/Impact.jsx` | `[x]` |

### 74.5 Grant Scheduling System `[x]`

**Acceptance Criteria**: Schedule recurring grants to charities from the DAF.

| Component | File Path | Status |
|-----------|-----------|--------|
| Scheduler | `services/planning/grant_scheduler.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py give suggest` | Best asset to donate | `[x]` |
| `python cli.py give check-cap` | AGI room left | `[x]` |

---

*Last verified: 2026-01-25*
