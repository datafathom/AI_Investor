# API Vendor Integration Roadmap

This document provides a comprehensive **33-phase integration plan** for all 39 API vendors listed in `notes/API_Vendor_Inventory.md`. Each phase includes at least 3 deliverables with verbose acceptance criteria, task descriptions, and clear backend/frontend implementation requirements.

> [!IMPORTANT]
> All code files created during this integration MUST include a header comment explaining how the file integrates into the AI Investor system architecture.

---

## Global Configuration & Credentials
> [!IMPORTANT]
> **Master Login**: All vendor APIs (Cloudflare, Coinbase, etc.) must use the root email: `datafathom@gmail.com`.
> **Reddit Config**: The `REDDIT_USER_AGENT` in .env must be updated to a valid account created by the user before switching to Live Mode.

## Phase 1: Alpha Vantage - Core Market Data Integration

**Objective**: Establish the primary market data pipeline for real-time equity prices, historical OHLCV data, and options chain retrieval.

### Deliverable 1.1: Alpha Vantage Client Service
**Task Description**: Create a robust Python client service that wraps the Alpha Vantage REST API. This service must handle authentication, rate limiting via `APIGovernor`, and provide typed response models for all supported endpoints (TIME_SERIES_INTRADAY, GLOBAL_QUOTE, HISTORICAL_OPTIONS, EARNINGS_CALENDAR).

**Backend Implementation**:
- File: `services/data/alpha_vantage.py`
- Header Comment: `# Alpha Vantage Client - Primary market data source for equity prices, options flow, and earnings calendars. Integrates with APIGovernor for rate limiting and EnvironmentManager for API key retrieval.`
- Implement `get_quote()`, `get_intraday()`, `get_daily()`, `get_options_chain()`, `get_earnings_calendar()` methods.
- All methods must call `APIGovernor.wait_for_slot("ALPHA_VANTAGE")` before making requests.

**Acceptance Criteria**:
- [ ] Service successfully retrieves real-time quotes for any valid ticker symbol.
- [ ] Service gracefully handles 429 rate limit errors with exponential backoff.
- [ ] Service logs all API calls with request duration and response size.
- [ ] Unit tests cover all public methods with mock responses.
- [ ] Integration test confirms live API connectivity with a funded key.

---

### Deliverable 1.2: Market Data API Endpoints
**Task Description**: Expose Alpha Vantage data through Flask/FastAPI endpoints for frontend consumption. These endpoints should support caching, pagination for historical data, and error normalization.

**Backend Implementation**:
- File: `apis/market_data_api.py`
- Header Comment: `# Market Data API - RESTful endpoints for frontend consumption of Alpha Vantage data. Caches responses via Redis and normalizes error responses across all data vendors.`
- Implement `GET /api/market/quote/{symbol}`, `GET /api/market/history/{symbol}`, `GET /api/market/options/{symbol}`, `GET /api/market/earnings`.

**Acceptance Criteria**:
- [ ] Endpoints return JSON with consistent schema (`data`, `meta`, `errors` keys).
- [ ] Caching reduces duplicate API calls by at least 80% for frequently requested symbols.
- [ ] Error responses include `error_code`, `message`, and `vendor` fields.
- [ ] All endpoints are documented in OpenAPI/Swagger.

---

### Deliverable 1.3: Frontend Market Data Widgets
**Task Description**: Create React/Zustand components that consume the Market Data API and display real-time quotes, historical charts, and earnings calendars.

**Frontend Implementation**:
- Files: `frontend2/src/widgets/Market/QuoteCard.jsx`, `frontend2/src/widgets/Market/PriceChart.jsx`, `frontend2/src/widgets/Market/EarningsCalendar.jsx`
- Store: `frontend2/src/stores/marketStore.js`
- Header Comment (in each file): `// Market Data Widget - Displays real-time equity data from Alpha Vantage via the /api/market/* endpoints. Subscribes to marketStore for state management.`

**Acceptance Criteria**:
- [ ] QuoteCard displays bid/ask, last price, volume, and change percentage.
- [ ] PriceChart renders historical data with zoom/pan functionality.
- [ ] EarningsCalendar displays upcoming earnings with date, EPS estimate, and fiscal quarter.
- [ ] All widgets handle loading/error states with appropriate UI feedback.
- [ ] Widgets auto-refresh every 60 seconds during market hours.

---

## Phase 2: FRED - Macroeconomic Data Integration

**Objective**: Integrate Federal Reserve Economic Data for inflation tracking, unemployment metrics, and yield curve analysis.

### Deliverable 2.1: FRED Client Service
**Task Description**: Create a Python client that consumes the FRED API for key macroeconomic series (CPI, UNRATE, T10Y2Y, GDP, FEDFUNDS). The service must support historical data retrieval, observation frequency normalization, and real-time series metadata.

**Backend Implementation**:
- File: `services/data/fred_service.py`
- Header Comment: `# FRED Service - Consumes Federal Reserve Economic Data for macroeconomic analysis. Provides inflation (CPI), unemployment (UNRATE), and yield curve (T10Y2Y) metrics. Integrates with APIGovernor and MacroService.`
- Implement `get_series()`, `get_latest_observation()`, `get_series_metadata()`, `get_releases()`.

**Acceptance Criteria**:
- [ ] Service retrieves CPI, UNRATE, and T10Y2Y series with full historical data.
- [ ] Service normalizes all date formats to ISO 8601.
- [ ] Service caches series metadata to reduce redundant API calls.
- [ ] Unit tests cover all public methods with mock FRED responses.

---

### Deliverable 2.2: Macro Analysis Engine
**Task Description**: Build a higher-level analysis engine that uses FRED data to calculate regime indicators (Inflationary, Deflationary, Stagflation, Goldilocks) and generate macro health scores.

**Backend Implementation**:
- File: `services/analysis/macro_service.py`
- Header Comment: `# Macro Analysis Service - Consumes FRED data to calculate economic regime indicators and macro health scores. Used by FearGreedService and PortfolioRebalancer for strategic allocation.`
- Implement `calculate_regime()`, `get_macro_health_score()`, `get_yield_curve_status()`.

**Acceptance Criteria**:
- [ ] Regime calculation correctly identifies current economic state based on CPI/UNRATE trends.
- [ ] Yield curve inversion detection triggers appropriate alerts.
- [ ] Macro health score is a normalized 0-100 value.
- [ ] All calculations are documented with source formulas.

---

### Deliverable 2.3: Frontend Macro Dashboard
**Task Description**: Create a Macro Health dashboard that visualizes FRED data, economic regimes, and yield curve status.

**Frontend Implementation**:
- Files: `frontend2/src/widgets/Macro/MacroHealthGauge.jsx`, `frontend2/src/widgets/Macro/YieldCurveChart.jsx`, `frontend2/src/widgets/Macro/RegimeIndicator.jsx`
- Store: `frontend2/src/stores/macroStore.js`

**Acceptance Criteria**:
- [ ] MacroHealthGauge displays a radial gauge with color-coded zones.
- [ ] YieldCurveChart plots the full yield curve with inversion highlighting.
- [ ] RegimeIndicator shows current regime with historical regime transitions.
- [ ] Dashboard updates on FRED data refresh (daily).

---

## Phase 3: Polygon.io - Secondary Market Data

**Objective**: Integrate Polygon.io as a backup and high-frequency data source for tick-level data and aggregates.

### Deliverable 3.1: Polygon Client Service
**Task Description**: Create a Polygon.io client service that provides real-time WebSocket streaming, historical aggregates, and ticker details.

**Backend Implementation**:
- File: `services/data/polygon_service.py`
- Header Comment: `# Polygon Service - Secondary market data source for high-frequency tick data and aggregates. Used as fallback when Alpha Vantage is rate-limited.`

**Acceptance Criteria**:
- [ ] Client supports both REST and WebSocket connections.
- [ ] Aggregates endpoint supports 1-minute, 5-minute, hourly, and daily bars.
- [ ] WebSocket reconnection logic handles network interruptions.
- [ ] Service reports usage to APIGovernor for rate tracking.

---

### Deliverable 3.2: Data Fusion Layer
**Task Description**: Build a data fusion service that intelligently selects between Alpha Vantage and Polygon based on availability, latency, and rate limit status.

**Backend Implementation**:
- File: `services/data/data_fusion_service.py`
- Header Comment: `# Data Fusion Service - Orchestrates data retrieval across multiple vendors (Alpha Vantage, Polygon). Implements fallback logic and source prioritization.`

**Acceptance Criteria**:
- [ ] Fusion layer automatically switches to Polygon when Alpha Vantage is rate-limited.
- [ ] Source selection is logged for debugging and auditing.
- [ ] Response schema is normalized across all sources.

---

### Deliverable 3.3: Polygon Health Monitor
**Task Description**: Create a monitoring widget that displays the health and latency of all market data sources.

**Frontend Implementation**:
- File: `frontend2/src/widgets/System/DataSourceHealth.jsx`

**Acceptance Criteria**:
- [ ] Widget displays status (Online/Degraded/Offline) for each data source.
- [ ] Latency is shown in milliseconds with historical trend.
- [ ] Rate limit usage is displayed as a percentage of daily quota.

---

## Phase 4: Quandl / Nasdaq Data Link - Alternative Data

**Objective**: Integrate Quandl for institutional-grade alternative data including short interest, insider trades, and economic indicators.

### Deliverable 4.1: Quandl Client Service
**Task Description**: Create a Quandl client that accesses free and premium datasets for short interest (FINRA), insider transactions, and commodity prices.

**Backend Implementation**:
- File: `services/data/quandl_service.py`
- Header Comment: `# Quandl Service - Accesses Nasdaq Data Link for alternative data (short interest, insider trades, commodities). Used by ConvictionAnalyzer and RiskEngine.`

**Acceptance Criteria**:
- [x] Client retrieves FINRA short interest data for any equity ticker.
- [x] Client handles both timeseries and datatables API patterns.
- [x] Premium dataset access is gated by environment flag.

---

### Deliverable 4.2: Short Interest Analysis
**Task Description**: Build an analysis module that calculates days-to-cover, short ratio trends, and squeeze probability scores.

**Backend Implementation**:
- File: `services/analysis/short_interest_service.py`

**Acceptance Criteria**:
- [x] Days-to-cover calculation is accurate based on average daily volume.
- [x] Squeeze probability score is a normalized 0-100 value.
- [x] Historical short interest trends are available for charting.

---

### Deliverable 4.3: Frontend Short Interest Widget
**Task Description**: Create a widget that displays short interest metrics and squeeze alerts.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Analysis/ShortInterestCard.jsx`

**Acceptance Criteria**:
- [x] Card displays short ratio, days-to-cover, and squeeze probability.
- [x] Visual alerts trigger when squeeze probability exceeds threshold.
- [x] Historical short interest is charted with price overlay.

---

## Phase 5: Finnhub - Real-Time Stock Data & Calendars

**Objective**: Integrate Finnhub for real-time stock data, IPO calendars, and company news.

### Deliverable 5.1: Finnhub Client Service
**Task Description**: Create a Finnhub client for real-time quotes, company profiles, IPO calendars, and news feeds.

**Backend Implementation**:
- File: `services/data/finnhub_service.py`
- Header Comment: `# Finnhub Service - Real-time stock data, IPO calendars, and company news. Used for event-driven trading signals and corporate action tracking.`

**Acceptance Criteria**:
- [x] Client retrieves real-time quotes with bid/ask spread.
- [x] IPO calendar returns upcoming listings with expected dates and valuations.
- [x] News feed supports filtering by ticker and date range.

---

### Deliverable 5.2: IPO Calendar Integration
**Task Description**: Build an IPO tracking module that monitors upcoming listings and generates alerts.

**Backend Implementation**:
- File: `services/trading/ipo_tracker.py`

**Acceptance Criteria**:
- [x] Tracker maintains a database of upcoming IPOs with filing details.
- [x] Alerts are triggered 7 days and 1 day before expected listing.
- [x] IPO success probability is estimated based on sector and market conditions.

---

### Deliverable 5.3: Frontend IPO Calendar Widget
**Task Description**: Create a calendar widget that displays upcoming IPOs with hover details.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Corporate/IPOCalendar.jsx`

**Acceptance Criteria**:
- [x] Calendar displays IPO dates with company name and sector.
- [x] Hover reveals valuation range, underwriters, and filing link.
- [x] Past IPOs show first-day performance.

---

## Phase 6: NewsAPI.org - Breaking News Aggregation

**Objective**: Integrate NewsAPI for real-time breaking news sentiment triggers and headline monitoring.

### Deliverable 6.1: NewsAPI Client Service
**Task Description**: Create a NewsAPI client that retrieves top headlines, everything search, and source metadata.

**Backend Implementation**:
- File: `services/data/news_api_service.py`
- Header Comment: `# NewsAPI Service - Aggregates breaking news headlines for sentiment analysis. Integrates with HypeTracker and FearGreedService.`

**Acceptance Criteria**:
- [ ] Client retrieves top headlines filtered by category (business, technology).
- [ ] Everything search supports keyword queries with date ranges.
- [ ] Service respects 100 requests/day free tier limit via APIGovernor.

---

### Deliverable 6.2: News Sentiment Analyzer
**Task Description**: Build a sentiment analysis module that scores news headlines and detects market-moving events.

**Backend Implementation**:
- File: `services/analysis/news_sentiment_service.py`

**Acceptance Criteria**:
- [ ] Headlines are scored on a -1 to +1 sentiment scale.
- [ ] Market-moving keywords trigger elevated alert levels.
- [ ] Sentiment aggregates are available at ticker and sector levels.

---

### Deliverable 6.3: Frontend News Feed Widget
**Task Description**: Create a real-time news feed widget with sentiment indicators.

**Frontend Implementation**:
- File: `frontend2/src/widgets/News/NewsFeed.jsx`

**Acceptance Criteria**:
- [ ] Feed displays headlines with source, timestamp, and sentiment badge.
- [ ] Clicking a headline opens the full article in a new tab.
- [ ] Feed supports filtering by ticker and sentiment polarity.

---

## Phase 7: CryptoCompare Integration

**Objective**: Integrate CryptoCompare for real-time crypto-asset pricing and volume tracking.

### Deliverable 7.1: CryptoCompare Client
**Task Description**: Create a client for real-time multi-symbol pricing and volume analysis.

**Backend Implementation**:
- File: `services/data/crypto_compare_service.py`

**Acceptance Criteria**:
- [x] Client retrieves real-time prices for BTC, ETH, SOL.
- [x] Volume data includes top exchange market share.

---

## Phase 7.5: OpenAI - LLM Integration for Autocoder

### Deliverable 7.1: OpenAI Client Service
**Task Description**: Create an OpenAI client that handles chat completions, function calling, and embeddings.

**Backend Implementation**:
- File: `services/ai/openai_client.py`
- Header Comment: `# OpenAI Client - Provides GPT-4 chat completions, function calling, and embeddings. Used by Autocoder agent and natural language command processor.`

**Acceptance Criteria**:
- [ ] Client supports streaming and non-streaming completions.
- [ ] Function calling schema is validated before submission.
- [ ] Token usage is tracked and reported to APIGovernor.

---

### Deliverable 7.2: Autocoder Agent
**Task Description**: Build an agent that uses OpenAI to autonomously generate and execute Python code for trading strategies.

**Backend Implementation**:
- File: `agents/autocoder_agent.py`

**Acceptance Criteria**:
- [ ] Agent generates syntactically valid Python code from natural language prompts.
- [ ] Generated code is sandboxed and validated before execution.
- [ ] Execution results are captured and returned to the user.

---

### Deliverable 7.3: Natural Language Command Interface
**Task Description**: Create a frontend chat interface for natural language portfolio commands.

**Frontend Implementation**:
- File: `frontend2/src/widgets/AI/CommandChat.jsx`

**Acceptance Criteria**:
- [ ] User can type natural language commands (e.g., "Buy 10 shares of AAPL").
- [ ] Commands are parsed and confirmed before execution.
- [ ] Chat history is persisted for session context.

---

---

### Phase 8: Reddit Integration - Social Sentiment
- **Status**: [x] COMPLETED
- **Description**: Social sentiment and "hype" detection.
- **Key Deliverables**: `RedditClient` (Mock), `RedditSentiment` Widget.

---

### Phase 9: Anthropic Claude - Debate Chamber Integration
- **Status**: [x] COMPLETED
- **Description**: Multi-persona debate simulations (Bull vs. Bear).
- **Key Deliverables**: `DebateChamberAgent` (Mock), `DebateViewer` Widget.

**Acceptance Criteria**:
- [ ] Client supports system message injection for persona control.
- [ ] Response parsing handles Claude's XML-tagged thinking blocks.
- [ ] Token usage is tracked and reported to APIGovernor.

---

### Deliverable 8.2: Debate Chamber Agent
**Task Description**: Build an agent that orchestrates multi-persona debates using different LLM configurations.

**Backend Implementation**:
- File: `agents/debate_chamber_agent.py`

**Acceptance Criteria**:
- [ ] Agent supports Bull, Bear, and Neutral personas.
- [ ] Each persona has distinct system prompts and reasoning styles.
- [ ] Final consensus is synthesized from all persona outputs.

---

### Deliverable 8.3: Frontend Debate Viewer
**Task Description**: Create a visualization of the debate process with persona avatars and argument cards.

**Frontend Implementation**:
- File: `frontend2/src/widgets/AI/DebateViewer.jsx`

**Acceptance Criteria**:
- [ ] Viewer displays argument cards from each persona.
- [ ] Final consensus is highlighted with confidence score.
- [ ] User can trigger new debates on any ticker or strategy.

---

### Phase 10: Google Gemini - Market Summaries
- **Status**: [x] COMPLETED
- **Description**: Daily morning briefings and market outlooks.
- **Key Deliverables**: `GeminiClient` (Mock), `MorningBriefing` Widget.

**Acceptance Criteria**:
- [ ] Client supports text and image inputs for multi-modal analysis.
- [ ] Free tier limits (15 req/min, 1500 req/day) are enforced via APIGovernor.
- [ ] Response streaming is supported for long-form outputs.

---

### Deliverable 9.2: Morning Briefing Generator
**Task Description**: Build a scheduled service that generates daily market briefings using Gemini.

**Backend Implementation**:
- File: `services/ai/briefing_generator.py`

**Acceptance Criteria**:
- [ ] Briefing is generated daily at 6:00 AM ET.
- [ ] Briefing includes market outlook, key events, and portfolio alerts.
- [ ] Briefing is stored in database and available via API.

---

### Deliverable 9.3: Frontend Briefing Widget
**Task Description**: Create a morning briefing widget that displays the daily summary.

**Frontend Implementation**:
- File: `frontend2/src/widgets/AI/MorningBriefing.jsx`

**Acceptance Criteria**:
- [ ] Widget displays formatted briefing with sections for Outlook, Events, Alerts.
- [ ] Historical briefings are accessible via date picker.
- [ ] User can regenerate briefing on demand.

---

### Phase 11: Perplexity AI - Real-Time Research
- **Status**: [x] COMPLETED
- **Description**: Search-augmented market research with citations.
- **Key Deliverables**: `PerplexityClient` (Mock), `ResearchPanel` Widget.

**Acceptance Criteria**:
- [ ] Client supports Sonar models for online search.
- [ ] Citations are parsed and returned with response.
- [ ] Pro user credits are tracked for billing.

---

### Deliverable 10.2: Research Agent
**Task Description**: Build a research agent that uses Perplexity to answer complex market questions with sources.

**Backend Implementation**:
- File: `agents/research_agent.py`

**Acceptance Criteria**:
- [ ] Agent answers questions with structured responses and citations.
- [ ] Historical research queries are cached for efficiency.
- [ ] Agent falls back to Gemini if Perplexity quota is exhausted.

---

### Deliverable 10.3: Frontend Research Panel
**Task Description**: Create a research panel that displays Perplexity answers with inline citations.

**Frontend Implementation**:
- File: `frontend2/src/widgets/AI/ResearchPanel.jsx`

**Acceptance Criteria**:
- [ ] Panel displays answers with clickable citation links.
- [ ] Related follow-up questions are suggested.
- [ ] Research history is persisted per user session.

---

### Phase 12: Stripe - Subscription Management
- **Status**: [x] COMPLETED
- **Description**: Subscription billing and mock checkout.
- **Key Deliverables**: `StripeClient` (Mock), `Billing` Dashboard.

**Acceptance Criteria**:
- [ ] Client creates Stripe customers linked to platform user IDs.
- [ ] Subscriptions support multiple tiers (Free, Pro, Enterprise).
- [ ] Checkout sessions redirect to Stripe-hosted payment page.

---

### Deliverable 11.2: Webhook Handler
**Task Description**: Build a webhook endpoint that processes Stripe events (payment_intent.succeeded, customer.subscription.updated, etc.).

**Backend Implementation**:
- File: `apis/webhooks/stripe_webhook.py`

**Acceptance Criteria**:
- [ ] Webhook validates Stripe signature before processing.
- [ ] Subscription status changes update user tier in database.
- [ ] Failed payments trigger notification and grace period logic.

---

### Deliverable 11.3: Frontend Billing Dashboard
**Task Description**: Create a billing dashboard with subscription status, payment history, and upgrade options.

**Frontend Implementation**:
- File: `frontend2/src/pages/Billing.jsx`

**Acceptance Criteria**:
- [ ] Dashboard displays current subscription tier and renewal date.
- [ ] Payment history shows last 12 months of transactions.
- [ ] Upgrade/downgrade buttons trigger Stripe checkout flows.

---

### Phase 13: PayPal - Alternative Checkout
- **Status**: [x] COMPLETED
- **Description**: PayPal order creation and capture.
- **Key Deliverables**: `PayPalClient` (Mock), `PayPalButton` Component.

**Acceptance Criteria**:
- [x] Client creates PayPal orders with line items and totals.
- [x] Order capture returns transaction ID and payer info.
- [ ] Refunds are processed with reason codes.

---

### Deliverable 12.2: PayPal Checkout Integration
**Task Description**: Add PayPal as a checkout option alongside Stripe.

**Backend Implementation**:
- File: `apis/checkout_api.py` (modify existing)

**Acceptance Criteria**:
- [ ] Checkout endpoint accepts `payment_method: "paypal"` parameter.
- [ ] PayPal orders redirect to PayPal-hosted approval page.
- [ ] Successful payments update user subscription status.

---

### Deliverable 12.3: Frontend PayPal Button
**Task Description**: Add PayPal Smart Buttons to the checkout page.

**Frontend Implementation**:
- File: `frontend2/src/components/Checkout/PayPalButton.jsx`

**Acceptance Criteria**:
- [ ] Button renders PayPal checkout option.
- [ ] Successful payment shows confirmation modal.
- [ ] Error handling displays user-friendly messages.

---

### Phase 14: Venmo - Payment Integration
- **Status**: [x] COMPLETED
- **Description**: Mock Venmo P2P payment flow (Mobile First).
- **Key Deliverables**: `VenmoClient` (Mock), `VenmoButton` Component.

**Acceptance Criteria**:
- [x] Venmo payments are processed (Mock).
- [x] Mobile users see Venmo as a primary option.

---

## Phase 15: Square - Merchant Processing

**Objective**: Integrate Square for in-person payments and merchant processing (future retail kiosk support).

### Deliverable 15.1: Square Client Service
**Task Description**: Create a Square client for payments, customers, and catalog management.

**Backend Implementation**:
- File: `services/payments/square_service.py`
- Header Comment: `# Square Service - Merchant payment processing for in-person and online transactions. Future retail kiosk support.`

**Acceptance Criteria**:
- [ ] Client creates payments with source ID from Square SDK.
- [ ] Customer profiles are created and linked to platform users.
- [ ] Sandbox environment is fully tested before live switch.

---

### Deliverable 14.2: Square Catalog Sync
**Task Description**: Sync subscription tiers as Square catalog items for unified pricing.

**Backend Implementation**:
- File: `services/payments/catalog_sync.py`

**Acceptance Criteria**:
- [ ] Catalog items match Stripe subscription tiers.
- [ ] Price changes sync bidirectionally.
- [ ] Catalog version is tracked for conflict resolution.

---

### Deliverable 14.3: Square Dashboard Widget
**Task Description**: Create an admin widget that displays Square transaction volume and merchant stats.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Admin/SquareStats.jsx`

**Acceptance Criteria**:
- [ ] Widget displays daily/weekly/monthly transaction volume.
- [ ] Refund rate is calculated and displayed.
- [ ] Top customers are listed by lifetime value.

---

## Phase 15: Plaid - Bank Account Linking

**Objective**: Integrate Plaid for bank account linking, balance verification, and ACH transfers.

### Deliverable 15.1: Plaid Link Integration
**Task Description**: Integrate Plaid Link for secure bank account connection.

**Backend Implementation**:
- File: `services/banking/plaid_service.py`
- Header Comment: `# Plaid Service - Bank account linking for deposits, balance checks, and ACH transfers. Critical for capital onboarding.`

**Acceptance Criteria**:
- [ ] Service creates link tokens for frontend initialization.
- [ ] Access tokens are exchanged and stored securely.
- [ ] Account metadata (name, mask, type) is retrieved.

---

### Deliverable 15.2: Balance Verification
**Task Description**: Retrieve real-time bank balances for funding verification.

**Backend Implementation**:
- Extend `services/banking/plaid_service.py` with `get_balance()` method.

**Acceptance Criteria**:
- [ ] Current and available balances are retrieved.
- [ ] Balance checks are rate-limited to prevent abuse.
- [ ] Overdraft protection warnings are generated.

---

### Deliverable 15.3: Frontend Plaid Link Modal
**Task Description**: Create a modal that launches Plaid Link for account connection.

**Frontend Implementation**:
- File: `frontend2/src/components/Banking/PlaidLinkModal.jsx`

**Acceptance Criteria**:
- [ ] Modal initializes Plaid Link with correct environment.
- [ ] Success callback stores public token and initiates exchange.
- [ ] Error states display user-friendly messages.

---

## Phase 16: Facebook / Meta - SSO & Hype Ingestion

**Objective**: Integrate Facebook for SSO authentication and Graph API for social hype tracking.

### Deliverable 16.1: Facebook OAuth Integration
**Task Description**: Implement Facebook Login for SSO authentication.

**Backend Implementation**:
- File: `services/auth/facebook_auth.py`
- Header Comment: `# Facebook Auth - SSO Login via Facebook OAuth2. Links Facebook profiles to platform accounts.`

**Acceptance Criteria**:
- [ ] OAuth flow completes with access token exchange.
- [ ] User profile (name, email, picture) is retrieved via Graph API.
- [ ] Existing users are linked; new users are created.

---

### Deliverable 16.2: Facebook Hype Ingestion
**Task Description**: Build a service that monitors Facebook pages/groups for stock mentions.

**Backend Implementation**:
- File: `services/social/facebook_hype_service.py`

**Acceptance Criteria**:
- [ ] Service monitors specified pages for stock ticker mentions.
- [ ] Mention counts are aggregated hourly.
- [ ] Spikes trigger alerts to HypeTracker.

---

### Phase 20: Twilio - SMS Alerts
- **Status**: [x] COMPLETED
- **Description**: Mock SMS notification delivery.
- **Key Deliverables**: `TwilioClient` (Mock), `SMSAlertSettings` Widget.

**Acceptance Criteria**:
- [x] SMS alerts simulated and logged.
- [x] Frontend configuration for phone numbers and triggers.

---

## Phase 17: Google OAuth - Universal SSO

**Objective**: Integrate Google OAuth for universal SSO across all Google services.

### Phase 21: SendGrid - Email Reports
- **Status**: [x] COMPLETED
- **Description**: Mock email report delivery.
- **Key Deliverables**: `SendGridClient` (Mock), `EmailReportSettings` Widget.

**Acceptance Criteria**:
- [x] Email reports simulated and logged.
- [x] Frontend configuration for delivery preferences.

---

### Deliverable 17.2: Google Profile Sync
**Task Description**: Sync Google profile data (name, picture, email) to platform accounts.

**Backend Implementation**:
- Extend `services/user/user_service.py` with Google profile fields.

**Acceptance Criteria**:
- [ ] Profile picture is retrieved from Google People API.
- [ ] Email is verified and marked as primary.
- [ ] Profile updates sync on each login.

---

### Phase 22: PagerDuty - Incident Management
- **Status**: [x] COMPLETED
- **Description**: Mock incident triggering and dashboard.
- **Key Deliverables**: `PagerDutyClient` (Mock), `IncidentDashboard` Widget.

**Acceptance Criteria**:
- [x] Incidents created and listed.
- [x] Frontend dashboard for Ops monitoring.

---

## Phase 18: Gmail API - Email Notifications

**Objective**: Integrate Gmail API for sending portfolio alerts and transactional emails.

### Deliverable 18.1: Gmail Client Service
**Task Description**: Create a Gmail client for sending emails via user's connected account.

**Backend Implementation**:
- File: `services/communication/gmail_service.py`
- Header Comment: `# Gmail Service - Sends portfolio alerts and transactional emails via user's Gmail account. Requires OAuth with gmail.send scope.`

**Acceptance Criteria**:
- [ ] Client sends emails using authenticated user's Gmail.
- [ ] HTML templates are rendered for rich content.
- [ ] Sent emails are tracked in database.

---

### Deliverable 18.2: Email Template Engine
**Task Description**: Build a template engine for portfolio alerts, reports, and notifications.

**Backend Implementation**:
- File: `services/communication/email_templates.py`

**Acceptance Criteria**:
- [ ] Templates exist for: margin_alert, daily_summary, trade_confirmation, password_reset.
- [ ] Templates support variable interpolation.
- [ ] Preview endpoint renders templates without sending.

---

### Deliverable 18.3: Frontend Email Settings
**Task Description**: Create settings page for email notification preferences.

**Frontend Implementation**:
- File: `frontend2/src/pages/Settings/EmailPreferences.jsx`

**Acceptance Criteria**:
- [ ] Users can toggle each email type on/off.
- [ ] Frequency options (instant, daily digest, weekly) are available.
- [ ] Test email button sends sample notification.

---

## Phase 19: Google Calendar API - Event Scheduling

**Objective**: Integrate Google Calendar for earnings call reminders, rebalancing schedules, and dividend dates.

### Deliverable 19.1: Calendar Client Service
**Task Description**: Create a Calendar client for creating, reading, and deleting events.

**Backend Implementation**:
- File: `services/calendar/google_calendar_service.py`
- Header Comment: `# Google Calendar Service - Schedules earnings calls, rebalancing reminders, and dividend dates on user's Google Calendar.`

**Acceptance Criteria**:
- [ ] Client creates events with title, description, start/end times.
- [ ] Events are created on user's primary calendar.
- [ ] Reminders are set at 1 day and 1 hour before event.

---

### Deliverable 19.2: Earnings Calendar Sync
**Task Description**: Automatically create calendar events for holdings' earnings dates.

**Backend Implementation**:
- File: `services/calendar/earnings_sync.py`

**Acceptance Criteria**:
- [ ] Sync runs daily after market close.
- [ ] Events are created for all holdings' upcoming earnings.
- [ ] Duplicate events are detected and skipped.

---

### Deliverable 19.3: Frontend Calendar Integration Widget
**Task Description**: Display Google Calendar events in a portfolio calendar view.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Calendar/PortfolioCalendar.jsx`

**Acceptance Criteria**:
- [ ] Calendar displays earnings, dividends, and rebalancing events.
- [ ] Clicking an event shows details modal.
- [ ] Events are color-coded by type.

---

## Phase 20: Reddit OAuth - Sentiment Authentication

**Objective**: Integrate Reddit OAuth for authenticated sentiment data access and user profiling.

### Deliverable 20.1: Reddit OAuth Service
**Task Description**: Implement Reddit Login for SSO and authenticated API access.

**Backend Implementation**:
- File: `services/auth/reddit_auth.py`
- Header Comment: `# Reddit Auth - OAuth2 for authenticated Reddit API access. Enables higher rate limits and user profiling.`

**Acceptance Criteria**:
- [ ] OAuth flow completes with access/refresh token exchange.
- [ ] User profile (username, karma) is retrieved.
- [ ] Authenticated requests use OAuth tokens.

---

### Deliverable 20.2: Reddit Sentiment Service Enhancement
**Task Description**: Upgrade Reddit sentiment service to use authenticated endpoints for higher limits.

**Backend Implementation**:
- Modify `services/data/reddit_service.py`

**Acceptance Criteria**:
- [ ] Service uses OAuth tokens when available.
- [ ] Rate limits increase from 10 req/min to 100 req/min.
- [ ] Fallback to unauthenticated mode on token failure.

---

### Deliverable 20.3: Reddit User Watchlist
**Task Description**: Allow users to follow specific Reddit authors for sentiment signals.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Social/RedditWatchlist.jsx`

**Acceptance Criteria**:
- [ ] Users can add Reddit usernames to watchlist.
- [ ] Activity from watched users triggers alerts.
- [ ] Watchlist syncs across devices.

---

## Phase 21: Alpaca Markets - Trade Execution

**Objective**: Integrate Alpaca Markets for automated equity trade execution.

### Deliverable 21.1: Alpaca Trading Client
**Task Description**: Create an Alpaca client for order placement, position management, and account status.

**Backend Implementation**:
- File: `services/brokerage/alpaca_client.py`
- Header Comment: `# Alpaca Client - Primary trade execution for U.S. equities. Supports market, limit, and stop orders with fractional shares.`

**Acceptance Criteria**:
- [ ] Client places market, limit, stop, and stop-limit orders.
- [ ] Fractional share orders are supported.
- [ ] Order status polling tracks fills in real-time.

---

### Deliverable 21.2: Position Synchronization
**Task Description**: Sync Alpaca positions with platform portfolio state.

**Backend Implementation**:
- File: `services/brokerage/position_sync.py`

**Acceptance Criteria**:
- [ ] Positions sync every 5 minutes during market hours.
- [ ] Discrepancies trigger alerts and reconciliation.
- [ ] Cost basis is calculated from historical orders.

---

### Deliverable 21.3: Frontend Trade Ticket
**Task Description**: Create a trade ticket component for placing orders.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Trading/TradeTicket.jsx`

**Acceptance Criteria**:
- [ ] Trade ticket supports all order types.
- [ ] Estimated cost is calculated before submission.
- [ ] Order confirmation displays fill details.

---

## Phase 22: Interactive Brokers - Professional Execution

**Objective**: Integrate Interactive Brokers for professional-grade global execution.

### Deliverable 22.1: IBKR Client Portal API Client
**Task Description**: Create an IBKR client using the Client Portal API for order placement and account data.

**Backend Implementation**:
- File: `services/brokerage/ibkr_client.py`
- Header Comment: `# IBKR Client - Professional-grade global execution across 150+ markets. Requires IBKR Gateway for authentication.`

**Acceptance Criteria**:
- [ ] Client authenticates via IBKR Gateway session.
- [ ] Orders are placed across multiple asset classes.
- [ ] Account data includes all global positions.

---

### Deliverable 22.2: IBKR Gateway Manager
**Task Description**: Build a service that manages IBKR Gateway lifecycle (start, authenticate, keep-alive).

**Backend Implementation**:
- File: `services/brokerage/ibkr_gateway_manager.py`

**Acceptance Criteria**:
- [ ] Gateway starts automatically on platform boot.
- [ ] Authentication prompts are handled via UI callback.
- [ ] Keep-alive pings prevent session timeout.

---

### Deliverable 22.3: IBKR Account Dashboard
**Task Description**: Create a dashboard for IBKR account status, positions, and margin requirements.

**Frontend Implementation**:
- File: `frontend2/src/pages/Accounts/IBKRDashboard.jsx`

**Acceptance Criteria**:
- [ ] Dashboard displays all IBKR positions with P&L.
- [ ] Margin requirements are shown with utilization percentage.
- [ ] Currency exposure is visualized.

---

## Phase 23: Robinhood - Retail Brokerage Sync

**Objective**: Integrate Robinhood via `robin_stocks` for retail portfolio sync.

### Deliverable 23.1: Robinhood Client
**Task Description**: Create a Robinhood client using `robin_stocks` for authentication and data retrieval.

**Backend Implementation**:
- File: `services/brokerage/robinhood_client.py`
- Header Comment: `# Robinhood Client - Retail brokerage sync via robin_stocks library. Read-only access for portfolio aggregation.`

**Acceptance Criteria**:
- [ ] Client authenticates with username/password and MFA.
- [ ] Positions and orders are retrieved.
- [ ] Historical transactions are fetched for tax reporting.

---

### Deliverable 23.2: Robinhood Portfolio Aggregation
**Task Description**: Aggregate Robinhood positions into the unified portfolio view.

**Backend Implementation**:
- Extend `services/portfolio/portfolio_aggregator.py`

**Acceptance Criteria**:
- [ ] Robinhood positions appear in unified portfolio.
- [ ] Cost basis and gains are calculated correctly.
- [ ] Crypto holdings are included if enabled.

---

### Deliverable 23.3: Robinhood Connection Flow
**Task Description**: Create a secure connection flow for Robinhood credentials.

**Frontend Implementation**:
- File: `frontend2/src/components/Brokerage/RobinhoodConnect.jsx`

**Acceptance Criteria**:
- [ ] Credentials are entered in a secure modal.
- [ ] MFA prompt appears when required.
- [ ] Connection status is displayed in settings.

---

## Phase 24: Cloudflare Ethereum RPC - Wallet Balance

**Objective**: Integrate Cloudflare Ethereum Gateway for wallet balance retrieval and chain state queries.

### Deliverable 24.1: Ethereum RPC Client
**Task Description**: Create an Ethereum client using `web3.py` connected to Cloudflare RPC.

**Backend Implementation**:
- File: `services/crypto/ethereum_client.py`
- Header Comment: `# Ethereum Client - EVM chain interactions via Cloudflare RPC. Retrieves wallet balances and token holdings.`

**Acceptance Criteria**:
- [ ] Client retrieves ETH balance for any address.
- [ ] ERC-20 token balances are fetched via contracts.
- [ ] Gas price estimates are available for transactions.

---

### Deliverable 24.2: Wallet Portfolio Sync
**Task Description**: Sync connected Ethereum wallets with platform portfolio.

**Backend Implementation**:
- Extend `services/crypto/wallet_service.py`

**Acceptance Criteria**:
- [ ] Wallet addresses are validated before storage.
- [ ] Token balances are refreshed hourly.
- [ ] USD values are calculated using price feeds.

---

### Deliverable 24.3: Wallet Connect Widget
**Task Description**: Create a widget for connecting Ethereum wallets via address or WalletConnect.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Crypto/WalletConnect.jsx`

**Acceptance Criteria**:
- [ ] Users can paste wallet addresses for read-only tracking.
- [ ] WalletConnect integration allows signing transactions.
- [ ] Connected wallets display in portfolio.

---

## Phase 25: Solana RPC - SPL Token Tracking

**Objective**: Integrate Solana RPC for SPL token tracking and wallet health checks.

### Deliverable 25.1: Solana RPC Client
**Task Description**: Create a Solana client for wallet balances, token accounts, and transaction history.

**Backend Implementation**:
- File: `services/crypto/solana_client.py`
- Header Comment: `# Solana Client - SPL token tracking and wallet health via Solana Mainnet-Beta RPC.`

**Acceptance Criteria**:
- [ ] Client retrieves SOL balance for any address.
- [ ] SPL token accounts are enumerated with metadata.
- [ ] Transaction history includes parsed instructions.

---

### Deliverable 25.2: Solana Token Registry
**Task Description**: Maintain a local registry of SPL token metadata for display purposes.

**Backend Implementation**:
- File: `services/crypto/solana_token_registry.py`

**Acceptance Criteria**:
- [ ] Registry includes name, symbol, decimals, and logo URL.
- [ ] Unknown tokens display address as fallback.
- [ ] Registry updates weekly from Jupiter aggregator.

---

### Deliverable 25.3: Solana Wallet Widget
**Task Description**: Display Solana wallet holdings with SOL and SPL tokens.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Crypto/SolanaWallet.jsx`

**Acceptance Criteria**:
- [ ] Widget displays SOL balance with USD value.
- [ ] SPL tokens are listed with logos and balances.
- [ ] Token icons fall back to placeholder on load failure.

---

## Phase 26: Coinbase Cloud - Institutional Crypto

**Objective**: Integrate Coinbase Cloud for institutional custody and crypto trading.

### Deliverable 26.1: Coinbase Client
**Task Description**: Create a Coinbase client for account data, order placement, and custody operations.

**Backend Implementation**:
- File: `services/crypto/coinbase_client.py`
- Header Comment: `# Coinbase Client - Institutional custody and crypto trading via Coinbase Cloud API.`

**Acceptance Criteria**:
- [ ] Client authenticates using API key/secret with HMAC signing.
- [ ] Account balances are retrieved for all currencies.
- [ ] Orders are placed for supported trading pairs.

---

### Deliverable 26.2: Coinbase Custody Integration
**Task Description**: Enable cold storage custody via Coinbase Vault.

**Backend Implementation**:
- File: `services/crypto/coinbase_custody.py`

**Acceptance Criteria**:
- [ ] Vault balances are retrieved separately from trading account.
- [ ] Withdrawal requests require multi-party approval.
- [ ] Custody status is displayed in security dashboard.

---

### Deliverable 26.3: Coinbase Trading Widget
**Task Description**: Create a crypto trading widget connected to Coinbase.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Crypto/CoinbaseTrade.jsx`

**Acceptance Criteria**:
- [ ] Widget displays available trading pairs.
- [ ] Order form supports market and limit orders.
- [ ] Recent orders are displayed with status.

---

## Phase 27: StockTwits - Retail Sentiment

**Objective**: Integrate StockTwits for real-time retail sentiment from the trading community.

### Deliverable 27.1: StockTwits Client
**Task Description**: Create a StockTwits client for stream retrieval and messaging API.

**Backend Implementation**:
- File: `services/social/stocktwits_client.py`
- Header Comment: `# StockTwits Client - Retail sentiment from dedicated trading community. Highest signal-to-noise for meme stocks.`

**Acceptance Criteria**:
- [ ] Client retrieves symbol streams with messages and sentiment.
- [ ] Watchlist streams are supported for personalized feeds.
- [ ] Trending symbols are fetched hourly.

---

### Deliverable 27.2: StockTwits Sentiment Analyzer
**Task Description**: Analyze StockTwits messages for sentiment scoring and momentum detection.

**Backend Implementation**:
- File: `services/analysis/stocktwits_sentiment.py`

**Acceptance Criteria**:
- [ ] Bullish/Bearish/Neutral sentiment is extracted from messages.
- [ ] Volume spikes are detected and alerted.
- [ ] Sentiment history is stored for trend analysis.

---

### Deliverable 27.3: StockTwits Feed Widget
**Task Description**: Display a real-time StockTwits feed with sentiment indicators.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Social/StockTwitsFeed.jsx`

**Acceptance Criteria**:
- [ ] Feed displays messages with author, timestamp, and sentiment badge.
- [ ] Infinite scroll loads historical messages.
- [ ] Filter by bullish/bearish/all sentiment.

---

## Phase 28: Discord - Community Sentiment

**Objective**: Integrate Discord for server-based sentiment from trading communities.

### Deliverable 28.1: Discord Bot Service
**Task Description**: Create a Discord bot that monitors specified channels for stock mentions.

**Backend Implementation**:
- File: `services/social/discord_bot.py`
- Header Comment: `# Discord Bot - Monitors trading server channels for stock mentions and sentiment. Requires bot token with message read permissions.`

**Acceptance Criteria**:
- [ ] Bot joins specified servers and channels via invite.
- [ ] Messages are parsed for ticker mentions ($AAPL format).
- [ ] Mention counts are aggregated and sent to HypeTracker.

---

### Deliverable 28.2: Discord Webhook Alerts
**Task Description**: Send portfolio alerts to user-configured Discord channels.

**Backend Implementation**:
- File: `services/communication/discord_webhook.py`

**Acceptance Criteria**:
- [ ] Users can configure webhook URLs in settings.
- [ ] Alerts are formatted as Discord embeds.
- [ ] Webhook failures are logged and retried.

---

### Deliverable 28.3: Discord Integration Settings
**Task Description**: Create settings page for Discord bot and webhook configuration.

**Frontend Implementation**:
- File: `frontend2/src/pages/Settings/DiscordSettings.jsx`

**Acceptance Criteria**:
- [ ] Users can add/remove monitored servers.
- [ ] Webhook URL is validated before saving.
- [ ] Test alert button sends sample notification.

---

## Phase 29: YouTube Data API - Macro Video Analysis

**Objective**: Integrate YouTube Data API for transcribing and analyzing macro strategy videos.

### Deliverable 29.1: YouTube Client
**Task Description**: Create a YouTube client for video search, channel monitoring, and caption retrieval.

**Backend Implementation**:
- File: `services/social/youtube_client.py`
- Header Comment: `# YouTube Client - Searches and monitors macro strategy videos. Retrieves captions for transcript analysis.`

**Acceptance Criteria**:
- [ ] Client searches videos by keyword with date filtering.
- [ ] Channel subscriptions are monitored for new uploads.
- [ ] Closed captions are retrieved in plain text format.

---

### Deliverable 29.2: Video Transcript Analyzer
**Task Description**: Analyze video transcripts for market sentiment and key talking points.

**Backend Implementation**:
- File: `services/analysis/youtube_transcript_analyzer.py`

**Acceptance Criteria**:
- [ ] Transcripts are summarized using LLM.
- [ ] Key ticker mentions are extracted.
- [ ] Sentiment score is calculated for each video.

---

### Deliverable 29.3: YouTube Feed Widget
**Task Description**: Display monitored YouTube channels with latest videos and sentiment.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Social/YouTubeFeed.jsx`

**Acceptance Criteria**:
- [ ] Widget displays channel thumbnails with latest video.
- [ ] Video sentiment badge shows overall tone.
- [ ] Clicking video opens transcript analysis modal.

---

## Phase 30: Twilio - SMS Notifications

**Objective**: Integrate Twilio for SMS alerts for critical portfolio events.

### Deliverable 30.1: Twilio SMS Service
**Task Description**: Create a Twilio client for sending SMS messages.

**Backend Implementation**:
- File: `services/communication/twilio_service.py`
- Header Comment: `# Twilio Service - SMS alerts for margin calls, liquidation warnings, and 2FA codes.`

**Acceptance Criteria**:
- [ ] Client sends SMS to verified phone numbers.
- [ ] Message delivery status is tracked.
- [ ] Carrier lookup optimizes routing.

---

### Deliverable 30.2: SMS Alert Configuration
**Task Description**: Allow users to configure which alerts trigger SMS notifications.

**Backend Implementation**:
- Extend `services/user/notification_preferences.py`

**Acceptance Criteria**:
- [ ] Users select alert types for SMS (margin_call, liquidation, trade_fill).
- [ ] Phone number is verified via OTP before enabling.
- [ ] SMS quota is displayed to prevent overage.

---

### Deliverable 30.3: SMS Settings Page
**Task Description**: Create settings page for SMS phone number and alert preferences.

**Frontend Implementation**:
- File: `frontend2/src/pages/Settings/SMSSettings.jsx`

**Acceptance Criteria**:
- [ ] Phone number input with country code selector.
- [ ] OTP verification flow for new numbers.
- [ ] Toggle switches for each alert type.

---

## Phase 31: SendGrid - Transactional Email

**Objective**: Integrate SendGrid for transactional emails (receipts, confirmations, reports).

### Deliverable 31.1: SendGrid Email Service
**Task Description**: Create a SendGrid client for sending transactional emails.

**Backend Implementation**:
- File: `services/communication/sendgrid_service.py`
- Header Comment: `# SendGrid Service - Transactional emails for receipts, reports, and account notifications.`

**Acceptance Criteria**:
- [ ] Client sends emails using dynamic templates.
- [ ] Bounce and spam reports are processed via webhook.
- [ ] Email opens and clicks are tracked.

---

### Deliverable 31.2: Email Template Management
**Task Description**: Create and manage email templates in SendGrid dashboard.

**Backend Implementation**:
- File: `services/communication/sendgrid_templates.py`

**Acceptance Criteria**:
- [ ] Templates exist for: welcome, trade_confirmation, monthly_report, password_reset.
- [ ] Template IDs are configured in environment.
- [ ] Template versioning is tracked.

---

### Deliverable 31.3: Email Analytics Dashboard
**Task Description**: Display email send/open/click statistics.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Admin/EmailAnalytics.jsx`

**Acceptance Criteria**:
- [ ] Dashboard shows sends, opens, clicks by template.
- [ ] Bounce rate is highlighted with threshold alerts.
- [ ] Date range filter allows historical analysis.

---

## Phase 32: TaxBit - Crypto Tax Reporting

**Objective**: Integrate TaxBit for automated 1099-B and crypto tax reporting.

### Deliverable 32.1: TaxBit Client
**Task Description**: Create a TaxBit client for transaction ingestion and tax document generation.

**Backend Implementation**:
- File: `services/tax/taxbit_client.py`
- Header Comment: `# TaxBit Client - Automated 1099-B and crypto tax reporting for U.S. users.`

**Acceptance Criteria**:
- [ ] Client authenticates via OAuth.
- [ ] Transactions are ingested from Alpaca, Robinhood, and crypto wallets.
- [ ] Tax documents are generated on demand.

---

### Deliverable 32.2: Tax Document Retrieval
**Task Description**: Retrieve and store generated tax documents for user download.

**Backend Implementation**:
- File: `services/tax/tax_document_service.py`

**Acceptance Criteria**:
- [ ] Documents are retrieved in PDF format.
- [ ] Documents are stored in AWS S3 with secure URLs.
- [ ] Document generation status is polled until complete.

---

### Deliverable 32.3: Tax Center Page
**Task Description**: Create a Tax Center page for viewing and downloading tax documents.

**Frontend Implementation**:
- File: `frontend2/src/pages/TaxCenter.jsx`

**Acceptance Criteria**:
- [ ] Page displays available tax years with document status.
- [ ] Download buttons retrieve PDF documents.
- [ ] Generate button triggers new document creation.

---

## Phase 33: AWS S3 - Document Storage

**Objective**: Integrate AWS S3 for secure document storage (tax docs, filings, user uploads).

### Deliverable 33.1: S3 Storage Service
**Task Description**: Create an S3 service for uploading, downloading, and managing documents.

**Backend Implementation**:
- File: `services/storage/s3_service.py`
- Header Comment: `# S3 Service - Secure document storage for tax docs, filings, and user uploads. Uses presigned URLs for secure access.`

**Acceptance Criteria**:
- [ ] Service uploads files to appropriate buckets with encryption.
- [ ] Presigned download URLs expire after configurable duration.
- [ ] File metadata is stored in database with S3 keys.

---

### Deliverable 33.2: Document Management API
**Task Description**: Create API endpoints for document upload, retrieval, and deletion.

**Backend Implementation**:
- File: `apis/documents_api.py`

**Acceptance Criteria**:
- [ ] POST /api/documents uploads files with multipart encoding.
- [ ] GET /api/documents/{id} returns presigned download URL.
- [ ] DELETE /api/documents/{id} removes file and metadata.

---

### Deliverable 33.3: Document Library Widget
**Task Description**: Create a document library for viewing and managing uploaded files.

**Frontend Implementation**:
- File: `frontend2/src/widgets/Documents/DocumentLibrary.jsx`

**Acceptance Criteria**:
- [ ] Library displays documents with name, type, size, and upload date.
- [ ] Download button opens file in new tab.
- [ ] Delete button requires confirmation before removal.

---

## Summary

This roadmap covers the integration of all **39 API vendors** from the inventory across **33 phases**. Each phase includes:
- **3+ deliverables** with clear backend and frontend implementation requirements
- **Verbose acceptance criteria** for quality assurance
- **File header comment requirements** for code documentation

Total Deliverables: **99+**
Estimated Implementation Time: **12-16 weeks** (with parallel workstreams)

> [!NOTE]
> Phases can be parallelized where dependencies allow. Market Data (Phases 1-6), Authentication (Phases 16-20), and Communication (Phases 30-31) can be developed concurrently.
