# Phase 147: Charitable Remainder Trust (CRT) Split-Interest Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax & Philanthropy Team

---

## 📋 Overview

**Description**: Implement the logic for Charitable Remainder Trusts (CRTs). A CRT allows a user to sell highly appreciated assets *tax-free* inside the trust, receive an income stream for life (Lead Interest), and donate the remainder to charity (Remainder Interest), receiving an immediate income tax deduction.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 7

---

## 🎯 Sub-Deliverables

### 147.1 Life Income Payout Service (IRS minimums) `[ ]`

**Acceptance Criteria**: Calculate the annual payout (Unitrust or Annuity). Verify it meets IRS 5% minimum and 50% maximum rules.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE crt_distributions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trust_id UUID NOT NULL,
    year INTEGER NOT NULL,
    
    -- Rules
    payout_type VARCHAR(10),               -- CRUT (%), CRAT (Fixed $)
    payout_rate DECIMAL(5, 4),             -- e.g. 0.06 (6%)
    
    -- Calculation
    trust_value_jan1 DECIMAL(20, 2),
    required_distribution DECIMAL(20, 2),
    
    -- Execution
    distributed_amount DECIMAL(20, 2),
    distribution_date DATE,
    tier_source VARCHAR(50),               -- ORINDARY, CAP_GAIN, EXEMPT, CORPUS
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/147_crt_distributions.sql` | `[ ]` |
| Distribution Calc | `services/trusts/crt_distribution.py` | `[ ]` |

---

### 147.2 Remainder Assets Transfer Trigger `[ ]`

**Acceptance Criteria**: Trigger the transfer of remaining assets to the designated charity upon the death of the income beneficiary or end of term.

| Component | File Path | Status |
|-----------|-----------|--------|
| Remainder Trigger | `services/trusts/remainder_trigger.py` | `[ ]` |

---

### 147.3 Tax Deduction Calculator `[ ]`

**Acceptance Criteria**: Calculate the present value of the charitable remainder interest (must be at least 10% of initial value) to determine the immediate income tax deduction.

```python
class CRTeductionCalculator:
    """
    Calculate PV of remainder using IRS 7520 rate.
    """
    def calculate_deduction(
        self,
        principal: Decimal,
        payout_rate: Decimal,
        term_years: int,
        irs_7520_rate: Decimal
    ) -> DeductionResult:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Deduction Calc | `services/tax/crt_deduction.py` | `[ ]` |
| IRS Rate Fetcher | `services/external/irs_rates.py` | `[ ]` |

---

### 147.4 Neo4j Grantor → Charity Relationship `[ ]`

**Acceptance Criteria**: Graph relationship linking the Grantor to the Charity via the CRT vehicle.

```cypher
(:PERSON:GRANTOR)-[:ESTABLISHED]->(:TRUST:CRT)
(:TRUST:CRT)-[:PAYS_INCOME]->(:PERSON:GRANTOR)
(:TRUST:CRT)-[:REMAINDER_TO]->(:CHARITY)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| CRT Graph Service | `services/neo4j/crt_graph.py` | `[ ]` |

---

### 147.5 Qualified Charity Status Verifier `[ ]`

**Acceptance Criteria**: Verify the designated remainder beneficiary is a valid 501(c)(3) organization using IRS Exempt Organizations Select Check.

| Component | File Path | Status |
|-----------|-----------|--------|
| Charity Verifier | `services/compliance/charity_verifier.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py crt calc-deduction` | Calculate tax break | `[ ]` |
| `python cli.py crt verify-charity` | Check 501c3 status | `[ ]` |

---

*Last verified: 2026-01-25*
