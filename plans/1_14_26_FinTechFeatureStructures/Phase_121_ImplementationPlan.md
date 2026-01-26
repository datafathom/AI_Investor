# Phase 121: Diversification & Non-Correlated Asset Mapper

> **Status**: `[ ]` Not Started | **Owner**: Quantitative Team
> **Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 1

## 📋 Overview
**Description**: Map asset classes with low or negative correlation (commodities, bonds, real estate, crypto) in Neo4j to enable true portfolio diversification beyond correlated equity exposures.

---

## 🎯 Sub-Deliverables

### 121.1 Neo4j Commodities/Bonds/Real Estate Nodes `[ ]`

```cypher
// Non-Correlated Asset Nodes
(:ASSET_CLASS:COMMODITY {
    id: "uuid",
    name: "Gold",
    ticker: "GLD",
    correlation_to_spy: -0.05,
    inflation_hedge: true
})

(:ASSET_CLASS:FIXED_INCOME {
    id: "uuid",
    name: "US Treasury 10-Year",
    correlation_to_spy: -0.20,
    duration: 8.5
})

(:ASSET_CLASS:REAL_ESTATE {
    id: "uuid", 
    name: "US REITs",
    ticker: "VNQ",
    correlation_to_spy: 0.65,
    dividend_yield: 0.038
})

// Non-Correlated Relationship
(:ASSET)-[:NEGATIVELY_CORRELATED_WITH {
    coefficient: -0.25,
    timeframe: "5Y",
    crisis_correlation: 0.15
}]->(:ASSET)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Asset Class Graph | `services/neo4j/asset_class_graph.py` | `[ ]` |
| Correlation Updater | `services/quantitative/correlation_updater.py` | `[ ]` |

### 121.2 Rolling Correlation Coefficient Function `[ ]`
Calculate rolling correlations across multiple timeframes.

| Component | File Path | Status |
|-----------|-----------|--------|
| Rolling Correlation | `services/quantitative/rolling_correlation.py` | `[ ]` |

### 121.3 'Out of Favor' Contrarian Rebalancing Service `[ ]`
Identify and recommend rebalancing into out-of-favor asset classes.

| Component | File Path | Status |
|-----------|-----------|--------|
| Contrarian Rebalancer | `services/portfolio/contrarian_rebalancer.py` | `[ ]` |

### 121.4 Correlation Alert (1.0 Coefficient Warning) `[ ]`
Alert when correlations approach 1.0 during crisis periods.

| Component | File Path | Status |
|-----------|-----------|--------|
| Correlation Alert | `services/alerts/correlation_alert.py` | `[ ]` |

### 121.5 Risk-Adjusted Return Prioritization `[ ]`
Prioritize assets by risk-adjusted returns (Sharpe-weighted).

| Component | File Path | Status |
|-----------|-----------|--------|
| Return Prioritizer | `services/quantitative/return_prioritizer.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED
