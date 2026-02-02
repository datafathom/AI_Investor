# Phase 137: 529 Plan Tax-Free Growth & Penalty Logic

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Education Planning Team

---

## 📋 Overview

**Description**: Manage the tax-advantaged status of 529 Education Savings Plans. Track cumulative contributions (basis) vs. earnings, verify qualified expenses to avoid the 10% penalty, and handle successor ownership logic.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 17

---

## 🎯 Sub-Deliverables

### 137.1 Postgres Tax-Free Accumulation Ledger `[x]`

**Acceptance Criteria**: Maintain a ledger distinguishing between principal (after-tax contributions) and earnings (tax-free growth).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE education_plan_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(20) NOT NULL, -- CONTRIBUTION, DISTRIBUTION, EARNINGS
    
    -- Amounts
    amount DECIMAL(20, 2) NOT NULL,
    principal_portion DECIMAL(20, 2),      -- Return of basis
    earnings_portion DECIMAL(20, 2),       -- Gain/Loss
    
    -- Running Totals
    total_basis DECIMAL(20, 2),
    total_earnings DECIMAL(20, 2),
    
    -- Distribution Details
    is_qualified_expense BOOLEAN,
    expense_category VARCHAR(50),          -- TUITION, ROOM_BOARD, BOOKS
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('education_plan_ledger', 'transaction_date');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/137_education_ledger.sql` | `[x]` |
| Ledger Service | `services/education/ledger_service.py` | `[x]` |
| Basis Tracker | `services/tax/basis_tracker_529.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Growth Chart | `frontend2/src/components/Education/GrowthChart.jsx` | `[x]` |
| Withdrawal Wizard | `frontend2/src/components/Education/WithdrawalWizard.jsx` | `[x]` |

---

### 137.2 Qualified Education Expense Verifier `[x]`

**Acceptance Criteria**: Feature to tag and verify expenses (Tuition, Room & Board, Computer Equipment) against IRS guidelines.

```python
class ExpenseVerifier:
    """
    Verify 529 distributions are qualified.
    
    Qualified:
    - College Tuition & Fees
    - Room & Board (if >= half-time)
    - Books & Supplies
    - Computer & Internet
    - K-12 Tuition (up to $10k/yr)
    - Student Loan Repayment ($10k lifetime)
    """
    
    def verify_expense(
        self,
        amount: Decimal,
        category: str,
        student_status: str  # FULL_TIME, HALF_TIME, LESS_THAN_HALF
    ) -> VerificationResult:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Expense Verifier | `services/compliance/expense_verifier.py` | `[x]` |
| IRS Limit Config | `config/irs_education_limits.py` | `[x]` |

---

### 137.3 Non-Qualified Tax & Penalty Calculator `[x]`

**Acceptance Criteria**: Calculate the exact tax liability (Ordinary Income + 10% Penalty) on the earnings portion of non-qualified withdrawals.

| Component | File Path | Status |
|-----------|-----------|--------|
| Penalty Calculator | `services/tax/penalty_calculator_529.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Penalty Estimate | `frontend2/src/components/Education/PenaltyEstimate.jsx` | `[x]` |

---

### 137.4 Neo4j Grandparent vs. Parent Ownership `[x]`

**Acceptance Criteria**: Model ownership in Neo4j to manage FAFSA implications (Grandparent-owned 529s no longer count as student income on FAFSA as of 2024, but Parent-owned do count as assets).

#### Neo4j Schema

```cypher
(:PERSON:GRANDPARENT)-[:OWNS_529 {
    fafsa_asset_impact: false,
    fafsa_income_impact: false 
}]->(:529_PLAN)

(:PERSON:PARENT)-[:OWNS_529 {
    fafsa_asset_impact: true, -- 5.64% assessment rate
    fafsa_income_impact: false
}]->(:529_PLAN)

(:529_PLAN)-[:BENEFITS]->(:STUDENT)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Ownership Graph | `services/neo4j/529_ownership_graph.py` | `[x]` |
| FAFSA Impact Calc | `services/education/fafsa_impact.py` | `[x]` |

---

### 137.5 State Tax Credit Mapper `[x]`

**Acceptance Criteria**: Map state-specific tax deduction/credit rules (e.g., $10k deduction in NY, tax credit in IN) to optimize contributions.

| Component | File Path | Status |
|-----------|-----------|--------|
| State Tax Mapper | `services/tax/state_tax_mapper.py` | `[x]` |
| Credit Optimizer | `services/planning/credit_optimizer.py` | `[x]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py 529 balance` | Show principal/earnings | `[x]` |
| `python cli.py 529 verify-expense` | Check if expense qualifies | `[x]` |
| `python cli.py 529 fafsa-impact` | Calculate FAFSA impact | `[x]` |

---

*Last verified: 2026-01-25*
