# Phase 129: Passive Index Overconcentration Monitor

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: Monitor and alert when passive index funds become overconcentrated in top holdings, addressing the systematic risk where the largest cap-weighted stocks dominate index returns and create hidden concentration risk.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 9

---

## 🎯 Sub-Deliverables

### 129.1 Top 10 > 40% Market Cap Detection `[x]`

**Acceptance Criteria**: Implement real-time detection when the top 10 holdings of any index exceed 40% of total market capitalization, indicating dangerous concentration.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE index_concentration_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    index_ticker VARCHAR(20) NOT NULL,         -- SPY, QQQ, IWM
    
    -- Top Holdings Analysis
    top_5_weight DECIMAL(8, 6) NOT NULL,
    top_10_weight DECIMAL(8, 6) NOT NULL,
    top_20_weight DECIMAL(8, 6) NOT NULL,
    
    -- Concentration Metrics
    herfindahl_index DECIMAL(10, 8),           -- HHI for concentration
    effective_holdings INTEGER,                 -- 1/HHI approximation
    
    -- Alert Status
    concentration_level VARCHAR(20),            -- NORMAL, ELEVATED, HIGH, CRITICAL
    threshold_breached BOOLEAN DEFAULT FALSE,
    alert_triggered BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('index_concentration_snapshots', 'snapshot_timestamp');
CREATE INDEX idx_concentration_index ON index_concentration_snapshots(index_ticker);
CREATE INDEX idx_concentration_level ON index_concentration_snapshots(concentration_level);

CREATE TABLE index_holding_weights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_id UUID NOT NULL REFERENCES index_concentration_snapshots(id),
    rank INTEGER NOT NULL,                      -- Position in index (1 = largest)
    ticker VARCHAR(20) NOT NULL,
    company_name VARCHAR(255),
    weight DECIMAL(8, 6) NOT NULL,
    sector VARCHAR(50),
    
    -- Historical Comparison
    weight_30d_ago DECIMAL(8, 6),
    weight_change DECIMAL(8, 6),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Backend Implementation

```python
class ConcentrationDetector:
    """
    Detect dangerous concentration levels in index funds.
    
    Concentration Thresholds:
    - NORMAL: Top 10 < 25%
    - ELEVATED: Top 10 25-35%
    - HIGH: Top 10 35-40%
    - CRITICAL: Top 10 > 40%
    
    Special Flags:
    - Top 5 Tech > 35%
    - Single holding > 10%
    - Single sector > 30%
    """
    
    THRESHOLDS = {
        'NORMAL': {'top_10': Decimal('0.25'), 'color': 'green'},
        'ELEVATED': {'top_10': Decimal('0.35'), 'color': 'yellow'},
        'HIGH': {'top_10': Decimal('0.40'), 'color': 'orange'},
        'CRITICAL': {'top_10': Decimal('1.00'), 'color': 'red'}
    }
    
    def analyze_concentration(self, index_ticker: str) -> ConcentrationResult:
        """Analyze current concentration levels for an index."""
        pass
    
    def calculate_herfindahl_index(self, weights: list[Decimal]) -> Decimal:
        """Calculate Herfindahl-Hirschman Index (HHI)."""
        return sum(w ** 2 for w in weights)
    
    def calculate_effective_holdings(self, hhi: Decimal) -> int:
        """Calculate effective number of holdings (1/HHI)."""
        return int(Decimal('1') / hhi)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/129_index_concentration.sql` | `[x]` |
| Concentration Detector | `services/risk/concentration_detector.py` | `[x]` |
| HHI Calculator | `services/quantitative/hhi_calculator.py` | `[x]` |
| Snapshot Service | `services/market/concentration_snapshot.py` | `[x]` |
| API Endpoint | `web/api/risk/concentration.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Concentration Dashboard | `frontend2/src/components/Risk/ConcentrationDashboard.jsx` | `[x]` |
| Top Holdings Table | `frontend2/src/components/Risk/TopHoldingsTable.jsx` | `[x]` |
| Concentration Gauge | `frontend2/src/components/Charts/ConcentrationGauge.jsx` | `[x]` |
| Alert Banner | `frontend2/src/components/Alerts/ConcentrationAlert.jsx` | `[x]` |
| useConcentration Hook | `frontend2/src/hooks/useConcentration.js` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Concentration Detector | `tests/unit/test_concentration_detector.py` | `[x]` |
| Unit: HHI Calculator | `tests/unit/test_hhi_calculator.py` | `[x]` |
| Unit: Snapshot Service | `tests/unit/test_concentration_snapshot.py` | `[x]` |
| Integration: Full Pipeline | `tests/integration/test_concentration_pipeline.py` | `[x]` |
| E2E: Dashboard UI | `tests/e2e/test_concentration_dashboard.py` | `[x]` |

---

### 129.2 Equal Weighted Rebalancing Service `[x]`

**Acceptance Criteria**: Implement a service that calculates equal-weighted allocations as an alternative to cap-weighted indices, reducing concentration risk.

#### Backend Implementation

```python
class EqualWeightedRebalancer:
    """
    Generate equal-weighted portfolio from cap-weighted index.
    
    Benefits:
    - Reduces concentration in mega-caps
    - Historical outperformance over long periods
    - More exposure to smaller companies
    
    Drawbacks:
    - Higher turnover/trading costs
    - May underperform in momentum-driven markets
    """
    
    def calculate_equal_weights(self, holdings: list[Holding]) -> list[Holding]:
        """Calculate equal weights for all holdings."""
        equal_weight = Decimal('1') / len(holdings)
        return [Holding(h.ticker, weight=equal_weight) for h in holdings]
    
    def generate_rebalance_trades(
        self, 
        current: list[Holding], 
        target: list[Holding]
    ) -> list[Trade]:
        """Generate trades to rebalance from current to target weights."""
        pass
    
    def estimate_transaction_costs(self, trades: list[Trade]) -> Decimal:
        """Estimate transaction costs for rebalancing."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Equal Weight Rebalancer | `services/portfolio/equal_weight_rebalancer.py` | `[x]` |
| Transaction Cost Estimator | `services/trading/transaction_cost.py` | `[x]` |
| Rebalance Trade Generator | `services/trading/rebalance_generator.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Rebalance Preview | `frontend2/src/components/Portfolio/RebalancePreview.jsx` | `[x]` |
| Weight Comparison Chart | `frontend2/src/components/Charts/WeightComparisonChart.jsx` | `[x]` |
| Cost Estimate Display | `frontend2/src/components/Portfolio/CostEstimate.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Equal Weight | `tests/unit/test_equal_weight_rebalancer.py` | `[x]` |
| Unit: Cost Estimator | `tests/unit/test_transaction_cost.py` | `[x]` |
| Integration: Rebalance Flow | `tests/integration/test_rebalance_flow.py` | `[x]` |

---

### 129.3 Cap Weighted vs. Fundamental Distortion Log `[x]`

**Acceptance Criteria**: Track and log instances where cap-weighted indices diverge from fundamental (revenue, earnings) weights, indicating potential distortion.

#### Postgres Schema

```sql
CREATE TABLE fundamental_distortion_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    log_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ticker VARCHAR(20) NOT NULL,
    
    -- Weights
    cap_weight DECIMAL(8, 6) NOT NULL,
    revenue_weight DECIMAL(8, 6),
    earnings_weight DECIMAL(8, 6),
    book_value_weight DECIMAL(8, 6),
    
    -- Distortion Metrics
    cap_vs_revenue_distortion DECIMAL(8, 6),
    cap_vs_earnings_distortion DECIMAL(8, 6),
    distortion_score DECIMAL(8, 6),            -- Composite score
    
    -- Classification
    distortion_level VARCHAR(20),               -- MINOR, MODERATE, SEVERE
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('fundamental_distortion_log', 'log_timestamp');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Distortion Logger | `services/analysis/fundamental_distortion.py` | `[x]` |
| Weight Comparator | `services/analysis/weight_comparator.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Distortion Heatmap | `frontend2/src/components/Charts/DistortionHeatmap.jsx` | `[x]` |
| Distortion Log Table | `frontend2/src/components/Tables/DistortionLog.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Distortion Logger | `tests/unit/test_fundamental_distortion.py` | `[x]` |
| Unit: Weight Comparator | `tests/unit/test_weight_comparator.py` | `[x]` |

---

### 129.4 Neo4j Tech Concentration Node `[x]`

**Acceptance Criteria**: Create Neo4j nodes specifically tracking technology sector concentration with relationships to dependent indices.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
// Tech Concentration Node
CREATE CONSTRAINT tech_concentration_id IF NOT EXISTS 
    FOR (t:TECH_CONCENTRATION) REQUIRE t.id IS UNIQUE;

(:TECH_CONCENTRATION {
    id: "uuid",
    snapshot_date: date(),
    total_tech_weight: 0.35,
    top_5_tech_weight: 0.28,
    apple_weight: 0.07,
    microsoft_weight: 0.06,
    nvidia_weight: 0.05,
    amazon_weight: 0.05,
    google_weight: 0.05,
    alert_level: "HIGH"
})

// Relationships
(:INDEX_FUND)-[:HAS_TECH_CONCENTRATION {
    as_of_date: date()
}]->(:TECH_CONCENTRATION)

(:TECH_CONCENTRATION)-[:DOMINATED_BY {
    weight: 0.07
}]->(:COMPANY:TECH {ticker: "AAPL"})

(:PORTFOLIO)-[:EXPOSED_TO {
    indirect_tech_weight: 0.35
}]->(:TECH_CONCENTRATION)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Tech Concentration Graph | `services/neo4j/tech_concentration_graph.py` | `[x]` |
| Sector Weight Analyzer | `services/analysis/sector_weight_analyzer.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Tech Concentration Graph | `frontend2/src/components/Neo4j/TechConcentrationGraph.jsx` | `[x]` |
| Sector Breakdown Chart | `frontend2/src/components/Charts/SectorBreakdown.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Tech Graph | `tests/unit/test_tech_concentration_graph.py` | `[x]` |
| Integration: Neo4j | `tests/integration/test_tech_concentration_neo4j.py` | `[x]` |

---

### 129.5 Diversification Repair Tool `[x]`

**Acceptance Criteria**: Build a tool that suggests trades to repair portfolio diversification when concentration thresholds are breached.

#### Backend Implementation

```python
class DiversificationRepairTool:
    """
    Suggest trades to repair portfolio diversification.
    
    Strategies:
    1. Trim overweight positions
    2. Add equal-weighted ETFs
    3. Add non-correlated assets
    4. Add sector-specific ETFs to balance
    """
    
    def analyze_diversification_gaps(
        self, 
        portfolio: Portfolio
    ) -> DiversificationAnalysis:
        """Identify diversification weaknesses."""
        pass
    
    def generate_repair_suggestions(
        self, 
        analysis: DiversificationAnalysis
    ) -> list[RepairSuggestion]:
        """Generate specific trade suggestions to improve diversification."""
        pass
    
    def estimate_improvement(
        self, 
        current: Portfolio, 
        after_repairs: Portfolio
    ) -> ImprovementMetrics:
        """Estimate the diversification improvement from suggested trades."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Diversification Repair Tool | `services/portfolio/diversification_repair.py` | `[x]` |
| Gap Analyzer | `services/portfolio/gap_analyzer.py` | `[x]` |
| Suggestion Generator | `services/portfolio/suggestion_generator.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Repair Tool Interface | `frontend2/src/components/Portfolio/RepairTool.jsx` | `[x]` |
| Suggestion Cards | `frontend2/src/components/Portfolio/SuggestionCards.jsx` | `[x]` |
| Before/After Comparison | `frontend2/src/components/Charts/BeforeAfterComparison.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Repair Tool | `tests/unit/test_diversification_repair.py` | `[x]` |
| Unit: Gap Analyzer | `tests/unit/test_gap_analyzer.py` | `[x]` |
| Integration: Full Repair Flow | `tests/integration/test_repair_flow.py` | `[x]` |
| E2E: Repair Tool UI | `tests/e2e/test_repair_tool_ui.py` | `[x]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 129.1 Top 10 > 40% Detection | `[x]` | `[ ]` |
| 129.2 Equal Weight Rebalancer | `[x]` | `[ ]` |
| 129.3 Fundamental Distortion Log | `[x]` | `[ ]` |
| 129.4 Neo4j Tech Concentration | `[x]` | `[ ]` |
| 129.5 Diversification Repair | `[x]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py concentration analyze <index>` | Analyze index concentration | `[x]` |
| `python cli.py concentration hhi <index>` | Calculate HHI | `[x]` |
| `python cli.py diversification repair <portfolio>` | Generate repair suggestions | `[x]` |
| `python cli.py rebalance equal-weight <portfolio>` | Generate equal-weight rebalance | `[x]` |

---

## 📦 Dependencies

- Phase 106: Diversification & Correlation Engine
- Phase 3: TimescaleDB (Postgres docker-compose)
- Phase 4: Neo4j Graph (Neo4j docker-compose)

---

*Last verified: 2026-01-25*
