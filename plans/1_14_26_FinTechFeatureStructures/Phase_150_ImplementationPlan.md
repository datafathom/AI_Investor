# Phase 150: 1031 Exchange Real Estate Timer & Deferral

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Real Estate & Tax Team

---

## 📋 Overview

**Description**: Manage Section 1031 "Like-Kind" Exchanges for real estate. This tax strategy allows investors to defer capital gains tax if they reinvest proceeds from a property sale into a new property of equal or greater value within strict timelines.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 10

---

## 🎯 Sub-Deliverables

### 150.1 Property Trade-Up Equal/Greater Value Service `[ ]`

**Acceptance Criteria**: Verify that the Replacement Property value is >= Relinquished Property value. If not, calculate the "Boot" (taxable portion) instantly.

```python
class ExchangeValidator:
    """
    Validate 1031 Exchange rules.
    
    Rules:
    1. Value Rule: Replacement Price >= Sales Price
    2. Equity Rule: Replacement Equity >= Sales Equity (Invest all cash)
    3. Debt Rule: New Mortgage >= Old Mortgage (or add cash)
    """
    
    def validate_metrics(
        self,
        relinquished: Property,
        replacement: Property
    ) -> ValidationMetrics:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Exchange Validator | `services/real_estate/exchange_validator.py` | `[ ]` |
| Equity Calculator | `services/real_estate/equity_calc.py` | `[ ]` |

---

### 150.2 45-Day / 180-Day Postgres Timer `[ ]`

**Acceptance Criteria**: Strict countdown timers. IRS rules: 45 days to Identify candidates, 180 days to Close. Missing these kills the tax break.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE exchange_timers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exchange_id UUID NOT NULL,
    
    -- Deadlines
    sale_closed_date DATE NOT NULL,
    identification_deadline DATE GENERATED ALWAYS AS (sale_closed_date + 45) STORED,
    closing_deadline DATE GENERATED ALWAYS AS (sale_closed_date + 180) STORED,
    
    -- Status
    identified_date DATE,
    purchase_closed_date DATE,
    status VARCHAR(20),            -- PENDING, IDENTIFIED, COMPLETED, FAILED
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Timer Service | `services/real_estate/timer_service.py` | `[ ]` |
| Deadline Notifier | `services/notifications/deadline_notifier.py` | `[ ]` |

---

### 150.3 'Boot' Tax Hit Calculator `[ ]`

**Acceptance Criteria**: Calculate tax liability on "Boot" (Cash taken out or mortgage reduction).

| Component | File Path | Status |
|-----------|-----------|--------|
| Boot Calculator | `services/tax/boot_calculator.py` | `[ ]` |

---

### 150.4 Neo4j Sold → Replacement Property Relationship `[ ]`

**Acceptance Criteria**: Track the chain of custody for properties to maintain the "deferred tax basis" history across multiple exchanges.

#### Neo4j Schema

```cypher
(:PROPERTY {address: "123 Old St", basis: 100000})-[:EXCHANGED_INTO {
    deferred_gain: 400000,
    exchange_date: date()
}]->(:PROPERTY {address: "456 New St", basis: 100000}) 
// Basis carries over!
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Chain Graph Service | `services/neo4j/property_chain.py` | `[ ]` |

---

### 150.5 $500k Primary Residence Exemption Validator `[ ]`

**Acceptance Criteria**: Handle the "Section 121" exclusion ($500k tax-free for married couples) on primary homes, often used in conjunction with 1031s for mixed-use properties.

| Component | File Path | Status |
|-----------|-----------|--------|
| Exclusion Validator | `services/tax/section121_validator.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py 1031 deadlines <sale_date>` | Calc dates | `[ ]` |
| `python cli.py 1031 calc-boot` | Calculate boot tax | `[ ]` |

---

*Last verified: 2026-01-25*
