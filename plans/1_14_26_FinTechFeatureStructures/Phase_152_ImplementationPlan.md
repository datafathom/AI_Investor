# Phase 152: Probate Expense & Intestacy Simulator

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Estate Planning Team

---

## 📋 Overview

**Description**: Visualize the cost and delay of dying *without* a Trust (Probate). Calculate statutory fees (e.g., CA fees are % of gross assets) and distribution delays to motivate Trust funding.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 12

---

## 🎯 Sub-Deliverables

### 152.1 Probate Gate ($184k CA threshold) `[ ]`

**Acceptance Criteria**: Check if client assets exceed state-specific "Small Estate" thresholds. If >$184,500 (CA 2024), full probate is required.

| Component | File Path | Status |
|-----------|-----------|--------|
| Threshold Checker | `services/estate/probate_checker.py` | `[ ]` |
| State Limits Config | `config/probate_limits.py` | `[ ]` |

---

### 152.2 Court Cost / Attorney Fee Projector `[ ]`

**Acceptance Criteria**: Calculate estimated fees. In CA: 4% of first $100k, 3% of next $100k, 2% of next $800k, 1% of next $9M. Fees apply to *Gross* value (before mortgage debt).

```python
class ProbateFeeCalculator:
    """
    Calculate statutory probate fees (California Model).
    
    Basis: Gross Asset Value (Debt is IGNORED).
    """
    def calculate_fees(self, gross_assets: Decimal) -> FeeSchedule:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Calculator | `services/estate/probate_fee_calc.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Probate Cost Chart | `frontend2/src/components/Charts/ProbateCostChart.jsx` | `[ ]` |

---

### 152.3 12-24 Month Distribution Delay Model `[ ]`

**Acceptance Criteria**: Model the timeline delay. Assets are frozen during the 4-month creditor claim period + court backlog time.

| Component | File Path | Status |
|-----------|-----------|--------|
| Delay Simulator | `services/simulation/delay_sim.py` | `[ ]` |

---

### 152.4 Trust vs. Probate Transfer Comparison `[ ]`

**Acceptance Criteria**: Side-by-side comparison. Trust: Private, Instant, Low Cost. Probate: Public, 18 Months, High Cost.

| Component | File Path | Status |
|-----------|-----------|--------|
| Comparison Engine | `services/reporting/trust_vs_probate.py` | `[ ]` |

---

### 152.5 Intestate Succession Rules Mapper `[ ]`

**Acceptance Criteria**: Map "Who gets what" if you die without a will (Intestacy). E.g., Spouse gets 100% of Community Property but only 33% of Separate Property if kids exist.

| Component | File Path | Status |
|-----------|-----------|--------|
| Intestacy Logic | `services/legal/intestacy_logic.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py probate calc-fees <value>` | Estimate fees | `[ ]` |
| `python cli.py probate intestacy` | Show heuristic heirs | `[ ]` |

---

*Last verified: 2026-01-25*
