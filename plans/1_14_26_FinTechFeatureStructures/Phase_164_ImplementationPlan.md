# Phase 164: Private Equity Leverage Buyout (LBO) Architecture

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Private Equity Team

---

## 📋 Overview

**Description**: Architect the data structures and logic for Private Equity "Leveraged Buyouts" (LBOs). This allows UHNW clients to model, track, and participate in direct company acquisitions where debt is used to amplify returns.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 4

---

## 🎯 Sub-Deliverables

### 164.1 LBO Calculator (EBITDA Growth, Cost Cutting, Debt Payback) `[ ]`

**Acceptance Criteria**: Quick LBO model. Inputs: Entry Multiple (e.g. 8x EBITDA), Debt/Equity Ratio (e.g. 60/40), Interest Rate, Revenue Growth, Margin Expansion. Outputs: IRR and MOIC (Multiple on Invested Capital).

```python
class LBOCalculator:
    """
    Calculate LBO Returns.
    
    Drivers:
    1. Deleveraging (Paying down debt).
    2. EBITDA Growth (Operational improvements).
    3. Multiple Expansion (Selling for higher multiple).
    """
    def calculate_returns(
        self,
        entry_ebitda: Decimal,
        entry_multiple: Decimal,
        debt_amount: Decimal,
        exit_year: int,
        growth_rate: Decimal
    ) -> LBOResult:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| LBO Engine | `services/pe/lbo_engine.py` | `[ ]` |
| API Endpoint | `web/api/pe/lbo_calc.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| LBO Modeler | `frontend2/src/components/PE/LBOModeler.jsx` | `[ ]` |
| Paydown Chart | `frontend2/src/components/Charts/DebtPaydown.jsx` | `[ ]` |

---

### 164.2 Neo4j Private Company ↔ PE/LBO Fund Nodes `[ ]`

**Acceptance Criteria**: Graph modeling of the PE ecosystem. Funds own Companies. Companies have Debt.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:PE_FIRM {name: "Blackstone"})-[:MANAGES]->(:FUND {name: "BREP IX"})

(:FUND)-[:ACQUIRED {
    date: date("2024-01-01"),
    ownership_pct: 0.95,
    deal_size: 500000000
}]->(:PRIVATE_COMPANY {name: "Hilton"})

(:PRIVATE_COMPANY)-[:HAS_DEBT]->(:LOAN_TRANCHE {
    amount: 300000000,
    rate_spread: 450, -- SOFR + 450bps
    maturity: date("2029-01-01")
})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| PE Graph Service | `services/neo4j/pe_graph.py` | `[ ]` |

---

### 164.3 Postgres Growth Equity vs. LBO Returns Tracker `[ ]`

**Acceptance Criteria**: Track performance of different PE strategies. LBO (Debt-fueled, lower growth) vs. Growth Equity (No debt, high growth, minority stakes).

#### Postgres Schema

```sql
CREATE TABLE pe_deal_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_name VARCHAR(100),
    strategy VARCHAR(20),              -- LBO, GROWTH, VENTURE
    vintage_year INTEGER,
    
    -- Metrics
    invested_capital DECIMAL(20, 2),
    current_nav DECIMAL(20, 2),
    distributions DECIMAL(20, 2),
    
    -- Calc
    moic DECIMAL(5, 2),                -- Multiple of Invested Capital
    irr DECIMAL(5, 2),                 -- Internal Rate of Return
    dpi DECIMAL(5, 2),                 -- Distributions to Paid-In
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/164_pe_performance.sql` | `[ ]` |
| Returns Tracker | `services/pe/returns_tracker.py` | `[ ]` |

---

### 164.4 Vintage Year Market Cycle Tracker `[ ]`

**Acceptance Criteria**: Analyze returns by "Vintage Year" (year funding began). PE returns are highly correlated to the economic cycle of the vintage year.

| Component | File Path | Status |
|-----------|-----------|--------|
| Vintage Analyzer | `services/analysis/vintage_analyzer.py` | `[ ]` |

---

### 164.5 Kafka Liquidity Event Trigger (Acquisition, IPO) `[ ]`

**Acceptance Criteria**: Trigger notifications when a portfolio company has a "Liquidity Event" (IPO, Sale), resulting in a cash distribution to the LPs.

#### Kafka Topic

```json
{
    "topic": "pe-liquidity-events",
    "schema": {
        "fund_id": "uuid",
        "company_name": "string",
        "event_type": "IPO",
        "distribution_per_share": "decimal",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Event Producer | `services/kafka/pe_event_producer.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py pe calc-lbo` | Run quick LBO model | `[ ]` |
| `python cli.py pe vintage-stats <year>` | Show vintage stats | `[ ]` |

---

*Last verified: 2026-01-25*
