# Phase 145: Dynasty Trust Multi-Generational Payout Engine

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Estate Planning Team

---

## 📋 Overview

**Description**: Architect a "Dynasty Trust" engine designed to last essentially forever (perpetuity). It manages multi-generational payouts, avoids the "Rule Against Perpetuities" where legally possible (e.g., Delaware, South Dakota), and minimizes Generation-Skipping Transfer (GST) tax.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 5

---

## 🎯 Sub-Deliverables

### 145.1 Perpetual Payout Estate Tax Bypass Logic `[ ]`

**Acceptance Criteria**: Ensure assets grow outside the taxable estate of future generations. Payouts are "Income Only" or "HEMS" (Health, Education, Maintenance, Support) to prevent assets from becoming part of a beneficiary's taxable estate.

#### Backend Implementation

```python
class DynastyPayoutEngine:
    """
    Calculate allowable distributions for Dynasty Trusts.
    
    Principles:
    - Principal is rarely distributed (to preserve capital).
    - Income is distributed to avoid Trust Tax Rates (compressed brackets).
    - Distributions strictly limited to HEMS standard to avoid estate inclusion.
    """
    
    def calculate_allowable_distribution(
        self,
        trust_assets: Portfolio,
        beneficiary_needs: ExpenseRequest,
        standard: str = 'HEMS'
    ) -> DistributionResult:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Payout Engine | `services/estate/dynasty_payout.py` | `[ ]` |
| HEMS Validator | `services/compliance/hems_validator.py` | `[ ]` |

---

### 145.2 Inter-Generational Transfer GST Ledger `[ ]`

**Acceptance Criteria**: Trace the allocation of the GST Tax Exemption (currently ~$13.6M) to ensuring the trust remains "GST Exempt" (Zero Inclusion Ratio).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE gst_exemption_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trust_id UUID NOT NULL,
    transaction_date DATE NOT NULL,
    
    -- Contribution
    contribution_amount DECIMAL(20, 2),
    gst_exemption_allocated DECIMAL(20, 2),
    
    -- Ratios
    inclusion_ratio DECIMAL(5, 4),         -- 0.0 = Fully Exempt, 1.0 = Fully Taxable
    applicable_fraction DECIMAL(5, 4),     -- 1 - Inclusion Ratio
    
    -- Tax Event
    taxable_distribution_amount DECIMAL(20, 2),
    gst_tax_due DECIMAL(20, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/145_gst_ledger.sql` | `[ ]` |
| GST Calculator | `services/tax/gst_calculator.py` | `[ ]` |

---

### 145.3 Neo4j Heir Payout History Graph `[ ]`

**Acceptance Criteria**: Graph visualization of payouts across generations to track "equality" (e.g., per stirpes vs. per capita) and ensure fairness over decades.

#### Neo4j Schema

```cypher
(:TRUST:DYNASTY)-[:DISTRIBUTED {year: 2024, amount: 50000}]->(:PERSON:GENERATION_2 {name: "Child"})
(:TRUST:DYNASTY)-[:DISTRIBUTED {year: 2024, amount: 25000}]->(:PERSON:GENERATION_3 {name: "Grandchild A"})
(:TRUST:DYNASTY)-[:DISTRIBUTED {year: 2024, amount: 25000}]->(:PERSON:GENERATION_3 {name: "Grandchild B"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Generation Graph | `services/neo4j/generation_graph.py` | `[ ]` |
| Fairness Monitor | `services/estate/fairness_monitor.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Family Tree Payouts | `frontend2/src/components/Estate/FamilyTreePayouts.jsx` | `[ ]` |

---

### 145.4 Trust Owns Assets Perpetual Service `[ ]`

**Acceptance Criteria**: Service validating that assets are *never* retitled into an individual's name, preventing a "step-up in basis" miss or estate inclusion error.

| Component | File Path | Status |
|-----------|-----------|--------|
| Retitle Blocker | `services/custody/retitle_blocker.py` | `[ ]` |

---

### 145.5 Tax Savings Dynasty Simulator `[ ]`

**Acceptance Criteria**: Simulator showing the compounding difference between a Dynasty Trust (0% estate tax at each generation) vs. outright inheritance (40% tax every generation).

| Component | File Path | Status |
|-----------|-----------|--------|
| Compounding Sim | `services/simulation/dynasty_sim.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Legacy Calculator | `frontend2/src/components/Simulator/LegacyCalculator.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py dynasty status` | Show exemption status | `[ ]` |
| `python cli.py dynasty simulate <years>` | Run tax savings sim | `[ ]` |

---

*Last verified: 2026-01-25*
