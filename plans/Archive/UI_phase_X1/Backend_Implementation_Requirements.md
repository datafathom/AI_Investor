# Backend Implementation Requirements

> Cross-cutting backend specifications for all 24 UI phases  
> Last Updated: 2026-01-18  
> Status: `[ ]` Not Started

---

## Architecture Overview

All backend implementations follow the existing project patterns:
- **Location**: `services/` directory (not `backend/`)
- **Testing**: `tests/` directory with pytest
- **Web Layer**: `web/` for FastAPI routes
- **Agents**: `agents/` for autonomous AI agents

---

## Backend Test Infrastructure

### Pytest Configuration
- **Command**: `pytest tests/ -v --cov=services --cov-report=html`
- **Existing Tests**: 16 test files in `tests/`
- **Coverage Target**: 80% minimum for new services

### Frontend Test Infrastructure
- **Command**: `npm run test` (Vitest)
- **Location**: `frontend2/tests/`
- **Existing Tests**: 89 test files
- **Coverage**: `npm run test:coverage`

---

## Phase 1 Backend Requirements

### New Services Required

#### `services/workspace/user_preferences_service.py`
```python
class UserPreferencesService:
    """Manages user workspace layouts and preferences in Postgres."""
    
    async def save_workspace(self, user_id: str, workspace: WorkspaceLayout) -> bool
    async def get_workspace(self, user_id: str) -> Optional[WorkspaceLayout]
    async def list_workspaces(self, user_id: str) -> List[WorkspaceMetadata]
    async def delete_workspace(self, user_id: str, workspace_id: str) -> bool
```

**Pytest Tests Required**: `tests/workspace/test_user_preferences_service.py`
- [ ] `test_save_workspace_new` - Save new workspace layout
- [ ] `test_save_workspace_update` - Update existing workspace
- [ ] `test_get_workspace_exists` - Retrieve existing workspace
- [ ] `test_get_workspace_not_found` - Handle missing workspace
- [ ] `test_restore_time_under_200ms` - Performance requirement

#### `services/agents/heartbeat_service.py`
```python
class HeartbeatService:
    """Tracks agent heartbeats via Kafka topic."""
    
    async def record_heartbeat(self, agent_id: str, status: AgentStatus) -> None
    async def get_agent_status(self, agent_id: str) -> AgentStatus
    async def get_all_agents(self) -> List[AgentHeartbeat]
    def is_agent_alive(self, last_heartbeat: datetime, threshold_seconds: int = 5) -> bool
```

**Pytest Tests Required**: `tests/agents/test_heartbeat_service.py`
- [ ] `test_record_heartbeat` - Record agent heartbeat
- [ ] `test_heartbeat_timeout` - Detect dead agents after 5s
- [ ] `test_kafka_topic_subscription` - Kafka integration test

### Web Routes Required

#### `web/routes/workspace_routes.py`
| Endpoint | Method | Handler | Auth |
|----------|--------|---------|------|
| `/api/v1/user/workspace` | GET | `get_user_workspace` | JWT |
| `/api/v1/user/workspace` | POST | `save_user_workspace` | JWT |
| `/api/v1/user/workspaces` | GET | `list_user_workspaces` | JWT |

**Pytest Tests Required**: `tests/web/test_workspace_routes.py`
- [ ] `test_save_workspace_authenticated` - Auth required
- [ ] `test_save_workspace_unauthenticated` - 401 response
- [ ] `test_get_workspace_performance` - <200ms response

---

## Phase 2 Backend Requirements

### Fear & Greed Index Service

#### `services/analysis/fear_greed_service.py`
```python
class FearGreedService:
    """Calculates Fear/Greed composite score from multiple signals."""
    
    async def calculate_composite(self) -> FearGreedScore
    async def get_vix_component(self) -> float
    async def get_put_call_ratio(self) -> float
    async def get_social_sentiment(self) -> float
    def get_weighted_score(self, vix: float, pcr: float, sentiment: float) -> int
```

**Pytest Tests Required**: `tests/analysis/test_fear_greed_service.py`
- [ ] `test_composite_score_range` - Score 0-100
- [ ] `test_extreme_fear_threshold` - <20 is extreme fear
- [ ] `test_extreme_greed_threshold` - >80 is extreme greed
- [ ] `test_weight_calculation` - Weights sum to 1.0

### Kafka Stream Monitor Service

#### `services/monitoring/kafka_monitor_service.py`
```python
class KafkaMonitorService:
    """Monitors Kafka topic health and latency."""
    
    async def get_topic_latencies(self) -> Dict[str, float]
    async def get_messages_per_second(self, topic: str) -> float
    async def get_consumer_lag(self, consumer_group: str) -> int
    def check_latency_threshold(self, latency_ms: float, threshold: int = 200) -> bool
```

**Pytest Tests Required**: `tests/monitoring/test_kafka_monitor_service.py`
- [ ] `test_latency_under_200ms` - Target latency met
- [ ] `test_consumer_lag_alert` - Alert when lag >2000

---

## Phase 3 Backend Requirements

### HypeMeter Engine Service

#### `services/analysis/hype_meter_service.py`
```python
class HypeMeterService:
    """Tracks social sentiment velocity for meme stock detection."""
    
    async def calculate_hype_score(self, ticker: str) -> HypeScore
    async def detect_viral_spike(self, ticker: str, std_dev_threshold: float = 5.0) -> bool
    async def get_mention_velocity(self, ticker: str) -> float
    async def extract_keywords(self, content: str) -> List[str]  # FinBERT NLP
```

**Pytest Tests Required**: `tests/analysis/test_hype_meter_service.py`
- [ ] `test_hype_score_calculation` - Weighted engagement
- [ ] `test_viral_spike_detection` - 5 std dev threshold
- [ ] `test_keyword_extraction` - FinBERT keywords

---

## Phase 4 Backend Requirements

### Options Chain Service

#### `services/trading/options_chain_service.py`
```python
class OptionsChainService:
    """Real-time options chain data with Greeks calculation."""
    
    async def get_options_chain(self, ticker: str, expiry: date) -> OptionsChain
    async def calculate_greeks(self, option: OptionContract) -> Greeks
    async def calculate_iv_rank(self, ticker: str) -> IVMetrics
    async def detect_whale_activity(self, option: OptionContract) -> bool
```

**Pytest Tests Required**: `tests/trading/test_options_chain_service.py`
- [ ] `test_greeks_calculation` - Delta, Gamma, Theta, Vega
- [ ] `test_iv_rank_percentile` - 0-100 range
- [ ] `test_whale_detection_heuristics` - Volume/OI ratio

### DOM Service

#### `services/trading/dom_service.py`
```python
class DOMService:
    """Level 2 market depth (DOM) data."""
    
    async def get_depth(self, ticker: str) -> OrderBook
    async def calculate_gap(self, order_book: OrderBook) -> float
    async def detect_whale_orders(self, order_book: OrderBook, threshold: float) -> List[Order]
```

---

## Phase 5 Backend Requirements

### Pre-Trade Risk Service

#### `services/risk/pre_trade_risk_service.py`
```python
class PreTradeRiskService:
    """AI-assisted pre-trade risk analysis."""
    
    async def analyze_trade(self, trade: TradeRequest) -> RiskAnalysis
    async def calculate_margin_impact(self, trade: TradeRequest) -> float
    async def check_sector_concentration(self, trade: TradeRequest) -> ConcentrationCheck
    async def get_ai_risk_rating(self, trade: TradeRequest) -> RiskRating  # SAFE/CAUTION/DANGER
```

**Pytest Tests Required**: `tests/risk/test_pre_trade_risk_service.py`
- [ ] `test_margin_impact_calculation` - Correct margin usage
- [ ] `test_sector_concentration_limit` - 25% max per sector
- [ ] `test_ai_risk_rating` - LLM integration

### Kill Switch Service

#### `services/emergency/kill_switch_service.py`
```python
class KillSwitchService:
    """Emergency trading halt and position liquidation."""
    
    async def activate_kill_switch(self, user_id: str, passcode: str) -> KillSwitchResult
    async def broadcast_emergency(self, command: EmergencyCommand) -> bool
    async def cancel_all_orders(self, account_id: str) -> List[CancelledOrder]
    async def verify_broker_confirmation(self, account_id: str) -> bool
```

**Pytest Tests Required**: `tests/emergency/test_kill_switch_service.py`
- [ ] `test_broadcast_latency_under_1s` - Performance critical
- [ ] `test_passcode_verification` - Security
- [ ] `test_broker_confirmation` - Within 1.5s

---

## Common Backend Patterns

### Service Base Class
```python
# services/base_service.py
class BaseService:
    """Base class for all services with circuit breaker support."""
    
    def __init__(self, db: AsyncSession, kafka: KafkaProducer):
        self.db = db
        self.kafka = kafka
        self.circuit_breaker = CircuitBreaker()
```

### Pytest Fixtures (tests/conftest.py)
```python
@pytest.fixture
async def db_session():
    """Async database session for tests."""
    
@pytest.fixture
def mock_kafka():
    """Mock Kafka producer for isolated tests."""
    
@pytest.fixture
def authenticated_client():
    """FastAPI test client with valid JWT."""
```

---

## Nice-to-Have Enhancements

### Performance Optimizations
- [ ] Redis caching layer for frequently accessed data
- [ ] Connection pooling for Postgres (asyncpg)
- [ ] Kafka consumer group load balancing

### Developer Experience
- [ ] Swagger/OpenAPI documentation for all endpoints
- [ ] Request/response logging middleware
- [ ] Performance timing decorators

### Security Enhancements
- [ ] Rate limiting per endpoint
- [ ] Request validation with Pydantic
- [ ] Audit logging for sensitive operations

### Observability
- [ ] Prometheus metrics export
- [ ] Distributed tracing (OpenTelemetry)
- [ ] Health check endpoints for all services

---

## Implementation Priority

| Priority | Services | Phases |
|----------|----------|--------|
| P0 (Week 1) | UserPreferences, Heartbeat, KillSwitch | 1, 5 |
| P1 (Week 2) | FearGreed, KafkaMonitor, PreTradeRisk | 2, 5 |
| P2 (Week 3) | HypeMeter, OptionsChain, DOM | 3, 4 |
| P3 (Week 4+) | Remaining services | 6-24 |

---

## Database Migrations

### Phase 1 Migrations
```sql
-- migrations/001_user_workspaces.sql
CREATE TABLE user_workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    workspace_name VARCHAR(255) NOT NULL,
    layout_json JSONB NOT NULL,
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_user_workspaces_user_id ON user_workspaces(user_id);
```

### Phase 5 Migrations
```sql
-- migrations/002_kill_switch_events.sql
CREATE TABLE kill_switch_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    trigger_type VARCHAR(50) NOT NULL,
    orders_cancelled INTEGER DEFAULT 0,
    broker_confirmed BOOLEAN DEFAULT false,
    triggered_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Document Created | Draft | Backend specs for Phases 1-5 |
| 2026-01-18 | Phase X2 Added | Draft | Backend specs for Phases 49-68 |

---

# Phase X2 Backend Requirements (Phases 49-68)

> Extension for advanced GUI features and Total Financial Homeostasis Engine

---

## Phase 49: Attribution Service

### `services/analysis/attribution_service.py`
```python
"""
Attribution Service - Brinson-Fachler Performance Decomposition

This service calculates portfolio performance attribution using the 
Brinson-Fachler model, decomposing returns into Allocation, Selection, 
and Interaction effects relative to benchmarks.
"""

class AttributionService:
    async def calculate_brinson_attribution(
        self, portfolio_id: str, benchmark_id: str, period: DateRange
    ) -> BrinsonAttribution
    
    async def get_sector_allocation_effect(
        self, portfolio_id: str, sector: str
    ) -> float
    
    async def get_selection_effect(
        self, portfolio_id: str, sector: str
    ) -> float
    
    async def detect_regime_shift(
        self, portfolio_id: str, benchmark_id: str
    ) -> List[RegimeShiftEvent]
```

**Pytest Tests**: `tests/analysis/test_attribution_service.py`
- [ ] `test_brinson_allocation_effect`
- [ ] `test_brinson_selection_effect`
- [ ] `test_brinson_interaction_effect`
- [ ] `test_total_active_return_sum`

---

## Phase 50: Fixed Income Service

### `services/analysis/fixed_income_service.py`
```python
"""
Fixed Income Service - Bond Analytics and Yield Curve Management

Manages bond ladder construction, duration/convexity calculations,
and yield curve analysis with FRED API integration.
"""

class FixedIncomeService:
    async def calculate_weighted_average_life(
        self, bond_ladder: List[Bond]
    ) -> float
    
    async def calculate_duration(self, bond: Bond) -> DurationMetrics
    async def calculate_convexity(self, bond: Bond) -> float
    
    async def get_rate_shock_impact(
        self, portfolio_id: str, basis_points: int
    ) -> MonetaryImpact
    
    async def detect_liquidity_gaps(
        self, bond_ladder: List[Bond]
    ) -> List[int]  # Years with zero maturities
```

### `services/data/fred_service.py`
```python
"""
FRED API Service - Federal Reserve Economic Data Integration

Fetches macroeconomic data from FRED API with Kafka integration
for yield curve updates and recession signal detection.
"""

class FREDService:
    async def get_yield_curve(self) -> YieldCurve
    async def detect_inversion(self) -> bool
    async def get_historical_curves(self, months: int) -> List[YieldCurve]
```

**Pytest Tests**: `tests/analysis/test_fixed_income_service.py`, `tests/data/test_fred_service.py`

---

## Phase 51: Web3 & Crypto Services

### `services/crypto/wallet_service.py`
```python
"""
Wallet Service - Hardware Wallet & Multi-Chain Balance Tracking

Manages connections to hardware wallets (Ledger/Trezor) and 
aggregates balances across multiple blockchain networks.
"""

class WalletService:
    async def get_wallet_balance(
        self, wallet_address: str, chain: str
    ) -> Balance
    
    async def get_aggregated_portfolio(
        self, user_id: str
    ) -> CryptoPortfolio
    
    async def verify_connection(self, wallet_type: str) -> bool
```

### `services/crypto/lp_tracker_service.py`
```python
"""
LP Tracker Service - Impermanent Loss Calculator

Tracks liquidity provider positions on DEXes and calculates
impermanent loss vs HODL strategy.
"""

class LPTrackerService:
    async def calculate_impermanent_loss(
        self, lp_position: LPPosition
    ) -> ImpermanentLossResult
    
    async def detect_pool_drain(
        self, pool_address: str
    ) -> PoolDrainAlert | None
```

### `services/crypto/gas_service.py`
```python
"""
Gas Service - Network Fee Optimization

Monitors gas prices across networks and provides optimization
strategies for transaction timing.
"""

class GasService:
    async def get_current_gas(self, chain: str) -> GasMetrics
    async def detect_spike(self, chain: str) -> bool
    async def get_optimal_execution_window(self) -> TimeWindow
```

---

## Phase 52: Tax Harvest Service

### `services/tax/harvest_service.py`
```python
"""
Tax Harvest Service - Tax-Loss Harvesting Automation

Identifies unrealized losses eligible for harvesting while
avoiding wash-sale violations through 30-day lookback.
"""

class TaxHarvestService:
    async def identify_harvest_candidates(
        self, portfolio_id: str
    ) -> List[HarvestCandidate]
    
    async def check_wash_sale_violation(
        self, ticker: str, user_id: str
    ) -> bool
    
    async def calculate_tax_savings(
        self, position: Position, tax_rate: float
    ) -> float
    
    async def suggest_replacement_assets(
        self, ticker: str
    ) -> List[ReplacementSuggestion]  # From Neo4j correlation
    
    async def project_capital_gains(
        self, portfolio_id: str, scenario: str
    ) -> CapitalGainsProjection
```

**Pytest Tests**: `tests/tax/test_harvest_service.py`
- [ ] `test_wash_sale_detection`
- [ ] `test_tax_savings_calculation`
- [ ] `test_replacement_correlation`

---

## Phase 53: Macro Service

### `services/analysis/macro_service.py`
```python
"""
Macro Service - Global Economic & Political Data Aggregation

Aggregates macroeconomic indicators, political insider trading,
and commodity data for the world map visualization.
"""

class MacroService:
    async def get_political_insider_trades(
        self, region: str | None
    ) -> List[InsiderTrade]
    
    async def get_regional_cpi(self, country_code: str) -> CPIData
    async def get_inflation_hedge_correlations(self) -> CorrelationMatrix
```

### `services/market/futures_service.py`
```python
"""
Futures Service - Commodity Term Structure Analysis

Provides futures curve data with contango/backwardation detection
and roll yield calculations.
"""

class FuturesService:
    async def get_futures_curve(self, commodity: str) -> FuturesCurve
    async def detect_contango(self, curve: FuturesCurve) -> bool
    async def calculate_roll_yield(self, curve: FuturesCurve) -> float
    async def calculate_crack_spread(self) -> SpreadData
```

---

## Phase 54-59: Security & Compliance Services

### `services/security/kyc_service.py`
```python
"""
KYC Service - Identity Verification & Document Management

Handles encrypted document storage, identity verification,
and regulatory filing management.
"""

class KYCService:
    async def verify_identity(self, user_id: str, documents: List[Document]) -> VerificationResult
    async def generate_13f_xml(self, portfolio_id: str) -> bytes
    async def get_filing_calendar(self) -> List[FilingDeadline]
```

### `services/security/estate_service.py`
```python
"""
Estate Service - Succession & Dead Man's Switch

Manages beneficiary allocations, heartbeat monitoring,
and inheritance protocol execution.
"""

class EstateService:
    async def check_heartbeat(self, user_id: str) -> bool
    async def trigger_succession(self, user_id: str) -> SuccessionResult
    async def calculate_estate_tax(self, allocations: List[Allocation]) -> TaxEstimate
```

### `services/compliance/abuse_detection_service.py`
```python
"""
Abuse Detection Service - Market Manipulation Prevention

Real-time detection of spoofing, layering, and wash trading
patterns to ensure regulatory compliance.
"""

class AbuseDetectionService:
    async def detect_spoofing(self, order_history: List[Order]) -> List[SpoofingFlag]
    async def detect_layering(self, order_book: OrderBook) -> List[LayeringFlag]
    async def detect_wash_trading(self, trades: List[Trade]) -> List[WashTradeFlag]
    async def pause_agent(self, agent_id: str, reason: str) -> bool
```

---

## Phase 60-61: Scenario & Impact Services

### `services/analysis/scenario_service.py`
```python
"""
Scenario Service - What-If Impact Simulation

Simulates portfolio impact under macro shock scenarios
using Neo4j correlation propagation.
"""

class ScenarioService:
    async def apply_shock(
        self, portfolio_id: str, shock: MacroShock
    ) -> ScenarioResult
    
    async def calculate_hedge_sufficiency(
        self, portfolio_id: str, shock: MacroShock
    ) -> float  # 0.0 to 1.0
    
    async def simulate_bank_run(
        self, portfolio_id: str
    ) -> LiquidityStressResult
    
    async def project_recovery_timeline(
        self, result: ScenarioResult
    ) -> RecoveryProjection
```

### `services/philanthropy/donation_service.py`
```python
"""
Donation Service - Automated Charitable Giving

Routes excess alpha to charities based on user preferences
with tax deduction optimization.
"""

class DonationService:
    async def calculate_excess_alpha(
        self, portfolio_id: str, threshold: float
    ) -> float
    
    async def execute_donation(
        self, amount: float, charity_id: str
    ) -> DonationReceipt
    
    async def calculate_tax_deduction(
        self, donation: Donation
    ) -> float
```

### `services/analysis/esg_service.py`
```python
"""
ESG Service - Environmental, Social, Governance Scoring

Aggregates ESG data from multiple providers and calculates
portfolio-level karma scores.
"""

class ESGService:
    async def get_portfolio_esg_score(self, portfolio_id: str) -> ESGScore
    async def check_sin_stock_exposure(self, portfolio_id: str) -> List[SinStockAlert]
    async def get_carbon_footprint(self, portfolio_id: str) -> CarbonMetrics
```

---

## Phase 62-66: Infrastructure & Integration Services

### `services/monitoring/kafka_health_service.py`
```python
"""
Kafka Health Service - Message Queue Monitoring

Monitors Kafka cluster health, consumer lag, and topic latencies.
"""

class KafkaHealthService:
    async def get_messages_per_second(self, topic: str) -> float
    async def get_consumer_lag(self, consumer_group: str) -> int
    async def restart_consumer(self, consumer_group: str) -> bool
```

### `services/risk/margin_service.py`
```python
"""
Margin Service - Leverage & Collateral Management

Calculates margin requirements, liquidation distances,
and provides de-leveraging recommendations.
"""

class MarginService:
    async def calculate_margin_buffer(self, portfolio_id: str) -> float
    async def get_liquidation_distance(self, position_id: str) -> float
    async def generate_deleverage_plan(self, target_buffer: float) -> DeleveragePlan
```

### `services/integration/api_connector_service.py`
```python
"""
API Connector Service - Third-Party Data Integration

Manages connections to external data providers with
failover and rate limit handling.
"""

class APIConnectorService:
    async def check_provider_health(self, provider: str) -> HealthStatus
    async def get_rate_limit_usage(self, provider: str) -> RateLimitStatus
    async def trigger_failover(self, primary: str, secondary: str) -> bool
```

---

## Phase 67-68: Wealth & Homeostasis Services

### `services/portfolio/assets_service.py` (Existing - Extended)
```python
"""
Assets Service - Illiquid Asset Management

Manages manual entry of real estate, art, and private equity
with JSON file persistence.
"""

class AssetsService:
    # Existing methods...
    async def link_to_entity_node(self, asset_id: str, entity_id: str) -> bool
    async def get_appreciation_history(self, asset_id: str) -> List[ValuationPoint]
```

### `services/portfolio/homeostasis_service.py` (Existing - Extended)
```python
"""
Homeostasis Service - The "Enough" Metric Engine

Manages the Zen Mode state, including Freedom Number tracking,
retirement probability, and autopilot mode.
"""

class HomeostasisService:
    # Existing methods...
    async def calculate_freedom_number_progress(self, user_id: str) -> float
    async def run_retirement_monte_carlo(self, params: RetirementParams) -> MCResult
    async def toggle_autopilot(self, user_id: str, enabled: bool) -> bool
    async def get_years_of_expenses_covered(self, user_id: str) -> float
```

---

## Implementation Priority - Phase X2

| Priority | Services | Phases |
|----------|----------|--------|
| P0 (Week 1) | Assets (67), Homeostasis (68), Margin (64) | 64, 67, 68 |
| P1 (Week 2) | Scenario (60), Compliance (59), Tax (52) | 52, 59, 60 |
| P2 (Week 3) | Attribution (49), FixedIncome (50), Macro (53) | 49, 50, 53 |
| P3 (Week 4+) | Remaining services | 51, 54-58, 61-66 |

---

## Test Command Reference

```bash
# Run all Phase X2 backend tests
.\venv\Scripts\python.exe -m pytest tests/analysis/ tests/tax/ tests/compliance/ tests/security/ tests/crypto/ tests/philanthropy/ -v --cov=services --cov-report=html

# Run specific phase tests
.\venv\Scripts\python.exe -m pytest tests/analysis/test_attribution_service.py -v  # Phase 49
.\venv\Scripts\python.exe -m pytest tests/analysis/test_scenario_service.py -v    # Phase 60
.\venv\Scripts\python.exe -m pytest tests/compliance/ -v                           # Phase 59
```
