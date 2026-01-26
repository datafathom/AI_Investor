# Phase 42: Traditional vs. Roth Tax Forecaster

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Wealth Planning Team

---

## 📋 Overview

**Description**: Visual 30-year forecaster for retirement tax liabilities. Compare "Pay Tax Now" (Roth) vs "Pay Tax Later" (Traditional). Crucial for optimizing "Net Spendable Income" in retirement.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 42

---

## 🎯 Sub-Deliverables

### 42.1 30-Year Compounding Simulator `[ ]`

**Acceptance Criteria**: Simulate 30-year wealth compounding. Model tax drag on Traditional withdrawals vs tax-free Roth withdrawals.

```python
class CompoundSim:
    def run_simulation(self, principal, annual_contrib, years, rate, tax_rate_now, tax_rate_future):
        # ... logic
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Simulator | `services/simulation/compound_wealth.py` | `[ ]` |

---

### 42.2 Tax Bracket Optimizer (Break-Even) `[ ]`

**Acceptance Criteria**: Suggest optimal split. If current bracket is 32% and projected is 15%, suggest Traditional. If equal, suggest Roth (lock in rate).

| Component | File Path | Status |
|-----------|-----------|--------|
| Bracket Opt | `services/planning/bracket_opt.py` | `[ ]` |

---

### 42.3 D3.js Spendable Income Chart `[ ]`

**Acceptance Criteria**: Display side-by-side D3.js area charts showing projected *spendable* income (after tax) in retirement for both scenarios.

| Component | File Path | Status |
|-----------|-----------|--------|
| Chart | `frontend2/src/components/Charts/TaxComp.jsx` | `[ ]` |

---

### 42.4 RMD (Required Minimum Distribution) Logic `[ ]`

**Acceptance Criteria**: Account for RMDs (starting age 73/75). Traditional IRAs *force* withdrawals, increasing taxable income. Roths do not.

| Component | File Path | Status |
|-----------|-----------|--------|
| RMD Calc | `services/planning/rmd_calc.py` | `[ ]` |

### 42.5 TimescaleDB Analysis Vault `[ ]`

**Acceptance Criteria**: Store all tax simulation parameters and results in TimescaleDB for historical comparison.

| Component | File Path | Status |
|-----------|-----------|--------|
| Vault Saver | `services/storage/sim_saver.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax forecast` | Run 30yr sim | `[ ]` |
| `python cli.py tax check-rmd <age>` | Calc required | `[ ]` |

---

*Last verified: 2026-01-25*
