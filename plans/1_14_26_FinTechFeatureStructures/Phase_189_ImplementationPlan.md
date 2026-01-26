# Phase 189: Options Hedging & Volatility Strategy Engine

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Trading & Risk Team

---

## 📋 Overview

**Description**: Advanced Options strategies for hedging (Protective Puts, Collars) and income generation (Covered Calls). Includes "Tail Risk Hedging" – systematically buying cheap OTM puts to profit during market crashes (the "Black Swan" strategy).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 9

---

## 🎯 Sub-Deliverables

### 189.1 Black-Scholes & Greeks Calculation Service `[ ]`

**Acceptance Criteria**: Real-time calculation of Delta, Gamma, Theta, Vega. Used to assess the "Cost of Insurance" (Theta decay) vs. "Protection" (Delta).

```python
class GreeksCalculator:
    """
    Calculate Greeks for option chain.
    """
    def calculate_greeks(
        self,
        spot_price: Decimal,
        strike: Decimal,
        time_to_expiry: Decimal,
        volatility: Decimal,
        rate: Decimal
    ) -> Greeks:
        # Standard Black-Scholes Implementation
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Greeks Engine | `services/options/greeks_engine.py` | `[ ]` |
| API Endpoint | `web/api/options/chain.py` | `[ ]` |

---

### 189.2 Tail Risk Hedging Implementation (VIX Calls/SPX Puts) `[ ]`

**Acceptance Criteria**: Strategy automation. Buy 2-month OTM puts (Delta -0.10) rolling monthly. Aim to spend 1-2% of portfolio per year to protect against 20% drops.

| Component | File Path | Status |
|-----------|-----------|--------|
| Tail Hedge Strategy | `services/strategies/tail_hedge.py` | `[ ]` |

---

### 189.3 Collar Strategy Automator (Cap & Floor) `[ ]`

**Acceptance Criteria**: For concentrated stock (Phase 167), implement a "Zero Cost Collar". Sell upside Call to fund the purchase of downside Put. Lock in value range.

| Component | File Path | Status |
|-----------|-----------|--------|
| Collar Automator | `services/strategies/collar_auto.py` | `[ ]` |

---

### 189.4 Kafka Volatility Surface Ingestion `[ ]`

**Acceptance Criteria**: Ingest the Implied Volatility (IV) Surface. Detect "Skew" (Puts more expensive than Calls) to time hedge entry.

#### Kafka Topic

```json
{
    "topic": "volatility-surface",
    "schema": {
        "ticker": "SPX",
        "expiry": "2024-06-21",
        "strikes": [4000, 4100, 4200],
        "ivs": [0.18, 0.16, 0.15],
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Surface Consumer | `services/kafka/surface_consumer.py` | `[ ]` |

---

### 189.5 Income Overlay (Covered Call) Generator `[ ]`

**Acceptance Criteria**: Suggest Covered Calls on stagnant positions to generate "Yield". target Delta 0.30 (30% probability of assignment).

| Component | File Path | Status |
|-----------|-----------|--------|
| Yield Generator | `services/strategies/covered_call.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Options Visualizer | `frontend2/src/components/Options/PayoffChar.jsx` | `[ ]` |
| Hedge Dashboard | `frontend2/src/components/Options/HedgeStatus.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py opt calc-greeks <ticker>` | Get Greeks | `[ ]` |
| `python cli.py opt suggest-collar` | Build collar trade | `[ ]` |

---

*Last verified: 2026-01-25*
