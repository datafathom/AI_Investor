# Phase 197: Social Class Maintenance (SCM) Ultimate KPI

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Strategy Team

---

## 📋 Overview

**Description**: The ultimate metric for UHNW clients. Not "Return on Investment" (ROI), but "Return on Lifestyle" (ROL). Did the portfolio growth exceed the "Personal Inflation Rate" (Private School, Country Clubs, Staff) required to maintain the family's social standing?

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 17

---

## 🎯 Sub-Deliverables

### 197.1 "Cost of Living Extremely Well" (CLEW) Index `[ ]`

**Acceptance Criteria**: Create a custom inflation index. Basket includes: Ivy League Tuition, Concierge Doctors, Luxury Travel, High-End Real Estate. Track this (usually 2x-3x CPI) vs. Portfolio Return.

```python
class CLEWIndex:
    """
    Calculate UHNW inflation.
    """
    def calculate_inflation(self, basket: dict) -> Decimal:
        # Tuition +7%, Travel +12%, Staff +5%
        return weighted_average(basket)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Index Calculator | `services/economics/clew_index.py` | `[ ]` |

---

### 197.2 Lifestyle Burn Rate Projector `[ ]`

**Acceptance Criteria**: Project current burn rate forward 30 years using the CLEW index. $1M annual spend today = $4M spend in 30 years.

| Component | File Path | Status |
|-----------|-----------|--------|
| Burn Projector | `services/planning/burn_projector.py` | `[ ]` |

---

### 197.3 "Drop in Class" Probability Simulator (Monte Carlo) `[ ]`

**Acceptance Criteria**: Probability that the portfolio runs out of money *relative to lifestyle*. "There is a 5% chance you will have to fly commercial."

| Component | File Path | Status |
|-----------|-----------|--------|
| Class Risk Sim | `services/simulation/class_risk.py` | `[ ]` |

---

### 197.4 Sustainable Withdrawal Rate (SWR) for UHNW `[ ]`

**Acceptance Criteria**: Adjust the "4% Rule" for UHNW. Due to higher personal inflation and longer lifespans, SWR might be 2.5% or 3%.

| Component | File Path | Status |
|-----------|-----------|--------|
| SWR Adjuster | `services/planning/swr_adjuster.py` | `[ ]` |

---

### 197.5 Inter-Generational Dilution Tracker `[ ]`

**Acceptance Criteria**: Model the dilution of wealth as the family tree expands. 1 Founder ($100M) -> 3 Kids -> 9 Grandkids. "shirt sleeves to shirt sleeves in three generations".

| Component | File Path | Status |
|-----------|-----------|--------|
| Dilution Tracker | `services/estate/dilution_tracker.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| KPI Dashboard | `frontend2/src/components/Reporting/SCMScore.jsx` | `[ ]` |
| Inflation Toggle | `frontend2/src/components/Settings/InflationBasket.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py sfc calc-clew` | Show lifestyle inflation | `[ ]` |
| `python cli.py sfc check-dilution` | Project per-capita wealth | `[ ]` |

---

*Last verified: 2026-01-25*
