# Phase 102: Index Fund Ticker Master & Passive Inflow Service

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Data Infrastructure Team

---

## 📋 Overview

**Description**: Build a comprehensive master database of index funds and ETFs with real-time tracking of passive inflow data to monitor the growth of passive investing and its market impact.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 102.1 Postgres Index Fund Master List `[ ]`

**Acceptance Criteria**: Create a Postgres master table containing all major index funds (SPY, QQQ, IWM, VOO, VTI) with metadata including expense ratios, AUM, and benchmark indices.

#### Database Schema

```sql
CREATE TABLE index_fund_master (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    fund_type VARCHAR(50) NOT NULL,  -- ETF, MUTUAL_FUND, INDEX
    benchmark_index VARCHAR(100),    -- S&P 500, NASDAQ 100, Russell 2000
    
    -- Fund Details
    expense_ratio DECIMAL(6, 4) NOT NULL,
    aum DECIMAL(20, 2),              -- Assets Under Management
    inception_date DATE,
    issuer VARCHAR(100),             -- Vanguard, BlackRock, State Street
    
    -- Trading Info
    avg_volume BIGINT,
    avg_spread DECIMAL(8, 6),
    tradability VARCHAR(20) DEFAULT 'HIGHLY_LIQUID',
    
    -- Classification
    asset_class VARCHAR(50),         -- EQUITY, FIXED_INCOME, COMMODITY
    sector_focus VARCHAR(50),        -- BROAD_MARKET, TECH, HEALTHCARE
    market_cap_focus VARCHAR(20),    -- LARGE_CAP, MID_CAP, SMALL_CAP
    geography VARCHAR(50),           -- US, INTERNATIONAL, EMERGING
    
    -- Metadata
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_index_fund_ticker ON index_fund_master(ticker);
CREATE INDEX idx_index_fund_type ON index_fund_master(fund_type);
CREATE INDEX idx_index_fund_benchmark ON index_fund_master(benchmark_index);
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/102_index_fund_master.sql` | `[ ]` |
| Model | `models/index_fund.py` | `[ ]` |
| Service | `services/funds/index_fund_service.py` | `[ ]` |
| API Endpoint | `web/api/funds/index_funds.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Index Fund List | `frontend2/src/components/IndexFunds/IndexFundList.jsx` | `[ ]` |
| Fund Detail Card | `frontend2/src/components/IndexFunds/FundDetailCard.jsx` | `[ ]` |
| useIndexFunds Hook | `frontend2/src/hooks/useIndexFunds.js` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Model | `tests/unit/test_index_fund_model.py` | `[ ]` |
| Unit: Service | `tests/unit/test_index_fund_service.py` | `[ ]` |
| Integration: API | `tests/integration/test_index_fund_api.py` | `[ ]` |
| E2E: Fund List UI | `tests/e2e/test_index_fund_ui.py` | `[ ]` |

---

### 102.2 Kafka Passive Inflow Ingestion Stream `[ ]`

**Acceptance Criteria**: Configure a Kafka topic to ingest daily passive fund inflow/outflow data from external data providers (Bloomberg, Morningstar) with < 500ms latency.

#### Kafka Topic Configuration

```json
{
    "topic": "passive-fund-flows",
    "partitions": 6,
    "replication_factor": 3,
    "retention_ms": 604800000,
    "schema": {
        "fund_id": "uuid",
        "ticker": "string",
        "flow_date": "date",
        "inflow_usd": "decimal",
        "outflow_usd": "decimal",
        "net_flow_usd": "decimal",
        "cumulative_aum": "decimal",
        "source": "string",
        "timestamp": "timestamp"
    }
}
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Kafka Consumer | `services/kafka/passive_flow_consumer.py` | `[ ]` |
| Flow Processor | `services/funds/flow_processor.py` | `[ ]` |
| Data Validator | `services/funds/flow_validator.py` | `[ ]` |
| Bloomberg Adapter | `services/external/bloomberg_adapter.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Flow Chart | `frontend2/src/components/Charts/PassiveFlowChart.jsx` | `[ ]` |
| Real-time Ticker | `frontend2/src/components/Tickers/FlowTicker.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Consumer | `tests/unit/test_passive_flow_consumer.py` | `[ ]` |
| Unit: Processor | `tests/unit/test_flow_processor.py` | `[ ]` |
| Integration: Kafka | `tests/integration/test_passive_flow_kafka.py` | `[ ]` |
| Load: Throughput | `tests/load/test_flow_throughput.py` | `[ ]` |

---

### 102.3 Neo4j Sector → Index Mapping Graph `[ ]`

**Acceptance Criteria**: Create Neo4j relationships mapping market sectors to their corresponding index funds, with weighted edges representing sector allocation percentages.

#### Neo4j Schema

```cypher
// Index Fund Nodes
CREATE CONSTRAINT index_fund_id IF NOT EXISTS FOR (f:INDEX_FUND) REQUIRE f.id IS UNIQUE;

(:INDEX_FUND {
    id: "uuid",
    ticker: "SPY",
    name: "SPDR S&P 500 ETF",
    aum: 400000000000,
    expense_ratio: 0.0945
})

// Sector Nodes
(:SECTOR {
    id: "uuid",
    name: "Technology",
    gics_code: "45"
})

// Relationships
(:INDEX_FUND)-[:ALLOCATES_TO {
    weight: 0.28,           // 28% allocation
    holdings_count: 75,
    updated_at: datetime()
}]->(:SECTOR)

(:INDEX_FUND)-[:TRACKS]->(:BENCHMARK_INDEX)
(:INDEX_FUND)-[:ISSUED_BY]->(:FUND_ISSUER)
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Sector Graph Service | `services/neo4j/sector_index_graph.py` | `[ ]` |
| Allocation Calculator | `services/funds/allocation_calculator.py` | `[ ]` |
| Graph Seed Script | `scripts/seed_sector_graph.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Sector Map | `frontend2/src/components/Charts/SectorAllocationMap.jsx` | `[ ]` |
| Graph Visualizer | `frontend2/src/components/Neo4j/IndexFundGraph.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Graph Service | `tests/unit/test_sector_index_graph.py` | `[ ]` |
| Integration: Neo4j | `tests/integration/test_sector_neo4j.py` | `[ ]` |
| Performance: Queries | `tests/performance/test_sector_query_perf.py` | `[ ]` |

---

### 102.4 International Index Tradability Classifier `[ ]`

**Acceptance Criteria**: Implement a classification service that flags international indices based on tradability (liquidity, capital controls, SOE exposure) with risk scores.

#### Backend Implementation

```python
class TradabilityClassifier:
    """
    Classify international indices by tradability risk.
    
    Risk Factors:
    - Liquidity: Average daily volume / AUM ratio
    - Capital Controls: Repatriation restrictions
    - SOE Exposure: State-owned enterprise concentration
    - Currency Risk: FX volatility and convertibility
    """
    
    TRADABILITY_TIERS = {
        'HIGHLY_LIQUID': {'min_score': 80, 'color': 'green'},
        'LIQUID': {'min_score': 60, 'color': 'yellow'},
        'MODERATE': {'min_score': 40, 'color': 'orange'},
        'ILLIQUID': {'min_score': 20, 'color': 'red'},
        'RESTRICTED': {'min_score': 0, 'color': 'darkred'}
    }
    
    def calculate_tradability_score(self, index: IndexFund) -> dict:
        """Calculate composite tradability score."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Tradability Classifier | `services/funds/tradability_classifier.py` | `[ ]` |
| Risk Scorer | `services/risk/intl_risk_scorer.py` | `[ ]` |
| Country Data Service | `services/external/country_data.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Tradability Badge | `frontend2/src/components/Badges/TradabilityBadge.jsx` | `[ ]` |
| Risk Breakdown | `frontend2/src/components/Risk/TradabilityBreakdown.jsx` | `[ ]` |
| World Map Overlay | `frontend2/src/components/Maps/TradabilityWorldMap.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Classifier | `tests/unit/test_tradability_classifier.py` | `[ ]` |
| Unit: Risk Scorer | `tests/unit/test_intl_risk_scorer.py` | `[ ]` |
| Integration: Full Pipeline | `tests/integration/test_tradability_pipeline.py` | `[ ]` |

---

### 102.5 Passive Indexing Stock-Picking Prevention Gate `[ ]`

**Acceptance Criteria**: Implement a guardrail that prevents active stock-picking within accounts designated for passive index investing, logging all blocked attempts.

#### Backend Implementation

```python
class PassiveIndexGuard:
    """
    Prevent active stock-picking in passive-designated accounts.
    
    Rules:
    1. Block individual stock purchases in passive accounts
    2. Allow only approved index funds and ETFs
    3. Log all blocked attempts for review
    4. Alert on repeated bypass attempts
    """
    
    def validate_trade(self, account: Account, trade: TradeRequest) -> ValidationResult:
        if account.investment_strategy == 'PASSIVE_INDEX':
            if trade.asset_type == 'INDIVIDUAL_STOCK':
                return ValidationResult(
                    allowed=False,
                    reason='Individual stock trading blocked in passive account',
                    suggestion='Consider adding to index fund allocation instead'
                )
        return ValidationResult(allowed=True)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Passive Guard | `services/compliance/passive_index_guard.py` | `[ ]` |
| Approved Fund List | `config/approved_passive_funds.py` | `[ ]` |
| Block Logger | `services/audit/passive_block_logger.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Block Modal | `frontend2/src/components/Modals/PassiveBlockModal.jsx` | `[ ]` |
| Alternative Suggester | `frontend2/src/components/Trading/AlternativeFundSuggester.jsx` | `[ ]` |
| Account Type Indicator | `frontend2/src/components/Account/StrategyIndicator.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Passive Guard | `tests/unit/test_passive_index_guard.py` | `[ ]` |
| Unit: Block Logger | `tests/unit/test_passive_block_logger.py` | `[ ]` |
| Integration: Trade Flow | `tests/integration/test_passive_trade_block.py` | `[ ]` |
| E2E: Block Modal UI | `tests/e2e/test_passive_block_modal.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 102.1 Index Fund Master | `[ ]` | `[ ]` |
| 102.2 Passive Inflow Stream | `[ ]` | `[ ]` |
| 102.3 Neo4j Sector Mapping | `[ ]` | `[ ]` |
| 102.4 Tradability Classifier | `[ ]` | `[ ]` |
| 102.5 Stock-Picking Prevention | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py index-funds list` | List all index funds | `[ ]` |
| `python cli.py index-funds flows <ticker>` | Show fund flows | `[ ]` |
| `python cli.py index-funds tradability <ticker>` | Check tradability | `[ ]` |
| `python cli.py index-funds seed` | Seed fund master data | `[ ]` |

---

## 📦 Dependencies

- Phase 3: TimescaleDB (Postgres schema)
- Phase 4: Neo4j Graph (sector relationships)
- Phase 1: Redpanda Cluster (Kafka topics)

---

*Last verified: 2026-01-25*
