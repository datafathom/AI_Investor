# Phase 159: Performance-Based Fee Carry & Hurdle Engine

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Billing & Accounting Team

---

## 📋 Overview

**Description**: Implement institutional-grade billing for Alternative Investments (Hedge Funds, Private Equity). Logic for "2 and 20" (2% Mgmt / 20% Performance), Hurdle Rates (no fee until X% return), and High Water Marks (no fee on recovery of losses).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 19

---

## 🎯 Sub-Deliverables

### 159.1 20% Carry Calculator (Above Hurdle) `[ ]`

**Acceptance Criteria**: Calculate "Carried Interest" (Performance Fee) accurately. Fee = (Profit - Hurdle) * Carry Rate.

#### Backend Implementation

```python
class CarryCalculator:
    """
    Calculate performance fees.
    
    Formula: Max(0, (Ending_NAV - Opening_NAV - Hurdle_Amount) * Carry_Rate)
    """
    def calculate_carry(
        self,
        opening_nav: Decimal,
        ending_nav: Decimal,
        hurdle_rate_pct: Decimal = 0.05,
        carry_rate: Decimal = 0.20
    ) -> CarryResult:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Carry Calculator | `services/billing/carry_calculatory.py` | `[ ]` |

---

### 159.2 Postgres 2% Management Fee Table `[ ]`

**Acceptance Criteria**: Track the base management fee (accrued daily/monthly, billed quarterly) separate from performance fees.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE fee_accruals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    date DATE NOT NULL,
    
    -- Components
    daily_aum DECIMAL(20, 2),
    mgmt_fee_rate_annual DECIMAL(5, 4), -- 0.02
    daily_mgmt_fee DECIMAL(10, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/159_fee_accrual.sql` | `[ ]` |
| Daily Accrual Svc | `services/billing/daily_accrual.py` | `[ ]` |

---

### 159.3 High Water Mark Logic Service `[ ]`

**Acceptance Criteria**: Ensure no performance fees are charged if the fund is recovering from a drawdown (must exceed previous peak NAV).

| Component | File Path | Status |
|-----------|-----------|--------|
| HWM Tracker | `services/billing/hwm_tracker.py` | `[ ]` |

---

### 159.4 Neo4j Accredited Investor Verification Node `[ ]`

**Acceptance Criteria**: Verify user is an "Accredited Investor" or "Qualified Client" (required by SEC to charge performance fees).

```cypher
(:PERSON)-[:HAS_STATUS]->(:ACCREDITED_INVESTOR {
    verified_date: date(),
    method: "NET_WORTH_GT_1M",
    expires: date() + duration({years: 2})
})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Accreditation Service | `services/neo4j/accreditation.py` | `[ ]` |

---

### 159.5 Incentive Alignment Aggression Flag `[ ]`

**Acceptance Criteria**: Monitor if managers are taking excessive risk to chase performance fees (Agency Risk). Flag portfolios with abnormal volatility spikes near billing periods.

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Taking Monitor | `services/risk/incentive_monitor.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py billing calc-carry` | Estimate performance fee | `[ ]` |
| `python cli.py billing check-hwm` | Show distance to HWM | `[ ]` |

---

*Last verified: 2026-01-25*
