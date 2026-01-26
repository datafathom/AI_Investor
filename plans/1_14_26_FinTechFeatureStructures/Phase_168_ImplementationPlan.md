# Phase 168: PPLI Insurance Wrapper Graph Integration

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Insurance Team

---

## 📋 Overview

**Description**: Integrate Private Placement Life Insurance (PPLI) deeply into the wealth graph. PPLI creates a "shell" where investments grow tax-free. The system must "look through" the policy to report on underlying asset allocation while respecting the legal wall that the Insurance Carrier is the owner.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 8

---

## 🎯 Sub-Deliverables

### 168.1 Neo4j PPLI Policy as Insurance Wrapper Node `[ ]`

**Acceptance Criteria**: Model the wrapper structure. The Policy owns a "Separate Account" (custody). The Separate Account holds the Assets. The Client owns the Policy.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:PERSON:CLIENT)-[:OWNS_POLICY]->(:PPLI_POLICY)
(:PPLI_POLICY)-[:WRAPS]->(:SEPARATE_ACCOUNT {custodian: "State Street"})
(:SEPARATE_ACCOUNT)-[:HOLDS]->(:ASSET:HEDGE_FUND)

// Look-through Query
MATCH (p:PPLI_POLICY)-[:WRAPS]->()-[:HOLDS]->(a:ASSET)
RETURN p.policy_number, sum(a.value) as total_value
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Wrapper Service | `services/neo4j/wrapper_service.py` | `[ ]` |

---

### 168.2 Postgres Tax-Free Growth + Loan Withdrawals Ledger `[ ]`

**Acceptance Criteria**: Tracking ledger. Growth inside the policy is not reported on 1099s. Withdrawals via "Loans" are not taxable income.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE ppli_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_id UUID NOT NULL,
    date DATE NOT NULL,
    
    -- Values
    cash_value DECIMAL(20, 2),
    death_benefit DECIMAL(20, 2),
    cost_basis DECIMAL(20, 2),         -- Premiums Paid
    
    -- Transactions
    premium_paid DECIMAL(20, 2) DEFAULT 0,
    policy_loan_taken DECIMAL(20, 2) DEFAULT 0,
    loan_interest_accrued DECIMAL(20, 2) DEFAULT 0,
    cost_of_insurance_deducted DECIMAL(20, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/168_ppli_ledger.sql` | `[ ]` |
| Ledger Manager | `services/insurance/ppli_ledger.py` | `[ ]` |

---

### 168.3 Modified Endowment Contract Avoidance Check `[ ]`

**Acceptance Criteria**: "MEC" Testing. If premiums are paid too quickly (7-Pay Test), the policy becomes a Modified Endowment Contract, losing tax-free loan withdrawals. System must block or warn against excessive premium payments.

| Component | File Path | Status |
|-----------|-----------|--------|
| MEC Tester | `services/compliance/mec_tester.py` | `[ ]` |

---

### 168.4 PPLI + Irrevocable Trust Asset Protection Flag `[ ]`

**Acceptance Criteria**: Verify ownership by an Asset Protection Trust (APT) or ILIT. If owned by an individual, it's exposed to creditors. If owned by APT, it's fortress-level protection.

| Component | File Path | Status |
|-----------|-----------|--------|
| Protection Logic | `services/legal/protection_verifier.py` | `[ ]` |

---

### 168.5 Cost-Amortization Tax Savings Schedule `[ ]`

**Acceptance Criteria**: Generate a schedule showing the "Breakeven Year". PPLI has high upfront costs (load factors) but saves massive taxes over time.

| Component | File Path | Status |
|-----------|-----------|--------|
| Amortization Calc | `services/analysis/ppli_amortization.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Policy Dashboard | `frontend2/src/components/Insurance/PolicyDashboard.jsx` | `[ ]` |
| Tax Equivalent Yield | `frontend2/src/components/Charts/TaxEquivalentYield.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py ppli check-mec` | Run 7-pay test | `[ ]` |
| `python cli.py ppli value <id>` | Get cash value | `[ ]` |

---

*Last verified: 2026-01-25*
