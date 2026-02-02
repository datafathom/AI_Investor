# Phase 114: Fee Structure & Prorated Billing Engine

> **Status**: `[x]` Completed | **Owner**: Billing Team
> **Source**: JIRA_PLANNING_JSON_2.txt - Phase 14

## 📋 Overview
**Description**: Build comprehensive fee calculation and billing infrastructure including tiered AUM fees, performance-based fees with high water marks, and prorated billing for partial periods.

---

## 🎯 Sub-Deliverables

### 114.1 Postgres Monthly/Quarterly Proration Service `[x]`

#### Database Schema (Docker-compose: timescaledb)
```sql
CREATE TABLE fee_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    advisor_id UUID NOT NULL,
    
    -- Fee Structure
    fee_type VARCHAR(20) NOT NULL,          -- AUM, FLAT, HOURLY, PERFORMANCE
    base_fee_pct DECIMAL(8, 6),             -- e.g., 0.01 = 1%
    
    -- Tiered Fees
    tier_1_max DECIMAL(20, 2),              -- First $1M
    tier_1_rate DECIMAL(8, 6),              -- 1.0%
    tier_2_max DECIMAL(20, 2),              -- $1M - $5M
    tier_2_rate DECIMAL(8, 6),              -- 0.75%
    tier_3_rate DECIMAL(8, 6),              -- >$5M: 0.50%
    
    -- Billing
    billing_frequency VARCHAR(20),           -- MONTHLY, QUARTERLY, ANNUALLY
    billing_method VARCHAR(20),              -- ADVANCE, ARREARS
    
    effective_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE billing_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fee_schedule_id UUID REFERENCES fee_schedules(id),
    billing_period_start DATE,
    billing_period_end DATE,
    
    -- Amounts
    aum_at_billing DECIMAL(20, 2),
    gross_fee DECIMAL(20, 2),
    proration_factor DECIMAL(8, 6),
    net_fee DECIMAL(20, 2),
    
    -- Status
    status VARCHAR(20) DEFAULT 'PENDING',
    invoiced_at TIMESTAMPTZ,
    paid_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/114_fee_billing.sql` | `[x]` |
| Fee Calculator | `services/billing/fee_calculator.py` | `[x]` |
| Proration Service | `services/billing/proration_service.py` | `[x]` |

### 114.2 Declining Fee Balance Logic (1% → 0.6%) `[x]`
| Component | File Path | Status |
|-----------|-----------|--------|
| Tiered Fee Calculator | `services/billing/tiered_fee_calc.py` | `[x]` |

### 114.3 Performance-Based Hurdle Rate Calculator `[x]`
| Component | File Path | Status |
|-----------|-----------|--------|
| Hurdle Calculator | `services/billing/hurdle_calculator.py` | `[x]` |
| Performance Fee Service | `services/billing/performance_fee.py` | `[x]` |

### 114.4 High Water Mark Validator `[x]`
Ensure performance fees only charged above previous high water mark.

| Component | File Path | Status |
|-----------|-----------|--------|
| HWM Tracker | `services/billing/high_water_mark.py` | `[x]` |

### 114.5 Neo4j Load/Wrap Fee Legacy Mapping `[x]`
Track legacy fee structures (12b-1, load fees) for comparison.

---

## 📊 Phase Status: `[ ]` NOT STARTED
