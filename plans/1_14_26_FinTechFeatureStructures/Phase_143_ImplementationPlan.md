# Phase 143: Tax Loss Harvesting Postgres Trigger & Offsetting

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax Team

---

## 📋 Overview

**Description**: Automate Tax Loss Harvesting (TLH). Monitor portfolio positions for unrealized losses, trigger harvesting when thresholds are met, and automatically select replacement securities to maintain market exposure while avoiding wash sales.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 3

---

## 🎯 Sub-Deliverables

### 143.1 Real-time Loser Position Trigger `[ ]`

**Acceptance Criteria**: Trigger an alert when a tax lot drops below a configurable threshold (e.g., -5% or -$5000), identifying it as a candidate for harvesting.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE tax_lots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    
    -- Cost Basis
    quantity DECIMAL(20, 6) NOT NULL,
    cost_basis_per_share DECIMAL(20, 4) NOT NULL,
    total_cost_basis DECIMAL(20, 2) GENERATED ALWAYS AS (quantity * cost_basis_per_share) STORED,
    purchase_date DATE NOT NULL,
    
    -- Current Status
    current_price DECIMAL(20, 4),
    unrealized_pl DECIMAL(20, 2),
    unrealized_pl_pct DECIMAL(8, 4),
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE harvesting_opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lot_id UUID REFERENCES tax_lots(id),
    
    -- Opportunity
    potential_loss DECIMAL(20, 2),
    status VARCHAR(20) DEFAULT 'OPEN',     -- OPEN, EXECUTED, IGNORED
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/143_tax_lots.sql` | `[ ]` |
| Lot Monitor | `services/tax/lot_monitor.py` | `[ ]` |
| Opportunity Generator | `services/tax/opportunity_gen.py` | `[ ]` |

---

### 143.2 Capital Loss ↔ Gain Matching (15% bracket) `[ ]`

**Acceptance Criteria**: Algorithm to match harvested losses against realized gains to minimize tax liability. Prioritize: 1. Short-term losses vs Short-term gains (highest tax), 2. Long-term vs Long-term, 3. Up to $3k against ordinary income.

| Component | File Path | Status |
|-----------|-----------|--------|
| Gain/Loss Matcher | `services/tax/gain_loss_matcher.py` | `[ ]` |
| Tax liability Calc | `services/tax/liability_calc.py` | `[ ]` |

---

### 143.3 Kafka Liquidity Needs Prioritization `[ ]`

**Acceptance Criteria**: Prioritize harvesting in accounts that have upcoming liquidity needs (withdrawals) to raise cash tax-efficiently.

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidity Consumer | `services/kafka/liquidity_consumer.py` | `[ ]` |
| Withdrawal Optimizer | `services/tax/withdrawal_optimizer.py` | `[ ]` |

---

### 143.4 30-Day Wash Sale Validator `[ ]`

**Acceptance Criteria**: Strictly prevent Wash Sales. Check if a "substantially identical" security was purchased 30 days before or after the loss sale.

```python
class WashSaleValidator:
    """
    Prevent Wash Sales (IRS Rule).
    
    Logic:
    - If selling Ticker X for loss:
    - Check buy transactions of X, options on X, or substantially identical ETFs
    - Window: 30 days before sale to 30 days after sale
    - If match found: Disallow loss deduction (add to basis of new holding)
    """
    
    def check_wash_sale(self, ticker: str, sale_date: Date) -> WashSaleResult:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Wash Sale Validator | `services/compliance/wash_sale_validator.py` | `[ ]` |
| Identical Security Map | `config/substantially_identical.json` | `[ ]` |

---

### 143.5 Net Tax Liability Calculator `[ ]`

**Acceptance Criteria**: Aggregate total tax liability across all accounts, factoring in harvested losses, carryforwards, and brackets.

| Component | File Path | Status |
|-----------|-----------|--------|
| Total Liability Calc | `services/tax/total_liability.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Harvesting Dashboard | `frontend2/src/components/Tax/HarvestingDashboard.jsx` | `[ ]` |
| Tax Savings Widget | `frontend2/src/components/Tax/TaxSavings.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax scan-losses` | Scan for harvesting opps | `[ ]` |
| `python cli.py tax wash-check <ticker>` | Check wash sale status | `[ ]` |

---

*Last verified: 2026-01-25*
