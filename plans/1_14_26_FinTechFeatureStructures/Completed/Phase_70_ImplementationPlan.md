# Phase 70: Risk Parity & 'All Weather' Allocation

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Strategy Team

---

## 📋 Overview

**Description**: Implement Ray Dalio's "All Weather" approach. Unlevered (or Levered) Risk Parity. Allocate risk equally, not capital. Because Bonds are less volatile than Stocks, you need MORE Bonds (or leverage) to balance the risk.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 70

---

## 🎯 Sub-Deliverables

### 70.1 Volatility-Weighted Allocation Logic `[x]`

**Acceptance Criteria**: Algorithm to equalize risk contribution.
`Weight_Asset = (1/Vol_Asset) / Sum(1/Vol_All)`.

```python
class RiskParity:
    def calculate_weights(self, assets):
        # Calculate inverse volatility
        # Normalize to 100%
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Parity Calc | `services/strategies/risk_parity.py` | `[x]` |

---

### 70.2 Correlation Adjustment `[x]`

**Acceptance Criteria**: Adjust for correlation. If stocks and bonds are highly correlated (Inflation regime), reduce total leverage.

| Component | File Path | Status |
|-----------|-----------|--------|
| Corr Adjust | `services/analysis/parity_corr.py` | `[x]` |

---

### 70.3 Regime-Based Portfolio Switching `[x]`

**Acceptance Criteria**: Switch between "Growth" mode (Equity Heavy) and "All Weather" mode (Risk Parity) based on VIX/Inflation signals.

| Component | File Path | Status |
|-----------|-----------|--------|
| Switcher | `services/strategies/regime_switch.py` | `[x]` |

---

### 70.4 Levered Bond Implementation (UPRO/TMF) `[x]`

**Acceptance Criteria**: Support Leveraged ETFs (UPRO, TMF) to achieve risk parity with smaller capital. Warning: Decay Risk.

| Component | File Path | Status |
|-----------|-----------|--------|
| Lev Manager | `services/risk/leveraged_etf.py` | `[x]` |

### 70.5 Backtest: All Weather vs 60/40 `[x]`

**Acceptance Criteria**: Continuous backtest showing how All Weather performs in 2008 and 2022 vs standard 60/40.

| Component | File Path | Status |
|-----------|-----------|--------|
| Comparator | `frontend2/src/components/Analysis/StratCompare.jsx` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py parity calc` | Get target weights | `[x]` |
| `python cli.py parity backtest` | Run comparison | `[x]` |

---

*Last verified: 2026-01-25*
