# Phase 183: FATCA Foreign Bank Disclosure Pipeline

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Compliance & Tax Team

---

## 📋 Overview

**Description**: Automate Foreign Account Tax Compliance Act (FATCA) reporting. For clients with international assets (Swiss Bank Accounts, Cayman Funds), ensure all Form 8938 and FBAR filings are tracked to prevent massive IRS penalties (up to 50% of account value).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 3

---

## 🎯 Sub-Deliverables

### 183.1 Postgres FATCA Disclosure Engine `[ ]`

**Acceptance Criteria**: Central repository for all foreign financial assets. Track "Max Value During Year" (required for FBAR).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE foreign_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    institution_name VARCHAR(100),
    country_code VARCHAR(3),
    account_number VARCHAR(100),
    
    -- Values
    max_value_year DECIMAL(20, 2),
    year_end_value DECIMAL(20, 2),
    
    -- Status
    is_reported_fbar BOOLEAN DEFAULT FALSE,
    is_reported_8938 BOOLEAN DEFAULT FALSE,
    
    year INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/183_foreign_assets.sql` | `[ ]` |
| Disclosure Engine | `services/compliance/fatca_engine.py` | `[ ]` |

---

### 183.2 Neo4j US Citizen → Foreign Tax Haven Mapping `[ ]`

**Acceptance Criteria**: Graph map of tax residency. Identify "US Persons" holding assets in "High Risk Jurisdictions" (e.g., Switzerland, BVI).

```cypher
(:PERSON:US_CITIZEN)-[:OWNS_ACCOUNT]->(:BANK {country: "Switzerland"})
(:BANK)-[:JURISDICTION]->(:COUNTRY {risk: "HIGH", fatca_compliant: true})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Residency Graph | `services/neo4j/residency_graph.py` | `[ ]` |

---

### 183.3 Swiss Bank Secrecy Compromise Detector `[ ]`

**Acceptance Criteria**: Log instances where foreign banks request "W-9" forms. This signals the bank is reporting to the IRS, ending any "secrecy".

| Component | File Path | Status |
|-----------|-----------|--------|
| Secrecy Monitor | `services/compliance/secrecy_monitor.py` | `[ ]` |

---

### 183.4 Kafka International FATCA Equivalent Reporter `[ ]`

**Acceptance Criteria**: Handle CRS (Common Reporting Standard) data streams for non-US global clients.

#### Kafka Topic

```json
{
    "topic": "crs-reports",
    "schema": {
        "client_id": "uuid",
        "jurisdiction_from": "UK",
        "jurisdiction_to": "FR",
        "account_balance": "decimal"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| CRS Consumer | `services/kafka/crs_consumer.py` | `[ ]` |

---

### 183.5 Asset Secrecy Risk Score by Jurisdiction `[ ]`

**Acceptance Criteria**: Score jurisdictions. Switzerland (Medium Secrecy now), USA (High Secrecy for foreigners), Maldives (High Secrecy).

| Component | File Path | Status |
|-----------|-----------|--------|
| Jurisdiction Scorer | `services/risk/jurisdiction_score.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| FBAR Dashboard | `frontend2/src/components/Tax/FBARDash.jsx` | `[ ]` |
| Jurisdiction Map | `frontend2/src/components/Maps/JurisdictionRisk.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py fatca list-assets` | Show foreign accts | `[ ]` |
| `python cli.py fatca gen-fbar` | Generate FinCEN 114 | `[ ]` |

---

*Last verified: 2026-01-25*
