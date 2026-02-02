# Phase 150: 1031 Exchange Real Estate Timer & Deferral

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Real Estate & Tax Team

---

## 📋 Overview

**Description**: Manage Section 1031 "Like-Kind" Exchanges for real estate. This tax strategy allows investors to defer capital gains tax if they reinvest proceeds from a property sale into a new property of equal or greater value within strict timelines.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 10

---

## 🎯 Sub-Deliverables

### 150.1 Property Trade-Up Equal/Greater Value Service `[x]`

**Acceptance Criteria**: Verify that the Replacement Property value is >= Relinquished Property value. If not, calculate the "Boot" (taxable portion) instantly.

**Implementation**: `ExchangeValidator` class validates all three 1031 rules:
- Value Rule: Replacement Price >= Sales Price
- Equity Rule: Replacement Equity >= Sales Equity
- Debt Rule: New Mortgage >= Old Mortgage

| Component | File Path | Status |
|-----------|-----------|--------|
| Exchange Validator | `services/real_estate/exchange_validator.py` | `[x]` |
| Equity Calculator | `services/real_estate/equity_calc.py` | `[x]` (Integrated into validator) |

---

### 150.2 45-Day / 180-Day Postgres Timer `[x]`

**Acceptance Criteria**: Strict countdown timers. IRS rules: 45 days to Identify candidates, 180 days to Close. Missing these kills the tax break.

**Implementation**: `ExchangeTimerService` with full database persistence:
- `create_exchange()`: Creates timer record with auto-calculated deadlines
- `get_exchange()`: Retrieves timer with days remaining
- `update_status()`: Updates status (PENDING → IDENTIFIED → COMPLETED/FAILED)
- `get_active_exchanges()`: Lists all in-progress exchanges

| Component | File Path | Status |
|-----------|-----------|--------|
| Timer Service | `services/real_estate/timer_service.py` | `[x]` |
| DB Migration | `migrations/150_exchange_timers.sql` | `[x]` |
| Deadline Notifier | `services/notifications/deadline_notifier.py` | `[/]` (Uses existing notification system) |

---

### 150.3 'Boot' Tax Hit Calculator `[x]`

**Acceptance Criteria**: Calculate tax liability on "Boot" (Cash taken out or mortgage reduction).

**Implementation**: `BootCalculator` with full tax breakdown:
- Depreciation recapture at 25%
- Long-term capital gains at bracket rates (0%, 15%, 20%)
- Net Investment Income Tax (NIIT) at 3.8% for high earners

| Component | File Path | Status |
|-----------|-----------|--------|
| Boot Calculator | `services/tax/boot_calculator.py` | `[x]` |

---

### 150.4 Neo4j Sold → Replacement Property Relationship `[x]`

**Acceptance Criteria**: Track the chain of custody for properties to maintain the "deferred tax basis" history across multiple exchanges.

**Implementation**: `PropertyChainGraph` with chain traversal:
- `link_exchange()`: Creates EXCHANGED_INTO relationship
- `get_exchange_chain()`: Full history from original to current
- `get_total_deferred_gain()`: Accumulated deferred gains in chain
- `get_original_basis()`: Original cost basis carried forward

| Component | File Path | Status |
|-----------|-----------|--------|
| Chain Graph Service | `services/neo4j/property_chain.py` | `[x]` |

---

### 150.5 $500k Primary Residence Exemption Validator `[x]`

**Acceptance Criteria**: Handle the "Section 121" exclusion ($500k tax-free for married couples) on primary homes, often used in conjunction with 1031s for mixed-use properties.

**Implementation**: `Section121Validator` with detailed eligibility:
- Ownership test (2 years in 5-year period)
- Use test (lived as primary residence)
- Lookback rule (once every 2 years)
- Mixed-use property split calculation

| Component | File Path | Status |
|-----------|-----------|--------|
| Exclusion Validator | `services/tax/section121_validator.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py 1031 deadlines <sale_date>` | Calc dates | `[x]` |
| `python cli.py 1031 calc-boot` | Calculate boot tax | `[x]` |

---

*Last verified: 2026-01-30*

