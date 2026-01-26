# Phase 194: Bank Sweep Revenue & Overnight Liquidity Tracker

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Treasury Team

---

## 📋 Overview

**Description**: Manage cash. Brokerages make billions by sweeping client cash into low-yield accounts (0.01%) and keeping the interest. This phase implements an automated "Cash Sweep" to high-yield Treasuries or Money Market Funds (5%+), reclaiming that revenue for the client.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 14

---

## 🎯 Sub-Deliverables

### 194.1 Cash Drag Alert System `[ ]`

**Acceptance Criteria**: Alert if uninvested cash > 2% of portfolio. "Lazy Cash" is a major drag on long-term returns.

| Component | File Path | Status |
|-----------|-----------|--------|
| Drag Monitor | `services/alerts/cash_drag.py` | `[ ]` |

---

### 194.2 Auto-Sweep to Treasury Money Market (Tickers: SGOV, BIL) `[ ]`

**Acceptance Criteria**: Execution logic. Every night (or week), identify excess cash and buy cash-equivalent ETFs (SGOV, BIL, USFR) to earn the Risk-Free Rate.

```python
class CashSweeper:
    """
    Automated cash management.
    """
    def generate_sweep_orders(self, portfolio: Portfolio) -> list[Order]:
        excess_cash = portfolio.cash - self.calculate_buffer(portfolio)
        if excess_cash > 1000:
            return [Order(action='BUY', ticker='SGOV', amount=excess_cash)]
        return []
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Sweep Engine | `services/trading/sweep_engine.py` | `[ ]` |

---

### 194.3 Postgres Interest Rate Arb Log `[ ]`

**Acceptance Criteria**: Track "Lost Opportunity Cost". Difference between Bank Sweep Rate (0.05%) and Fed Funds Rate (5.33%). Show client "Found Money".

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE cash_yield_arb (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    date DATE NOT NULL,
    
    cash_balance DECIMAL(20, 2),
    broker_yield DECIMAL(5, 4),
    market_yield DECIMAL(5, 4),
    
    daily_lost_revenue DECIMAL(10, 2) GENERATED ALWAYS AS (cash_balance * (market_yield - broker_yield) / 365) STORED,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/194_yield_arb.sql` | `[ ]` |
| Arb Calculator | `services/analysis/yield_arb.py` | `[ ]` |

---

### 194.4 FDIC Insurance Limit Breaker (>$250k) `[ ]`

**Acceptance Criteria**: Split cash across multiple banks (Program Banks) to maximize FDIC coverage if holding actual cash.

| Component | File Path | Status |
|-----------|-----------|--------|
| FDIC Optimizer | `services/treasury/fdic_split.py` | `[ ]` |

---

### 194.5 Treasury Ladder Builder (4-Week, 8-Week Bills) `[ ]`

**Acceptance Criteria**: Build a "T-Bill Ladder" for larger cash piles. Maturities rolling every week to ensure liquidity while capturing yield curve premiums.

| Component | File Path | Status |
|-----------|-----------|--------|
| Ladder Builder | `services/strategies/ladder_builder.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Treasury Dashboard | `frontend2/src/components/Treasury/Dashboard.jsx` | `[ ]` |
| Smart Cash Toggle | `frontend2/src/components/Settings/SmartCash.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py treasury sweep` | Run auto sweep | `[ ]` |
| `python cli.py treasury show-lost` | Show lost interest | `[ ]` |

---

*Last verified: 2026-01-25*
