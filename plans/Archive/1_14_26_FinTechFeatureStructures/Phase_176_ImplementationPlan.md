# Phase 176: LBO Cost-Cutting & EBITDA Growth Simulator

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Private Equity Team

---

## 📋 Overview

**Description**: Advanced LBO modeling. Simulate the operational "Value Creation" plan. How much value comes from cutting headcount? Optimizing supply chain? Raising prices? This models the "Operator" side of PE.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 16

---

## 🎯 Sub-Deliverables

### 176.1 Headcount Reduction & Efficiency Model `[ ]`

**Acceptance Criteria**: Simulator for OpEx reduction. Input: Current SG&A. Action: "Reduce Back Office 20%". Output: Increased EBITDA.

```python
class EfficiencySimulator:
    """
    Simulate operational improvements.
    """
    def simulate_opex_cut(
        self,
        income_stmt: IncomeStatement,
        cut_pct: Decimal,
        department: str
    ) -> ImpactResult:
        savings = income_stmt.get_expense(department) * cut_pct
        new_ebitda = income_stmt.ebitda + savings
        return ImpactResult(savings=savings, new_ebitda=new_ebitda)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Efficiency Engine | `services/pe/efficiency_sim.py` | `[ ]` |

---

### 176.2 Supply Chain Optimization Calculator `[ ]`

**Acceptance Criteria**: Calculate working capital improvements. Extend payables (DPO), collect receivables faster (DSO), reduce inventory (DIO).

| Component | File Path | Status |
|-----------|-----------|--------|
| Working Capital Calc | `services/pe/working_capital.py` | `[ ]` |

---

### 176.3 Pricing Power & Margin Expansion Tool `[ ]`

**Acceptance Criteria**: Model the elasticity of demand. If we raise prices 5%, how much volume do we lose? Net impact on Gross Margin?

| Component | File Path | Status |
|-----------|-----------|--------|
| Pricing Model | `services/analysis/pricing_power.py` | `[ ]` |

---

### 176.4 Add-On Acquisition Synergy Estimator `[ ]`

**Acceptance Criteria**: Estimate synergies from "Buy and Build". Revenue Synergies (Cross-sell) and Cost Synergies (Duplicate HQ).

| Component | File Path | Status |
|-----------|-----------|--------|
| Synergy Estimator | `services/pe/synergy_est.py` | `[ ]` |

---

### 176.5 Sensitivity Analysis (Base, Bull, Bear) `[ ]`

**Acceptance Criteria**: Run Monte Carlo simulations on the business plan. What if recession hits? What if growth is 2x expected?

| Component | File Path | Status |
|-----------|-----------|--------|
| Sensitivity Engine | `services/simulation/sensitivity_analysis.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Value Creation Bridge | `frontend2/src/components/PE/ValueBridge.jsx` | `[ ]` |
| Sensitivity Table | `frontend2/src/components/PE/SensitivityTable.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py pe sim-cuts` | Run efficiency sim | `[ ]` |
| `python cli.py pe sensitize` | Run sensitivity analysis | `[ ]` |

---

*Last verified: 2026-01-25*
