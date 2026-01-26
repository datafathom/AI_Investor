# Phase 191: Norway Wealth Tax 'Tax-on-Tax' Spiral Calculator

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax Team

---

## 📋 Overview

**Description**: Specialized module for Wealth Tax jurisdictions (Norway, Spain, Switzerland). Model the "Death Spiral" where a wealthy individual must sell illiquid assets to pay the Wealth Tax, incurring Capital Gains Tax on the sale, which requires selling *more* assets.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 11

---

## 🎯 Sub-Deliverables

### 191.1 Wealth Tax Liability Projector (1.1% on Net Wealth) `[ ]`

**Acceptance Criteria**: Calculate the annual bill based on "Net Wealth" (Assets - Liabilities). Include valuation discounts (e.g., 20% discount for Private Shares in Norway).

```python
class WealthTaxCalculator:
    def calculate_liability(self, assets: Portfolio, jurisdiction: str = 'NO') -> TaxBill:
        net_wealth = self.aggregator.get_net_wealth(assets)
        if jurisdiction == 'NO':
            rate = 0.011
            bill = net_wealth * rate
            return TaxBill(amount=bill, due_date="2025-06-01")
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Tax Calculator | `services/tax/wealth_tax_calc.py` | `[ ]` |

---

### 191.2 Liquidity Needs for Tax Payment `[ ]`

**Acceptance Criteria**: Determine if the portfolio generates enough cash yield (Dividends/Interest) to pay the tax. If Yield < Tax (e.g., Tech Founder with 0% yield stock), forced selling occurs.

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidity Gap Analysis | `services/analysis/liquidity_gap.py` | `[ ]` |

---

### 191.3 "Tax-on-Tax" Spiral Simulator `[ ]`

**Acceptance Criteria**: The spiral loop. To pay $1M wealth tax, you sell $1M stock. Selling $1M stock triggers $200k Cap Gains tax. Now you need $1.2M. Selling $1.2M triggers...

| Component | File Path | Status |
|-----------|-----------|--------|
| Spiral Simulator | `services/simulation/tax_spiral.py` | `[ ]` |

---

### 191.4 Relocation ROI Calculator (Move to Switzerland/Dubai) `[ ]`

**Acceptance Criteria**: ROI of moving. Compare "Stay and Pay" vs. "Cost of Moving". Switzerland has a "Lump Sum Tax" (Forfail) which caps liability, often cheaper than Norway's % tax for billionaires.

#### Postgres Schema

```sql
CREATE TABLE relocation_scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    current_country VARCHAR(3),
    target_country VARCHAR(3),
    
    -- Costs
    one_time_exit_tax DECIMAL(20, 2),
    moving_costs DECIMAL(20, 2),
    annual_savings DECIMAL(20, 2),
    
    -- Result
    breakeven_years DECIMAL(5, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/191_relocation.sql` | `[ ]` |
| ROI Calculator | `services/tax/relocation_roi.py` | `[ ]` |

---

### 191.5 Holding Company Shielding Logic `[ ]`

**Acceptance Criteria**: Check if assets can be shielded by holding them in a corporate entity (AS/AB) where wealth tax valuation rules might be favorable.

| Component | File Path | Status |
|-----------|-----------|--------|
| Structure Optimizer | `services/legal/holdco_shield.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Wealth Tax Dashboard | `frontend2/src/components/Tax/WealthTaxDash.jsx` | `[ ]` |
| Spiral Visualizer | `frontend2/src/components/Charts/SpiralChart.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax calc-wealth-tax` | Estimate liability | `[ ]` |
| `python cli.py tax sim-spiral` | Run spiral sim | `[ ]` |

---

*Last verified: 2026-01-25*
