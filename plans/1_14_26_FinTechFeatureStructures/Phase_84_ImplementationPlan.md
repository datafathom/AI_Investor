# Phase 84: Quantitative Factor Model (Smart Beta)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Implement Fama-French 5-Factor model (Market, Size, Value, Profitability, Investment). Assess portfolio exposure to these factors. "Are we just lucky or are we harvesting factor premia?"

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 84

---

## 🎯 Sub-Deliverables

### 84.1 Factor Regression Engine `[ ]`

**Acceptance Criteria**: Regress portfolio returns against Fama-French factors. Determine Factor Loadings (Betas).

```python
class FactorRegression:
    def regress(self, returns):
        # OLS regression against Mkt-RF, SMB, HML, RMW, CMA
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Regression | `services/analysis/factor_reg.py` | `[ ]` |

---

### 84.2 Real-time Factor Tilt Monitor `[ ]`

**Acceptance Criteria**: Visualize tilts. "You are heavily tilted towards Small Cap Value (SMB+, HML+)."

| Component | File Path | Status |
|-----------|-----------|--------|
| Tilt UI | `frontend2/src/components/Analysis/FactorTilt.jsx` | `[ ]` |

---

### 84.3 Smart Beta ETF Scanner `[ ]`

**Acceptance Criteria**: Scan for ETFs that provide specific factor exposure efficiently (e.g., AVUV for Small Cap Value).

| Component | File Path | Status |
|-----------|-----------|--------|
| ETF Scanner | `services/strategies/smart_beta.py` | `[ ]` |

---

### 84.4 Factor Decay Alert `[ ]`

**Acceptance Criteria**: Alert if a factor stops performing (e.g., Value has underperformed for 10 years). "Is the factor broken?"

| Component | File Path | Status |
|-----------|-----------|--------|
| Decay Monitor | `services/alerts/factor_decay.py` | `[ ]` |

### 84.5 Custom Factor Creation `[ ]`

**Acceptance Criteria**: Allow user to define custom factors (e.g., "AI Exposure").

| Component | File Path | Status |
|-----------|-----------|--------|
| Custom Fac | `services/analysis/custom_factors.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py factor regress` | Run analysis | `[ ]` |
| `python cli.py factor suggest` | Optimize tilt | `[ ]` |

---

*Last verified: 2026-01-25*
