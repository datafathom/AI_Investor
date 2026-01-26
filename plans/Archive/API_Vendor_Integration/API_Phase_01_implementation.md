# Phase 1: Alpha Vantage - Core Market Data Integration

## Phase Status: `PARTIALLY COMPLETE` ⚠️
**Last Updated**: 2026-01-21
**Estimated Duration**: 5-7 days
**Priority**: CRITICAL (Foundation for all market data)
**Started Date**: 2026-01-21
**Completion Status**: Backend + API Complete, Frontend Incomplete

---

## Phase Overview

Alpha Vantage serves as the **primary market data source** for the AI Investor platform. This phase establishes the foundational data pipeline that all other market-dependent services will consume. The integration must be robust, rate-limit aware, and provide consistent data schemas across all endpoints.

### Dependencies
- `APIGovernor` service must be operational
- `EnvironmentManager` must provide `ALPHA_VANTAGE_API_KEY`
- Redis cache infrastructure for response caching
- Kafka infrastructure for real-time data streaming

### Risk Factors
- Alpha Vantage Free Tier limits (25 requests/day, 5 requests/minute) are extremely restrictive
- Premium API key recommended for production use
- Data quality varies during pre-market and after-hours periods

---

## Deliverable 1.1: Alpha Vantage Client Service

### Status: `COMPLETE` ✅
### Assignee: TBD
### Start Date: TBD
### Completion Date: TBD

### Detailed Task Description

Create a comprehensive Python client service that wraps the Alpha Vantage REST API. This service is critical infrastructure that will be consumed by multiple downstream services including:
- `DataFusionService` for unified market data access
- `OptionsFlowService` for options chain analysis
- `CorporateService` for earnings calendar tracking
- `PortfolioManager` for real-time position valuation

The client must implement:
1. **Authentication Management**: Secure retrieval of API key from `EnvironmentManager`, never hardcoded or logged
2. **Rate Limiting Integration**: Every API call must first call `APIGovernor.wait_for_slot("ALPHA_VANTAGE")` to ensure compliance with free tier limits
3. **Response Normalization**: All API responses must be transformed into consistent internal data models using Pydantic
4. **Error Handling**: Graceful handling of all Alpha Vantage error codes (rate limits, invalid symbols, API key issues)
5. **Caching Layer**: Redis-based caching with configurable TTL per endpoint type
6. **Logging**: Comprehensive request/response logging for debugging and usage auditing

### Backend Implementation Details

**File**: `services/data/alpha_vantage.py`

**Required Header Comment**:
```python
"""
==============================================================================
FILE: services/data/alpha_vantage.py
ROLE: Primary Market Data Client
PURPOSE: Wraps Alpha Vantage REST API for equity prices, options flow, and
         earnings calendars. This is the foundation data source for all
         market-dependent services in the AI Investor platform.
         
INTEGRATION POINTS:
    - APIGovernor: Rate limiting enforcement (25/day, 5/min free tier)
    - EnvironmentManager: API key retrieval
    - DataFusionService: Consumed as primary data source
    - Redis: Response caching layer
    - Kafka: Real-time quote streaming

USAGE:
    from services.data.alpha_vantage import AlphaVantageClient
    client = AlphaVantageClient()
    quote = await client.get_quote("AAPL")
    
DEPENDENCIES:
    - httpx (async HTTP client)
    - pydantic (data validation)
    - redis (caching)
    
AUTHOR: AI Investor Team
CREATED: TBD
LAST_MODIFIED: TBD
==============================================================================
"""
```

**Class Structure**:
```python
class AlphaVantageClient:
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, use_cache: bool = True, cache_ttl: int = 60):
        """Initialize client with optional caching configuration."""
        
    async def get_quote(self, symbol: str) -> QuoteModel:
        """
        Retrieve real-time quote for a symbol.
        Uses GLOBAL_QUOTE endpoint.
        Cache TTL: 60 seconds (market hours), 3600 seconds (after hours)
        """
        
    async def get_intraday(self, symbol: str, interval: str = "5min", 
                           outputsize: str = "compact") -> List[OHLCVModel]:
        """
        Retrieve intraday time series data.
        Intervals: 1min, 5min, 15min, 30min, 60min
        Outputsize: compact (100 points) or full (all available)
        Cache TTL: 300 seconds
        """
        
    async def get_daily(self, symbol: str, outputsize: str = "compact") -> List[OHLCVModel]:
        """
        Retrieve daily adjusted time series.
        Includes adjusted close and dividend data.
        Cache TTL: 3600 seconds
        """
        
    async def get_options_chain(self, symbol: str, date: Optional[str] = None) -> OptionsChainModel:
        """
        Retrieve full options chain for a symbol.
        Uses HISTORICAL_OPTIONS endpoint.
        Cache TTL: 1800 seconds
        """
        
    async def get_earnings_calendar(self, symbol: Optional[str] = None, 
                                    horizon: str = "3month") -> List[EarningsModel]:
        """
        Retrieve upcoming earnings dates.
        Horizon: 3month, 6month, 12month
        Cache TTL: 3600 seconds
        """
        
    async def _make_request(self, params: Dict) -> Dict:
        """
        Internal method for making API requests.
        Handles: rate limiting, retries, caching, error normalization
        """
```

**Data Models** (in `models/market_data.py`):
```python
class QuoteModel(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    price: float
    volume: int
    latest_trading_day: date
    previous_close: float
    change: float
    change_percent: str
    timestamp: datetime
    source: str = "alpha_vantage"

class OHLCVModel(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    adjusted_close: Optional[float]
    volume: int
    dividend: Optional[float]
    split_coefficient: Optional[float]

class OptionsChainModel(BaseModel):
    symbol: str
    retrieved_at: datetime
    contracts: List[OptionsContractModel]
    
class EarningsModel(BaseModel):
    symbol: str
    name: str
    report_date: date
    fiscal_date_ending: date
    estimate: Optional[float]
    currency: str
```

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-1.1.1 | Service successfully retrieves real-time quotes for any valid ticker symbol (AAPL, MSFT, GOOGL, etc.) | `NOT_STARTED` | | |
| AC-1.1.2 | Service returns appropriate error model for invalid symbols (e.g., "INVALID123") without crashing | `NOT_STARTED` | | |
| AC-1.1.3 | Service gracefully handles 429 rate limit errors with exponential backoff (1s, 2s, 4s, max 60s) | `NOT_STARTED` | | |
| AC-1.1.4 | Service logs all API calls with: request URL, response status, duration (ms), response size (bytes), cache hit/miss | `NOT_STARTED` | | |
| AC-1.1.5 | Unit tests achieve 90%+ coverage of all public methods with mock responses | `NOT_STARTED` | | |
| AC-1.1.6 | Integration test confirms live API connectivity with a funded key (manual test) | `NOT_STARTED` | | |
| AC-1.1.7 | Redis caching reduces duplicate API calls by measuring cache hit rate >= 80% for repeated requests | `NOT_STARTED` | | |
| AC-1.1.8 | All Pydantic models validate incoming data and reject malformed responses | `NOT_STARTED` | | |

### Test Plan

**Unit Tests** (`tests/test_alpha_vantage.py`):
1. `test_get_quote_success` - Mock successful quote response, verify model parsing
2. `test_get_quote_invalid_symbol` - Mock error response, verify error handling
3. `test_get_quote_rate_limited` - Mock 429 response, verify backoff logic
4. `test_get_intraday_all_intervals` - Test all interval options
5. `test_get_options_chain_parsing` - Verify complex options data parsing
6. `test_cache_hit` - Verify second request uses cache
7. `test_cache_miss_on_expiry` - Verify cache respects TTL
8. `test_api_governor_integration` - Verify wait_for_slot is called

**Integration Tests** (manual, requires funded API key):
1. Retrieve live quote for AAPL, verify price is reasonable
2. Retrieve intraday data, verify timestamps are recent
3. Hit rate limit intentionally, verify service recovers

---

## Deliverable 1.2: Market Data API Endpoints

### Status: `COMPLETE` ✅
### Assignee: TBD
### Start Date: TBD
### Completion Date: TBD

### Detailed Task Description

Expose the Alpha Vantage data through RESTful Flask/FastAPI endpoints that the frontend can consume. These endpoints must:
1. Abstract away the underlying data source (frontend doesn't need to know about Alpha Vantage)
2. Provide consistent error responses across all endpoints
3. Support request caching at the HTTP layer (ETag, Cache-Control headers)
4. Include request validation and sanitization
5. Support pagination for historical data
6. Document all endpoints in OpenAPI/Swagger

### Backend Implementation Details

**File**: `apis/market_data_api.py`

**Required Header Comment**:
```python
"""
==============================================================================
FILE: apis/market_data_api.py
ROLE: Market Data REST API
PURPOSE: RESTful endpoints for frontend consumption of market data. Abstracts
         underlying data sources (Alpha Vantage, Polygon) behind unified API.
         
INTEGRATION POINTS:
    - AlphaVantageClient: Primary data source
    - PolygonClient: Fallback data source
    - DataFusionService: Intelligent source selection
    - Redis: HTTP response caching
    
ENDPOINTS:
    GET /api/market/quote/{symbol} - Real-time quote
    GET /api/market/history/{symbol} - Historical OHLCV data
    GET /api/market/options/{symbol} - Options chain
    GET /api/market/earnings - Earnings calendar
    
AUTHENTICATION: JWT Bearer token required
RATE LIMITING: 60 requests/minute per user

AUTHOR: AI Investor Team
==============================================================================
"""
```

**Endpoint Specifications**:

```python
@router.get("/quote/{symbol}", response_model=QuoteResponse)
async def get_quote(
    symbol: str = Path(..., regex="^[A-Z]{1,5}$", description="Stock ticker symbol"),
    current_user: User = Depends(get_current_user)
) -> QuoteResponse:
    """
    Retrieve real-time quote for a stock symbol.
    
    Returns:
        QuoteResponse containing price, volume, and change data
        
    Raises:
        404: Symbol not found
        429: Rate limit exceeded
        503: Market data service unavailable
    """

@router.get("/history/{symbol}", response_model=HistoryResponse)
async def get_history(
    symbol: str = Path(..., regex="^[A-Z]{1,5}$"),
    period: str = Query("1M", regex="^(1D|1W|1M|3M|6M|1Y|5Y|MAX)$"),
    interval: str = Query("1d", regex="^(1m|5m|15m|1h|1d|1w|1mo)$"),
    current_user: User = Depends(get_current_user)
) -> HistoryResponse:
    """
    Retrieve historical OHLCV data with specified period and interval.
    
    Period options: 1D, 1W, 1M, 3M, 6M, 1Y, 5Y, MAX
    Interval options: 1m, 5m, 15m, 1h, 1d, 1w, 1mo
    
    Note: Intraday intervals (1m-1h) only available for 1D-1W periods
    """

@router.get("/options/{symbol}", response_model=OptionsResponse)
async def get_options_chain(
    symbol: str = Path(..., regex="^[A-Z]{1,5}$"),
    expiration: Optional[date] = Query(None),
    option_type: Optional[str] = Query(None, regex="^(call|put)$"),
    current_user: User = Depends(get_current_user)
) -> OptionsResponse:
    """
    Retrieve options chain with optional filtering.
    """

@router.get("/earnings", response_model=EarningsResponse)
async def get_earnings_calendar(
    symbols: Optional[List[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user)
) -> EarningsResponse:
    """
    Retrieve earnings calendar for portfolio or specific symbols.
    """
```

**Response Models**:
```python
class APIResponse(BaseModel):
    """Base response model for all endpoints"""
    data: Any
    meta: MetaModel
    errors: List[ErrorModel] = []
    
class MetaModel(BaseModel):
    request_id: str
    timestamp: datetime
    source: str  # "alpha_vantage", "polygon", "cache"
    cache_hit: bool
    processing_time_ms: int

class ErrorModel(BaseModel):
    error_code: str
    message: str
    vendor: Optional[str]
    retry_after: Optional[int]
```

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-1.2.1 | All endpoints return JSON with consistent schema (`data`, `meta`, `errors` keys) | `NOT_STARTED` | | |
| AC-1.2.2 | HTTP caching headers (ETag, Cache-Control) reduce duplicate requests by 80%+ | `NOT_STARTED` | | |
| AC-1.2.3 | Error responses include `error_code`, `message`, and `vendor` fields | `NOT_STARTED` | | |
| AC-1.2.4 | All endpoints are documented in OpenAPI/Swagger with examples | `NOT_STARTED` | | |
| AC-1.2.5 | Invalid symbol requests return 404 with descriptive error | `NOT_STARTED` | | |
| AC-1.2.6 | Rate limited requests return 429 with `Retry-After` header | `NOT_STARTED` | | |
| AC-1.2.7 | All endpoints require valid JWT authentication | `NOT_STARTED` | | |
| AC-1.2.8 | Request validation rejects malformed parameters with 400 response | `NOT_STARTED` | | |

---

## Deliverable 1.3: Frontend Market Data Widgets

### Status: `NOT_STARTED` ❌
**BLOCKER**: Frontend widgets are missing and must be completed.
### Assignee: TBD
### Start Date: TBD
### Completion Date: TBD

### Detailed Task Description

Create React components that consume the Market Data API and provide rich, interactive visualizations. These widgets will be used throughout the platform in dashboards, portfolio views, and analysis pages.

The widgets must:
1. Handle all loading and error states gracefully
2. Auto-refresh during market hours without user intervention
3. Support dark/light theme toggle
4. Be fully responsive for mobile, tablet, and desktop
5. Use Zustand store for centralized state management
6. Implement virtualization for large datasets (historical data)

### Frontend Implementation Details

**Files to Create**:
- `frontend2/src/widgets/Market/QuoteCard.jsx`
- `frontend2/src/widgets/Market/PriceChart.jsx`
- `frontend2/src/widgets/Market/EarningsCalendar.jsx`
- `frontend2/src/stores/marketStore.js`
- `frontend2/src/services/marketService.js`
- `frontend2/src/widgets/Market/Market.css`

**QuoteCard.jsx Header Comment**:
```javascript
/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Market/QuoteCard.jsx
 * ROLE: Real-Time Quote Display Widget
 * PURPOSE: Displays real-time stock quote with price, volume, and change data.
 *          Supports auto-refresh during market hours and manual refresh.
 *          
 * INTEGRATION POINTS:
 *     - marketStore: Zustand state management for quote data
 *     - marketService: API calls to /api/market/quote/{symbol}
 *     - ThemeContext: Dark/light theme support
 *     
 * PROPS:
 *     - symbol (string, required): Stock ticker symbol
 *     - showVolume (boolean, default: true): Display volume indicator
 *     - autoRefresh (boolean, default: true): Enable auto-refresh
 *     - refreshInterval (number, default: 60000): Refresh interval in ms
 *     
 * USAGE:
 *     <QuoteCard symbol="AAPL" showVolume={true} autoRefresh={true} />
 *     
 * AUTHOR: AI Investor Team
 * ==============================================================================
 */
```

**Component Structure**:
```jsx
// QuoteCard.jsx
const QuoteCard = ({ symbol, showVolume = true, autoRefresh = true, refreshInterval = 60000 }) => {
    const { quote, loading, error, fetchQuote } = useMarketStore();
    const [lastUpdated, setLastUpdated] = useState(null);
    
    useEffect(() => {
        fetchQuote(symbol);
        
        if (autoRefresh && isMarketOpen()) {
            const interval = setInterval(() => {
                fetchQuote(symbol);
                setLastUpdated(new Date());
            }, refreshInterval);
            return () => clearInterval(interval);
        }
    }, [symbol, autoRefresh, refreshInterval]);
    
    if (loading) return <QuoteCardSkeleton />;
    if (error) return <QuoteCardError error={error} onRetry={() => fetchQuote(symbol)} />;
    
    return (
        <div className="quote-card">
            <div className="quote-card__header">
                <span className="quote-card__symbol">{symbol}</span>
                <span className="quote-card__price">${quote.price.toFixed(2)}</span>
            </div>
            <div className={`quote-card__change ${quote.change >= 0 ? 'positive' : 'negative'}`}>
                {quote.change >= 0 ? '+' : ''}{quote.change.toFixed(2)} ({quote.change_percent})
            </div>
            {showVolume && (
                <div className="quote-card__volume">
                    Vol: {formatVolume(quote.volume)}
                </div>
            )}
            <div className="quote-card__footer">
                <span className="quote-card__last-updated">
                    Updated: {formatRelativeTime(lastUpdated)}
                </span>
            </div>
        </div>
    );
};
```

**Zustand Store** (`marketStore.js`):
```javascript
/**
 * ==============================================================================
 * FILE: frontend2/src/stores/marketStore.js
 * ROLE: Market Data State Management
 * PURPOSE: Centralized state management for all market data including quotes,
 *          historical data, options chains, and earnings calendar.
 *          
 * INTEGRATION POINTS:
 *     - marketService: API calls
 *     - All Market widgets consume this store
 *     
 * STATE SHAPE:
 *     quotes: { [symbol]: QuoteData }
 *     history: { [symbol]: { [period]: HistoryData } }
 *     options: { [symbol]: OptionsData }
 *     earnings: EarningsData[]
 *     loading: { quotes: boolean, history: boolean, ... }
 *     errors: { quotes: Error | null, history: Error | null, ... }
 * ==============================================================================
 */

import { create } from 'zustand';
import { marketService } from '../services/marketService';

export const useMarketStore = create((set, get) => ({
    quotes: {},
    history: {},
    options: {},
    earnings: [],
    loading: { quotes: false, history: false, options: false, earnings: false },
    errors: { quotes: null, history: null, options: null, earnings: null },
    
    fetchQuote: async (symbol) => {
        set((state) => ({ 
            loading: { ...state.loading, quotes: true },
            errors: { ...state.errors, quotes: null }
        }));
        try {
            const data = await marketService.getQuote(symbol);
            set((state) => ({
                quotes: { ...state.quotes, [symbol]: data },
                loading: { ...state.loading, quotes: false }
            }));
        } catch (error) {
            set((state) => ({
                errors: { ...state.errors, quotes: error },
                loading: { ...state.loading, quotes: false }
            }));
        }
    },
    
    fetchHistory: async (symbol, period, interval) => {
        // Similar pattern for historical data
    },
    
    fetchOptionsChain: async (symbol) => {
        // Similar pattern for options data
    },
    
    fetchEarningsCalendar: async (symbols) => {
        // Similar pattern for earnings data
    },
    
    // Selector helpers
    getQuote: (symbol) => get().quotes[symbol],
    isLoading: (dataType) => get().loading[dataType],
    getError: (dataType) => get().errors[dataType],
}));
```

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-1.3.1 | QuoteCard displays bid/ask, last price, volume, and change percentage correctly | `NOT_STARTED` | | |
| AC-1.3.2 | PriceChart renders historical data with zoom/pan functionality (using Recharts or similar) | `NOT_STARTED` | | |
| AC-1.3.3 | EarningsCalendar displays upcoming earnings with date, EPS estimate, and fiscal quarter | `NOT_STARTED` | | |
| AC-1.3.4 | All widgets display loading skeleton during data fetch | `NOT_STARTED` | | |
| AC-1.3.5 | All widgets display error state with retry button on API failure | `NOT_STARTED` | | |
| AC-1.3.6 | Widgets auto-refresh every 60 seconds during market hours (9:30 AM - 4:00 PM ET) | `NOT_STARTED` | | |
| AC-1.3.7 | Widgets support both dark and light themes via CSS variables | `NOT_STARTED` | | |
| AC-1.3.8 | All widgets are responsive and render correctly on mobile (320px) and desktop (1920px) | `NOT_STARTED` | | |
| AC-1.3.9 | Storybook stories exist for all widget states (loading, error, empty, populated) | `NOT_STARTED` | | |

---

## Phase Completion Checklist

| Item | Status | Notes |
|------|--------|-------|
| All deliverables completed | `NOT_STARTED` | |
| All acceptance criteria verified | `NOT_STARTED` | |
| Code review completed | `NOT_STARTED` | |
| Unit tests passing | `NOT_STARTED` | |
| Integration tests passing | `NOT_STARTED` | |
| Documentation updated | `NOT_STARTED` | |
| Stakeholder sign-off | `NOT_STARTED` | |

---

## Change Log

| Date | Author | Change Description |
|------|--------|-------------------|
| 2026-01-21 | System | Initial creation of Phase 1 implementation plan |
