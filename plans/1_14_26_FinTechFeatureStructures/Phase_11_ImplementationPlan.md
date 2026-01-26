# Phase 11: Market Depth & Liquidity Monitoring

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Trading Infrastructure Team

---

## 📋 Overview

**Description**: Implement real-time monitoring of asset liquidity to minimize slippage and ensure institutional-grade execution.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 11.1 Order Book Stream Subscription `[ ]`

**Acceptance Criteria**: Subscribe the SearcherAgent to Order Book depth streams via the `market-telemetry` Kafka topic.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Order Book Consumer | `services/kafka/orderbook_consumer.py` | `[ ]` |
| Depth Aggregator | `services/market/depth_aggregator.py` | `[ ]` |
| Level 2 Parser | `services/market/level2_parser.py` | `[ ]` |

#### Kafka Topic Schema

```json
{
    "topic": "orderbook-depth",
    "schema": {
        "symbol": "EUR/USD",
        "timestamp": "2026-01-25T21:30:00Z",
        "bids": [
            {"price": 1.08500, "size": 5000000},
            {"price": 1.08495, "size": 3000000}
        ],
        "asks": [
            {"price": 1.08505, "size": 4000000},
            {"price": 1.08510, "size": 2500000}
        ],
        "spread": 0.00005,
        "mid_price": 1.085025
    }
}
```

---

### 11.2 Liquidity Threshold Gate `[ ]`

**Acceptance Criteria**: Define a 'Liquidity Threshold' that blocks trade entries for assets with insufficient institutional volume.

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidity Validator | `services/risk/liquidity_validator.py` | `[ ]` |
| Threshold Config | `config/liquidity_thresholds.py` | `[ ]` |

#### Threshold Configuration

| Asset Type | Min Volume (24h) | Min Depth | Max Spread |
|------------|------------------|-----------|------------|
| Major FX | $1B | $5M | 2 pips |
| Minor FX | $100M | $1M | 5 pips |
| Exotic FX | $10M | $100K | 15 pips |

---

### 11.3 Pre-trade Slippage Estimator `[ ]`

**Acceptance Criteria**: Implement a pre-trade slippage estimator that evaluates the spread before order transmission.

| Component | File Path | Status |
|-----------|-----------|--------|
| Slippage Estimator | `services/trading/slippage_estimator.py` | `[ ]` |
| Impact Calculator | `services/trading/market_impact.py` | `[ ]` |

---

### 11.4 Toxic Liquidity Detection `[ ]`

**Acceptance Criteria**: Configure the Warden to monitor liquidity gaps every 60 seconds and flag 'Toxic Liquidity' environments.

| Component | File Path | Status |
|-----------|-----------|--------|
| Toxic Liquidity Detector | `services/risk/toxic_liquidity.py` | `[ ]` |
| Gap Monitor | `services/market/gap_monitor.py` | `[ ]` |

---

### 11.5 Historical Liquidity Snapshots `[ ]`

**Acceptance Criteria**: Store historical liquidity snapshots in TimescaleDB to calibrate future backtest simulation accuracy.

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidity Snapshot Service | `services/market/liquidity_snapshot.py` | `[ ]` |
| Migration | `migrations/011_liquidity_snapshots.sql` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 11.1 Order Book Stream | `[ ]` | `[ ]` |
| 11.2 Liquidity Threshold | `[ ]` | `[ ]` |
| 11.3 Slippage Estimator | `[ ]` | `[ ]` |
| 11.4 Toxic Liquidity | `[ ]` | `[ ]` |
| 11.5 Historical Snapshots | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py liquidity-check <pair>` | Check liquidity | `[ ]` |
| `python cli.py slippage-estimate <pair> <size>` | Estimate slippage | `[ ]` |

---

*Last verified: 2026-01-25*
