# Phase 78: Debt Shielding & Liability Optimization

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Wealth Planning Team

---

## 📋 Overview

**Description**: Manage the "Liability" side of the balance sheet. Optimize mortgage rates, consolidate high-interest debt, and use "Asset-Backed Lines of Credit" (SBLOC) to avoid selling stocks (and triggering taxes).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 78

---

## 🎯 Sub-Deliverables

### 78.1 SBLOC Feasibility Calculator `[x]`

**Acceptance Criteria**: Calculate borrowing power. "You can borrow $200k against your $400k portfolio at 6% interest." Compare vs Selling Stock (Cap Gains tax).

```python
class SBLUCCalculator:
    def compare_borrow_vs_sell(self, amount, portfolio_yield, borrow_rate, tax_rate):
        cost_borrow = amount * borrow_rate
        cost_sell = (amount / (1-tax_rate)) * tax_rate # Gross up + Lost Yield
        return "BORROW" if cost_borrow < cost_sell else "SELL"
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Calc Tool | `services/analysis/sbloc_calc.py` | `[x]` |

---

### 78.2 Debt Payoff Optimizer (Avalanche/Snowball) `[x]`

**Acceptance Criteria**: Logic to optimize debt payoff. Avalanche (Highest Interest First) = Math Optimal. Snowball (Smallest Balance First) = Psych Optimal. User chooses.

| Component | File Path | Status |
|-----------|-----------|--------|
| Optimizer | `services/planning/payoff_opt.py` | `[x]` |

---

### 78.3 Mortgage Refinance Alert `[x]`

**Acceptance Criteria**: Monitor 30Y fixed rates. If current_rate < my_rate - 0.75%, alert "Refinance Opportunity".

| Component | File Path | Status |
|-----------|-----------|--------|
| Refi Alert | `services/alerts/refi_alert.py` | `[x]` |

---

### 78.4 Liability Dashboard `[x]`

**Acceptance Criteria**: Visualize all debts. "Good Debt" (Mortgage < Inflation) vs "Bad Debt" (Credit Card > 15%).

| Component | File Path | Status |
|-----------|-----------|--------|
| Debt Dash | `frontend2/src/components/Dashboard/LiabilityDash.jsx` | `[x]` |

### 78.5 Margin Loan Risk Monitor `[x]`

**Acceptance Criteria**: If SBLOC/Margin usage > 30% of portfolio, flag "Margin Call Risk".

| Component | File Path | Status |
|-----------|-----------|--------|
| Margin Monitor | `services/risk/loan_monitor.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py liability compare <amount>` | Borrow vs Sell | `[x]` |
| `python cli.py liability list` | Show all debts | `[x]` |

---

*Last verified: 2026-01-25*
