# Phase 1: Advanced Portfolio Analytics Engine

## Phase Status: `NOT_STARTED` ⚠️
**Last Updated**: 2026-01-21
**Estimated Duration**: 7-10 days
**Priority**: CRITICAL (Foundation for advanced analytics)
**Started Date**: TBD
**Completion Status**: Not Started

---

## Phase Overview

Build a sophisticated portfolio analytics engine that provides deep insights into portfolio composition, performance attribution, and risk decomposition. This phase establishes the foundation for all advanced portfolio analysis features and enables users to understand exactly how their portfolio is performing and why.

### Dependencies
- Portfolio service must be operational
- Market data APIs (Alpha Vantage, Polygon, etc.)
- Historical price data access
- Redis cache for performance
- Database schema for analytics storage

### Risk Factors
- Complex calculations may impact performance
- Large portfolios may require optimization
- Real-time updates may be computationally expensive
- Data accuracy depends on market data quality

---

## Deliverable 1.1: Portfolio Performance Attribution Engine

### Status: `NOT_STARTED` ⚠️
### Assignee: TBD
### Start Date: TBD
### Completion Date: TBD

### Detailed Task Description

Create a comprehensive performance attribution engine that decomposes portfolio returns by multiple dimensions including asset class, sector, geography, individual holdings, and time periods. This engine must handle complex scenarios such as:

- **Multi-period attribution**: Calculate attribution across different time horizons (1 day, 1 week, 1 month, 3 months, 6 months, 1 year, YTD, All-time)
- **Multi-factor attribution**: Decompose returns by factors such as sector allocation, stock selection, currency effects, and timing effects
- **Hierarchical attribution**: Support nested hierarchies (e.g., Asset Class → Sector → Industry → Individual Stock)
- **Benchmark comparison**: Compare portfolio performance against custom or standard benchmarks (S&P 500, custom indices)
- **Contribution analysis**: Identify which holdings contributed most to overall performance

The attribution engine must:
1. **Handle cash flows**: Properly account for deposits, withdrawals, dividends, and rebalancing
2. **Calculate time-weighted returns**: Use industry-standard methodologies (Modified Dietz, BAI, etc.)
3. **Support multiple currencies**: Handle multi-currency portfolios with FX attribution
4. **Provide drill-down capabilities**: Allow users to drill down from high-level to detailed attribution
5. **Cache results**: Cache attribution calculations for performance
6. **Handle edge cases**: Gracefully handle missing data, corporate actions, splits, etc.

### Backend Implementation Details

**File**: `services/analytics/performance_attribution_service.py`

**Required Header Comment**:
```python
"""
==============================================================================
FILE: services/analytics/performance_attribution_service.py
ROLE: Portfolio Performance Attribution Engine
PURPOSE: Decomposes portfolio returns by asset class, sector, geography, and
         individual holdings. Provides multi-period and multi-factor attribution
         analysis with benchmark comparison capabilities.

INTEGRATION POINTS:
    - PortfolioService: Portfolio holdings and transactions
    - MarketDataService: Historical price data and benchmarks
    - CacheService: Caching attribution calculations
    - AnalyticsAPI: REST endpoints for attribution data
    - FrontendAnalytics: Dashboard widgets consuming attribution data

METHODOLOGY:
    - Time-weighted returns using Modified Dietz method
    - Multi-factor attribution (Brinson-Fachler model)
    - Hierarchical attribution with drill-down support
    - Benchmark-relative attribution

USAGE:
    from services.analytics.performance_attribution_service import PerformanceAttributionService
    service = PerformanceAttributionService()
    attribution = await service.calculate_attribution(
        portfolio_id="portfolio_123",
        start_date="2024-01-01",
        end_date="2024-12-31",
        benchmark="SPY"
    )

DEPENDENCIES:
    - pandas (data manipulation)
    - numpy (numerical calculations)
    - redis (caching)
    
AUTHOR: AI Investor Team
CREATED: TBD
LAST_MODIFIED: TBD
==============================================================================
"""
```

**Class Structure**:
```python
class PerformanceAttributionService:
    """
    Service for calculating portfolio performance attribution.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.portfolio_service = get_portfolio_service()
        self.market_data_service = get_market_data_service()
        self.cache_service = get_cache_service()
        
    async def calculate_attribution(
        self,
        portfolio_id: str,
        start_date: datetime,
        end_date: datetime,
        benchmark: Optional[str] = None,
        attribution_type: str = "multi_factor"
    ) -> AttributionResult:
        """
        Calculate performance attribution for a portfolio.
        
        Args:
            portfolio_id: Portfolio identifier
            start_date: Start date for attribution period
            end_date: End date for attribution period
            benchmark: Optional benchmark symbol (e.g., "SPY")
            attribution_type: Type of attribution ("multi_factor", "hierarchical", "simple")
            
        Returns:
            AttributionResult with decomposed returns
        """
        
    async def calculate_contribution(
        self,
        portfolio_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[HoldingContribution]:
        """
        Calculate contribution of each holding to overall return.
        
        Returns:
            List of holdings sorted by contribution (absolute and percentage)
        """
        
    async def calculate_benchmark_attribution(
        self,
        portfolio_id: str,
        benchmark_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> BenchmarkAttributionResult:
        """
        Calculate attribution relative to a benchmark.
        
        Returns:
            BenchmarkAttributionResult with active return decomposition
        """
```

**Data Models** (in `models/analytics.py`):
```python
class AttributionResult(BaseModel):
    """Result of performance attribution calculation."""
    portfolio_id: str
    period_start: datetime
    period_end: datetime
    total_return: float
    total_return_pct: float
    attribution_by_asset_class: Dict[str, AttributionBreakdown]
    attribution_by_sector: Dict[str, AttributionBreakdown]
    attribution_by_geography: Dict[str, AttributionBreakdown]
    attribution_by_holding: List[HoldingAttribution]
    benchmark_comparison: Optional[BenchmarkComparison]
    calculation_metadata: CalculationMetadata

class AttributionBreakdown(BaseModel):
    """Breakdown of attribution for a category."""
    category: str
    allocation_effect: float
    selection_effect: float
    interaction_effect: float
    total_effect: float
    weight: float
    return_pct: float

class HoldingContribution(BaseModel):
    """Contribution of a single holding."""
    symbol: str
    name: str
    weight: float
    return_pct: float
    contribution_absolute: float
    contribution_pct: float
    rank: int
```

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-1.1.1 | Service calculates time-weighted returns using Modified Dietz methodology with accuracy within 0.01% of manual calculations | `NOT_STARTED` | | |
| AC-1.1.2 | Attribution correctly decomposes returns by asset class (equity, fixed income, cash, alternatives) with allocation and selection effects | `NOT_STARTED` | | |
| AC-1.1.3 | Attribution correctly decomposes returns by sector (Technology, Healthcare, Finance, etc.) with drill-down to individual holdings | `NOT_STARTED` | | |
| AC-1.1.4 | Attribution correctly handles multi-currency portfolios with FX effect separation | `NOT_STARTED` | | |
| AC-1.1.5 | Service calculates contribution analysis identifying top 10 and bottom 10 contributors to performance | `NOT_STARTED` | | |
| AC-1.1.6 | Benchmark comparison correctly calculates active return and decomposes it into allocation, selection, and interaction effects | `NOT_STARTED` | | |
| AC-1.1.7 | Attribution calculations are cached with appropriate TTL (1 hour for daily, 24 hours for historical) | `NOT_STARTED` | | |
| AC-1.1.8 | Service handles edge cases: missing price data, corporate actions, splits, dividends, and cash flows | `NOT_STARTED` | | |
| AC-1.1.9 | Attribution supports multiple time periods (1D, 1W, 1M, 3M, 6M, 1Y, YTD, All-time) | `NOT_STARTED` | | |
| AC-1.1.10 | Calculation completes within 5 seconds for portfolios with up to 500 holdings | `NOT_STARTED` | | |
| AC-1.1.11 | Unit tests cover all attribution methods with synthetic data | `NOT_STARTED` | | |
| AC-1.1.12 | Integration tests verify attribution accuracy against known portfolio scenarios | `NOT_STARTED` | | |

---

## Deliverable 1.2: Risk Decomposition Service

### Status: `NOT_STARTED` ⚠️
### Assignee: TBD
### Start Date: TBD
### Completion Date: TBD

### Detailed Task Description

Build a comprehensive risk decomposition service that analyzes portfolio risk from multiple angles including factor exposure, concentration risk, correlation analysis, and tail risk. This service must provide:

- **Factor Risk Decomposition**: Decompose portfolio risk by factors (market, size, value, momentum, quality, low volatility)
- **Concentration Risk Analysis**: Identify concentration risk by holding, sector, geography, and asset class
- **Correlation Analysis**: Calculate portfolio correlation matrix and identify diversification opportunities
- **Tail Risk Metrics**: Calculate Value-at-Risk (VaR), Conditional VaR, and tail risk contributions
- **Risk Budgeting**: Allocate risk budget across holdings and identify risk-efficient portfolios
- **Risk Attribution**: Attribute portfolio risk to individual holdings and factors

The risk service must:
1. **Support multiple risk models**: Factor models, historical simulation, Monte Carlo
2. **Handle missing data**: Gracefully handle missing returns or factor data
3. **Calculate rolling metrics**: Support rolling windows for dynamic risk analysis
4. **Provide risk forecasts**: Forecast future risk based on current portfolio composition
5. **Compare to benchmarks**: Compare portfolio risk to benchmark risk
6. **Generate alerts**: Alert on significant risk changes or threshold breaches

### Backend Implementation Details

**File**: `services/analytics/risk_decomposition_service.py`

**Required Header Comment**:
```python
"""
==============================================================================
FILE: services/analytics/risk_decomposition_service.py
ROLE: Portfolio Risk Decomposition Engine
PURPOSE: Analyzes portfolio risk by factor exposure, concentration, correlation,
         and tail risk. Provides risk budgeting and risk attribution capabilities.

INTEGRATION POINTS:
    - PortfolioService: Portfolio holdings and weights
    - MarketDataService: Historical returns and factor data
    - RiskService: Existing risk metrics (VaR, CVaR)
    - AnalyticsAPI: REST endpoints for risk data
    - FrontendAnalytics: Risk visualization widgets

METHODOLOGY:
    - Factor risk models (Fama-French, Barra)
    - Historical simulation for tail risk
    - Correlation matrix analysis
    - Risk contribution analysis

USAGE:
    from services.analytics.risk_decomposition_service import RiskDecompositionService
    service = RiskDecompositionService()
    risk_analysis = await service.decompose_risk(
        portfolio_id="portfolio_123",
        risk_model="factor",
        lookback_days=252
    )

DEPENDENCIES:
    - pandas (data manipulation)
    - numpy (numerical calculations)
    - scipy (statistical functions)
    
AUTHOR: AI Investor Team
CREATED: TBD
LAST_MODIFIED: TBD
==============================================================================
"""
```

**Class Structure**:
```python
class RiskDecompositionService:
    """
    Service for decomposing portfolio risk.
    """
    
    async def decompose_factor_risk(
        self,
        portfolio_id: str,
        factor_model: str = "fama_french",
        lookback_days: int = 252
    ) -> FactorRiskDecomposition:
        """
        Decompose portfolio risk by factor exposure.
        
        Returns:
            FactorRiskDecomposition with factor exposures and contributions
        """
        
    async def calculate_concentration_risk(
        self,
        portfolio_id: str,
        dimensions: List[str] = ["holding", "sector", "geography"]
    ) -> ConcentrationRiskAnalysis:
        """
        Calculate concentration risk across multiple dimensions.
        
        Returns:
            ConcentrationRiskAnalysis with concentration metrics
        """
        
    async def analyze_correlation(
        self,
        portfolio_id: str,
        lookback_days: int = 252
    ) -> CorrelationAnalysis:
        """
        Analyze portfolio correlation structure.
        
        Returns:
            CorrelationAnalysis with correlation matrix and insights
        """
        
    async def calculate_tail_risk_contributions(
        self,
        portfolio_id: str,
        confidence_level: float = 0.95,
        method: str = "historical"
    ) -> TailRiskContributions:
        """
        Calculate tail risk contributions of holdings.
        
        Returns:
            TailRiskContributions with VaR/CVaR contributions
        """
```

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-1.2.1 | Factor risk decomposition correctly identifies portfolio exposure to market, size, value, momentum, quality, and low volatility factors | `NOT_STARTED` | | |
| AC-1.2.2 | Concentration risk correctly calculates Herfindahl-Hirschman Index (HHI) for holdings, sectors, and geographies | `NOT_STARTED` | | |
| AC-1.2.3 | Correlation analysis generates accurate correlation matrix for all portfolio holdings with statistical significance testing | `NOT_STARTED` | | |
| AC-1.2.4 | Tail risk contributions correctly attribute VaR and CVaR to individual holdings using historical simulation method | `NOT_STARTED` | | |
| AC-1.2.5 | Risk budgeting allocates risk budget across holdings and identifies holdings exceeding risk budget | `NOT_STARTED` | | |
| AC-1.2.6 | Service supports multiple risk models (Fama-French, Barra, custom factor models) | `NOT_STARTED` | | |
| AC-1.2.7 | Risk forecasts are generated with confidence intervals and compared to historical realized risk | `NOT_STARTED` | | |
| AC-1.2.8 | Risk alerts are triggered when portfolio risk exceeds user-defined thresholds or changes significantly | `NOT_STARTED` | | |
| AC-1.2.9 | Risk decomposition handles portfolios with up to 500 holdings within 10 seconds | `NOT_STARTED` | | |
| AC-1.2.10 | Unit tests verify risk calculations against known portfolio scenarios | `NOT_STARTED` | | |
| AC-1.2.11 | Integration tests confirm risk metrics match external risk calculation tools | `NOT_STARTED` | | |
| AC-1.2.12 | Risk decomposition results are cached appropriately to reduce computation load | `NOT_STARTED` | | |

---

## Deliverable 1.3: Advanced Portfolio Dashboard

### Status: `NOT_STARTED` ⚠️
### Assignee: TBD
### Start Date: TBD
### Completion Date: TBD

### Detailed Task Description

Create an interactive, comprehensive portfolio dashboard that visualizes all analytics data with drill-down capabilities, customizable views, and real-time updates. The dashboard must provide:

- **Performance Overview**: High-level performance metrics with trend visualization
- **Attribution Visualization**: Interactive charts showing attribution breakdowns
- **Risk Dashboard**: Risk metrics with heatmaps and correlation visualizations
- **Contribution Analysis**: Tables and charts showing top/bottom contributors
- **Benchmark Comparison**: Side-by-side comparison with benchmarks
- **Customizable Views**: User-defined views and saved layouts
- **Export Capabilities**: Export analytics data to PDF, Excel, CSV
- **Real-time Updates**: Live updates during market hours

The dashboard must:
1. **Be responsive**: Work on desktop, tablet, and mobile devices
2. **Support drill-down**: Allow users to drill from high-level to detailed views
3. **Be performant**: Load within 2 seconds and update smoothly
4. **Handle large datasets**: Efficiently render large portfolios and long time series
5. **Be accessible**: Meet WCAG 2.1 AA accessibility standards
6. **Support customization**: Allow users to customize layouts and metrics displayed

### Frontend Implementation Details

**Files**: 
- `frontend2/src/widgets/Analytics/PerformanceAttributionWidget.jsx`
- `frontend2/src/widgets/Analytics/RiskDecompositionWidget.jsx`
- `frontend2/src/widgets/Analytics/ContributionAnalysisWidget.jsx`
- `frontend2/src/widgets/Analytics/PortfolioAnalyticsDashboard.jsx`
- `frontend2/src/stores/analyticsStore.js`

**Required Header Comment** (in each file):
```javascript
/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Analytics/[WidgetName].jsx
 * ROLE: Portfolio Analytics Widget
 * PURPOSE: Displays [specific analytics] with interactive visualization and
 *          drill-down capabilities. Consumes data from PerformanceAttributionService
 *          and RiskDecompositionService via AnalyticsAPI.
 * 
 * INTEGRATION POINTS:
 *    - AnalyticsAPI: REST endpoints for analytics data
 *    - analyticsStore: Zustand store for analytics state
 *    - ChartLibrary: Recharts/D3 for visualizations
 *    - ExportService: PDF/Excel export functionality
 * 
 * FEATURES:
 *    - Interactive charts with zoom/pan
 *    - Drill-down from summary to detail
 *    - Real-time updates during market hours
 *    - Export to PDF/Excel/CSV
 *    - Customizable views and layouts
 * 
 * AUTHOR: AI Investor Team
 * CREATED: TBD
 * LAST_MODIFIED: TBD
 * ==============================================================================
 */
```

**Component Structure**:
```javascript
// PerformanceAttributionWidget.jsx
const PerformanceAttributionWidget = ({ portfolioId, period, benchmark }) => {
  const { attribution, loading, error } = useAttribution(portfolioId, period, benchmark);
  
  return (
    <WidgetContainer>
      <AttributionChart data={attribution} />
      <AttributionTable data={attribution} />
      <DrillDownPanel />
      <ExportButtons />
    </WidgetContainer>
  );
};

// PortfolioAnalyticsDashboard.jsx
const PortfolioAnalyticsDashboard = () => {
  const { portfolio } = usePortfolio();
  const { customViews, saveView } = useCustomViews();
  
  return (
    <DashboardLayout>
      <PerformanceOverview />
      <PerformanceAttributionWidget />
      <RiskDecompositionWidget />
      <ContributionAnalysisWidget />
      <BenchmarkComparisonWidget />
      <CustomizationPanel />
    </DashboardLayout>
  );
};
```

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-1.3.1 | Dashboard displays performance attribution with interactive charts showing allocation, selection, and interaction effects | `NOT_STARTED` | | |
| AC-1.3.2 | Risk decomposition widget visualizes factor exposures, concentration risk, and correlation matrix with heatmaps | `NOT_STARTED` | | |
| AC-1.3.3 | Contribution analysis table displays top 10 and bottom 10 contributors with sortable columns and filtering | `NOT_STARTED` | | |
| AC-1.3.4 | Dashboard supports drill-down from asset class → sector → industry → individual holding | `NOT_STARTED` | | |
| AC-1.3.5 | Benchmark comparison displays portfolio vs benchmark with active return decomposition | `NOT_STARTED` | | |
| AC-1.3.6 | Dashboard loads within 2 seconds and updates smoothly without lag | `NOT_STARTED` | | |
| AC-1.3.7 | Export functionality generates PDF reports with charts, tables, and formatted data | `NOT_STARTED` | | |
| AC-1.3.8 | Export functionality generates Excel files with multiple sheets for different analytics | `NOT_STARTED` | | |
| AC-1.3.9 | Custom views allow users to save and restore dashboard layouts with selected widgets | `NOT_STARTED` | | |
| AC-1.3.10 | Dashboard is responsive and works on desktop (1920x1080), tablet (768x1024), and mobile (375x667) | `NOT_STARTED` | | |
| AC-1.3.11 | Dashboard meets WCAG 2.1 AA accessibility standards with screen reader support | `NOT_STARTED` | | |
| AC-1.3.12 | Real-time updates refresh analytics data every 60 seconds during market hours | `NOT_STARTED` | | |
| AC-1.3.13 | Dashboard handles error states gracefully with user-friendly error messages | `NOT_STARTED` | | |
| AC-1.3.14 | Loading states show progress indicators during data fetching | `NOT_STARTED` | | |
| AC-1.3.15 | Unit tests cover all widget components with React Testing Library | `NOT_STARTED` | | |
| AC-1.3.16 | E2E tests verify dashboard functionality with Playwright | `NOT_STARTED` | | |

---

## Phase Completion Summary

Upon completion of Phase 1, the platform will have:

- ✅ Comprehensive performance attribution engine
- ✅ Advanced risk decomposition capabilities
- ✅ Interactive analytics dashboard
- ✅ Foundation for all future analytics features

**Next Phase**: Phase 2 - Portfolio Optimization & Rebalancing

---

## Change Log

| Date | Author | Change Description |
|------|--------|-------------------|
| 2026-01-21 | System | Initial creation of Phase 1 implementation plan |
