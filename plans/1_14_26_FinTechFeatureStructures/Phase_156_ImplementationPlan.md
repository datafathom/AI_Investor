# Phase 156: Trust-Held Life Insurance (ILIT) Architect

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Insurance & Legal Team

---

## 📋 Overview

**Description**: Manage Irrevocable Life Insurance Trusts (ILITs). These structures hold life insurance policies *outside* of the insured's estate, ensuring the death benefit remains 100% estate tax-free. Requires strict adherence to "Crummey Letters" and premium gifting rules.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 16

---

## 🎯 Sub-Deliverables

### 156.1 Neo4j ILIT Node for Insurance Policies `[ ]`

**Acceptance Criteria**: Establish the ILIT as the *Owner* and *Beneficiary* of the policy in Neo4j. The Insured Person effectively has no ownership rights (incidents of ownership).

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:TRUST:ILIT {
    id: "uuid",
    name: "John Doe Insurance Trust",
    tax_id: "XX-XXXXXXX"
})

(:POLICY:LIFE_INSURANCE {
    policy_number: "LI-123456",
    death_benefit: 5000000,
    carrier: "MassMutual"
})

// Correct Structure
(:TRUST:ILIT)-[:OWNS]->(:POLICY:LIFE_INSURANCE)
(:POLICY:LIFE_INSURANCE)-[:INSURES]->(:PERSON {name: "John Doe"})
(:POLICY:LIFE_INSURANCE)-[:PAYS_BENEFIT_TO]->(:TRUST:ILIT)

// INCORRECT Structure (Flag as Error)
(:PERSON)-[:OWNS]->(:POLICY:LIFE_INSURANCE)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| ILIT Graph Service | `services/neo4j/ilit_graph.py` | `[ ]` |
| Structure Validator | `services/insurance/structure_validator.py` | `[ ]` |

---

### 156.2 Crummey Power Notice Tracking Schema `[ ]`

**Acceptance Criteria**: Track "Crummey Letters". When the Grantor gifts money to the ILIT to pay premiums, beneficiaries must be notified of their (temporary) right to withdraw that money. This technicality qualifies the gift for the Annual Gift Tax Exclusion ($18k in 2024).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE crummey_notices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ilit_id UUID NOT NULL,
    gift_id UUID NOT NULL,
    
    -- Notification Details
    beneficiary_id UUID NOT NULL,
    notice_sent_date DATE NOT NULL,
    withdrawal_window_days INTEGER DEFAULT 30,
    withdrawal_deadline DATE GENERATED ALWAYS AS (notice_sent_date + withdrawal_window_days) STORED,
    
    -- Status
    status VARCHAR(20),                -- SENT, RECEIVED, WAIVED, EXPIRED
    proof_of_receipt_url VARCHAR(255), -- PDF Scan
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/156_crummey_notices.sql` | `[ ]` |
| Notice Generator | `services/estate/crummey_generator.py` | `[ ]` |
| Deadline Tracker | `services/estate/crummey_tracker.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Crummey Dashboard | `frontend2/src/components/Estate/CrummeyDashboard.jsx` | `[ ]` |

---

### 156.3 ILIT Sole Owner/Beneficiary Gate `[ ]`

**Acceptance Criteria**: Automated check to ensure the policy is *never* retitled back to the insured individually, which would trigger the "3-Year Rule" and pull the death benefit back into the taxable estate.

| Component | File Path | Status |
|-----------|-----------|--------|
| Owner Gate | `services/compliance/ilit_owner_gate.py` | `[ ]` |

---

### 156.4 Estate Tax Liability Reducer (Zero Tax) `[ ]`

**Acceptance Criteria**: Calculator showing the "Net Benefit" of the ILIT strategy: (Death Benefit * 40%) saved in estate taxes.

```python
class ILITBenefitCalculator:
    """
    Calculate estate tax savings from ILIT.
    """
    def calculate_savings(self, death_benefit: Decimal, estate_rate: Decimal = 0.40) -> Decimal:
        return death_benefit * estate_rate
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Benefit Calc | `services/tax/ilit_benefit.py` | `[ ]` |

---

### 156.5 Premium Payment Stream Mapping `[ ]`

**Acceptance Criteria**: Automate the flow: Grantor Bank -> ILIT Bank (Gift) -> Carrier (Premium). Ensure the "Gift" step happens before the "Premium" step to maintain trust integrity.

| Component | File Path | Status |
|-----------|-----------|--------|
| Payment Flow | `services/payment/ilit_flow.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py ilit send-notices` | Generate Crummey Notices | `[ ]` |
| `python cli.py ilit verify-owner` | Check Neo4j ownership | `[ ]` |

---

*Last verified: 2026-01-25*
