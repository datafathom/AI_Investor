# Phase 7: SearcherAgent Hunting Logic Development

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: AI Team

---

## 📋 Overview

**Description**: Configure the SearcherAgent (The Hunter) to identify high-probability oscillations using logic-based market structure.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 7.1 Market Structure Algorithms `[ ]` <!-- NOT STARTED -->

**Acceptance Criteria**: Develop SearcherAgent algorithms focusing on Market Structure (Higher Highs/Lower Lows) rather than retail indicators.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| SearcherAgent Core | `agents/searcher_agent.py` | `[ ]` |
| Market Structure Detector | `services/analysis/market_structure.py` | `[ ]` |
| Higher High/Lower Low Logic | `services/analysis/swing_detection.py` | `[ ]` |
| Trend Identification | `services/analysis/trend_analyzer.py` | `[ ]` |

#### Algorithm Specifications

| Algorithm | Description | Status |
|-----------|-------------|--------|
| Swing Point Detection | Identify local highs/lows | `[ ]` |
| Trend Structure | HH/HL (Uptrend), LH/LL (Downtrend) | `[ ]` |
| Break of Structure (BOS) | Trend continuation signals | `[ ]` |
| Change of Character (CHoCH) | Trend reversal signals | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| SearcherAgent Dashboard | `pages/SearcherAgentDashboard.jsx` | `[ ]` |
| Market Structure Overlay | `components/Charts/MarketStructureOverlay.jsx` | `[ ]` |
| Swing Point Markers | `components/Charts/SwingMarkers.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Swing Detection | `tests/unit/test_swing_detection.py` | `[ ]` |
| Unit: Trend Analyzer | `tests/unit/test_trend_analyzer.py` | `[ ]` |
| Integration: SearcherAgent | `tests/integration/test_searcher_agent.py` | `[ ]` |

---

### 7.2 Smart Money Order Flow `[ ]` <!-- NOT STARTED -->

**Acceptance Criteria**: Implement 'Smart Money' order flow detection to identify institutional liquidity traps.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Order Block Detector | `services/analysis/order_blocks.py` | `[ ]` |
| Fair Value Gap (FVG) Finder | `services/analysis/fair_value_gaps.py` | `[ ]` |
| Liquidity Sweep Detector | `services/analysis/liquidity_sweeps.py` | `[ ]` |
| Imbalance Identifier | `services/analysis/imbalances.py` | `[ ]` |

#### Smart Money Concepts

| Concept | Description | Status |
|---------|-------------|--------|
| Order Blocks | Institutional buying/selling zones | `[ ]` |
| Fair Value Gaps | Price imbalances to be filled | `[ ]` |
| Liquidity Pools | Areas where stops cluster | `[ ]` |
| Mitigation Blocks | Retracement zones | `[ ]` |

---

### 7.3 Trade Thesis Broadcasting `[ ]` <!-- NOT STARTED -->

**Acceptance Criteria**: Configure the agent to broadcast 'Trade Theses' to the `market-telemetry` topic with a logic-based justification.

#### Kafka Message Schema

```json
{
  "thesis_id": "uuid",
  "agent_id": "searcher-001",
  "currency_pair": "EUR/USD",
  "direction": "LONG",
  "entry_zone": { "min": 1.0850, "max": 1.0860 },
  "stop_loss": 1.0820,
  "take_profit": [1.0920, 1.0950],
  "r_multiple_target": 3.0,
  "confidence": 0.78,
  "logic": {
    "market_structure": "Higher High confirmed at 1.0880",
    "order_block": "Bullish OB at 1.0855 (H4)",
    "liquidity": "Sweep of Asian lows complete",
    "confluence_count": 3
  },
  "timestamp": "2026-01-25T21:30:00Z"
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Thesis Publisher | `services/kafka/thesis_publisher.py` | `[ ]` |
| Thesis Schema | `schemas/trade_thesis.avsc` | `[ ]` |

---

### 7.4 Major Pair Prioritization `[ ]` <!-- NOT STARTED -->

**Acceptance Criteria**: Ensure the SearcherAgent prioritizes high-volume Major Pairs (USD, EUR, GBP) to guarantee liquidity.

#### Configuration

| Pair | Priority | Minimum Volume | Status |
|------|----------|----------------|--------|
| EUR/USD | 1 | $5T daily | `[ ]` |
| GBP/USD | 2 | $2.5T daily | `[ ]` |
| USD/JPY | 3 | $1.5T daily | `[ ]` |
| USD/CHF | 4 | $500B daily | `[ ]` |
| AUD/USD | 5 | $400B daily | `[ ]` |
| USD/CAD | 6 | $300B daily | `[ ]` |

---

### 7.5 Mean-Reversion Detection `[ ]` <!-- NOT STARTED -->

**Acceptance Criteria**: Integrate mean-reversion detection logic within the SearcherAgent swarm to exploit market inefficiencies.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Mean Reversion Calculator | `services/analysis/mean_reversion.py` | `[ ]` |
| Standard Deviation Bands | `services/analysis/volatility_bands.py` | `[ ]` |
| Fair Value Calculator | `services/analysis/fair_value.py` | `[ ]` |

#### Reversion Signals

| Signal | Trigger Condition | Status |
|--------|-------------------|--------|
| Extreme Extension | Price > 2σ from mean | `[ ]` |
| Volume Exhaustion | Volume declining at extremes | `[ ]` |
| Divergence | Price/momentum divergence | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 7.1 Market Structure Algorithms | `[ ]` | `[ ]` |
| 7.2 Smart Money Order Flow | `[ ]` | `[ ]` |
| 7.3 Trade Thesis Broadcasting | `[ ]` | `[ ]` |
| 7.4 Major Pair Prioritization | `[ ]` | `[ ]` |
| 7.5 Mean-Reversion Detection | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands for This Phase

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py agent-searcher-status` | Check SearcherAgent health | `[ ]` |
| `python cli.py agent-searcher-scan <pair>` | Trigger manual scan | `[ ]` |
| `python cli.py agent-searcher-thesis --list` | List active theses | `[ ]` |

---

## 📦 Dependencies

This phase depends on:
- Phase 2: FX Stream Topic (for price data)
- Phase 4: Neo4j Graph (for liquidity zone mapping)
- Phase 5: Pip Calculator (for price precision)

---

*Last verified: 2026-01-25*
