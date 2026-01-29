# Phase 112: Index Fund 'Freeloader' Problem Monitor

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Monitor and analyze the systemic risk posed by passive indexing's "freeloader problem" - where passive investors benefit from active price discovery without contributing to it, potentially leading to market distortions.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Phase 12 (Index Fund 'Freeloader' Problem Monitor)

---

## 🎯 Sub-Deliverables

### 112.1 Kafka Active vs. Passive Volume Tracker `[x]`

**Acceptance Criteria**: Stream real-time data tracking the ratio of active trading volume to passive fund flows, detecting when passive dominance exceeds dangerous thresholds.

#### Kafka Topic (Docker-compose: redpanda service)

```json
{
    "topic": "active-passive-ratio",
    "partitions": 3,
    "schema": {
        "timestamp": "timestamp",
        "ticker": "string",
        "active_volume": "decimal",
        "passive_volume": "decimal",
        "active_pct": "decimal",
        "passive_pct": "decimal",
        "threshold_breach": "boolean"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Volume Tracker | `services/market/active_passive_tracker.py` | `[x]` |
| Kafka Producer | `services/kafka/volume_ratio_producer.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Ratio Dashboard | `frontend2/src/components/Market/ActivePassiveRatio.jsx` | `[x]` |
| Threshold Alert | `frontend2/src/components/Alerts/PassiveThreshold.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Volume Tracker | `tests/unit/test_active_passive_tracker.py` | `[x]` |
| Integration: Kafka | `tests/integration/test_volume_ratio_kafka.py` | `[x]` |

---

### 112.2 Postgres Price Discovery Delay Log `[x]`

**Acceptance Criteria**: Log instances where price discovery appears delayed due to passive dominance, measuring time for new information to be reflected in prices.

#### Postgres Schema

```sql
CREATE TABLE price_discovery_delays (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_timestamp TIMESTAMPTZ NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    
    -- Event Details
    event_type VARCHAR(50),              -- EARNINGS, ANALYST, NEWS, MACRO
    expected_impact DECIMAL(8, 6),
    
    -- Delay Measurement
    discovery_delay_seconds INTEGER,     -- Time to 90% price adjustment
    passive_pct_at_event DECIMAL(8, 6),
    
    -- Analysis
    attributed_to_passive BOOLEAN,
    correlation_score DECIMAL(5, 4),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('price_discovery_delays', 'event_timestamp');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/112_price_discovery.sql` | `[x]` |
| Delay Analyzer | `services/market/discovery_delay_analyzer.py` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Delay Analyzer | `tests/unit/test_discovery_delay.py` | `[x]` |

---

### 112.3 Overconcentration Skew Alert `[x]`

**Acceptance Criteria**: Alert when passive fund concentration in top holdings creates dangerous market skew.

| Component | File Path | Status |
|-----------|-----------|--------|
| Skew Detector | `services/risk/overconcentration_skew.py` | `[x]` |
| Alert Service | `services/alerts/skew_alerts.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Skew Warning Panel | `frontend2/src/components/Risk/SkewWarning.jsx` | `[x]` |

---

### 112.4 Freeloader Dilemma Simulator `[x]`

**Acceptance Criteria**: Build a simulation engine demonstrating how increased passive adoption degrades price efficiency.

| Component | File Path | Status |
|-----------|-----------|--------|
| Freeloader Simulator | `services/simulation/freeloader_sim.py` | `[x]` |
| Efficiency Calculator | `services/quantitative/efficiency_calc.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Simulation Interface | `frontend2/src/components/Simulator/FreeloaderSim.jsx` | `[x]` |

---

### 112.5 Market Cycle Active Manager Recommender `[x]`

**Acceptance Criteria**: Recommend active management during market cycles when passive investing may underperform due to concentration.

| Component | File Path | Status |
|-----------|-----------|--------|
| Cycle Analyzer | `services/market/cycle_analyzer.py` | `[x]` |
| Manager Recommender | `services/funds/active_recommender.py` | `[x]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

*Last verified: 2026-01-25*
