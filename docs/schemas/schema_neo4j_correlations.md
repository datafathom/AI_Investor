# Schema: Neo4j Correlations

## File Location
`schemas/neo4j/correlations.cypher`

## Purpose
Cypher schema definitions for CORRELATED_WITH relationships between assets. Supports the currency correlation analysis system for detecting statistical relationships between assets.

---

## Relationship Type

### CORRELATED_WITH
**Represents statistical correlation between two assets.**

Direction: `(:ASSET)-[:CORRELATED_WITH]->(:ASSET)`

| Property | Type | Range | Description |
|----------|------|-------|-------------|
| `coefficient` | float | -1.0 to 1.0 | Pearson correlation coefficient |
| `confidence` | float | 0.0 to 1.0 | Statistical confidence level |
| `timeframe` | string | `1D`, `4H`, `1W` | Calculation time window |
| `direction` | string | `POSITIVE`, `NEGATIVE`, `NEUTRAL` | Correlation direction classification |
| `updated_at` | datetime | - | Last recalculation timestamp |

---

## Correlation Interpretation

| Coefficient Range | Direction | Interpretation |
|-------------------|-----------|----------------|
| 0.7 to 1.0 | POSITIVE | Strong positive correlation |
| 0.3 to 0.7 | POSITIVE | Moderate positive correlation |
| -0.3 to 0.3 | NEUTRAL | Weak or no correlation |
| -0.7 to -0.3 | NEGATIVE | Moderate negative correlation |
| -1.0 to -0.7 | NEGATIVE | Strong negative correlation |

---

## Usage Examples

```cypher
// Find strongly correlated assets to a given symbol
MATCH (a:ASSET {symbol: 'EURUSD'})-[r:CORRELATED_WITH]->(b:ASSET)
WHERE r.coefficient > 0.7
RETURN b.symbol, r.coefficient, r.timeframe
ORDER BY r.coefficient DESC

// Find hedging candidates (negative correlation)
MATCH (a:ASSET {symbol: 'SPY'})-[r:CORRELATED_WITH]->(b:ASSET)
WHERE r.coefficient < -0.6
RETURN b.symbol, r.coefficient

// Get correlations updated within last 24 hours
MATCH (a:ASSET)-[r:CORRELATED_WITH]->(b:ASSET)
WHERE r.updated_at > datetime() - duration('P1D')
RETURN a.symbol, b.symbol, r.coefficient
```

---

## Data Flow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│ Market Data     │ ──▶ │ Correlation      │ ──▶ │ Neo4j       │
│ Service         │     │ Calculation      │     │ Graph       │
└─────────────────┘     │ Service          │     └─────────────┘
                        └──────────────────┘
```

---

## Integration Points

| Service | Usage |
|---------|-------|
| `CorrelationService` | Coefficient calculations |
| `PairsTradingService` | Pair identification |
| `RiskManagementService` | Diversification analysis |
| `PortfolioOptimizationService` | Correlation matrix construction |
