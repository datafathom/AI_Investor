# Phase 139: Risk-Free Rate (Treasury) Ingestion Service

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Data Infrastructure Team

---

## 📋 Overview

**Description**: Ingest and maintain a live "Risk-Free Rate" based on US Treasury yields (3-month, 10-year). This rate is the denominator for all excess return calculations (Sharpe, Alpha) and valuation models (DCF).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 19

---

## 🎯 Sub-Deliverables

### 139.1 10-Year Treasury API Integration `[ ]`

**Acceptance Criteria**: Connect to Treasury.gov or FRED API to fetch daily yield curve rates.

| Component | File Path | Status |
|-----------|-----------|--------|
| Treasury Client | `services/external/treasury_client.py` | `[ ]` |
| Yield Curve Fetcher | `services/market/yield_curve.py` | `[ ]` |

---

### 139.2 Postgres Risk-Free Rate History Table `[ ]`

**Acceptance Criteria**: Store historical rates to allow accurate point-in-time calculation of past Sharpe ratios (using the rate *at that time*).

#### Postgres Schema

```sql
CREATE TABLE risk_free_rates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rate_date DATE NOT NULL UNIQUE,
    
    -- Yields
    yield_1mo DECIMAL(5, 4),
    yield_3mo DECIMAL(5, 4),
    yield_2yr DECIMAL(5, 4),
    yield_10yr DECIMAL(5, 4),
    yield_30yr DECIMAL(5, 4),
    
    -- Inversion Check
    is_inverted_10y_2y BOOLEAN GENERATED ALWAYS AS (yield_10yr < yield_2yr) STORED,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('risk_free_rates', 'rate_date');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/139_risk_free_rates.sql` | `[ ]` |
| Rate Service | `services/market/risk_free_service.py` | `[ ]` |

---

### 139.3 Kafka Rate Change Broadcaster `[ ]`

**Acceptance Criteria**: Broadcast significant rate changes via Kafka to update valuation models and risk metrics instantly.

#### Kafka Topic

```json
{
    "topic": "market-rates",
    "schema": {
        "rate_type": "TREASURY_10Y",
        "current_rate": "decimal",
        "change_bps": "integer",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Rate Producer | `services/kafka/rate_producer.py` | `[ ]` |

---

### 139.4 Sharpe/Sortino Rate Subtraction Validator `[ ]`

**Acceptance Criteria**: Ensure that all risk calculators subtract the correct duration risk-free rate (e.g., 3-month T-Bill for annual Sharpe) to compute Excess Return.

| Component | File Path | Status |
|-----------|-----------|--------|
| Excess Return Calc | `services/quantitative/excess_return.py` | `[ ]` |

---

### 139.5 Global Risk-Free Rates (Bunds, Gilts) `[ ]`

**Acceptance Criteria**: Expand support for international portfolios by tracking German Bunds (Euro RFR) and UK Gilts.

| Component | File Path | Status |
|-----------|-----------|--------|
| Global Rates Adapter | `services/external/global_rates.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py rates current` | Show today's yields | `[ ]` |
| `python cli.py rates update` | Force fetch latest rates | `[ ]` |

---

*Last verified: 2026-01-25*
