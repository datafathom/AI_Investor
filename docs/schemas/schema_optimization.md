# Schema: Optimization

## File Location
`schemas/optimization.py`

## Purpose
Pydantic models for portfolio optimization including optimization objectives, constraints, results, and rebalancing strategies using modern portfolio theory and advanced optimization techniques.

---

## Enums

### OptimizationObjective
**Portfolio optimization goals.**

| Value | Description |
|-------|-------------|
| `MAX_SHARPE` | Maximize Sharpe ratio |
| `MIN_VOLATILITY` | Minimize portfolio volatility |
| `MAX_RETURN` | Maximize expected return |
| `RISK_PARITY` | Equal risk contribution |

---

### OptimizationMethod
**Optimization algorithms.**

| Value | Description |
|-------|-------------|
| `MEAN_VARIANCE` | Markowitz mean-variance |
| `BLACK_LITTERMAN` | Black-Litterman model |
| `HIERARCHICAL_RISK_PARITY` | HRP optimization |
| `MINIMUM_VARIANCE` | Minimum variance portfolio |

---

## Models

### PositionConstraint
**Constraint on individual position sizes.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `symbol` | `str` | *required* | Stock ticker | Identification |
| `min_weight` | `float` | `0.0` | Minimum weight | Lower bound |
| `max_weight` | `float` | `1.0` | Maximum weight | Upper bound |

---

### SectorConstraint
**Constraint on sector allocations.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `sector` | `str` | *required* | Sector name | Identification |
| `min_weight` | `float` | `0.0` | Minimum allocation | Lower bound |
| `max_weight` | `float` | `1.0` | Maximum allocation | Upper bound |

---

### OptimizationConstraints
**Complete constraint set for optimization.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `position_constraints` | `List[PositionConstraint]` | `[]` | Position limits | Security limits |
| `sector_constraints` | `List[SectorConstraint]` | `[]` | Sector limits | Sector limits |
| `max_turnover` | `Optional[float]` | `None` | Maximum turnover | Transaction limits |
| `min_positions` | `Optional[int]` | `None` | Minimum holdings | Diversification |
| `max_positions` | `Optional[int]` | `None` | Maximum holdings | Concentration |

---

### OptimizationResult
**Optimization output.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `result_id` | `str` | *required* | Unique result ID | Primary key |
| `objective` | `OptimizationObjective` | *required* | Optimization goal | Context |
| `method` | `OptimizationMethod` | *required* | Algorithm used | Methodology |
| `optimal_weights` | `Dict[str, float]` | *required* | Optimal portfolio weights | Result |
| `expected_return` | `float` | *required* | Portfolio expected return | Performance |
| `expected_volatility` | `float` | *required* | Portfolio volatility | Risk |
| `sharpe_ratio` | `float` | *required* | Risk-adjusted return | Quality |
| `optimization_date` | `datetime` | *required* | When optimized | Freshness |

---

### RebalancingStrategy
**Rebalancing approach configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `strategy_id` | `str` | *required* | Strategy identifier | Primary key |
| `strategy_type` | `str` | *required* | Type: `calendar`, `threshold`, `optimizer` | Approach |
| `calendar_frequency` | `Optional[str]` | `None` | Frequency: `monthly`, `quarterly` | Calendar trigger |
| `drift_threshold` | `Optional[float]` | `None` | Trigger threshold | Threshold trigger |
| `tax_aware` | `bool` | `False` | Consider tax impact | Tax optimization |

---

### RebalancingRecommendation
**Generated rebalancing trades.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `recommendation_id` | `str` | *required* | Unique ID | Primary key |
| `portfolio_id` | `str` | *required* | Target portfolio | Linking |
| `current_weights` | `Dict[str, float]` | *required* | Current allocation | Baseline |
| `target_weights` | `Dict[str, float]` | *required* | Target allocation | Goal |
| `trades` | `List[Dict]` | *required* | Recommended trades | Execution |
| `estimated_cost` | `float` | *required* | Transaction costs | Cost analysis |
| `tax_impact` | `Optional[float]` | `None` | Estimated tax impact | Tax awareness |
| `generated_date` | `datetime` | *required* | Generation timestamp | Freshness |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `PortfolioOptimizationService` | Optimization engine |
| `RebalancingService` | Rebalancing execution |
| `TaxLossHarvestingService` | Tax-aware rebalancing |

## Frontend Components
- Optimization dashboard (FrontendOptimization)
- Efficient frontier chart
- Rebalancing preview
