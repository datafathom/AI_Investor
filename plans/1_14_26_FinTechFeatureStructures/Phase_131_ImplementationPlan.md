# Phase 131: Inflation-Hedged Principal Optimizer

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Create a dedicated engine to protect portfolio principal purchasing power against inflation. This involves real-time CPI ingestion, calculating real (inflation-adjusted) returns, and optimizing exposure to inflation-resistant assets like TIPS, Gold, Commodities, and Real Estate.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 11

---

## 🎯 Sub-Deliverables

### 131.1 Kafka CPI Data Consumer `[ ]`

**Acceptance Criteria**: Ingest monthly CPI (Consumer Price Index) and PPI (Producer Price Index) data from FRED/BLS APIs to track inflation trends in real-time.

#### Kafka Topic (Docker-compose: redpanda service)

```json
{
    "topic": "economic-indicators",
    "partitions": 2,
    "schema": {
        "indicator": "string",     // CPI, PPI, PCE
        "value": "decimal",
        "yoy_change": "decimal",
        "mom_change": "decimal",
        "release_date": "date",
        "period": "date",
        "timestamp": "timestamp"
    }
}
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| FRED Adapter | `services/external/fred_adapter.py` | `[ ]` |
| Inflation Consumer | `services/kafka/inflation_consumer.py` | `[ ]` |
| Inflation Tracker | `services/economics/inflation_tracker.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Inflation Dashboard | `frontend2/src/components/Economics/InflationDashboard.jsx` | `[ ]` |
| Real Return Toggle | `frontend2/src/components/Portfolio/RealReturnToggle.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: FRED Adapter | `tests/unit/test_fred_adapter.py` | `[ ]` |
| Integration: Kafka | `tests/integration/test_inflation_kafka.py` | `[ ]` |

---

### 131.2 Hedge Effectiveness Score (Gold, REITs, Stocks) `[ ]`

**Acceptance Criteria**: Calculate a dynamic "Inflation Beta" for assets to score their effectiveness as a hedge.

```python
class InflationHedgeScorer:
    """
    Calculate asset correlation with inflation (Inflation Beta).
    
    Scores:
    - > 1.0: Super-hedger (Leveraged Commodities)
    - 0.5 - 1.0: Strong hedger (Gold, Energy, Real Estate)
    - 0.0 - 0.5: Weak hedger (Broad Equities)
    - < 0.0: Vulnerable (Long-duration Bonds, Growth Tech)
    """
    
    def calculate_inflation_beta(
        self,
        asset_returns: list[Decimal],
        inflation_changes: list[Decimal]
    ) -> Decimal:
        """Calculate sensitivity of asset to inflation shocks."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Hedge Scorer | `services/quantitative/hedge_scorer.py` | `[ ]` |
| Inflation Beta Calc | `services/quantitative/inflation_beta.py` | `[ ]` |

---

### 131.3 Target Return Inflation Adjustment Logic `[ ]`

**Acceptance Criteria**: Automatically adjust portfolio target returns based on current inflation. E.g., if target real return is 5% and inflation is 3%, nominal target becomes 8%.

| Component | File Path | Status |
|-----------|-----------|--------|
| Target Adjuster | `services/planning/target_adjuster.py` | `[ ]` |
| Plan Updater | `services/planning/plan_updater.py` | `[ ]` |

---

### 131.4 Neo4j Inflation-Resistant Asset Graph `[ ]`

**Acceptance Criteria**: Map assets in Neo4j with properties defining their inflation resistance profile.

#### Neo4j Schema

```cypher
(:ASSET_CLASS:COMMODITY {
    name: "Broad Commodities",
    ticker: "DBC",
    inflation_beta: 0.85,
    hedge_type: "COST_PUSH"
})

(:ASSET_CLASS:TIPS {
    name: "Treasury Inflation-Protected",
    ticker: "TIP",
    inflation_beta: 1.0,
    hedge_type: "DIRECT_INDEXED"
})

(:PORTFOLIO)-[:HEDGES_INFLATION {
    allocation_weight: 0.15,
    weighted_beta: 0.65
}]->(:ASSET_CLASS)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Hedge Graph Service | `services/neo4j/hedge_graph.py` | `[ ]` |

---

### 131.5 Social Class Maintenance Validator `[ ]`

**Acceptance Criteria**: Validate that the portfolio's real growth is sufficient to maintain the client's social class/lifestyle purchasing power over 30 years.

| Component | File Path | Status |
|-----------|-----------|--------|
| Lifestyle Validator | `services/planning/lifestyle_validator.py` | `[ ]` |
| Purchasing Power Calc | `services/economics/purchasing_power.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Lifestyle Projection | `frontend2/src/components/Planning/LifestyleProjection.jsx` | `[ ]` |
| Class Maintenance Alert | `frontend2/src/components/Alerts/ClassMaintenance.jsx` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 131.1 CPI Consumer | `[ ]` | `[ ]` |
| 131.2 Hedge Scorer | `[ ]` | `[ ]` |
| 131.3 Return Adjuster | `[ ]` | `[ ]` |
| 131.4 Neo4j Graph | `[ ]` | `[ ]` |
| 131.5 Class Validator | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py inflation status` | Show current inflation metrics | `[ ]` |
| `python cli.py inflation hedge-score <ticker>` | Calculate inflation beta | `[ ]` |
| `python cli.py inflation project-lifestyle` | Run lifestyle maintenance check | `[ ]` |

---

*Last verified: 2026-01-25*
