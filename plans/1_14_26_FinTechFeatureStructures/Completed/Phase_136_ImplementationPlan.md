# Phase 136: Indirect Leverage & Margin Monitor

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: Monitor indirect leverage through margin balances, options, and futures. Calculate "True Leverage" (gross exposure / equity) and implement safety stops to prevent margin calls or "blowing up" the account.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 16

---

## 🎯 Sub-Deliverables

### 136.1 Postgres Margin Balance/Interest Tracking `[x]`

**Acceptance Criteria**: Track margin loan balances and accrued interest daily. Calculate the effective annual interest rate (APR) paid on margin debt.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE margin_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    log_date DATE NOT NULL,
    
    -- Balances
    debit_balance DECIMAL(20, 2) NOT NULL,     -- Amount borrowed
    equity_balance DECIMAL(20, 2) NOT NULL,    -- Client's money
    market_value DECIMAL(20, 2) NOT NULL,      -- Total value
    
    -- Leverage Metrics
    margin_ratio DECIMAL(8, 6),                -- Debt / Equity
    maintenance_excess DECIMAL(20, 2),         -- Buffer before margin call
    
    -- Cost
    interest_rate_apr DECIMAL(5, 4),
    daily_interest_cost DECIMAL(10, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('margin_history', 'log_date');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/136_margin_history.sql` | `[x]` |
| Margin Tracker | `services/risk/margin_tracker.py` | `[x]` |
| Interest Calculator | `services/finance/interest_calculator.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Margin Dashboard | `frontend2/src/components/Risk/MarginDashboard.jsx` | `[x]` |
| Interest Cost Chart | `frontend2/src/components/Charts/MarginInterest.jsx` | `[x]` |

---

### 136.2 Equity vs. Borrowed Funds Kafka Monitor `[x]`

**Acceptance Criteria**: Stream real-time equity vs. debt ratios via Kafka to trigger immediate alerts if leverage spikes due to market drops.

#### Kafka Topic

```json
{
    "topic": "leverage-monitor",
    "schema": {
        "account_id": "uuid",
        "equity_pct": "decimal",
        "debt_pct": "decimal",
        "leverage_ratio": "decimal",
        "status": "SAFE | WARNING | CRITICAL",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Leverage Monitor | `services/kafka/leverage_monitor.py` | `[x]` |
| Alert Service | `services/alerts/leverage_alerts.py` | `[x]` |

---

### 136.3 Futures/Options Indirect Leverage Logic `[x]`

**Acceptance Criteria**: Calculate "Notional Leverage" from derivatives. E.g., holding 1 ES contract (S&P 500 future) is ~$250k notional exposure, even if margin requirement is only $15k.

```python
class IndirectLeverageCalculator:
    """
    Calculate True Leverage including derivatives.
    
    Formula:
    True Leverage = (Stock Value + Option Notional + Futures Notional) / Account Equity
    
    Example:
    - Equity: $100k
    - Stocks: $100k
    - 1 ES Future: $250k Notional
    - Total Exposure: $350k
    - Leverage: 3.5x (Dangerous)
    """
    
    def calculate_notional_exposure(self, holdings: list[Holding]) -> Decimal:
        """Sum notional value of all positions."""
        pass
    
    def calculate_true_leverage(self, portfolio: Portfolio) -> Decimal:
        """Calculate leverage ratio based on notional exposure."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Indirect Calc | `services/risk/indirect_leverage.py` | `[x]` |
| Notional Service | `services/market/notional_value.py` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Indirect Calc | `tests/unit/test_indirect_leverage.py` | `[x]` |
| Unit: Notional Service | `tests/unit/test_notional_value.py` | `[x]` |

---

### 136.4 Double-Edged Sword Simulator (±40%) `[x]`

**Acceptance Criteria**: Simulate the impact of leverage on returns. Show that 2x leverage doubles gains but can wipe out equity with a 50% drop.

| Component | File Path | Status |
|-----------|-----------|--------|
| Leverage Simulator | `services/simulation/leverage_sim.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Leverage Simulator UI | `frontend2/src/components/Simulator/LeverageSim.jsx` | `[x]` |

---

### 136.5 Margin Call Alert Trigger `[x]`

**Acceptance Criteria**: Predictive alert that triggers *before* a margin call happens (e.g., when buffer drops below 10%).

| Component | File Path | Status |
|-----------|-----------|--------|
| Pre-Call Trigger | `services/risk/pre_call_trigger.py` | `[x]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py risk leverage` | Show true leverage | `[x]` |
| `python cli.py risk margin` | Show margin utilization | `[x]` |

---

*Last verified: 2026-01-25*
