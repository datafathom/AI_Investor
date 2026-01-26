# Phase 188: Dual Citizenship & EU Passport Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Legal & Immigration Team

---

## 📋 Overview

**Description**: Manage "Plan B" citizenship. Support clients acquiring Golden Visas (Portugal, Greece) or Citizenship by Investment (St. Kitts, Malta) for tax residency optionality or geopolitical hedging.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 8

---

## 🎯 Sub-Deliverables

### 188.1 Investment Requirement Tracker (Golden Visa assets) `[ ]`

**Acceptance Criteria**: Track specific assets that qualify for visas (e.g., €500k in VCs for Portugal). Flag them as "Restricted" (cannot sell without losing visa) for the required holding period (5 years).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE visa_investments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    country_code VARCHAR(3),
    program_name VARCHAR(100),         -- PORTUGAL_GOLDEN_VISA
    
    -- Investment
    asset_id UUID NOT NULL,
    invested_amount_local DECIMAL(20, 2),
    required_holding_period_months INTEGER,
    
    -- Timeline
    start_date DATE,
    citizenship_eligible_date DATE GENERATED ALWAYS AS (start_date + (required_holding_period_months * INTERVAL '1 month')) STORED,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/188_visa_investments.sql` | `[ ]` |
| Visa Tracker | `services/legal/visa_tracker.py` | `[ ]` |

---

### 188.2 Residency Days Counter (183-Day Rule) `[ ]`

**Acceptance Criteria**: Calendar heatmap tracked automatically (via locations or manual entry) to manage Tax Residency. stay <183 days to avoid becoming a tax resident in high-tax EU countries.

| Component | File Path | Status |
|-----------|-----------|--------|
| Day Counter | `services/compliance/day_counter.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Residency Calendar | `frontend2/src/components/Calendar/ResidencyTracker.jsx` | `[ ]` |

---

### 188.3 Property Management Integration for Visa Real Estate `[ ]`

**Acceptance Criteria**: Link foreign real estate used for visas to property managers. Track income/expenses to ensure "net yield" isn't eaten by management fees.

| Component | File Path | Status |
|-----------|-----------|--------|
| Prop Mgmt API | `services/real_estate/foreign_prop.py` | `[ ]` |

---

### 188.4 Neo4j Jurisdiction Optionality Graph `[ ]`

**Acceptance Criteria**: Graph showing "What If" options. If Citizenship A fails, what is the path to Citizenship B?

```cypher
(:PASSPORT {country: "USA"})-[:ALLOWS_ENTRY]->(:COUNTRY {name: "Canada", visa_free: true})
(:RESIDENCY {country: "Portugal"})-[:LEADS_TO]->(:PASSPORT {country: "EU"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Optionality Graph | `services/neo4j/passport_graph.py` | `[ ]` |

---

### 188.5 Blocked Person/Sanction List Screening `[ ]`

**Acceptance Criteria**: Ensure the client isn't inadvertently doing business with sanctioned individuals in the target country (common risk in CIP programs).

| Component | File Path | Status |
|-----------|-----------|--------|
| Sanction Screener | `services/compliance/sanction_screen.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py visa check-hold` | Verify asset hold | `[ ]` |
| `python cli.py visa calc-days` | Count residency days | `[ ]` |

---

*Last verified: 2026-01-25*
