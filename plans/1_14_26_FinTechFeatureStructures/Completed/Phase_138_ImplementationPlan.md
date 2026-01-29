# Phase 138: Risk-Adjusted Performance Dashboard

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Create a centralized dashboard for advanced risk-adjusted performance metrics. Move beyond simple returns to show Sharpe, Sortino, Treynor ratios, and Information Ratio, providing a professional-grade view of portfolio efficiency.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 18

---

## 🎯 Sub-Deliverables

### 138.1 Rolling 3-Year Sharpe/Sortino UI `[x]`

**Acceptance Criteria**: Implement rolling window charts for risk metrics (3-year rolling Sharpe) to show consistency of performance over time.

| Component | File Path | Status |
|-----------|-----------|--------|
| Rolling Metrics Calc | `services/quantitative/rolling_metrics.py` | `[x]` |
| Metrics API | `web/api/performance/risk_metrics.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Dashboard | `frontend2/src/components/Performance/RiskDashboard.jsx` | `[x]` |
| Rolling Metric Chart | `frontend2/src/components/Charts/RollingMetricChart.jsx` | `[x]` |

---

### 138.2 Manager Ranking by Sortino `[x]`

**Acceptance Criteria**: Rank different portfolios or managers primarily by Sortino Ratio (downside efficiency) rather than raw return.

| Component | File Path | Status |
|-----------|-----------|--------|
| Ranker Service | `services/analysis/manager_ranker.py` | `[x]` |

---

### 138.3 Postgres Historical Risk Metrics Storage `[x]`

**Acceptance Criteria**: Store calculated daily risk metrics history for trend analysis and reporting.

#### Postgres Schema

```sql
CREATE TABLE risk_metrics_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    metric_date DATE NOT NULL,
    
    -- Ratios (Annualized)
    sharpe_ratio DECIMAL(8, 4),
    sortino_ratio DECIMAL(8, 4),
    treynor_ratio DECIMAL(8, 4),
    information_ratio DECIMAL(8, 4),
    calmar_ratio DECIMAL(8, 4),
    
    -- Components
    annualized_return DECIMAL(8, 4),
    annualized_volatility DECIMAL(8, 4),
    max_drawdown DECIMAL(8, 4),
    beta DECIMAL(8, 4),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('risk_metrics_history', 'metric_date');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/138_risk_metrics.sql` | `[x]` |
| Storage Service | `services/data/risk_metrics_storage.py` | `[x]` |

---

### 138.4 Kafka End-of-Day NAV Stream `[x]`

**Acceptance Criteria**: Stream daily Net Asset Value (NAV) snapshots to trigger risk recalculations overnight.

#### Kafka Topic

```json
{
    "topic": "eod-nav-snapshots",
    "schema": {
        "portfolio_id": "uuid",
        "date": "date",
        "nav": "decimal",
        "cash_balance": "decimal",
        "positions_value": "decimal",
        "daily_return_pct": "decimal"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| NAV Producer | `services/kafka/nav_producer.py` | `[x]` |
| Risk Calculator Consumer | `services/kafka/risk_calc_consumer.py` | `[x]` |

---

### 138.5 Portfolio Stress Test Sharpe Projection `[x]`

**Acceptance Criteria**: Project how Sharpe Ratio would degrade under various stress scenarios (e.g., interest rate spike, recession).

| Component | File Path | Status |
|-----------|-----------|--------|
| Stress Test Engine | `services/simulation/stress_sharpe.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Stress Test UI | `frontend2/src/components/Simulator/StressTestRisk.jsx` | `[x]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py perfromance risk` | Show current risk metrics | `[x]` |
| `python cli.py performance rolling <metric>` | Show rolling history | `[x]` |

---

*Last verified: 2026-01-25*
