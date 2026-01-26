# Phase 146: PPLI Eligibility & Tax-Free Growth Wrapper

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Insurance & Tax Team

---

## 📋 Overview

**Description**: Implement Private Placement Life Insurance (PPLI) logic. This "Super Roth" for the ultra-wealthy creates a tax-free wrapper around hedge funds and high-tax assets. Requires strict eligibility checks ($10M+ NW) and diversification rules.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 6

---

## 🎯 Sub-Deliverables

### 146.1 Neo4j PPLI Insurance Wrapper Node `[ ]`

**Acceptance Criteria**: Model PPLI policies in Neo4j, showing the policy wrapping underlying investment accounts.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:PPLI_POLICY {
    id: "uuid",
    carrier: "Lombard International",
    policy_number: "P-998877",
    death_benefit: 25000000,
    cash_value: 5000000,
    cost_of_insurance_bps: 65
})

(:HEDGE_FUND {name: "Millennium"})<-[:INVESTED_IN {amount: 2000000}]-(:SEPARATE_ACCOUNT)
(:SEPARATE_ACCOUNT)-[:WRAPPED_BY]->(:PPLI_POLICY)
(:PPLI_POLICY)-[:OWNED_BY]->(:IRREVOCABLE_TRUST)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| PPLI Graph Service | `services/neo4j/ppli_graph.py` | `[ ]` |

---

### 146.2 Tax-Free Withdrawal Logic `[ ]`

**Acceptance Criteria**: Implement the "Wash Loan" logic. Withdrawals are structured as policy loans (tax-free) rather than distributions (taxable), reducing cash value but keeping the policy in force.

```python
class PPLIWithdrawalEngine:
    """
    Manage tax-free access to PPLI cash value via policy loans.
    
    Constraint: Loan amount must not cause policy lapse.
    Equation: Cash Value - Loan balance > Cost of Insurance for X years.
    """
    
    def calculate_max_loan(self, policy_id: UUID) -> MaxLoanResult:
        pass
    
    def project_lapse_risk(self, loan_amount: Decimal) -> LapseProjection:
        """Project when policy will lapse if loan is taken."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Withdrawal Engine | `services/insurance/ppli_withdrawal.py` | `[ ]` |
| Loan Tracker | `services/insurance/loan_tracker.py` | `[ ]` |

---

### 146.3 $1M Income / $10M Net Worth Gate `[ ]`

**Acceptance Criteria**: Strict KYC gate. PPLI is only for "Qualified Purchasers" (>$5M investments). System must block setup if financial criteria aren't met.

| Component | File Path | Status |
|-----------|-----------|--------|
| Acceditation Gate | `services/compliance/ppli_gate.py` | `[ ]` |

---

### 146.4 Cost-to-Setup vs. Tax Savings Analyzer `[ ]`

**Acceptance Criteria**: Calculator comparing high setup costs (legal, M&E, COI) vs. long-term tax drag of a taxable portfolio. PPLI usually makes sense only >$5M assets and >10 year horizon.

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Breakeven Calculator | `frontend2/src/components/Insurance/PPLIBreakeven.jsx` | `[ ]` |
| Fee Drag Chart | `frontend2/src/components/Charts/FeeVsTaxChart.jsx` | `[ ]` |

---

### 146.5 PPLI + Irrevocable Trust Asset Protection `[ ]`

**Acceptance Criteria**: Verify that the PPLI policy is owned by an Irrevocable Life Insurance Trust (ILIT) for maximum estate tax + creditor protection.

| Component | File Path | Status |
|-----------|-----------|--------|
| Structure Validator | `services/legal/ppli_structure.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py ppli check-eligibility` | Check QP status | `[ ]` |
| `python cli.py ppli sim-loan` | Simulate policy loan | `[ ]` |

---

*Last verified: 2026-01-25*
