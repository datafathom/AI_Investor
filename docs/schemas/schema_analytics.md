# Schema: Analytics

## File Location
`schemas/analytics.py`

## Purpose
Comprehensive Pydantic models for portfolio analytics including performance attribution, risk decomposition, concentration analysis, and tail risk metrics. Used for institutional-grade portfolio analysis and reporting.

---

## Enums

### AttributionType
**Types of performance attribution calculations.**

| Value | Description |
|-------|-------------|
| `MULTI_FACTOR` | Multi-factor model attribution |
| `HIERARCHICAL` | Hierarchical/nested attribution analysis |
| `SIMPLE` | Basic attribution calculation |

---

## Performance Attribution Models

### AttributionBreakdown
**Breakdown of attribution effects for a category.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `category` | `str` | *required* | Category name (sector, asset class, etc.) | Grouping attribution results |
| `allocation_effect` | `float` | *required* | Allocation effect in basis points | Measures impact of weight decisions vs. benchmark |
| `selection_effect` | `float` | *required* | Selection effect in basis points | Measures impact of security selection within category |
| `interaction_effect` | `float` | *required* | Interaction effect in basis points | Cross-effect between allocation and selection |
| `total_effect` | `float` | *required* | Total effect in basis points | Sum of all effects |
| `weight` | `float` | *required* | Portfolio weight (0-1) | Category exposure |
| `return_pct` | `float` | *required* | Return percentage for category | Performance contribution |

---

### HoldingAttribution
**Attribution metrics for individual holdings.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `symbol` | `str` | Security ticker | Identification |
| `name` | `str` | Security name | Display |
| `weight` | `float` | Portfolio weight | Position sizing |
| `return_pct` | `float` | Holding return | Performance measurement |
| `contribution_absolute` | `float` | Dollar contribution to portfolio return | Absolute impact |
| `contribution_pct` | `float` | Percentage contribution | Relative impact |
| `allocation_effect` | `float` | Weight decision impact | Attribution decomposition |
| `selection_effect` | `float` | Security choice impact | Attribution decomposition |

---

### BenchmarkComparison
**Portfolio vs. benchmark comparison results.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `benchmark_symbol` | `str` | Benchmark identifier (e.g., SPY, AGG) | Reference point |
| `portfolio_return` | `float` | Portfolio total return | Performance |
| `benchmark_return` | `float` | Benchmark total return | Comparison baseline |
| `active_return` | `float` | Portfolio return minus benchmark | Alpha measurement |
| `allocation_effect` | `float` | Sector/category allocation impact | Attribution analysis |
| `selection_effect` | `float` | Security selection impact | Attribution analysis |
| `interaction_effect` | `float` | Allocation-selection interaction | Attribution analysis |
| `tracking_error` | `float` | Standard deviation of active returns | Risk vs. benchmark |

---

### CalculationMetadata
**Metadata about how the calculation was performed.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `calculation_method` | `str` | *required* | Algorithm used | Transparency, reproducibility |
| `calculation_date` | `datetime` | *required* | When calculated | Freshness |
| `data_quality` | `str` | *required* | Data quality assessment | Confidence level |
| `missing_data_points` | `int` | *required* | Count of missing data | Quality indicator |
| `cache_hit` | `bool` | `False` | Whether result was cached | Performance monitoring |

---

### AttributionResult
**Complete performance attribution result.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `portfolio_id` | `str` | Portfolio identifier | Linking to portfolio |
| `period_start` | `datetime` | Analysis start date | Time period |
| `period_end` | `datetime` | Analysis end date | Time period |
| `total_return` | `float` | Portfolio total return (absolute) | Performance summary |
| `total_return_pct` | `float` | Portfolio total return (percentage) | Performance summary |
| `attribution_by_asset_class` | `Dict[str, AttributionBreakdown]` | Attribution by asset class | Asset allocation analysis |
| `attribution_by_sector` | `Dict[str, AttributionBreakdown]` | Attribution by sector | Sector analysis |
| `attribution_by_geography` | `Dict[str, AttributionBreakdown]` | Attribution by geography | Geographic analysis |
| `attribution_by_holding` | `List[HoldingAttribution]` | Per-holding attribution | Security-level analysis |
| `benchmark_comparison` | `Optional[BenchmarkComparison]` | Benchmark analysis | Active management analysis |
| `calculation_metadata` | `CalculationMetadata` | Calculation details | Audit trail |

---

### HoldingContribution
**Individual holding performance contribution.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `symbol` | `str` | Security ticker | Identification |
| `name` | `str` | Security name | Display |
| `weight` | `float` | Portfolio weight | Position size |
| `return_pct` | `float` | Holding return | Performance |
| `contribution_absolute` | `float` | Dollar contribution | Absolute impact |
| `contribution_pct` | `float` | Percentage contribution | Relative impact |
| `rank` | `int` | Contribution ranking | Top/bottom performers |

---

## Risk Decomposition Models

### FactorExposure
**Single factor exposure within a factor model.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `factor_name` | `str` | Factor identifier (e.g., "Value", "Momentum") | Factor identification |
| `exposure` | `float` | Portfolio beta to factor | Factor loading |
| `contribution` | `float` | Return contribution from factor | Performance decomposition |
| `risk_contribution` | `float` | Risk contribution from factor | Risk decomposition |

---

### FactorRiskDecomposition
**Complete factor risk decomposition result.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `portfolio_id` | `str` | Portfolio identifier | Linking |
| `factor_model` | `str` | Model used (e.g., "Fama-French 5") | Methodology |
| `total_risk` | `float` | Total portfolio risk | Risk summary |
| `factor_exposures` | `List[FactorExposure]` | All factor exposures | Detailed decomposition |
| `idiosyncratic_risk` | `float` | Security-specific risk | Diversification measure |
| `r_squared` | `float` | Model explanatory power | Model fit |

---

## Concentration Risk Models

### ConcentrationMetric
**Concentration metrics for a single dimension.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `dimension` | `str` | What is being measured (holding, sector, etc.) | Categorization |
| `herfindahl_hirschman_index` | `float` | HHI concentration index | Standard concentration measure |
| `top_5_concentration` | `float` | Weight of top 5 holdings/categories | Quick concentration check |
| `top_10_concentration` | `float` | Weight of top 10 holdings/categories | Extended check |
| `max_weight` | `float` | Largest single weight | Maximum exposure |
| `max_weight_symbol` | `str` | Symbol with largest weight | Top position identification |

---

### ConcentrationRiskAnalysis
**Multi-dimensional concentration risk analysis.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `portfolio_id` | `str` | Portfolio identifier | Linking |
| `by_holding` | `ConcentrationMetric` | Security-level concentration | Position concentration |
| `by_sector` | `ConcentrationMetric` | Sector concentration | Sector diversification |
| `by_geography` | `ConcentrationMetric` | Geographic concentration | Geographic diversification |
| `by_asset_class` | `ConcentrationMetric` | Asset class concentration | Asset allocation |

---

### CorrelationAnalysis
**Portfolio correlation analysis.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `portfolio_id` | `str` | Portfolio identifier | Linking |
| `correlation_matrix` | `Dict[str, Dict[str, float]]` | Full correlation matrix | Correlation visualization |
| `average_correlation` | `float` | Mean pairwise correlation | Diversification summary |
| `diversification_ratio` | `float` | Diversification benefit measure | Diversification effectiveness |
| `highly_correlated_pairs` | `List[Dict[str, str]]` | Pairs with correlation > threshold | Risk concentration alerts |

---

## Tail Risk Models

### TailRiskContribution
**Individual holding tail risk contribution.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `symbol` | `str` | Security ticker | Identification |
| `var_contribution` | `float` | Contribution to portfolio VaR | VaR decomposition |
| `cvar_contribution` | `float` | Contribution to portfolio CVaR | CVaR decomposition |
| `marginal_var` | `float` | Marginal VaR (impact of adding 1 unit) | Position sizing |
| `marginal_cvar` | `float` | Marginal CVaR | Tail risk management |

---

### TailRiskContributions
**Portfolio-level tail risk contributions.**

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `portfolio_id` | `str` | Portfolio identifier | Linking |
| `confidence_level` | `float` | Confidence level (e.g., 0.95, 0.99) | Risk threshold |
| `portfolio_var` | `float` | Total portfolio VaR | Risk summary |
| `portfolio_cvar` | `float` | Total portfolio CVaR (expected shortfall) | Tail risk summary |
| `contributions` | `List[TailRiskContribution]` | Per-holding contributions | Risk allocation |
| `method` | `str` | Calculation method used | Methodology |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `PerformanceAttributionService` | Generates attribution results |
| `RiskDecompositionService` | Factor risk analysis |
| `ConcentrationRiskService` | Concentration metrics |
| `TailRiskService` | VaR/CVaR calculations |

## API Endpoints
- `GET /api/analytics/attribution/{portfolio_id}` - Performance attribution
- `GET /api/analytics/factor-risk/{portfolio_id}` - Factor decomposition
- `GET /api/analytics/concentration/{portfolio_id}` - Concentration analysis
- `GET /api/analytics/tail-risk/{portfolio_id}` - Tail risk metrics

## Frontend Components
- Analytics dashboard (FrontendAnalytics)
- Attribution charts
- Factor exposure heatmaps
- Concentration visualizations
