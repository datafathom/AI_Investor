# Phase 2: Global FX Stream Topic Configuration

> **Status**: `[/]` In Progress  
> **Last Updated**: 2026-01-25  
> **Owner**: Backend Team

---

## 📋 Overview

**Description**: Establish the Kafka-based infrastructure for real-time ingestion of Major Currency Pairs (EUR/USD, GBP/USD, USD/JPY).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 2.1 FX Stream Topic Provisioning `[/]` <!-- IN PROGRESS -->

**Acceptance Criteria**: Provision the `fx-stream-global` topic specifically for Major Pair price ingestion from institutional providers.

#### Topic Configuration

| Property | Value | Status |
| :--- | :--- | :--- |
| Topic Name | `fx-stream-global` | `[/]` |
| Partitions | 6 (one per major pair) | `[ ]` |
| Replication Factor | 3 | `[ ]` |
| Retention (ms) | 86400000 (24 hours) | `[ ]` |

#### Backend Implementation

| Component | File Path | Status |
| :--- | :--- | :--- |
| FX Stream Producer | `services/fx_stream_producer.py` | `[/]` |
| FX Stream Consumer | `services/fx_stream_consumer.py` | `[ ]` |
| Price Model | `models/fx_price.py` | `[/]` |

#### Tests

| Test Type | File Path | Status |
| :--- | :--- | :--- |
| Unit: Producer | `tests/unit/test_fx_stream_producer.py` | `[ ]` |
| Unit: Consumer | `tests/unit/test_fx_stream_consumer.py` | `[ ]` |
| Integration | `tests/integration/test_fx_stream.py` | `[ ]` |

---

### 2.2 10-Second Update Interval `[ ]` <!-- NOT STARTED -->

**Acceptance Criteria**: Implement a 10-second update interval for price quotes as defined in the technical specification.

#### Backend Implementation

| Component | File Path | Status |
| :--- | :--- | :--- |
| Rate Limiter | `services/rate_limiter.py` | `[ ]` |
| Scheduler Config | `config/scheduler.py` | `[ ]` |

#### Configuration

| Setting | Value | Status |
| :--- | :--- | :--- |
| Update Interval | 10000ms | `[ ]` |
| Batch Size | 100 | `[ ]` |
| Max Retry | 3 | `[ ]` |

---

### 2.3 Consumer Group Partitioning `[ ]` <!-- NOT STARTED -->

**Acceptance Criteria**: Ensure Kafka consumer groups are partitioned by currency pair to allow horizontal scaling of the analysis engine.

#### Consumer Group Design

| Consumer Group | Currency Pair | Partition | Status |
| :--- | :--- | :--- | :--- |
| fx-consumer-eurusd | EUR/USD | 0 | `[ ]` |
| fx-consumer-gbpusd | GBP/USD | 1 | `[ ]` |
| fx-consumer-usdjpy | USD/JPY | 2 | `[ ]` |
| fx-consumer-usdchf | USD/CHF | 3 | `[ ]` |
| fx-consumer-audusd | AUD/USD | 4 | `[ ]` |
| fx-consumer-usdcad | USD/CAD | 5 | `[ ]` |

---

### 2.4 Price Payload Validation `[ ]` <!-- NOT STARTED -->

**Acceptance Criteria**: Validate the integrity of incoming price payloads against an external institutional benchmark.

#### Backend Implementation

| Component | File Path | Status |
| :--- | :--- | :--- |
| Price Validator | `services/validators/price_validator.py` | `[ ]` |
| Benchmark Client | `services/external/benchmark_client.py` | `[ ]` |

#### Validation Rules

| Rule | Description | Status |
| :--- | :--- | :--- |
| Price Range | Within 5% of benchmark | `[ ]` |
| Timestamp Freshness | < 30 seconds old | `[ ]` |
| Decimal Precision | 5 decimal places | `[ ]` |
| Schema Compliance | Valid Avro schema | `[ ]` |

---

### 2.5 TimescaleDB Offset Mapping `[ ]` <!-- NOT STARTED -->

**Acceptance Criteria**: Map Kafka topic offsets to TimescaleDB for historical replayability and backtesting accuracy.

#### Database Schema

```sql
CREATE TABLE kafka_offset_map (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    partition INT NOT NULL,
    offset BIGINT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('kafka_offset_map', 'timestamp');
```

| Component | File Path | Status |
| :--- | :--- | :--- |
| Offset Mapper | `services/offset_mapper.py` | `[ ]` |
| Migration | `migrations/002_kafka_offset_map.sql` | `[ ]` |

---

## Phase Completion Summary

| Deliverable | Status | E2E Verified |
| :--- | :--- | :--- |
| 2.1 Topic Provisioning | `[/]` | `[ ]` |
| 2.2 10-Second Interval | `[ ]` | `[ ]` |
| 2.3 Consumer Partitioning | `[ ]` | `[ ]` |
| 2.4 Payload Validation | `[ ]` | `[ ]` |
| 2.5 Offset Mapping | `[ ]` | `[ ]` |

**Phase Status**: `[/]` IN PROGRESS

---

## CLI Commands for This Phase

| Command | Description | Status |
| :--- | :--- | :--- |
| `python cli.py fx-stream-status` | Check FX stream health | `[ ]` |
| `python cli.py fx-stream-test <pair>` | Test specific pair stream | `[ ]` |
| `python cli.py fx-stream-replay <timestamp>` | Replay from offset | `[ ]` |

---

*Last verified: 2026-01-25*
