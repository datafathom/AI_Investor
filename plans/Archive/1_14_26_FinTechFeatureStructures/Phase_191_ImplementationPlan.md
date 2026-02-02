# Phase 191: Norway Wealth Tax 'Tax-on-Tax' Spiral Calculator

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Tax Team

---

## 📋 Overview

**Description**: Specialized module for Wealth Tax jurisdictions (Norway, Spain, Switzerland).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 11

---

## 🎯 Sub-Deliverables

### 191.1 Wealth Tax Liability Projector (1.1% on Net Wealth) `[x]`

**Acceptance Criteria**: Calculate the annual bill based on "Net Wealth".

| Component | File Path | Status |
|-----------|-----------|--------|
| Tax Calculator | `services/tax/wealth_tax_engine.py` | `[x]` |

---

### 191.2 Liquidity Needs for Tax Payment `[x]`

**Acceptance Criteria**: Determine if the portfolio generates enough cash yield.

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidity Gap Analysis | `services/analysis/liquidity_gap.py` | `[x]` |

---

### 191.3 "Tax-on-Tax" Spiral Simulator `[x]`

**Acceptance Criteria**: The spiral loop.

| Component | File Path | Status |
|-----------|-----------|--------|
| Spiral Simulator | `services/simulation/tax_spiral.py` | `[x]` |

---

### 191.4 Relocation ROI Calculator (Move to Switzerland/Dubai) `[x]`

**Acceptance Criteria**: ROI of moving.

| Component | File Path | Status |
|-----------|-----------|--------|
| ROI Calculator | `services/tax/relocation_roi.py` | `[x]` |

---

### 191.5 Holding Company Shielding Logic `[x]`

**Acceptance Criteria**: Check if assets can be shielded by holding them in a corporate entity.

| Component | File Path | Status |
|-----------|-----------|--------|
| Structure Optimizer | `services/legal/holdco_shield.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax calc-wealth-tax` | Estimate liability | `[x]` |
| `python cli.py tax sim-spiral` | Run spiral sim | `[x]` |

---

*Last verified: 2026-01-30*


---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax calc-wealth-tax` | Estimate liability | `[ ]` |
| `python cli.py tax sim-spiral` | Run spiral sim | `[ ]` |

---

*Last verified: 2026-01-25*
