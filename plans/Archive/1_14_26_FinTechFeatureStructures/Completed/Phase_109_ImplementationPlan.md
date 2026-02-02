# Phase 109: Private Banker White-Glove Data Model

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: UHNW Services Team

---

## 📋 Overview

**Description**: Build the data model and services for private banking clients ($10M+ net worth), including commercial lending relationships, tax deferral strategies, estate planning integration, and private equity access.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Phase 9 (Private Banker White-Glove Data Model)

---

## 🎯 Sub-Deliverables

### 109.1 $10M Net Worth Gate for Private Banking `[x]`

**Acceptance Criteria**: Implement a qualification gate that validates client eligibility for private banking services based on $10M minimum net worth.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE private_banking_clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    
    -- Qualification
    verified_net_worth DECIMAL(20, 2) NOT NULL,
    qualification_date DATE NOT NULL,
    verification_method VARCHAR(50),          -- DOCUMENT, CUSTODIAN, SELF_REPORTED
    last_verification TIMESTAMPTZ,
    
    -- Status
    tier VARCHAR(20) NOT NULL,                -- PRIVATE ($10M+), ULTRA ($50M+), FAMILY_OFFICE ($100M+)
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Assigned Team
    relationship_manager_id UUID,
    investment_specialist_id UUID,
    lending_specialist_id UUID,
    estate_attorney_id UUID,
    
    -- Service Level
    service_level VARCHAR(50),                -- WHITE_GLOVE, CONCIERGE, STANDARD
    max_clients_per_rm INTEGER DEFAULT 50,
    
    -- Metadata
    onboarded_at TIMESTAMPTZ DEFAULT NOW(),
    annual_review_date DATE
);

CREATE INDEX idx_pb_net_worth ON private_banking_clients(verified_net_worth);
CREATE INDEX idx_pb_tier ON private_banking_clients(tier);
```

#### Backend Implementation

```python
class PrivateBankingQualifier:
    """
    Qualify clients for private banking tiers.
    
    Tiers:
    - PRIVATE: $10M - $50M net worth
    - ULTRA: $50M - $100M net worth
    - FAMILY_OFFICE: $100M+ net worth
    """
    
    TIER_THRESHOLDS = {
        'PRIVATE': Decimal('10000000'),
        'ULTRA': Decimal('50000000'),
        'FAMILY_OFFICE': Decimal('100000000')
    }
    
    def qualify_client(self, net_worth: Decimal) -> QualificationResult:
        pass
    
    def assign_team(self, client: PrivateBankingClient) -> TeamAssignment:
        """Assign relationship team based on tier and availability."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/109_private_banking.sql` | `[x]` |
| PB Client Model | `models/private_banking_client.py` | `[x]` |
| Qualifier Service | `services/private_banking/qualifier.py` | `[x]` |
| Team Assignment Service | `services/private_banking/team_assignment.py` | `[x]` |
| API Endpoint | `web/api/private_banking/clients.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Qualification Form | `frontend2/src/components/PrivateBanking/QualificationForm.jsx` | `[x]` |
| Tier Badge | `frontend2/src/components/Badges/PBTierBadge.jsx` | `[x]` |
| Team Display | `frontend2/src/components/PrivateBanking/TeamDisplay.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Qualifier | `tests/unit/test_pb_qualifier.py` | `[x]` |
| Unit: Team Assignment | `tests/unit/test_team_assignment.py` | `[x]` |
| Integration: Qualification Flow | `tests/integration/test_pb_qualification.py` | `[x]` |

---

### 109.2 Neo4j Commercial Lending Relationships `[x]`

**Acceptance Criteria**: Model commercial lending relationships in Neo4j including collateral, covenants, and cross-default provisions.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
// Private Banking Client Node
(:PRIVATE_BANKING_CLIENT {
    id: "uuid",
    name: "John Smith",
    tier: "ULTRA",
    verified_net_worth: 75000000,
    relationship_since: date()
})

// Loan Nodes
(:COMMERCIAL_LOAN {
    id: "uuid",
    loan_type: "SECURITIES_BACKED",     // SECURITIES_BACKED, REAL_ESTATE, BUSINESS
    principal: 25000000,
    outstanding_balance: 23500000,
    interest_rate: 0.055,
    term_months: 60,
    ltv: 0.50,                          -- Loan-to-Value
    status: "ACTIVE"
})

// Collateral Nodes
(:COLLATERAL {
    id: "uuid",
    type: "SECURITIES_PORTFOLIO",
    current_value: 50000000,
    margin_requirement: 0.50,
    maintenance_margin: 0.35
})

// Relationships
(:PRIVATE_BANKING_CLIENT)-[:HAS_LOAN {
    origination_date: date(),
    maturity_date: date()
}]->(:COMMERCIAL_LOAN)

(:COMMERCIAL_LOAN)-[:SECURED_BY {
    pledge_date: date(),
    lien_position: 1
}]->(:COLLATERAL)

(:COMMERCIAL_LOAN)-[:CROSS_DEFAULTS_WITH]->(:COMMERCIAL_LOAN)

(:COMMERCIAL_LOAN)-[:HAS_COVENANT {
    type: "FINANCIAL",
    description: "Maintain 50% LTV",
    threshold: 0.50,
    current_value: 0.47,
    in_compliance: true
}]->(:COVENANT)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Lending Graph Service | `services/neo4j/lending_graph.py` | `[x]` |
| Collateral Tracker | `services/lending/collateral_tracker.py` | `[x]` |
| Covenant Monitor | `services/lending/covenant_monitor.py` | `[x]` |
| LTV Calculator | `services/lending/ltv_calculator.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Lending Dashboard | `frontend2/src/components/Lending/Dashboard.jsx` | `[x]` |
| Loan Detail View | `frontend2/src/components/Lending/LoanDetail.jsx` | `[x]` |
| Collateral Graph | `frontend2/src/components/Neo4j/CollateralGraph.jsx` | `[x]` |
| Covenant Status Panel | `frontend2/src/components/Lending/CovenantStatus.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Lending Graph | `tests/unit/test_lending_graph.py` | `[x]` |
| Unit: LTV Calculator | `tests/unit/test_ltv_calculator.py` | `[x]` |
| Unit: Covenant Monitor | `tests/unit/test_covenant_monitor.py` | `[x]` |
| Integration: Neo4j Lending | `tests/integration/test_lending_neo4j.py` | `[x]` |

---

### 109.3 Tax Deferral Strategy Tracking Service `[x]`

**Acceptance Criteria**: Track and optimize tax deferral strategies including installment sales, opportunity zones, 1031 exchanges, and stock option timing.

#### Postgres Schema

```sql
CREATE TABLE tax_deferral_strategies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES private_banking_clients(id),
    
    -- Strategy Details
    strategy_type VARCHAR(50) NOT NULL,       -- INSTALLMENT_SALE, OPPORTUNITY_ZONE, 1031_EXCHANGE, OPTION_TIMING
    description TEXT,
    
    -- Amounts
    gain_deferred DECIMAL(20, 2) NOT NULL,
    tax_savings_estimate DECIMAL(20, 2),
    
    -- Timeline
    initiation_date DATE NOT NULL,
    expiration_date DATE,                      -- When deferral ends
    days_remaining INTEGER,
    
    -- Status
    status VARCHAR(20) DEFAULT 'ACTIVE',
    compliance_verified BOOLEAN DEFAULT FALSE,
    
    -- Opportunity Zone Specific
    oz_investment_id UUID,
    oz_holding_period_start DATE,
    oz_10_year_exclusion_eligible BOOLEAN,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Tax Deferral Migration | `migrations/109_tax_deferral.sql` | `[x]` |
| Deferral Model | `models/tax_deferral.py` | `[x]` |
| Deferral Tracker | `services/tax/deferral_tracker.py` | `[x]` |
| OZ Compliance Checker | `services/tax/oz_compliance.py` | `[x]` |
| 1031 Timer Service | `services/tax/exchange_1031_timer.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Deferral Dashboard | `frontend2/src/components/Tax/DeferralDashboard.jsx` | `[x]` |
| Timeline View | `frontend2/src/components/Tax/DeferralTimeline.jsx` | `[x]` |
| OZ Investment Tracker | `frontend2/src/components/Tax/OZTracker.jsx` | `[x]` |
| 1031 Exchange Timer | `frontend2/src/components/Tax/Exchange1031Timer.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Deferral Tracker | `tests/unit/test_deferral_tracker.py` | `[x]` |
| Unit: OZ Compliance | `tests/unit/test_oz_compliance.py` | `[x]` |
| Unit: 1031 Timer | `tests/unit/test_exchange_1031_timer.py` | `[x]` |
| Integration: Tax Deferral | `tests/integration/test_tax_deferral.py` | `[x]` |

---

### 109.4 Estate Planning & PE Access Ancillary Nodes `[x]`

**Acceptance Criteria**: Extend the Neo4j graph with ancillary service nodes for estate planning and private equity access unique to private banking clients.

#### Neo4j Schema

```cypher
// Estate Planning Integration
(:PRIVATE_BANKING_CLIENT)-[:HAS_ESTATE_PLAN {
    document_type: "REVOCABLE_TRUST",
    last_updated: date(),
    attorney_id: "uuid"
}]->(:ESTATE_PLAN)

(:ESTATE_PLAN)-[:INCLUDES]->(TRUST)
(:ESTATE_PLAN)-[:INCLUDES]->(WILL)
(:ESTATE_PLAN)-[:INCLUDES]->(POWER_OF_ATTORNEY)

// Private Equity Access
(:PRIVATE_BANKING_CLIENT)-[:HAS_ACCESS_TO {
    tier: "ULTRA",
    min_investment: 1000000
}]->(:PE_FUND)

(:PE_FUND {
    id: "uuid",
    name: "Blackstone Real Estate Partners",
    strategy: "REAL_ESTATE",
    vintage_year: 2024,
    target_return: 0.18,
    minimum_investment: 5000000
})

// Investment in PE
(:PRIVATE_BANKING_CLIENT)-[:INVESTED_IN {
    commitment: 5000000,
    called_capital: 2500000,
    distributions: 500000,
    nav: 2750000
}]->(:PE_FUND)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Estate Graph Service | `services/neo4j/estate_graph.py` | `[x]` |
| PE Access Service | `services/private_banking/pe_access.py` | `[x]` |
| PE Investment Tracker | `services/investments/pe_tracker.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Estate Planning Dashboard | `frontend2/src/components/Estate/Dashboard.jsx` | `[x]` |
| PE Opportunity List | `frontend2/src/components/PrivateEquity/OpportunityList.jsx` | `[x]` |
| PE Investment Summary | `frontend2/src/components/PrivateEquity/InvestmentSummary.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Estate Graph | `tests/unit/test_estate_graph.py` | `[x]` |
| Unit: PE Access | `tests/unit/test_pe_access.py` | `[x]` |
| Integration: PE Flow | `tests/integration/test_pe_investment_flow.py` | `[x]` |

---

### 109.5 Service Quality Load Balancer (Low Client Count) `[x]`

**Acceptance Criteria**: Implement a load balancer that ensures relationship managers maintain low client counts (max 50 for ULTRA tier) to preserve white-glove service quality.

| Component | File Path | Status |
|-----------|-----------|--------|
| RM Load Balancer | `services/private_banking/rm_load_balancer.py` | `[x]` |
| Capacity Monitor | `services/private_banking/capacity_monitor.py` | `[x]` |
| Alert Service | `services/alerts/rm_capacity_alerts.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| RM Capacity Dashboard | `frontend2/src/components/Admin/RMCapacity.jsx` | `[x]` |
| Assignment Queue | `frontend2/src/components/Admin/AssignmentQueue.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Load Balancer | `tests/unit/test_rm_load_balancer.py` | `[x]` |
| Unit: Capacity Monitor | `tests/unit/test_capacity_monitor.py` | `[x]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 109.1 $10M Net Worth Gate | `[x]` | `[ ]` |
| 109.2 Neo4j Lending | `[x]` | `[ ]` |
| 109.3 Tax Deferral Tracking | `[x]` | `[ ]` |
| 109.4 Estate & PE Nodes | `[x]` | `[ ]` |
| 109.5 RM Load Balancer | `[x]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py pb qualify <net_worth>` | Check PB qualification | `[x]` |
| `python cli.py pb lending status` | Show lending status | `[x]` |
| `python cli.py pb deferral list` | List tax deferrals | `[x]` |
| `python cli.py pb rm-capacity` | Check RM capacity | `[x]` |

---

*Last verified: 2026-01-25*
