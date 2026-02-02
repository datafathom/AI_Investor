# Phase 111: Professional Service Provider Graph

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Integration Team

---

## 📋 Overview

**Description**: Build a comprehensive Neo4j graph modeling the network of professional service providers (estate attorneys, CPAs, insurance agents) that collaborate with financial advisors, enabling coordinated client service delivery.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Phase 11 (Professional Service Provider Graph)

---

## 🎯 Sub-Deliverables

### 111.1 Neo4j Estate Attorney Nodes `[x]`

**Acceptance Criteria**: Define estate attorney nodes with specializations (trusts, probate, tax), bar admissions, and client relationships.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:ESTATE_ATTORNEY {
    id: "uuid",
    name: "Jane Smith, JD",
    firm: "Smith & Associates",
    bar_admissions: ["NY", "CA"],
    specializations: ["TRUSTS", "PROBATE", "TAX"],
    years_experience: 25,
    average_client_net_worth: 15000000,
    hourly_rate: 650
})

(:CLIENT)-[:REPRESENTED_BY {
    engagement_type: "ESTATE_PLANNING",
    retainer_amount: 25000,
    start_date: date()
}]->(:ESTATE_ATTORNEY)

(:ESTATE_ATTORNEY)-[:COLLABORATES_WITH]->(:FINANCIAL_ADVISOR)
(:ESTATE_ATTORNEY)-[:DRAFTED]->(:TRUST)
(:ESTATE_ATTORNEY)-[:DRAFTED]->(:WILL)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Attorney Graph Service | `services/neo4j/attorney_graph.py` | `[x]` |
| Service Provider Model | `models/service_provider.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Attorney Directory | `frontend2/src/components/Providers/AttorneyDirectory.jsx` | `[x]` |
| Provider Network Graph | `frontend2/src/components/Neo4j/ProviderNetwork.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Attorney Graph | `tests/unit/test_attorney_graph.py` | `[x]` |
| Integration: Provider Network | `tests/integration/test_provider_network.py` | `[x]` |

---

### 111.2 Insurance Provider Postgres Entities `[x]`

**Acceptance Criteria**: Create Postgres tables for insurance providers, policies, and coverage details for term life, PPLI, and property insurance.

#### Postgres Schema

```sql
CREATE TABLE insurance_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    provider_type VARCHAR(50),           -- CARRIER, BROKER, AGENT
    am_best_rating VARCHAR(10),
    specializations JSONB,               -- ["LIFE", "PPLI", "PROPERTY"]
    licensed_states JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE insurance_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    provider_id UUID REFERENCES insurance_providers(id),
    
    -- Policy Details
    policy_type VARCHAR(50) NOT NULL,    -- TERM_LIFE, WHOLE_LIFE, PPLI, UMBRELLA
    policy_number VARCHAR(100),
    
    -- Coverage
    death_benefit DECIMAL(20, 2),
    cash_value DECIMAL(20, 2),
    annual_premium DECIMAL(20, 2),
    
    -- Term Details
    effective_date DATE,
    expiration_date DATE,
    
    -- Status
    status VARCHAR(20) DEFAULT 'ACTIVE',
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/111_insurance_providers.sql` | `[x]` |
| Insurance Model | `models/insurance.py` | `[x]` |
| Insurance Service | `services/insurance/insurance_service.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Insurance Dashboard | `frontend2/src/components/Insurance/Dashboard.jsx` | `[x]` |
| Policy List | `frontend2/src/components/Insurance/PolicyList.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Insurance Service | `tests/unit/test_insurance_service.py` | `[x]` |
| Integration: Insurance API | `tests/integration/test_insurance_api.py` | `[x]` |

---

### 111.3 Financial Planner ↔ Life Insurance Logic `[x]`

**Acceptance Criteria**: Implement logic connecting financial planners with life insurance needs analysis, including coverage gap calculations.

| Component | File Path | Status |
|-----------|-----------|--------|
| Needs Analyzer | `services/insurance/needs_analyzer.py` | `[x]` |
| Coverage Gap Calculator | `services/insurance/coverage_gap.py` | `[x]` |
| Referral Manager | `services/providers/referral_manager.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Coverage Gap Widget | `frontend2/src/components/Insurance/CoverageGap.jsx` | `[x]` |
| Needs Analysis Form | `frontend2/src/components/Insurance/NeedsAnalyzer.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Needs Analyzer | `tests/unit/test_needs_analyzer.py` | `[x]` |
| Unit: Coverage Gap | `tests/unit/test_coverage_gap.py` | `[x]` |

---

### 111.4 CPA/Accountant Entity Mapping `[x]`

**Acceptance Criteria**: Map CPA relationships in Neo4j with specializations (high-net-worth, business, international) and tax preparation history.

#### Neo4j Schema

```cypher
(:CPA {
    id: "uuid",
    name: "Robert Johnson, CPA",
    firm: "Johnson Tax Advisory",
    credentials: ["CPA", "CFP", "EA"],
    specializations: ["UHNW", "TRUST_TAX", "INTERNATIONAL"],
    avg_return_complexity: "HIGH"
})

(:CLIENT)-[:TAX_PREPARED_BY {
    years_of_service: 10,
    last_return_date: date()
}]->(:CPA)

(:CPA)-[:COORDINATES_WITH]->(:FINANCIAL_ADVISOR)
(:CPA)-[:ADVISES_ON]->(TAX_STRATEGY)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| CPA Graph Service | `services/neo4j/cpa_graph.py` | `[x]` |
| Tax Coordination Service | `services/tax/coordination_service.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| CPA Directory | `frontend2/src/components/Providers/CPADirectory.jsx` | `[x]` |
| Tax Coordination Panel | `frontend2/src/components/Tax/CoordinationPanel.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: CPA Graph | `tests/unit/test_cpa_graph.py` | `[x]` |

---

### 111.5 Shared Tax Efficiency Goals Record `[x]`

**Acceptance Criteria**: Create a shared record system where all service providers (advisor, CPA, attorney) can coordinate on tax efficiency strategies.

| Component | File Path | Status |
|-----------|-----------|--------|
| Shared Goals Service | `services/coordination/shared_goals.py` | `[x]` |
| Collaboration Platform | `services/coordination/collab_platform.py` | `[x]` |
| API Endpoint | `web/api/providers/collaboration.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Collaboration Dashboard | `frontend2/src/components/Coordination/Dashboard.jsx` | `[x]` |
| Goal Tracker | `frontend2/src/components/Coordination/GoalTracker.jsx` | `[x]` |
| Team Communication | `frontend2/src/components/Coordination/TeamComm.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Shared Goals | `tests/unit/test_shared_goals.py` | `[x]` |
| Integration: Collaboration | `tests/integration/test_provider_collab.py` | `[x]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 111.1 Estate Attorney Nodes | `[x]` | `[ ]` |
| 111.2 Insurance Entities | `[x]` | `[ ]` |
| 111.3 Insurance Logic | `[x]` | `[ ]` |
| 111.4 CPA Mapping | `[x]` | `[ ]` |
| 111.5 Shared Tax Goals | `[x]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py providers list` | List all providers | `[x]` |
| `python cli.py providers find attorney` | Find estate attorneys | `[x]` |
| `python cli.py providers network <client>` | Show provider network | `[x]` |

---

*Last verified: 2026-01-25*
