# Phase 167: Borrowing Against Concentrated Stock (UHNW)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Private Banking & Lending Team

---

## 📋 Overview

**Description**: Implement systems for UHNW clients to borrow against concentrated stock positions(e.g., a founder with $1B in one stock) using "Prepaid Variable Forward Contracts" (PVFC) or Margin Loans. This provides liquidity without triggering an immediate capital gains tax event.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 7

---

## 🎯 Sub-Deliverables

### 167.1 Stock Loan Service ($250M loan on $1B stock) `[ ]`

**Acceptance Criteria**: Service to model loan terms. Loan-to-Value (LTV) is usually lower for single stocks (20-50%) than diversified portfolios. Calculate capacity based on volatility and liquidity.

#### Backend Implementation

```python
class LendingCapacityEngine:
    """
    Calculate borrowing capacity for concentrated positions.
    """
    def calculate_ltv(self, ticker: str, volatility: Decimal) -> Decimal:
        """
        Determine max LTV based on risk.
        Low Vol (KO, JNJ) -> 50% LTV
        High Vol (TSLA, NVDA) -> 25% LTV
        """
        base_ltv = Decimal('0.50')
        if volatility > 0.40:
            return Decimal('0.20')
        elif volatility > 0.20:
            return Decimal('0.35')
        return base_ltv
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Lending Engine | `services/lending/stock_loan.py` | `[ ]` |
| Volatility Service | `services/market/volatility_feed.py` | `[ ]` |

---

### 167.2 Postgres Interest-Tax Spread Analyzer (10% vs. 24.8%) `[ ]`

**Acceptance Criteria**: Compare the cost of borrowing (Interest Expense) vs. the cost of selling (Capital Gains Tax). If Rate < Tax Drag on Return, borrowing wins.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE lending_tax_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    position_id UUID NOT NULL,
    current_value DECIMAL(20, 2),
    cost_basis DECIMAL(20, 2),
    
    -- Scenarios
    tax_cost_sell DECIMAL(20, 2),      -- (Value - Basis) * TaxRate
    loan_cost_1yr DECIMAL(20, 2),      -- LoanAmount * InterestRate
    loan_cost_5yr DECIMAL(20, 2),
    
    -- Decision
    break_even_years DECIMAL(5, 2),
    recommendation VARCHAR(20),        -- BORROW or SELL
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/167_lending_analysis.sql` | `[ ]` |
| Spread Analyzer | `services/analysis/borrow_vs_sell.py` | `[ ]` |

---

### 167.3 Kafka Margin Call Alert (Collateral Drop) `[ ]`

**Acceptance Criteria**: Real-time alerts if the concentrated stock drops significantly, threatening a margin call. UHNW loans usually have "Cure Periods" allowed.

#### Kafka Topic

```json
{
    "topic": "collateral-alerts",
    "schema": {
        "loan_id": "uuid",
        "ticker": "string",
        "current_price": "decimal",
        "drop_pct": "decimal",
        "cushion_remaining": "decimal",
        "status": "WARNING",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Alert Producer | `services/kafka/collateral_monitor.py` | `[ ]` |

---

### 167.4 Neo4j Concentrated Position ↔ Lending Bank `[ ]`

**Acceptance Criteria**: Map the pledge relationship. The stock acts as collateral for the loan. If the bank is different from the custodian, track the "Control Agreement" (ACA).

```cypher
(:ASSET:STOCK {ticker: "AMZN"})-[:PLEDGED_AS_COLLATERAL {
    amount_shares: 1000000,
    release_price: 250.00
}]->(:LOAN {principal: 50000000})

(:LOAN)-[:ISSUED_BY]->(:BANK {name: "Goldman Sachs"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Collateral Graph | `services/neo4j/collateral_graph.py` | `[ ]` |

---

### 167.5 Interest-Only Payment Schedule Tracker `[ ]`

**Acceptance Criteria**: Track "Interest-Only" lines of credit. Unlike mortgages, principal is rarely paid down until the "Liquidity Event" (death or final sale).

| Component | File Path | Status |
|-----------|-----------|--------|
| Payment Tracker | `services/lending/payment_sched.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidity Access Dashboard | `frontend2/src/components/Lending/LiquidityAccess.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py lend calc-capacity` | Check borrow limit | `[ ]` |
| `python cli.py lend analyze-spread` | Borrow vs Sell | `[ ]` |

---

*Last verified: 2026-01-25*
