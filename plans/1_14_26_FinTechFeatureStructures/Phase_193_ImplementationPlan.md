# Phase 193: ESG Sector Flow & Reflexivity Displacement

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Model the distortion caused by ESG (Environmental, Social, Governance) mandates. Trillions of dollars are forced to sell "Sin Stocks" (Oil, Tobacco, Defense) and buy "Green Stocks". This creates value opportunities in the sold-off sectors (high yield, low valuation) and bubbles in the bought sectors.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 13

---

## 🎯 Sub-Deliverables

### 193.1 ESG Flow Tracker (Inflow/Outflow) `[ ]`

**Acceptance Criteria**: Track fund flows specifically labeled "ESG". Correlate with P/E expansion in Tech (often high ESG) vs. P/E compression in Energy (low ESG).

| Component | File Path | Status |
|-----------|-----------|--------|
| Flow Tracker | `services/market/esg_flow.py` | `[ ]` |

---

### 193.2 "Sin Stock" Valuation Premium Analyzer `[ ]`

**Acceptance Criteria**: Identify the "Cost of Capital" advantage. If Oil companies trade at 5x PE due to ESG bans, their expected return is 20% (Earnings Yield). Identify these deep value pockets.

```python
class SinStockScanner:
    """
    Find artificially depressed assets due to ESG mandates.
    """
    def find_opportunities(self) -> list[Asset]:
        # Look for High FCF, Low PE, Low Institutional Ownership
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Opportunity Scanner | `services/strategies/sin_stock.py` | `[ ]` |

---

### 193.3 Postgres ESG Exclusion List Manager `[ ]`

**Acceptance Criteria**: Manage "Negative Screening" lists. Allow clients to customize their own morals (e.g., "Anti-ESG" pro-oil, or "Strict ESG" no-nuclear).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE exclusion_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    sector_code VARCHAR(20),           -- ENERGY, TOBACCO, WEAPONS
    strictness_level INTEGER,          -- 1 (Restrict Direct), 5 (Restrict ETFs)
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/193_exclusion_rules.sql` | `[ ]` |
| Screening Engine | `services/compliance/esg_screen.py` | `[ ]` |

---

### 193.4 Greenwashing Detector (Portfolio vs. Marketing) `[ ]`

**Acceptance Criteria**: NLP analysis of fund prospectuses vs. actual holdings. Flag funds that claim "Green" but hold major polluters.

| Component | File Path | Status |
|-----------|-----------|--------|
| Greenwash Detector | `services/analysis/greenwash_check.py` | `[ ]` |

---

### 193.5 Impact Reporting Service (CO2 Saved) `[ ]`

**Acceptance Criteria**: For pro-ESG clients, quantify impact. "Your portfolio offset 50 tons of Carbon".

| Component | File Path | Status |
|-----------|-----------|--------|
| Impact Calculator | `services/reporting/impact_calc.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Values Dashboard | `frontend2/src/components/ESG/Valuesboard.jsx` | `[ ]` |
| Impact Report | `frontend2/src/components/Reporting/ImpactScore.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py esg scan-sin` | Find undervalued sin | `[ ]` |
| `python cli.py esg check-greenwash` | Audit holdings | `[ ]` |

---

*Last verified: 2026-01-25*
