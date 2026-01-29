# Phase 106: Diversification & Correlation Engine

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Build a comprehensive correlation analysis engine that tracks asset class relationships in Neo4j, detects concentration risks, and monitors non-correlated asset movements to ensure true portfolio diversification.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Phase 6 (Diversification & Correlation Engine)

---

## 🎯 Sub-Deliverables

### 106.1 Neo4j Asset Class Correlation Graph `[x]`

**Acceptance Criteria**: Create a comprehensive Neo4j graph modeling correlations between all asset classes (stocks, bonds, commodities, real estate, crypto) with time-varying edge weights.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
// Asset Class Nodes
CREATE CONSTRAINT asset_class_id IF NOT EXISTS FOR (a:ASSET_CLASS) REQUIRE a.id IS UNIQUE;

(:ASSET_CLASS {
    id: "uuid",
    name: "Large Cap US Equities",
    category: "EQUITY",        // EQUITY, FIXED_INCOME, COMMODITY, REAL_ESTATE, CRYPTO
    subcategory: "US_LARGE_CAP",
    benchmark_ticker: "SPY",
    volatility_annual: 0.18,   // 18% annual volatility
    expected_return: 0.10      // 10% expected return
})

// Correlation Relationships (Time-varying)
(:ASSET_CLASS)-[:CORRELATED_WITH {
    coefficient: 0.85,         // Pearson correlation -1.0 to 1.0
    timeframe: "1Y",           // 1M, 3M, 6M, 1Y, 3Y, 5Y
    p_value: 0.01,
    sample_size: 252,          // Trading days
    is_significant: true,
    updated_at: datetime()
}]->(:ASSET_CLASS)

// Portfolio Holdings
(:PORTFOLIO)-[:ALLOCATES {
    weight: 0.25,              // 25% allocation
    target_weight: 0.30,
    drift: -0.05
}]->(:ASSET_CLASS)

// Diversification Benefit Edges
(:ASSET_CLASS)-[:PROVIDES_DIVERSIFICATION {
    benefit_score: 0.85,       // 0 to 1
    crisis_correlation: 0.95,  // Correlation during market stress
    normal_correlation: 0.45
}]->(:ASSET_CLASS)
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Correlation Graph Service | `services/neo4j/correlation_graph.py` | `[x]` |
| Correlation Calculator | `services/quantitative/correlation_calculator.py` | `[x]` |
| Graph Updater | `services/neo4j/correlation_updater.py` | `[x]` |
| API Endpoint | `web/api/portfolio/correlations.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Correlation Matrix | `frontend2/src/components/Correlation/CorrelationMatrix.jsx` | `[x]` |
| Asset Graph Visualizer | `frontend2/src/components/Neo4j/AssetCorrelationGraph.jsx` | `[x]` |
| useCorrelation Hook | `frontend2/src/hooks/useCorrelation.js` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Correlation Calculator | `tests/unit/test_correlation_calculator.py` | `[x]` |
| Unit: Graph Service | `tests/unit/test_correlation_graph.py` | `[x]` |
| Integration: Neo4j | `tests/integration/test_correlation_neo4j.py` | `[x]` |
| E2E: Matrix UI | `tests/e2e/test_correlation_matrix.py` | `[x]` |

---

### 106.2 Concentration Risk Detector (40% Threshold) `[x]`

**Acceptance Criteria**: Implement automatic detection when any single asset class, sector, or holding exceeds 40% of portfolio value, triggering rebalancing alerts.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE concentration_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Concentration Details
    concentration_type VARCHAR(50) NOT NULL,  -- ASSET_CLASS, SECTOR, SINGLE_HOLDING
    entity_id UUID NOT NULL,
    entity_name VARCHAR(255),
    
    -- Metrics
    current_weight DECIMAL(8, 6) NOT NULL,
    threshold_weight DECIMAL(8, 6) NOT NULL,
    excess_weight DECIMAL(8, 6) GENERATED ALWAYS AS 
        (current_weight - threshold_weight) STORED,
    
    -- Alert Status
    alert_level VARCHAR(20) NOT NULL,        -- WARNING, CRITICAL
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMPTZ,
    
    -- Timestamps
    triggered_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

CREATE INDEX idx_concentration_portfolio ON concentration_alerts(portfolio_id);
CREATE INDEX idx_concentration_level ON concentration_alerts(alert_level);
```

#### Backend Implementation

```python
class ConcentrationRiskDetector:
    """
    Detect portfolio concentration risks.
    
    Thresholds (configurable):
    - Single holding: 10%
    - Sector: 25%
    - Asset class: 40%
    - Top 5 holdings: 50%
    """
    
    DEFAULT_THRESHOLDS = {
        'SINGLE_HOLDING': Decimal('0.10'),
        'SECTOR': Decimal('0.25'),
        'ASSET_CLASS': Decimal('0.40'),
        'TOP_5_HOLDINGS': Decimal('0.50'),
        'TOP_5_TECH': Decimal('0.35')  # Phase 106.3
    }
    
    def detect_concentrations(self, portfolio: Portfolio) -> list[ConcentrationAlert]:
        """Scan portfolio for all concentration risks."""
        pass
    
    def calculate_herfindahl_index(self, portfolio: Portfolio) -> Decimal:
        """Calculate HHI for concentration measurement."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/106_concentration_alerts.sql` | `[x]` |
| Concentration Detector | `services/risk/concentration_detector.py` | `[x]` |
| Alert Generator | `services/alerts/concentration_alerts.py` | `[x]` |
| Rebalance Suggester | `services/portfolio/rebalance_suggester.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Concentration Alert Banner | `frontend2/src/components/Alerts/ConcentrationAlert.jsx` | `[x]` |
| Pie Chart with Thresholds | `frontend2/src/components/Charts/ConcentrationPieChart.jsx` | `[x]` |
| Rebalance Suggestions | `frontend2/src/components/Portfolio/RebalanceSuggestions.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Detector | `tests/unit/test_concentration_detector.py` | `[x]` |
| Unit: HHI Calculation | `tests/unit/test_herfindahl_index.py` | `[x]` |
| Integration: Full Pipeline | `tests/integration/test_concentration_pipeline.py` | `[x]` |

---

### 106.3 Top 5 Tech Concentration Identifier (35%) `[x]`

**Acceptance Criteria**: Specifically track concentration in top 5 technology holdings (AAPL, MSFT, GOOGL, AMZN, NVDA) with a 35% threshold alert, addressing the "Diversification Myth" in index funds.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Tech Concentration Tracker | `services/risk/tech_concentration.py` | `[x]` |
| Index Holdings Analyzer | `services/analysis/index_holdings.py` | `[x]` |
| Overlap Calculator | `services/portfolio/overlap_calculator.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Tech Concentration Widget | `frontend2/src/components/Risk/TechConcentrationWidget.jsx` | `[x]` |
| Holdings Overlap Chart | `frontend2/src/components/Charts/HoldingsOverlapChart.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Tech Tracker | `tests/unit/test_tech_concentration.py` | `[x]` |
| Unit: Overlap Calculator | `tests/unit/test_overlap_calculator.py` | `[x]` |
| Integration: Tech Alert | `tests/integration/test_tech_concentration_alert.py` | `[x]` |

---

### 106.4 Non-Correlated Movement Matrix `[x]`

**Acceptance Criteria**: Build a real-time matrix tracking when supposedly non-correlated assets suddenly move together (correlation breakdown), a key indicator of systemic risk.

#### Kafka Topic (Docker-compose: redpanda service)

```json
{
    "topic": "correlation-breakdown-alerts",
    "partitions": 3,
    "retention_ms": 604800000,
    "schema": {
        "alert_id": "uuid",
        "asset_pair": ["ASSET_A", "ASSET_B"],
        "expected_correlation": "decimal",
        "actual_correlation": "decimal",
        "deviation": "decimal",
        "timeframe": "string",
        "severity": "string",
        "timestamp": "timestamp"
    }
}
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Movement Matrix Service | `services/quantitative/movement_matrix.py` | `[x]` |
| Correlation Breakdown Detector | `services/risk/correlation_breakdown.py` | `[x]` |
| Kafka Alert Publisher | `services/kafka/correlation_alert_publisher.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Correlation Heatmap | `frontend2/src/components/Charts/CorrelationHeatmap.jsx` | `[x]` |
| Breakdown Alert Panel | `frontend2/src/components/Alerts/CorrelationBreakdownAlert.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Movement Matrix | `tests/unit/test_movement_matrix.py` | `[x]` |
| Unit: Breakdown Detector | `tests/unit/test_correlation_breakdown.py` | `[x]` |
| Integration: Kafka Alerts | `tests/integration/test_correlation_kafka.py` | `[x]` |

---

### 106.5 Risk-Adjusted Return Volatility Calculator `[x]`

**Acceptance Criteria**: Implement comprehensive volatility calculations including standard deviation, downside deviation, and max drawdown to complement correlation analysis.

#### Backend Implementation

```python
class VolatilityCalculator:
    """
    Calculate various volatility and risk metrics.
    
    Metrics:
    - Standard Deviation (annualized)
    - Downside Deviation (Sortino denominator)
    - Maximum Drawdown and duration
    - Ulcer Index (downside risk)
    - Value at Risk (VaR) at 95% and 99%
    """
    
    def calculate_standard_deviation(
        self, 
        returns: list[Decimal], 
        annualize: bool = True
    ) -> Decimal:
        pass
    
    def calculate_var(
        self, 
        returns: list[Decimal], 
        confidence: Decimal = Decimal('0.95')
    ) -> Decimal:
        """Calculate Value at Risk at given confidence level."""
        pass
    
    def calculate_max_drawdown(
        self, 
        equity_curve: list[Decimal]
    ) -> MaxDrawdownResult:
        """Calculate maximum drawdown and recovery time."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Volatility Calculator | `services/quantitative/volatility_calculator.py` | `[x]` |
| VaR Calculator | `services/risk/var_calculator.py` | `[x]` |
| Max Drawdown Analyzer | `services/risk/max_drawdown.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Volatility Dashboard | `frontend2/src/components/Risk/VolatilityDashboard.jsx` | `[x]` |
| Drawdown Chart | `frontend2/src/components/Charts/DrawdownChart.jsx` | `[x]` |
| VaR Gauge | `frontend2/src/components/Risk/VaRGauge.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Volatility Calculator | `tests/unit/test_volatility_calculator.py` | `[x]` |
| Unit: VaR | `tests/unit/test_var_calculator.py` | `[x]` |
| Unit: Max Drawdown | `tests/unit/test_max_drawdown.py` | `[x]` |
| Integration: Full Risk Suite | `tests/integration/test_risk_metrics.py` | `[x]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 106.1 Neo4j Correlation Graph | `[x]` | `[ ]` |
| 106.2 Concentration Detector | `[x]` | `[ ]` |
| 106.3 Top 5 Tech Identifier | `[x]` | `[ ]` |
| 106.4 Non-Correlated Matrix | `[x]` | `[ ]` |
| 106.5 Volatility Calculator | `[x]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py correlation matrix` | Show correlation matrix | `[x]` |
| `python cli.py concentration check` | Check concentration risks | `[x]` |
| `python cli.py volatility calc <portfolio_id>` | Calculate volatility | `[x]` |
| `python cli.py diversification score` | Calculate diversification score | `[x]` |

---

## 📦 Dependencies

- Phase 3: TimescaleDB (Postgres docker-compose)
- Phase 4: Neo4j Graph (Neo4j docker-compose)
- Phase 1: Redpanda Cluster (Kafka docker-compose)

---

*Last verified: 2026-01-25*
