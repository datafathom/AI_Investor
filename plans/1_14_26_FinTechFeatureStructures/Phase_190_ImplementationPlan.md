# Phase 190: Michael Green 'Forced Seller' Liquidity Tracker

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Model the "Forced Seller" dynamic in markets. Identify players who *must* sell regardless of price (Margin Calls, Risk Parity De-leveraging, Target Date Fund rebalancing). Trading against forced sellers is one of the few sources of true alpha.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 10

---

## 🎯 Sub-Deliverables

### 190.1 Risk Parity De-leveraging Signal `[ ]`

**Acceptance Criteria**: Monitor volatility relative to historical norms. When Vol spikes, Risk Parity funds (Bridgewater All Weather) mechanically sell assets to maintain constant volatility. Predict this flow.

```python
class RiskParityMonitor:
    """
    Predict selling pressure from Risk Parity funds.
    """
    def predict_flow(self, current_vol: Decimal, target_vol: Decimal, aum_est: Decimal) -> FlowPrediction:
        if current_vol > target_vol:
            # Need to de-lever
            selling_pressure = aum_est * (1 - (target_vol / current_vol))
            return FlowPrediction(direction="SELL", amount=selling_pressure)
        return FlowPrediction(direction="HOLD")
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Volatility Monitor | `services/risk/vol_monitor.py` | `[ ]` |
| Selling Predictor | `services/strategies/forced_selling.py` | `[ ]` |

---

### 190.2 Margin Debt Contraction Monitor `[ ]`

**Acceptance Criteria**: Track FINRA Margin Debt levels. Rising debt fuels bubbles; Rapid contraction signals forced liquidation spirals.

| Component | File Path | Status |
|-----------|-----------|--------|
| Margin Tracker | `services/market/finra_margin.py` | `[ ]` |

---

### 190.3 Target Date Fund Rebalancing Calendar `[ ]`

**Acceptance Criteria**: Predict Month-End and Quarter-End rebalancing flows. If Stocks are up 10% and Bonds down 5%, TDFs *must* sell Stocks and buy Bonds.

| Component | File Path | Status |
|-----------|-----------|--------|
| Rebalance Predictor | `services/strategies/tdf_flow.py` | `[ ]` |

---

### 190.4 CTAs (Trend Followers) Positioning Proxy `[ ]`

**Acceptance Criteria**: Model Commodity Trading Advisors (CTAs). They chase trends. If trend breaks (e.g., moves below 50-day MA), they flip from Long to Short mechanically.

| Component | File Path | Status |
|-----------|-----------|--------|
| CTA Modeler | `services/strategies/cta_positioning.py` | `[ ]` |

---

### 190.5 Postgres Order Flow Toxicity Log `[ ]`

**Acceptance Criteria**: Log "Toxic Flow" (VPIN metric). High toxicity often precedes a liquidity crash (Flash Crash).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE market_toxicity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    
    -- Metrics
    vpin DECIMAL(5, 4),                -- Volume-Synchronized Probability of Informed Trading
    bid_ask_spread_bps DECIMAL(5, 2),
    depth_imbalance DECIMAL(5, 4),
    
    is_toxic BOOLEAN GENERATED ALWAYS AS (vpin > 0.4) STORED
);

SELECT create_hypertable('market_toxicity', 'timestamp');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/190_toxicity.sql` | `[ ]` |
| Toxicity Calc | `services/market/toxicity_calc.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidity Dashboard | `frontend2/src/components/Market/LiquidityDash.jsx` | `[ ]` |
| Forced Seller Alert | `frontend2/src/components/Alerts/ForcedSeller.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py liquidity check-risk-parity` | Est selling pressure | `[ ]` |
| `python cli.py liquidity calc-vpin <ticker>` | Measure toxicity | `[ ]` |

---

*Last verified: 2026-01-25*
