# Phase 171: Private Credit & Debt Syndication Tracker

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Private Credit Team

---

## 📋 Overview

**Description**: Manage investments in Private Credit (Direct Lending). UHNW investors act as the bank, lending to middle-market companies at high rates (e.g., SOFR + 6%). Requires tracking loan tapes, default rates, and payment schedules that are often manual/PDF-based.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 11

---

## 🎯 Sub-Deliverables

### 171.1 Loan Tape Ingestion Engine `[ ]`

**Acceptance Criteria**: System to ingest "Loan Tapes" (Excel spreadsheets) from managers showing the status of 100+ underlying loans in a private credit fund.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE private_loan_positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fund_id UUID NOT NULL,
    borrower_name VARCHAR(255),
    sector VARCHAR(50),
    
    -- Loan Terms
    principal_balance DECIMAL(20, 2),
    interest_rate_spread DECIMAL(5, 4), -- 6.5% = 0.065
    floor_rate DECIMAL(5, 4),
    maturity_date DATE,
    
    -- Status
    payment_status VARCHAR(20),         -- CURRENT, WATCHLIST, DEFAULT
    ltv_ratio DECIMAL(5, 4),
    
    data_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/171_loan_tape.sql` | `[ ]` |
| Tape Ingester | `services/ingestion/tape_ingester.py` | `[ ]` |

---

### 171.2 Default Risk & Recovery Rate Projector `[ ]`

**Acceptance Criteria**: Calculator estimating expected losses. Yield = Gross Interest - (Default Rate * (1 - Recovery Rate)).

```python
class CreditRiskModel:
    def calculate_net_yield(
        self, 
        gross_yield: Decimal, 
        default_probability: Decimal, 
        recovery_rate: Decimal
    ) -> Decimal:
        loss_given_default = 1 - recovery_rate
        expected_loss = default_probability * loss_given_default
        return gross_yield - expected_loss
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Model | `services/credit/risk_model.py` | `[ ]` |

---

### 171.3 Payment Waterfall Distribution (Interest vs Principal) `[ ]`

**Acceptance Criteria**: Track cash flows. Private credit pays monthly/quarterly interest (Income) but principal is often bullet at maturity.

| Component | File Path | Status |
|-----------|-----------|--------|
| Waterfall Service | `services/credit/waterfall_dist.py` | `[ ]` |

---

### 171.4 Neo4j Borrower Constraint Graph `[ ]`

**Acceptance Criteria**: Graph modeling covenants. Ensure borrower is not violating Debt/EBITDA ratios.

```cypher
(:BORROWER)-[:BOUND_BY]->(:COVENANT {
    type: "MAX_LEVERAGE",
    limit: 4.5,
    current: 4.2
})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Covenant Graph | `services/neo4j/covenant_graph.py` | `[ ]` |

---

### 171.5 Floating Rate vs. Fixed Rate Exposure Analyzer `[ ]`

**Acceptance Criteria**: Analyze sensitivity to interest rates. Private Credit is usually Floating Rate (good when rates rise), unlike Bonds (Fixed).

| Component | File Path | Status |
|-----------|-----------|--------|
| Rate Analyzer | `services/analysis/rate_exposure.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Credit Dashboard | `frontend2/src/components/Credit/Dashboard.jsx` | `[ ]` |
| Loan Tape Viewer | `frontend2/src/components/Credit/LoanTapeViewer.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py credit ingest-tape <file>` | Load loan tape | `[ ]` |
| `python cli.py credit calc-risk` | Show net yield | `[ ]` |

---

*Last verified: 2026-01-25*
