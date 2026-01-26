# Phase 116: International Index & Emerging Market SOE Filter

> **Status**: `[ ]` Not Started | **Owner**: International Team
> **Source**: JIRA_PLANNING_JSON_2.txt - Phase 16

## 📋 Overview
**Description**: Build filters and analysis tools for international indices that identify state-owned enterprises (SOE) exposure, single-company concentration, and geopolitical tradability risks.

---

## 🎯 Sub-Deliverables

### 116.1 State-Owned Enterprise Postgres Flag `[ ]`

```sql
CREATE TABLE international_holdings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(20) NOT NULL,
    company_name VARCHAR(255),
    country_code VARCHAR(2),
    
    -- SOE Status
    is_state_owned BOOLEAN DEFAULT FALSE,
    government_ownership_pct DECIMAL(5, 2),
    controlling_entity VARCHAR(255),
    
    -- Risk Factors
    sanction_risk VARCHAR(20),
    repatriation_risk VARCHAR(20),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| SOE Classifier | `services/international/soe_classifier.py` | `[ ]` |
| Country Risk Service | `services/risk/country_risk.py` | `[ ]` |

### 116.2 Single-Company Concentration Analyzer `[ ]`
Flag indices with excessive single-company weighting (e.g., TSMC in Taiwan).

| Component | File Path | Status |
|-----------|-----------|--------|
| Concentration Analyzer | `services/international/concentration_analyzer.py` | `[ ]` |

### 116.3 Neo4j Foreign Capital Tradability Graph `[ ]`
Map capital control restrictions and foreign investment limitations.

```cypher
(:COUNTRY)-[:HAS_CAPITAL_CONTROL {
    type: "FOREIGN_OWNERSHIP_LIMIT",
    limit_pct: 0.49,
    sectors_restricted: ["BANKING", "TELECOM"]
}]->(:RESTRICTION)
```

### 116.4 Kafka Geopolitical Methodology Stream `[ ]`
Stream geopolitical risk updates affecting index methodology changes.

### 116.5 Inefficient Index Government Interest Filter `[ ]`
Identify indices distorted by government intervention or state capitalism.

---

## 📊 Phase Status: `[ ]` NOT STARTED
