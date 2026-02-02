# Phase 152: Probate Expense & Intestacy Simulator

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Estate Planning Team

---

## 📋 Overview

**Description**: Visualize the cost and delay of dying *without* a Trust (Probate). Calculate statutory fees (e.g., CA fees are % of gross assets) and distribution delays to motivate Trust funding.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 12

---

## 🎯 Sub-Deliverables

### 152.1 Probate Gate ($184k CA threshold) `[x]`

**Acceptance Criteria**: Check if client assets exceed state-specific "Small Estate" thresholds.

**Implementation**: `ProbateChecker` class with state thresholds:
- CA: $184,500 | NV: $25,000 | NY: $50,000 | FL: $75,000 | TX: $75,000
- Returns FULL PROBATE or SMALL ESTATE AFFIDAVIT procedure

| Component | File Path | Status |
|-----------|-----------|--------|
| Threshold Checker | `services/estate/probate_checker.py` | `[x]` |
| State Limits Config | (Embedded in checker) | `[x]` |

---

### 152.2 Court Cost / Attorney Fee Projector `[x]`

**Acceptance Criteria**: Calculate estimated statutory fees (CA model).

**Implementation**: `ProbateFeeCalculator` class:
- Tiered calculation: 4% of first $100k, 3% next $100k, 2% next $800k, 1% next $9M
- Returns attorney + executor fees (double the statutory fee)
- Includes estimated court costs

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Calculator | `services/estate/probate_fee_calc.py` | `[x]` |

---

### 152.3 12-24 Month Distribution Delay Model `[x]`

**Acceptance Criteria**: Model the timeline delay for probate distributions.

| Component | File Path | Status |
|-----------|-----------|--------|
| Delay Simulator | `services/simulation/delay_sim.py` | `[x]` |

---

### 152.4 Trust vs. Probate Transfer Comparison `[x]`

**Acceptance Criteria**: Side-by-side comparison engine.

| Component | File Path | Status |
|-----------|-----------|--------|
| Comparison Engine | `services/reporting/trust_vs_probate.py` | `[x]` |

---

### 152.5 Intestate Succession Rules Mapper `[x]`

**Acceptance Criteria**: Map "Who gets what" under intestacy rules.

**Implementation**: `IntestacyLogic` class with CA heuristic:
- Community property: 100% to spouse (or children if no spouse)
- Separate property: Split based on children count and surviving parents
- Includes risk warning about unintended heirs

| Component | File Path | Status |
|-----------|-----------|--------|
| Intestacy Logic | `services/legal/intestacy_logic.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py probate calc-fees <value>` | Estimate fees | `[x]` |
| `python cli.py probate intestacy` | Show heuristic heirs | `[x]` |

---

*Last verified: 2026-01-30*

