# Services - Combined Documentation
Auto-generated on: Sat 02/07/2026 07:18 AM

---

## Source: service_accounting.md

# Backend Service: Accounting

## Overview
The **Accounting Service** is responsible for recording and tracking financial data related to asset valuations, specifically focusing on mark-to-model updates for illiquid assets. It provides a structured way to log manual or appraisal-based valuation updates, ensuring a clear audit trail for private asset performance.

## Components

### Private Valuation Log (`private_val.py`)
This component handles the logging of manual or appraisal-based valuation updates for assets that do not have real-time market pricing.

#### Classes

##### `PrivateValuationLog`
The main class used for logging valuation updates.

**Methods:**
- `record_update(asset_id: str, new_val: float, source: str) -> Dict[str, Any]`
    - **Purpose**: Records a new valuation update for a specific asset.
    - **Arguments**:
        - `asset_id`: The unique identifier of the asset.
        - `new_val`: The new valuation amount.
        - `source`: The source of the valuation (e.g., "Internal Appraisal", "External Auditor").
    - **Returns**: A dictionary containing the timestamp, asset ID, and the new valuation.
    - **Logging**: Outputs a `VAL_UPDATE` log message with the details.

## Dependencies
- `logging`: Standard Python logging for audit trails.
- `datetime`: Used for timestamping valuation updates.

## Usage Example
```python
from services.accounting.private_val import PrivateValuationLog

logger = PrivateValuationLog()
result = logger.record_update("PRO-REAL-ESTATE-01", 1250000.0, "Sotheby's Appraisal")
print(result)
```


---

## Source: service_admin.md

# Backend Service: Admin

## Overview
The **Admin Service** provides administrative and overarching control capabilities for the AI Investor platform. It includes high-level system monitoring through a "God Mode" dashboard and intelligent communication management via automated email triage.

## Components

### Command Center Service (`command_center_svc.py`)
This service acts as the backend for the platform's central command dashboard. It aggregates status reports and performance metrics from all 200 phases of the system.

#### Classes

##### `CommandCenterService`
A singleton service that provides a unified view of system health.

**Methods:**
- `get_system_status() -> Dict[str, Any]`
    - **Purpose**: Polls key subsystems (tax engine, risk engine, trading bots, etc.) for their current operational status.
    - **Returns**: A dictionary containing:
        - `orchestrator_status`: Current status of the master orchestrator.
        - `active_phases`: Number of active operational phases.
        - `global_risk_level`: Current system-wide risk assessment.
        - `subsystems`: Individual RAG (Red/Amber/Green) statuses for core engines.

---

### Inbox Service (`inbox_service.py`)
Part of the Phase 8 (Global HQ) implementation, this service handles the intelligent triage of the executive inbox to minimize noise and surface actionable communication.

#### Classes

##### `InboxService`
A singleton service that leverages Local LLMs for email classification.

**Methods:**
- `classify_email(subject: str, sender: str, snippet: str) -> Dict[str, Any]` (Async)
    - **Purpose**: Triages an incoming email into actionable categories.
    - **Arguments**:
        - `subject`: Email subject line.
        - `sender`: Sender's email address.
        - `snippet`: A short snippet of the email content.
    - **Logic**: Uses a local Llama3 model (via Ollama) to classify the email as `ACTIONABLE`, `PROMO`, or `NOISE`.
    - **Returns**: A JSON object containing the `classification`, the `reason` for the triage, and an `urgency` score (1-10).

## Dependencies
- `services.system.model_manager`: Used by `InboxService` to interact with local LLMs.
- `json` & `re`: Used for parsing LLM outputs.
- `logging`: Standard system logging.

## Usage Example

### Checking System Status
```python
from services.admin.command_center_svc import CommandCenterService

admin_svc = CommandCenterService()
status = admin_svc.get_system_status()
print(f"Global Risk: {status['global_risk_level']}")
```

### Triaging Emails
```python
from services.admin.inbox_service import get_inbox_service

inbox = get_inbox_service()
result = await inbox.classify_email(
    subject="Urgent: Margin Call on TSLA",
    sender="broker@example.com",
    snippet="TSLA has dropped below..."
)
print(f"Priority: {result['urgency']} | Action: {result['classification']}")
```


---

## Source: service_agents.md

# Backend Service: Agents

## Overview
The **Agents Service** is the brain of the AI Investor platform. it orchestrates a swarm of specialized AI agents, each with unique financial personas. The service handles multi-agent consensus, competitive debates between "Bull" and "Bear" perspectives, agent health monitoring, and critical security protocols to prevent rogue behavior.

## Core Components

### CIO Agent (`cio_agent.py`)
Represents the Chief Investment Officer persona for a Family Office.
- **Role**: Provides high-level portfolio oversight and high-fidelity investment recommendations.
- **Logic**: Analyzes portfolio weights and suggests rebalancing (e.g., reducing equity if >70%).

### Consensus Engine (`consensus_engine.py`)
A democratic decision-making layer for the agent swarm.
- **Purpose**: Ensures major decisions (e.g., large trades) are backed by a quorum of agents.
- **Mechanism**: Agents cast votes, and the engine calculates the approval rate against a configurable threshold (Default: 70%).

---

### Debate Ecosystem
Multi-agent competitive analysis to simulate deep market research.

#### Debate Chamber (`debate_chamber.py`)
Provides the analytical logic for weighing arguments.
- **Personas**: Includes `AGGRESSIVE_GROWTH`, `CONSERVATIVE_YIELD`, `MACRO_BEAR`, and `QUANT_ARBITRAGE`.
- **Logic**: Aggregates confidence scores for bullish vs. bearish arguments to reach a consensus verdict.

#### Debate Orchestrator (`debate_orchestrator.py`)
A singleton service that manages live debate sessions.
- **Features**: 
    - Handles turn-taking between participants like "The Bull", "The Bear", and "The Risk Manager". 
    - Maintains a transcript of the debate.
    - Allows human intervention (user arguments) to influence the AI debate.
    - Continuously recalculates sentiment scores based on recent turns.

---

### Operations & Security

#### Heartbeat Service (`heartbeat_service.py`)
A real-time monitoring system for the agent workforce.
- **Tracking**: Monitors heartbeats via Kafka to ensure agents are `ALIVE`.
- **Auto-Detection**: Automatically marks agents as `DEAD` if no heartbeat is received within 5 seconds.

#### Persona Rotator (`persona_rotator.py`)
Optimizes the agent workforce based on market conditions.
- **Logic**: Dynamically switches active personas based on the market regime (e.g., uses `SEARCHER` for Trending markets, `PROTECTOR` for High Volatility).

#### Rogue Killer (`rogue_killer.py`)
A critical security circuit breaker.
- **Function**: Monitors the "Trades Per Minute" (TPM) of every agent.
- **Trigger**: If an agent exceeds 100 TPM, it is flagged as a "Rogue Agent" and a `KILL` action is triggered to terminate the process immediately.

## Dependencies
- `services.system.model_manager`: Used for LLM-based agent responses.
- `asyncio`: Used for non-blocking heartbeat tracking.
- `datetime`: Used for session timing and heartbeat thresholds.

## Usage Example

### Orchestrating a Debate
```python
from services.agents.debate_orchestrator import DebateOrchestrator

orch = DebateOrchestrator()
session = orch.start_debate(ticker="NVDA")
print(f"Session {session['id']} started for {session['ticker']}")
```

### Checking Agent Health
```python
from services.agents.heartbeat_service import heartbeat_service

agents = await heartbeat_service.get_all_agents()
for agent in agents:
    status = "✅" if agent['is_alive'] else "❌"
    print(f"{status} Agent {agent['agent_id']} ({agent['status']})")
```


---

## Source: service_ai.md

# Backend Service: AI

## Overview
The **AI Service** is the core intelligence layer of the system. It abstracts multiple LLM providers (OpenAI, Anthropic, Google Gemini, Perplexity) and implements specialized financial analytical engines for sentiment analysis, market cycle classification, and executive briefing generation.

## LLM Gateway Clients
The service provides a unified interface to various state-of-the-art AI models, with built-in mock modes for development.

### OpenAI Client (`openai_client.py`)
- **Role**: Primary client for GPT-4o and embeddings.
- **Features**: Supports streaming, function calling, and token usage tracking.
- **Consumer**: `AutocoderAgent`, `CommandProcessor`.

### Anthropic Client (`anthropic_client.py`)
- **Role**: Client for Claude.
- **Features**: Specifically optimized for generating multi-persona responses in "Bull vs. Bear" debates.
- **Consumer**: `DebateChamberAgent`.

### Gemini Client (`gemini_client.py`)
- **Role**: Client for Google Gemini.
- **Features**: Focused on generating structured morning briefings and synthesizing market data.
- **Consumer**: `BriefingGenerator`.

### Perplexity Client (`perplexity_client.py`)
- **Role**: Real-time research client (Sonar models).
- **Features**: Provides citation-backed market research answers with verified news links.
- **Consumer**: `ResearchAgent`.

---

## Analytical Engines

### Business Cycle Classifier (`cycle_classifier.py`)
- **Purpose**: Classifies the current macroeconomic phase.
- **Inputs**: PMI, Yield Curve (10Y-2Y), CPI rate of change.
- **Phases**: CONTRACTION (Recession Risk), EXPANSION (Late Cycle), RECOVERY.

### Sentiment & Emotion Detection
- **Emotion Detector (`emotion_detector.py`)**: Identifies high-risk trading patterns based on keywords (e.g., "yolo", "revenge").
- **FinBERT Service (`finbert.py`)**: Uses a financial transformer model to classify headlines as Positive, Negative, or Neutral.
- **Sentiment Engine (`sentiment_engine.py`)**: Detects emotional "tilt" and irrationality in user commands.

### Executive & Strategic Intelligence
- **Master Objective Optimizer (`master_objective.py`)**: The system's ultimate utility function. Calculates **Return on Lifestyle (ROL)** and enforces survival constraints (e.g., Value at Risk < 25%).
- **Briefing Generator (`briefing_generator.py`)**: Orchestrates the assembly of daily market reports by synthesizing data through Gemini.
- **Exec Summary Service (`exec_summary.py`)**: Provides concise, voice-ready status briefings on portfolio and market status.

## Usage Examples

### Generating a Market Briefing
```python
from services.ai.briefing_generator import get_briefing_generator

generator = get_briefing_generator()
briefing = await generator.get_daily_briefing()
print(f"Market Outlook: {briefing['market_outlook']}")
```

### Checking Survival Constraints
```python
from services.ai.master_objective import MasterObjectiveOptimizer

ghost = MasterObjectiveOptimizer()
is_safe = ghost.check_survival_constraint(liquidity_ratio=0.15, value_at_risk=0.12)
if not is_safe:
    print("WARNING: Survival constraint violated!")
```


---

## Source: service_ai_assistant.md

# Backend Service: AI Assistant

## Overview
The **AI Assistant Service** provides a conversational interface for users to interact with the AI Investor platform. It combines natural language understanding with a personalized learning system to offer context-aware advice, answer investment questions, and adapt to individual user preferences over time.

## Core Components

### Assistant Service (`assistant_service.py`)
The primary orchestrator for user-AI conversations.
- **Role**: Manages the lifecycle of a conversation and coordinates with the LLM and the learning engine.
- **Key Features**:
    - **Session Management**: Creates and stores unique conversation IDs.
    - **Context Aggregation**: Pulls user preferences and portfolio data to ground the AI's responses.
    - **Interaction Loop**: processes incoming user messages and generates structured AI responses.

### Learning Service (`learning_service.py`)
The personalization and recommendation engine.
- **Role**: Tracks user behavior and preferences to ensure the assistant becomes more relevant over time.
- **Key Features**:
    - **Preference Tracking**: Learns and stores investment parameters like risk tolerance and style (e.g., Growth vs. Value).
    - **Recommendation Engine**: Generates proactive investment suggestions (e.g., "Consider diversifying your portfolio") based on user state and preferences.
    - **Interactive Learning**: Analyzes conversation transcripts to refine its understanding of the user.

## Dependencies
- `services.ai`: Used for the underlying LLM completions.
- `services.system.cache_service`: Used for fast retrieval of conversation history and learned preferences.
- `schemas.ai_assistant`: Defines the data models for conversations and messages.

## Usage Example

### Starting a Conversation
```python
from services.ai_assistant.assistant_service import get_assistant_service

assistant = get_assistant_service()
conv = await assistant.create_conversation(user_id="USR-001", title="Retirement Planning")
print(f"Conversation {conv.conversation_id} created.")
```

### Getting Recommendations
```python
from services.ai_assistant.learning_service import get_learning_service

learning = get_learning_service()
recs = await learning.get_recommendations(user_id="USR-001")
for r in recs:
    print(f"Suggestion [{r.confidence*100}% Confidence]: {r.title} - {r.description}")
```


---

## Source: service_ai_predictions.md

# Backend Service: AI Predictions

## Overview
The **AI Predictions Service** is the quantitative forecasting arm of the AI Investor platform. It provides advanced analytics to detect market regimes, analyze the sentiment impact of news, and generate high-fidelity price and trend forecasts across various time horizons.

## Core Components

### AI Analytics Service (`ai_analytics_service.py`)
Provides high-level qualitative and contextual market analysis.
- **Role**: Combines news sentiment with price data to detect secondary effects and market cycles.
- **Key Features**:
    - **Sentiment Analysis**: Evaluates raw text to produce structured sentiment scores (Positive/Negative/Neutral).
    - **Market Regime Detection**: Classifies the overall market state (e.g., Bull, Bear, Sideways) and calculates detection confidence.
    - **News Impact Prediction**: Calculates the expected price change (%) and volatility impact driven by specific news events or social trends.

### Prediction Engine (`prediction_engine.py`)
The quantitative core responsible for numerical forecasting.
- **Role**: Uses historical data and ML models to project future asset performance.
- **Key Features**:
    - **Price Forecasting**: Predicts future price points for specific symbols across horizons (1d, 1w, 1m, 3m, 1y).
    - **Confidence Intervals**: Calculates lower and upper bounds for predictions based on historical volatility and model uncertainty.
    - **Trend Prediction**: Determines the overal direction (Bullish/Bearish) and strength of a price movement without necessarily predicting an exact price.
    - **Caching Layer**: Integrates with the system cache to serve repeated prediction requests instantly while maintaining freshness via TTL.

## Dependencies
- `numpy`: Used for numerical operations and interval calculations.
- `services.system.cache_service`: For result persistence and low-latency retrieval.
- `schemas.ai_predictions`: Defines models for `PricePrediction`, `TrendPrediction`, and `MarketRegime`.

## Usage Example

### Predicting Asset Price
```python
from services.ai_predictions.prediction_engine import get_prediction_engine

engine = get_prediction_engine()
pred = await engine.predict_price(symbol="AAPL", time_horizon="1m")
print(f"Predicted AAPL Price: ${pred.predicted_price:.2f}")
print(f"Range: ${pred.confidence_interval['lower']:.2f} - ${pred.confidence_interval['upper']:.2f}")
```

### Detecting Market Regime
```python
from services.ai_predictions.ai_analytics_service import get_ai_analytics_service

analytics = get_ai_analytics_service()
regime = await analytics.detect_market_regime(market_index="SPY")
print(f"Current Regime: {regime.regime_type} ({regime.confidence*100}% Confidence)")
```


---

## Source: service_alerts.md

# Backend Service: Alerts

## Overview
The **Alerts Service** provides a diverse range of monitoring and notification capabilities designed to flag critical risks and high-conviction signals. It covers multiple domains including geopolitical exposure, demographic shifts in macroeconomic data, personal liquidity thresholds, and anomalies in institutional trading prints.

## Monitoring Components

### Financial & Market Alerts

#### High Conviction Insider Alert (`high_conviction.py`)
- **Purpose**: Filters market data for significant insider activity.
- **Threshold**: Only flags purchases greater than or equal to **$500,000**.
- **Usage**: Surfaces high-fidelity signals that suggest strong management confidence in a company's future.

#### Factor Decay Monitor (`factor_decay.py`)
- **Purpose**: Detects if historically successful investment factors (e.g., Value, Momentum) are experiencing structural breaks.
- **Logic**: Alerts when the rolling 10-year return of a factor turns negative, suggesting the premium may have disappeared or "decayed."

#### Signature Print Alert (`signature_print.py`)
- **Purpose**: Detects out-of-sequence trade prints ("Z" or "T" codes) which often signal significant institutional intent or late-reporting of large blocks.

---

### Risk Exposure Alerts

#### Conflict Zone Detector (`conflict_zone.py`)
- **Purpose**: Identifies exposure to global geopolitical hotzones in a company's supply chain.
- **Example**: Flags "CRITICAL" risk for tickers like TSM if tensions escalate in the Taiwan Strait.

#### Demographic Risk Monitor (`demographic_risk.py`)
- **Purpose**: Tracks the "Ticking Time Bomb" of 401k net outflows.
- **Logic**: Alerts when Boomer withdrawals exceed Gen Z contributions at a national or fund level, signaling a potential structural headwind for passive index flows.
- **Recommendation**: Suggests hedging passive exposure when flows turn negative.

---

### Personal Liquidity Alerts

#### Emergency Fund Alert Service (`emergency_fund_alerts.py`)
- **Purpose**: A tiered monitoring system for personal cash reserves.
- **Tiers**:
    - **CRITICAL (0-3 months)**: Blocks trades and sends urgent SMS/Email alerts.
    - **LOW (3-6 months)**: Warning status.
    - **ADEQUATE (6-12 months)**: Normal operations.
    - **STRONG/FORTRESS (12+ months)**: High liquidity security.

## Dependencies
- `logging`: Used for `ALERT_LOG` and `ALERT_EVAL` audit trails.
- `datetime`: Used for time-stamped status calculations.

## Usage Example

### Evaluating Emergency Coverage
```python
from services.alerts.emergency_fund_alerts import EmergencyFundAlertService

service = EmergencyFundAlertService()
eval = service.evaluate_coverage(months=2.5)

if eval['action_required']:
    print(f"TRADING LOCKED: {eval['message']}")
```

### Checking Geopolitical Risk
```python
from services.alerts.conflict_zone import ConflictDetector

detector = ConflictDetector()
risk = detector.check_exposure("TSM", ["TAIWAN_STRAIT"])
print(f"Risk Level: {risk['risk']}")
```


---

## Source: service_alternative.md

# Backend Service: Alternative

## Overview
The **Alternative Assets Service** specializes in mapping liquidity and valuation dynamics within the Private Equity (PE) secondary markets. It provides tools for investors to evaluate "Discount to NAV" opportunities and track critical fund exit windows.

## Core Components

### PE Secondary Service (`pe_secondary_service.py`)
This component models the secondary market for private equity interests, focusing on arbitrage opportunities and redemption logistics.

#### Classes

##### `PESecondaryService`
Handles the quantitative analysis of secondary market listings and LP (Limited Partner) obligations.

**Methods:**
- `calculate_nav_discount(reported_nav: Decimal, secondary_ask: Decimal) -> Dict[str, Any]`
    - **Purpose**: Calculates the percentage discount of a secondary market ask price relative to the fund's reported Net Asset Value (NAV).
    - **Logic**: Flags any discount greater than 30% as a "HIGH" opportunity rank.
    - **Returns**: A breakdown of the NAV, Ask, and calculated discount percentage.
- `track_redemption_window(fund_id: str, lockup_expiry: str) -> Dict[str, Any]`
    - **Purpose**: Tracks the time remaining until a fund's lockup period expires.
    - **Usage**: Essential for liquidity planning and identifying when LPs may be susceptible to "forced-seller" dynamics.

## Dependencies
- `decimal`: Used for high-precision financial calculations.
- `logging`: Records secondary market transactions and timer events.

## Usage Example

### Evaluating a Secondary Listing
```python
from decimal import Decimal
from services.alternative.pe_secondary_service import PESecondaryService

pe_svc = PESecondaryService()
result = pe_svc.calculate_nav_discount(
    reported_nav=Decimal("1000000.00"), 
    secondary_ask=Decimal("650000.00")
)

print(f"Opportunity: {result['opportunity_rank']} ({result['discount_pct']}% Discount)")
```


---

## Source: service_alts.md

# Backend Service: Alts (Physical Assets)

## Overview
The **Alts Service** (Alternative Assets) focuses on the "Negative Carry" and maintenance costs associated with physical alternative investments such as Art, Luxury Watches, Fine Wine, and self-custodied Crypto hardware.

## Core Components

### Alts Cost Tracker (`cost_tracker.py`)
This component tracks the ongoing expenses required to maintain and insure high-value physical assets.

#### Classes

##### `AltsCostTracker`
Calculates insurance premiums and storage fees based on asset type and current market value.

**Methods:**
- `calculate_annual_maintenance(asset_id: str, value: float, asset_type: str) -> Dict[str, Any]`
    - **Purpose**: Determines the total annual "Carry Cost" for a physical asset.
    - **Insurance logic**:
        - **ART**: 1% of value.
        - **WATCH**: 0.8% of value.
        - **WINE**: 0.5% of value.
        - **CRYPTO_HW**: 2% of value (due to elevated security risks).
    - **Storage logic**: Simulations incorporate flat monthly fees (e.g., $100/mo) for specialized vaulting.
    - **Returns**: A detailed breakdown of insurance, storage, and total carry as a percentage of asset value.

## Dependencies
- `decimal`: Ensures precision in cost aggregation.
- `logging`: Tracks maintenance audits and carry-cost updates.

## Usage Example

### Calculating Carry Cost for a Watch
```python
from services.alts.cost_tracker import AltsCostTracker

tracker = AltsCostTracker()
report = tracker.calculate_annual_maintenance(
    asset_id="PATEK-5711", 
    value=150000.0, 
    asset_type="WATCH"
)

print(f"Total Negative Carry: ${report['total_carry_cost']:,.2f}")
print(f"Annual Carry %: {report['carry_pct']}%")
```


---

## Source: service_analysis.md

# Backend Service: Analysis

## Overview
The **Analysis Service** is the most extensive component of the AI Investor platform, containing 84 specialized modules for financial modeling, market research, and performance evaluation. It provides the analytical backbone for the system's decision-making across all asset classes.

## Primary Analytical Pillars

### 1. Performance Attribution & Evaluation
This pillar decomposes portfolio performance to identify the true sources of alpha (manager skill) versus beta (market exposure).
- **Attribution Service (`attribution_service.py`)**: Implements the **Brinson-Fachler model** to decompose active returns into Allocation, Selection, and Interaction effects. It supports GICS sector-level benchmarking against the S&P 500 and NASDAQ.
- **Alpha Attributor (`alpha_attributor.py`)**: Specifically calculates non-market-related excess returns.
- **Manager Ranker (`manager_ranker.py`)**: Quantitatively ranks internal agent performance.

### 2. Backtesting & Monte Carlo Simulation
Provides rigorous testing for trading strategies before they are deployed in live or demo environments.
- **Backtest Engine (`backtest_engine.py`)**: The core execution engine for historical simulations.
- **Monte Carlo Service (`monte_carlo_service.py`)**: Implements **Geometric Brownian Motion (GBM)** simulations to calculate ruin probability, max drawdowns, and "Pain Index" metrics. It features "Hype-Adjusted Drift" to simulate the impact of social media trends on asset paths.
- **Genetic Distillery (`genetic_distillery.py`)**: Uses evolutionary algorithms to optimize strategy parameters and prevent over-fitting.

### 3. Macro & Economic Analysis
Aggregates global data to detect business cycle shifts and geopolitical risks.
- **Macro Service (`macro_service.py`)**: Integrates with **FRED (Federal Reserve Economic Data)** to fetch real-time CPI, GDP, and unemployment metrics for world-map visualization.
- **Global M2 Tracker (`global_m2.py`)**: Monitors global money supply liquidity.
- **OPEC Compliance (`opec_compliance.py`)**: Tracks commodity-specific political risks in the energy sector.

### 4. Quantitative Metrics & Modeling
Mathematical models for structural market analysis.
- **Factor Service (`factor_service.py`)**: Decomposes returns into known factors like Value, Momentum, and Size.
- **FFT & HMM Engines (`fft_engine.py`, `hmm_engine.py`)**: Uses Fast Fourier Transforms and Hidden Markov Models to detect cyclicality and market regime shifts.
- **GEX & Zero Gamma (`gex_calc.py`, `zero_gamma.py`)**: Calculates Gamma Exposure and option-driven market structure levels.

### 5. Sentiment & "Political Alpha"
Alternative data sources that provide an edge through non-traditional information flow.
- **Congress Tracker (`congress_tracker.py`)**: Correlates congressional stock disclosures with lobbying activity to generate a **Political Alpha Signal**.
- **YouTube & TikTok Analyzers (`youtube_transcript_analyzer.py`)**: Extracts sentiment and trend data from social media transcripts.
- **Earnings Sentiment (`earnings_sentiment.py`)**: Analyzes transcript sentiment from corporate earnings calls.

### 6. Technical Analysis & Structure
- **Technical Analysis Service (`technical_analysis_service.py`)**: Provides **50+ technical indicators** (RSI, MACD, Bollinger Bands, ATR, etc.) and pattern recognition logic (Flags, Triangles, Head & Shoulders).
- **Supply/Demand Zones (`supply_demand_zones.py`)**: Automatically identifies institutional "Order Blocks" and structural accumulation/distribution levels.

## Dependencies
- `pandas` & `numpy`: Core data manipulation.
- `random` & `math`: Statistical simulations.
- `services.data.fred_service`: External economic data provider.
- `services.system.api_governance`: Resource rate-limiting for data providers.

## Usage Examples

### Running a Monte Carlo GBM Simulation
```python
from services.analysis.monte_carlo_service import get_monte_carlo_service

mc = get_monte_carlo_service()
result = mc.run_gbm_simulation(initial_value=100000, ticker="SPY", days=30)

print(f"Ruin Probability: {result.ruin_probability:.2%}")
print(f"Expected Final Value: ${result.mean_final:,.2f}")
```

### Calculating Portfolio Attribution
```python
from services.analysis.attribution_service import AttributionService, DateRange

attr = AttributionService()
period = DateRange(start="2025-01-01", end="2025-12-31")
report = await attr.calculate_brinson_attribution("my-portfolio", "sp500", period)

print(f"Total Active Return: {report.total_active_return} bps")
print(f"Selection Effect: {report.total_selection_effect} bps")
```


---

## Source: service_analytics.md

# Backend Service: Analytics

## Overview
The **Analytics Service** is responsible for deep-dive quantitative analysis of portfolio performance and risk. It transforms raw holding and trade data into actionable insights through sophisticated attribution models, risk decomposition frameworks, and secure performance reporting.

## Core Engines

### 1. Performance Attribution Engine (`performance_attribution_service.py`)
This engine decomposes portfolio returns to identify whether gains were driven by market timing (allocation) or asset selection.
- **Methodology**: 
    - **Modified Dietz**: Calculates time-weighted returns.
    - **Brinson-Fachler Model**: Decomposes active returns into Allocation, Selection, and Interaction effects.
- **Features**:
    - **Benchmark Comparison**: Real-time relative performance against indices like SPY or QQQ.
    - **Hierarchical Drill-down**: Analyze performance by Asset Class, Sector, Geography, or individual Holding.
    - **Contribution Analysis**: Ranks every position by its absolute and percentage contribution to the total P&L.

### 2. Risk Decomposition Engine (`risk_decomposition_service.py`)
Provides a multi-dimensional view of portfolio volatility and the potential for extreme losses.
- **Methodology**:
    - **Factor Models**: Decomposes risk into Fama-French factors (Market, Size, Value, Momentum, Quality).
    - **Concentration Analysis**: Calculates the **Herfindahl-Hirschman Index (HHI)** to detect over-concentration in specific holdings or sectors.
    - **Tail Risk**: Computes **Value at Risk (VaR)** and **Conditional Value at Risk (CVaR)** using historical simulations.
- **Features**:
    - **Correlation Matrix**: Analyzes inter-holding relationships to determine diversification ratios.
    - **Marginal Risk Contribution**: Identifies which specific assets are adding the most to the portfolio's overall volatility profile.

### 3. Alpha Reporting Service (`alpha_reporting.py`)
Generates secure, high-integrity performance summaries for audit and review.
- **Role**: Synthesizes the output of the attribution and risk engines into summarized EOD (End-of-Day) reports.
- **Security**: Features a **Sovereign PGP-simulated encryption layer** (using Fernet) to ensure performance data is secured before transmission or storage.
- **Metrics**: Highlights "MVP Agents" and "Laggard Sectors" to provide a quick executive snapshot.

## Dependencies
- `pandas` & `numpy`: Heavy-duty numerical processing.
- `scipy.stats`: Used for VaR/CVaR and normalized risk distributions.
- `cryptography`: Powers the secure reporting encryption layer.
- `services.portfolio.portfolio_aggregator`: Source of truth for holdings and weights.

## Usage Examples

### Running Risk Decomposition
```python
from services.analytics.risk_decomposition_service import get_risk_decomposition_service

risk_svc = get_risk_decomposition_service()
analysis = await risk_svc.calculate_concentration_risk(portfolio_id="user_77")

print(f"Holding Concentration (HHI): {analysis.by_holding.herfindahl_hirschman_index:.4f}")
print(f"Top 5 Concentration: {analysis.by_holding.top_5_concentration:.2%}")
```

### Generating a Secure Alpha Report
```python
from services.analytics.alpha_reporting import get_alpha_reporting_service

reporter = get_alpha_reporting_service()
report = reporter.generate_eod_report(encrypt=True)

print(f"Secure Report Generated. Checksum: {report['checksum']}")
# Payload is encrypted string: report['payload']
```


---

## Source: service_architect.md

# Backend Service: Architect

## Overview
The **Architect Service** is responsible for long-term strategic wealth modeling. It provides the "Financial Fortress" logic used to project net worth over several decades, adjusting for inflation, taxes, and lifestyle changes to determine critical milestones such as the **Year of Financial Independence (FI Year)**.

## Core Components

### Life-Cycle Service (`life_cycle_service.py`)
This component simulates the long-term architectural health of a user's financial life.

#### Classes

##### `LifeCycleService`
A high-performance simulator designed to project financial trajectories over a 50-year horizon.

**Methods:**
- `run_simulation(current_nw, monthly_savings, monthly_burn, expected_return, inflation, horizon_years, current_age) -> ProjectionResult`
    - **Purpose**: Runs a deterministic simulation of wealth accumulation and depletion.
    - **Logic**:
        - **4% Rule Integration**: Automatically calculates the FI Year when 4% of net worth exceeds annual spending.
        - **Inflation Adjustments**: Dynamically scales the "burn rate" (spending) each year to account for purchasing power decay.
        - **Performance**: Guaranteed execution time of under 1 second for instant UI responsiveness.
    - **Returns**: A `ProjectionResult` containing year-by-year paths for net worth, real spending, and critical age/year milestones.

## Dependencies
- `math`: Used for compound growth and exponential spending calculations.
- `dataclasses`: Defines the structured `ProjectionResult` output.

## Usage Example

### Calculating Financial Independence
```python
from services.architect.life_cycle_service import get_lifecycle_service

architect = get_lifecycle_service()
result = architect.run_simulation(
    current_nw=500000.0,
    monthly_savings=5000.0,
    monthly_burn=4000.0,
    expected_return=0.08,
    inflation=0.03,
    current_age=35
)

if result.fi_year:
    print(f"Projected FI Year: {result.fi_year} (Age: {result.fi_age})")
    print(f"Final Net Worth (Year 50): ${result.net_worth[-1]:,.2f}")
else:
    print("FI not achieved within the 50-year horizon.")
```


---

## Source: service_audit.md

# Backend Service: Audit

## Overview
The **Audit Service** provides high-integrity "Forensic Vault" capabilities designed for institutional-grade post-incident analysis. It is triggered during extreme ("nuclear-level") market risk events to capture full-state snapshots of the environment, system health, and agent activity.

## Core Components

### Forensic Vault (`forensic_vault.py`)
A specialized recorder for documenting critical system failure or extreme market drawdowns.

#### Classes

##### `ForensicVault`
Acts as a cold-storage auditor for preserving evidence and data during high-volatility regimes.

**Methods:**
- `capture_incident(symbol: str, drawdown: float, market_context: Dict[str, Any])`
    - **Purpose**: Packages the current system state, asset performance, and drawdown metrics into an immutable forensic record.
    - **Logic**: Logs a `CRITICAL` severity event and prepares a data package for permanent preservation.
    - **Returns**: A structured "incident package" containing timestamps, severity levels, and market snapshots.
- `get_market_context() -> Dict[str, Any]`
    - **Purpose**: Gathers a multi-layered snapshot of market conditions (VIX levels, asset correlations, active agent list) to provide context for the audit.

## Dependencies
- `logging`: Uses `logger.critical` for immediate visibility of forensic capture events.
- `datetime`: Provides high-resolution ISO timestamps for audit trails.

## Usage Example

### Manually Recording a Risk Incident
```python
from services.audit.forensic_vault import ForensicVault

vault = ForensicVault()
context = vault.get_market_context()

# Simulated extreme drawdown event on ETH
incident = vault.capture_incident(
    symbol="ETH", 
    drawdown=0.25, 
    market_context=context
)

print(f"Incident recorded: {incident['timestamp']} | Severity: {incident['severity']}")
```


---

## Source: service_auth.md

# Backend Service: Auth

## Overview
The **Auth Service** provides a multi-layered security architecture designed for the high-stakes environment of a personal financial OS. It combines biometric non-repudiation via WebAuthn, multi-tenant isolation for privacy, and unique legacy-planning features like the "Dead Man's Switch."

## Core Security Pillars

### 1. Sovereign Auth Gateway (`sovereign_auth_service.py`)
This is the "Sovereign Kernel" of the system.
- **Role**: All "write-level" API actions (trades, transfers, config edits) require a valid cryptographic signature.
- **Mechanism**: Implements a **WebAuthn challenge-response cycle**.
    - **Command Binding**: Every challenge is cryptographically bound to the hash of the specific command payload, ensuring users sign exactly what is executed.
    - **Single-Use**: Challenges are consumed immediately or expire after 120 seconds to prevent replay attacks.
- **Latency**: Performance is optimized for <300ms total loop budget.

### 2. Multi-Tenant Isolation (`tenant_manager.py`)
Ensures strict data privacy between different family offices or sub-entities using the platform.
- **Role**: The "Landlord" component that manages tenant-specific schemas (e.g., `tenant_alpha`).
- **RBAC**: Implements Role-Based Access Control with standard roles: `admin`, `trader`, and `viewer`.

### 3. Inheritance & Dead Man's Switch (`inheritance_service.py`)
A critical feature for long-term wealth preservation and continuity.
- **Role**: Monitors tenant activity heartbeats.
- **Logic**: If no activity is detected for a configurable threshold (default: 30 days), the **Sovereign Inheritance Protocol** is triggered.
- **Action**: Automatically executes asset transfer logic to pre-configured heir wallets or distributes encrypted access keys.

### 4. MFA & Identity Integration
- **MFA Service (`mfa_service.py`)**: standard TOTP (Time-based One-Time Password) support using `pyotp` for secondary verification of critical overrides.
- **Social Connectors**: Provides legacy OAuth2 integrations for **Google**, **Facebook**, and **Reddit** for initial onboarding or low-stakes utility.

## Dependencies
- `pyotp`: Powers the MFA TOTP logic.
- `cryptography`: Provides secure hashing and challenge generation.
- `utils.database_manager`: Used by the Inheritance service to persist heartbeat data in PostgreSQL.

## Usage Examples

### Generating a Sovereign Challenge for a Trade
```python
from services.auth.sovereign_auth_service import sovereign_auth_service

# Define the command intent
trade_payload = {"action": "BUY", "symbol": "BTC", "amount": 0.5}

# Generate challenge bound to this specific move
challenge = sovereign_auth_service.generate_challenge(trade_payload)
print(f"Generated Challenge: {challenge['challenge_id']} (Expires in {challenge['expires_in_seconds']}s)")
```

### Recording a User Heartbeat
```python
from services.auth.inheritance_service import inheritance_service

# Call this on every dashboard load or critical action
inheritance_service.record_heartbeat(tenant_id="family_alpha")
```


---

## Source: service_backtest.md

# Backend Service: Backtest

## Overview
The **Backtest Service** is a high-performance simulation engine designed to validate trading strategies against historical data. Built on top of the **Polars** library, it leverages vectorized, columnar operations to achieve sub-second execution speeds, even when processing decade-long datasets of 1-minute intervals.

## Core Components

### Polars Backtest Engine (`polars_backtest_engine.py`)
The primary engine for strategy simulation and performance metric calculation.

#### Classes

##### `PolarsBacktestEngine`
A singleton service that manages the execution of various quantitative strategies.

**Supported Strategies:**
- **SMA Crossover**: A classic trend-following strategy using fast and slow Simple Moving Averages.
- **Momentum Strategy**: Captures gains by following existing market trends based on lookback and holding periods.
- **Mean Reversion**: Uses Z-score thresholds to identify overextended price movements for potential reversals.

**Key Features:**
- **Vectorized Calculations**: Uses Polars rolling windows and columnar transformations to eliminate slow row-by-row iteration.
- **Memory Efficiency**: Ensures large data frames are discarded immediately after calculation to prevent memory bloat during batch simulations.
- **Performance**: Capable of executing a 10-year SMA crossover on 1-minute data in less than 2 seconds.

#### Data Models

##### `BacktestConfig`
Defines the parameters for a simulation run:
- `ticker`: The asset symbol.
- `initial_capital`: Starting bankroll (default: $100,000).
- `commission` & `slippage`: Friction modeling for realistic results.

##### `BacktestMetrics`
The structured output of a backtest, including:
- `total_return_pct` & `annualized_return_pct`.
- `sharpe_ratio`: Risk-adjusted return metric.
- `max_drawdown_pct`: Measures the largest peak-to-trough decline.
- `win_rate` & `profit_factor`.
- `execution_time_ms`: Engine performance measurement.

## Dependencies
- `polars`: The core high-performance data processing engine.
- `dataclasses`: Used for structured configuration and result objects.

## Usage Example

### Running a Fast SMA Crossover Backtest
```python
from services.backtest.polars_backtest_engine import get_backtest_engine, BacktestConfig

engine = get_backtest_engine()

config = BacktestConfig(
    strategy_name="QuickSMA",
    ticker="TSLA",
    start_date="2020-01-01",
    end_date="2024-12-31"
)

# Run the vectorized crossover
metrics = engine.run_sma_crossover(
    config=config,
    fast_period=20,
    slow_period=100
)

print(f"Total Return: {metrics.total_return_pct:.2f}%")
print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
print(f"Simulation completed in {metrics.execution_time_ms:.1f}ms")
```


---

## Source: service_banking.md

# Backend Service: Banking

## Overview
The **Banking Service** serves as the bridge between the Sovereign OS and traditional financial institutions. It enables secure capital onboarding, real-time balance monitoring, and automated cash management workflows such as reconciliation and liquidity sweeps.

## Core Components

### 1. Plaid Integration (`plaid_service.py`, `banking_service.py`)
The primary gateway for connecting to legacy bank accounts.
- **Plaid Service**:
    - **Account Linking**: Generates Link Tokens and exchanges Public Tokens for persistent Access Tokens.
    - **Balance Verification**: Provides real-time "current" and "available" balance checks with a built-in **Rate Limiter** (e.g., 3 checks per hour per user).
    - **Overdraft Protection**: Proactively checks for sufficient funds before triggering funding events.
- **Banking Service Wrapper**: Provides a "Simulation Mode" for developers, allowing the platform to function without active Plaid credentials by using mock data.

### 2. Reconciliation Engine (`reconciliation_service.py`)
Ensures internal accounting matches external truth.
- **Role**: Automatically matches bank transactions with internal system ledger entries.
- **Fuzzy Matching Logic**: Uses a multi-factor matching algorithm:
    - **Amount**: Exact numerical match.
    - **Date**: Matches within a configurable window (e.g., +/- 2 days).
    - **Description**: Uses string similarity (starts-with/contains) to associate bank descriptions (e.g., "Starbucks Coffee") with ledger notes (e.g., "Starbucks NYC").

### 3. Treasury & Cash Flow Management (`treasury_service.py`)
Automates the optimization of liquid capital.
- **Automated Cash Sweeps**: Implements the **"Financial Fortress" threshold logic**. If a checking account balance exceeds a pre-set limit (e.g., $5,000), the excess is automatically "swept" into a higher-yield savings account or emergency fund.
- **Bill OCR Processing**: Features a specialized parser for extracting "Amount Due" and "Due Date" from bill/invoice text, preparing them for automated payment workflows.

## Dependencies
- `plaid-python`: The official SDK for bank connectivity.
- `pyotp`: Used for MFA during sensitive banking operations.
- `pydantic`: Defines structured data models for transactions and accounts.

## Usage Examples

### Initializing a Plaid Link
```python
from services.banking.banking_service import get_banking_service

banking = get_banking_service()
link_token = banking.create_link_token(user_id="user_vanguard_1")

# Frontend will use this token to open the Plaid UI
print(f"Plaid Link Token: {link_token}")
```

### Executing an Automated Cash Sweep
```python
from services.banking.treasury_service import get_treasury_service

treasury = get_treasury_service()
treasury.sync_accounts()

# Sweep any excess above $5000 from primary checking
sweeps = treasury.execute_cash_sweep(threshold=5000.0)

for s in sweeps:
    print(f"Swept ${s['amount']} from {s['source']} to {s['destination']}")
```


---

## Source: service_billing.md

# Backend Service: Billing

## Overview
The **Billing Service** manages all financial obligations within the platform, including consumer bill tracking and institutional-grade fee calculations. It features complex logic for AUM-based tiered fees and performance-driven "Carried Interest," ensuring transparent and fair billing through mechanisms like High-Water Marks and Hurdle Rates.

## Core Components

### 1. Consumer Bill Management (`bill_payment_service.py`)
Provides the infrastructure for users to track and pay external bills.
- **Features**:
    - **Bill Lifecycle**: Supports transitioning bills from `PENDING` to `SCHEDULED` and `PAID`.
    - **Recurrence**: Manages one-time or recurring (monthly, annual) payments.
    - **Scheduling**: Integrates with the `BankingService` to execute transfers on specific dates.
    - **History**: Maintains a permanent record of all payments for audit purposes.

### 2. Institutional Fee Engines
These components automate the billing logic for wealth managers and family offices.
- **Tiered Fee Calculator (`tiered_fee_calc.py`)**: 
    - Implements a **declining-balance schedule**. 
    - Automatically applies different rates to different "tiers" of AUM (e.g., 1.0% on the first $1M, 0.75% on the next $4M, etc.).
- **Carry Engine (`carry_calculator.py`)**: 
    - Calculates **Performance Fees** (typically 20%) on trading profits.
    - **Hurdle Rate**: Ensures a minimum return (e.g., 5% "risk-free" hurdle) is met before any fees accrue.
    - **High-Water Mark (HWM)**: Ensures fees are only charged on *new* gains. If a portfolio loses value, no performance fees are paid until the original peak value is recovered.

### 3. Utility Services
- **Proration Service (`proration_service.py`)**: Calculates partial-month fees for mid-cycle capital additions or withdrawals.
- **Payment Reminders (`payment_reminder_service.py`)**: Handles the generation of notifications for upcoming or overdue bills.

## Dependencies
- `decimal`: Used for all fee calculations to avoid floating-point rounding errors.
- `services.system.cache_service`: For rapid retrieval of bill and payment states.
- `schemas.billing` & `schemas.fee_billing`: Structured pydantic models for fee schedules and bill objects.

## Usage Examples

### Calculating an Annual AUM Fee
```python
from services.billing.tiered_fee_calc import TieredFeeCalculator
from schemas.fee_billing import FeeSchedule

calc = TieredFeeCalculator()
schedule = FeeSchedule(
    tier_1_max=1000000, tier_1_rate=0.01,
    tier_2_max=5000000, tier_2_rate=0.0075,
    tier_3_rate=0.005
)

fee = calc.calculate_annual_fee(aum=7500000, schedule=schedule)
print(f"Annual Billing Amount: ${fee:,.2f}")
```

### Accruing Performance Fees (Carry)
```python
from services.billing.carry_calculator import CarryEngine
from decimal import Decimal

engine = CarryEngine()
report = engine.calculate_performance_fee(
    current_nav=Decimal('1200000.00'),
    previous_peak_nav=Decimal('1100000.00'),
    opening_nav=Decimal('1000000.00'),
    hurdle_rate=Decimal('0.05')
)

if report['status'] == "ACRUED":
    print(f"Accrued Fee: ${report['fee_amount']:,.2f} on {report['basis_alpha']:,.2f} of alpha.")
```


---

## Source: service_bio.md

# Backend Service: Bio

## Overview
The **Bio Service** is a unique component of the Sovereign OS that treats the user's biological health as an essential asset. It integrates health telemetry, genomic data, and longevity protocols to maximize the user's "Human Alpha"—ensuring the biological operator of the system remains high-performing and resilient over the long term.

## Core Health Pillars

### 1. Biological Age & Epigenetics (`biological_age.py`)
Computes the difference between chronological and biological age.
- **PhenoAge Calculation**: Uses blood biomarkers (Glucose, CRP, Albumin, etc.) to estimate biological aging rates.
- **Rejuvenation Protocols**: Automatically suggests lifestyle or physiological adjustments (e.g., Zone 2 cardio, sleep optimization) if the biological age is accelerating beyond the chronological baseline.

### 2. Genomic Vault & Pharmacogenomics (`genomic_vault.py`)
Provides a secure environment for managing sensitive DNA-based risk profiles.
- **Drug Sensitivity Checks**: Compares drug names against a pharmacogenomic map (e.g., CYP2D6 gene) to identify potential toxicities or ineffective treatments.
- **Longevity Profiling**: Identifies genetic strengths (FOXO3) and risks (APOE4) to inform long-term preventative health strategies.

### 3. Longevity Stack Management (`supplement_mgr.py`)
Manages the inventory and compliance of the user's daily longevity supplements.
- **Inventory Tracking**: Monitors "on-hand" counts for items like NMN, Resveratrol, and Magnesium.
- **Auto-Reorder**: Generates order lists when stocks fall below defined thresholds, integrating with preferred high-quality vendors.

### 4. Health Telemetry Ingestion (`wearable_ingest.py`)
The data hub for real-time biological monitoring.
- **Provider Support**: Designed to ingest data from Oura, Apple Health, and Whoop.
- **Biometric Sync**: Captures daily scores for **Readiness**, **Sleep**, **HRV**, and **Resting Heart Rate** to inform the system's assessment of the user's current cognitive and physical capacity.

## Dependencies
- `pyotp`: Used to secure access to the Genomic Vault.
- `decimal`: Ensures precision in biomarker and dosage calculations.
- `logging`: Used for bio-feedback alerts and low-stock warnings.

## Usage Examples

### Assessing Pharmacogenomic Risk
```python
from services.bio.genomic_vault import GenomicVaultService

vault = GenomicVaultService()
check = vault.check_drug_sensitivity("Codeine")

if check['status'] == "WARNING":
    print(f"ALERT: Genetic risk detected on gene {check['gene']}. {check['implication']}")
```

### Checking Supplement Inventory
```python
from services.bio.supplement_mgr import SupplementManager

mgr = SupplementManager()
low_stock = mgr.check_inventory()

if low_stock:
    print(f"Items to reorder: {', '.join(low_stock)}")
    order = mgr.generate_order_list()
    print(f"Order status: {order['status']} via {order['vendor']}")
```


---

## Source: service_blue_green.md

# Backend Service: Blue-Green

## Overview
The **Blue-Green Service** provides the infrastructure for **Zero-Downtime Hot-Swapping** of agent logic and system components. It ensures that new code can be deployed, verified, and promoted to production without interrupting active financial operations or agent processing.

## Core Concepts

### 1. Environment Topology
- **GREEN (Production)**: The currently active and trusted version of the logic.
- **BLUE (Staging)**: The new version of the logic being prepared for cutover.

### 2. Hot-Swap Lifecycle (`deploy_hot_swap`)
The service automates a robust 4-stage deployment cycle:
1. **Backup Green**: Creates a timestamped snapshot of the current logic in the `backups/agents` directory before any changes are made.
2. **Deploy Blue**: Writes the new code to the target execution path.
3. **Verify Blue**: Performs a simulated verification phase (static analysis or startup check) to ensure the new logic is viable.
4. **Cutover**: Officially promotes the BLUE version to LIVE status and updates the internal version metadata registry.

### 3. Automated Rollback
If a deployment fails at any stage (verification error, runtime crash), the service can automatically or manually revert to the most recent GREEN backup. This maintains system stability and prevents "half-deployed" or broken states.

## Version Registry
The service maintains an in-memory `active_versions` registry that tracks:
- `deployment_id`: A unique identifies for the swap event.
- `timestamp`: When the deployment occurred.
- `backup_path`: The location of the previous version's snapshot.
- `status`: Current lifecycle state (`LIVE`, `ROLLED_BACK`, etc.).

## Usage Examples

### Executing a Logic Hot-Swap
```python
from services.blue_green_service import get_blue_green_service

bg_service = get_blue_green_service()

new_agent_logic = """
def process_event(event):
    print("New Optimized Logic V2")
    return True
"""

# Deploy and verify
result = await bg_service.deploy_hot_swap(
    agent_id="trading_agent_alpha",
    new_code=new_agent_logic,
    file_path="services/agents/trading_agent_alpha.py"
)

if result['status'] == "success":
    print(f"Hot-Swap Complete: Deployment ID {result['deployment_id']}")
```

### Performing a Manual Rollback
```python
from services.blue_green_service import get_blue_green_service

bg_service = get_blue_green_service()

success = bg_service.rollback(
    agent_id="trading_agent_alpha",
    file_path="services/agents/trading_agent_alpha.py"
)

if success:
    print("System restored to previous stable Green version.")
```


---

## Source: service_broker.md

# Backend Service: Broker

## Overview
The **Broker Service** acts as the "Hands" of the Sovereign OS, providing the execution layer for traditional brokerage platforms. It translates high-level investment decisions into low-level API calls for order placement, position monitoring, and multi-asset account management.

## Core Components

### Robinhood Service (`robinhood_service.py`)
A specialized interface for the Robinhood platform, supporting equities, options, and cryptocurrency.

#### Classes

##### `RobinhoodService`
A wrapper around the `robin_stocks` library that manages session lifecycle and transactional logic.

**Core Capabilities:**
- **Dynamic Authentication**: Supports username/password login combined with **TOTP-based 2-Factor Authentication (2FA)** for secure session initialization.
- **Account Intelligence**: Fetches real-time "Buying Power," cash balances, and total portfolio equity.
- **Position Enrichment**: Retrieves all open stock and crypto positions, automatically enriching them with ticker symbols and current cost-basis data.
- **Transactional Execution**: Provides simplified methods for placing market buy and sell orders with integrated error logging and status tracking.
- **Safety Mechanism**: Includes a full **Mock Mode** enabling safe end-to-end testing of trading workflows without risking real capital.

## Dependencies
- `robin_stocks`: The underlying library for Robinhood API communication.
- `utils.core.config`: Manages the secure retrieval of brokerage credentials from environment variables.

## Usage Examples

### Fetching Portfolio Buying Power
```python
from services.broker.robinhood_service import RobinhoodService

broker = RobinhoodService()
if broker.login():
    profile = broker.get_account_profile()
    print(f"Current Buying Power: ${profile['buying_power']}")
```

### Executing a "Safety-First" Market Order
```python
from services.broker.robinhood_service import RobinhoodService

# Initialize in Mock Mode for testing
broker = RobinhoodService(mock=True)

order = broker.place_market_order(
    symbol="AAPL", 
    quantity=1.0, 
    side="buy"
)

if "error" not in order:
    print(f"Mock Order Success: {order['id']} at ${order['price']}")
```


---

## Source: service_brokerage.md

# Backend Service: Brokerage

## Overview
The **Brokerage Service** is the platform's multi-institutional orchestration layer. It abstracts the complexities of various brokerage APIs (Alpaca, IBKR, Robinhood) into a unified interface, enabling global asset execution, real-time position synchronization, and professional-grade risk management.

## Core Abstractions

### 1. The Universal Connector (`brokerage_service.py`)
This is the master registry of all connected financial institutions.
- **Support Matrix**:
    - **Execution**: Alpaca, Interactive Brokers, TradeStation.
    - **Aggregation**: Fidelity, Charles Schwab, Vanguard, E*TRADE.
    - **Crypto**: Coinbase, Kraken, Binance.US.
- **Role**: Manages the lifecycle of multiple concurrent brokerage connections and provides consolidated account status (e.g., total buying power across all linked vendors).

### 2. Specialized Execution Clients
The service provides dedicated clients for specific institutional needs:
- **Alpaca Client (`alpaca_client.py`)**: Optimized for automated US equity trading, supporting fractional shares and high-frequency order submission to both Paper and Live markets.
- **IBKR Client (`ibkr_client.py`)**: A professional-grade client for Interactive Brokers.
    - **Global Reach**: Access to 150+ markets across equities, options, futures, and forex.
    - **Deep Analytics**: Provides detailed **Margin Requirements**, **Currency Exposure**, and multi-asset position summaries.

### 3. Execution Engine & Safety Framework (`execution_service.py`)
The "Last Mile" of the trade lifecycle where orders are validated before being sent to the market.
- **Pre-Flight Safety Checks**:
    - **System Kill Switch**: Blocks all order routing if a global `SYSTEM_HALTED` flag is detected.
    - **Risk Limit Validation**: Rejects orders that violate defined parameters (e.g., maximum order quantity or exposure limits).
- **Routing Logic**: Dynamically maps trade intents to the most appropriate brokerage client based on asset class and account configuration.

### 4. Post-Trade Lifecycle
- **Position Sync (`position_sync.py`)**: Ensures the internal "Sovereign Book" matches the real-time holdings reported by the brokers.
- **Settlement Service (`settlement_service.py`)**: Tracks the transition of trades from execution to final cash settlement (T+1/T+2).

## Dependencies
- `alpaca-trade-api`: Powers the primary automated execution logic.
- `ib_insync` / `ibapi`: Interfaces with the Interactive Brokers Gateway/TWS.
- `services.system.secret_manager`: Securely retrieves and rotates institutional API keys.

## Usage Examples

### Fetching Consolidated Buying Power
```python
from services.brokerage.brokerage_service import get_brokerage_service

brokerage = get_brokerage_service()
status = brokerage.get_status()

print(f"Summary: {status['summary']}")
for conn in status['connections']:
    print(f"- {conn['name']}: {conn['status']}")
```

### Routing a Safety-Checked Order
```python
from services.brokerage.execution_service import get_execution_service

execution = get_execution_service()

# Order payload
order_intent = {
    "symbol": "NVDA",
    "qty": 50,
    "side": "buy",
    "type": "market"
}

# The engine performs risk checks and kill-switch checks before routing
result = execution.place_order(order_intent)

if result['status'] == "FILLED":
    print(f"Trade successful. ID: {result['order_id']}")
elif result['status'] == "REJECTED":
    print(f"Safety Violation: {result['reason']}")
```


---

## Source: service_brokers.md

# Backend Service: Brokers (Specific)

## Overview
The **Brokers Service** directory houses specialized modules for brokerage simulation and multi-account data aggregation. These components are essential for the system's "Paper Trading" mode and for generating a holistic view of wealth across fragmented brokerage accounts.

## Core Components

### 1. Demo Broker Service (`demo_broker.py`)
A high-fidelity simulator that provides a risk-free environment for testing algorithms.
- **Role**: Emulates a live brokerage for paper trading.
- **Internal State Management**:
    - **Balance & Equity**: Maintains a virtual cash balance and tracks total equity.
    - **Position Tracking**: Manages a dictionary of open positions, calculating **weighted average buy prices** on every trade to ensure realistic P&L reporting.
- **Execution Logic**: Supports a "Market Order" execution model that immediately fills orders at specified mock prices, updating the internal ledger synchronously.
- **Lifecycle Support**: Includes a `reset_account` feature to clear all positions and return the virtual balance to a baseline (e.g., $100,000) for new testing cycles.

### 2. Broker Aggregator (`aggregator.py`)
Provides a consolidated view of the user's total brokerage footprint.
- **Purpose**: Combines disparate data streams from multiple registered broker instances.
- **Capabilities**:
    - **Equity Consolidation**: Calculates `total_equity` by summing the equity reported across all linked brokers (e.g., aggregating values from Alpaca, IBKR, and Robinhood).
    - **Position Mapping**: Flattens all account positions into a single unified list, enabling system-wide asset concentration analysis.

## Usage Examples

### Executing a Simulated Trade in Demo Mode
```python
from services.brokers.demo_broker import DemoBrokerService

demo = DemoBrokerService()

# Simulate a market buy of 10 shares of TSLA at $200
trade = demo.execute_market_order(
    symbol="TSLA",
    side="BUY",
    quantity=10,
    current_price=200.00
)

summary = demo.get_account_summary()
print(f"New Balance: ${summary['balance']}")
print(f"Position: {summary['positions']['TSLA']}")
```

### Aggregating Multi-Account Equity
```python
from services.brokers.aggregator import BrokerAggregator

agg = BrokerAggregator()

# Register data from different accounts
agg.register_broker("alpaca_personal", {"equity": 50000.00, "positions": [{"symbol": "AAPL", "qty": 100}]})
agg.register_broker("ibkr_joint", {"equity": 150000.00, "positions": [{"symbol": "SPY", "qty": 500}]})

total_wealth = agg.get_total_equity()
print(f"Total Brokerage Equity: ${total_wealth:,.2f}")
```


---

## Source: service_budgeting.md

# Backend Service: Budgeting

## Overview
The **Budgeting Service** provides the financial planning and discipline layer for the Sovereign OS. It enables users to set structured spending goals, automatically categorize real-world expenses, and receive analytical insights into their spending trends and budget compliance.

## Core Components

### 1. Budget Orchestrator (`budgeting_service.py`)
Manages the lifecycle of multiple concurrent budgets (e.g., "Monthly Operations," "Personal Surplus").
- **Dynamic Allocation**: Supports defining budgets across 10+ categories (Housing, Transport, Food, etc.) for specific time periods.
- **Delta Analysis**: Compares `total_budgeted` vs `total_spent` in real-time, providing actionable metrics like `remaining_balance` and identifying over-budget "problem categories."

### 2. Expense Tracking Engine (`expense_tracking_service.py`)
The transactional intake system for the budgeting framework.
- **Auto-Categorization**: Uses a sophisticated keyword-based matching engine to automatically assign transactions to categories (e.g., "Starbucks" -> "Food," "Mortgage" -> "Housing").
- **Spending Insights**: Calculates total spending velocity over rolling 30-day windows.
- **Trend Analysis**: Monitors spending behavior over a 90-day window to detect if a category is "Increasing," "Stable," or "Decreasing" in cost.

## Categories Supported
The system uses the `ExpenseCategory` schema to track:
- **Core Essentials**: Housing, Utilities, Healthcare, Insurance.
- **Lifestyle**: Transportation, Food, Entertainment, Shopping.
- **Financial Strategy**: Debt (loan payments), Education, and Other.

## Dependencies
- `pydantic`: Defines the `Budget`, `Expense`, and `SpendingTrend` data models.
- `services.system.cache_service`: For rapid persistence and retrieval of spending history.
- `datetime`: Manages all period-based analysis for monthly and annual trends.

## Usage Examples

### Creating a Monthly Personal Budget
```python
from services.budgeting.budgeting_service import get_budgeting_service

budget_service = get_budgeting_service()

# Define categories and limits
limits = {
    "housing": 3000.00,
    "food": 800.00,
    "transportation": 400.00,
    "entertainment": 200.00
}

budget = await budget_service.create_budget(
    user_id="user_vanguard_1",
    budget_name="Feb_2026_Baseline",
    period="monthly",
    categories=limits
)

print(f"Budget Created: {budget.budget_id} (Total: ${budget.total_budget:,.2f})")
```

### Analyzing Spending Against Budget
```python
from services.budgeting.budgeting_service import get_budgeting_service

budget_service = get_budgeting_service()

analysis = await budget_service.get_budget_analysis(
    budget_id="budget_user_vanguard_1_123456789"
)

print(f"Total Spent: ${analysis.total_spent:,.2f}")
print(f"Remaining: ${analysis.remaining:,.2f}")

if analysis.over_budget_categories:
    print(f"CRITICAL: Over budget in {', '.join(analysis.over_budget_categories)}")
```


---

## Source: service_caching.md

# Backend Service: Caching

## Overview
The **Caching Service** is the platform's high-performance data persistence layer for transient system states. It is designed to optimize expensive quantitative computations, such as risk simulations and portfolio attribution, by storing results in a low-latency **Redis** backend with a robust in-memory fallback.

## Core Components

### 1. Performance Cache (`performance_cache.py`)
A singleton implementation that provides a tiered caching strategy.

#### Tiers of Storage
1. **Primary (Redis)**: Uses an external Redis instance (configured via `REDIS_URL`) for shared state across distributed service instances.
2. **Fallback (In-Memory)**: Automatically switches to a local Python dictionary if Redis is unavailable, ensuring the system remains functional even during infrastructure degradation.

#### Key Features
- **TTL (Time-To-Live)**: All cached entries support a mandatory expiration window (default: 3600s) to prevent data staleness.
- **Atomic Cache Operations**: Provides high-level methods like `get_or_set` for thread-safe computation and storage patterns.
- **Pattern Invalidation**: Allows clearing specific subsets of cached data using glob-style patterns (e.g., `invalidate_pattern("attribution:*")`).

### 2. The `@cached` Decorator
Enables seamless integration with any internal function. It automatically generates a unique cache key based on the function name and its arguments (using MD5 hashing for complex objects), dramatically reducing the boilerplate required for performance optimization.

## Dependencies
- `redis`: The primary backend driver.
- `hashlib`: Used for deterministic cache key generation.
- `json`: Handles serialization and deserialization of cached Python objects.

## Usage Examples

### Using the `@cached` Decorator
```python
from services.caching.performance_cache import cached

@cached(ttl=300)
def compute_complex_risk_metric(portfolio_id: str, factor: float):
    # This expensive operation will only run once every 5 minutes
    # Results for identical (portfolio_id, factor) pairs will be served from cache
    return some_heavy_math(portfolio_id, factor)
```

### Manual Cache Management
```python
from services.caching.performance_cache import get_cache

cache = get_cache()

# Try to get data with a fallback computation
data = cache.get_or_set(
    key="market_regime:2026-02-07",
    func=determine_market_regime,
    ttl=3600
)

# Invalidate a specific group of keys
cache.invalidate_pattern("auth:challenges:*")
```


---

## Source: service_calendar.md

# Backend Service: Calendar

## Overview
The **Calendar Service** serves as the system's temporal orchestration layer. It bridges the gap between raw market event data (earnings calls, dividend dates) and the user's personal scheduling tools, providing a unified, color-coded timeline for financial awareness and decision-making.

## Core Components

### 1. Google Calendar Integration (`google_calendar_service.py`)
A comprehensive wrapper for the Google Calendar v3 API.
- **Visual Categorization**: Automatically applies internal color coding to events:
    - **Blue (ID 9)**: Corporate Earnings.
    - **Green (ID 10)**: Dividend Payments.
    - **Yellow (ID 5)**: Portfolio Rebalancing.
- **Intelligent Reminders**: Configures multi-channel alerts (e.g., Email 24 hours prior, Popup 1 hour prior) for all financial milestones.
- **CRUD Lifecycle**: Full support for creating, listing, updating, and asynchronously deleting calendar events across any user-authorized Google Calendar.

### 2. Earnings & Dividend Sync (`earnings_sync.py`)
An automated pipeline that monitors the user's investment universe.
- **AlphaVantage Integration**: Periodically fetches global earnings and dividend calendars.
- **Holdings Filtering**: Cross-references the global calendar against the user's real-time portfolio holdings to isolate relevant events.
- **Sync Logic**: Creates high-visibility events on the user's calendar with detailed descriptions, including **Estimated EPS** and conference call links where available. It includes a de-duplication mechanism to ensure the calendar remains clean across multiple sync cycles.

## Dependencies
- `google-api-python-client`: Powers the underlying Google Calendar API communication.
- `services.data.alpha_vantage`: Source of corporate financial event data.
- `services.system.secret_manager`: Manages OAuth2 credentials and user access tokens safely.

## Usage Examples

### Syncing Earnings for a User's Portfolio
```python
from services.calendar.earnings_sync import get_earnings_sync_service

sync_service = get_earnings_sync_service()

# holdings = ["AAPL", "TSLA", "NVDA"]
stats = await sync_service.sync_earnings_for_user(
    user_id="user_vanguard_1",
    access_token="YA29.GLC...", # OAuth token from Auth service
    holdings=my_holdings,
    days_ahead=90
)

print(f"Calendar Sync Success. Created {stats['events_created']} new events.")
```

### Manually Creating a Rebalancing Reminder
```python
from services.calendar.google_calendar_service import get_calendar_service
from datetime import datetime, timedelta

cal = get_calendar_service()

await cal.create_event(
    access_token="YA29.GLC...",
    title="Quarterly Portfolio Rebalance",
    description="Analyze factor exposures and adjust weights per AI Alpha engine.",
    start_time=datetime.now() + timedelta(days=7),
    event_type="rebalance"
)
```


---

## Source: service_charting.md

# Backend Service: Charting

## Overview
The **Charting Service** is the backbone of the platform's visual intelligence. It transforms raw financial time-series data into structured, multi-timeframe datasets optimized for high-performance rendering in the frontend. It supports professional-grade chart types, technical indicator overlays, and dynamic aggregation.

## Core Capabilities

### 1. Data Preparation Engine (`charting_service.py`)
Prepares OHLCV (Open, High, Low, Close, Volume) data for consumption by D3.js or Plotly charts.
- **Advanced Chart Types**:
    - **Standard**: Candlestick, Line, and Area charts.
    - **Quantitative**: **Heikin-Ashi** transformations for noise reduction and trend clarity.
- **Multi-Timeframe Support**: Dynamically resamples high-frequency data into 10 distinct timeframes ranging from **1-minute** (intraday) to **1-year** (macro) periods, ensuring correct OHLC aggregation at every level.

### 2. Analytical Overlays
The service orchestrates the calculation of technical studies ($indicators$) and maps them directly to the price timeline, enabling a unified view of market action and signal data.

### 3. Smart Persistence
To minimize the load on market data providers and ensure sub-second chart loading:
- **Tiered Caching**:
    - **Intraday Charts**: 5-minute cache TTL to maintain freshness.
    - **Daily+ Charts**: 1-hour cache TTL for stable historical data.

## Constants & Schema
- **Timeframes**: `1min`, `5min`, `15min`, `30min`, `1hr`, `4hr`, `1day`, `1week`, `1month`, `1year`.
- **Chart Types**: `CANDLESTICK`, `LINE`, `AREA`, `HEIKIN_ASHI`.

## Dependencies
- `pandas`: Powers the high-speed resampling and Heikin-Ashi mathematical transformations.
- `numpy`: Used for volatility and returns simulation in mock modes.
- `services.analysis.technical_analysis_service`: Provides the underlying math for indicators.
- `services.data.alpha_vantage`: The primary source for historical price bars.

## Usage Examples

### Fetching Daily Candlestick Data with Indicators
```python
from services.charting.charting_service import get_charting_service

chart_svc = get_charting_service()

# Get 1-day candlestick data for AAPL with SMA and RSI overlays
chart_data = await chart_svc.get_chart_data(
    symbol="AAPL",
    timeframe="1day",
    chart_type="candlestick",
    indicators=["SMA", "RSI"]
)

print(f"Retrieved {chart_data['metadata']['data_points']} data points.")
print(f"Indicators available: {list(chart_data['indicators'].keys())}")
```

### Aggregating 1-Minute Data to 15-Minute Bars
```python
import pandas as pd
from services.charting.charting_service import get_charting_service

chart_svc = get_charting_service()

# source_df contains 1-minute OHLCV data
fifteen_min_df = await chart_svc.aggregate_timeframe(
    data=source_df,
    source_timeframe="1min",
    target_timeframe="15min"
)
```


---

## Source: service_communication.md

# Backend Service: Communication

## Overview
The **Communication Service** is the platform's multi-channel notification and alert orchestration layer. It manages outgoing messages through diverse channels including Email (Professional and Personal), Discord Webhooks, and SMS, ensuring critical financial signals reach the user with high reliability and appropriate urgency.

## Core Dispatchers

### 1. Unified Email Service (`email_service.py`)
A production-ready engine with support for multiple high-deliverability providers.
- **Provider Agnostic**: Supports **SendGrid**, **AWS SES**, and standard **SMTP**.
- **Transactional Framework**: Includes a template engine for automated workflows like "Welcome" series, "Password Reset," and "Onboarding Completion."

### 2. Gmail Specialized Client (`gmail_service.py`)
A dedicated interface for the user's personal Google account.
- **Advanced Quota Management**: Tracks daily send counts and enforces rate limits (e.g., 500 emails/day) to protect the user's Gmail reputation.
- **Rich Media Support**: Handles MIME-encoded messages with HTML bodies and attachments for daily portfolio reports.

### 3. Discord Alerting (`discord_webhook.py`)
Direct integration for high-speed trading signals and community alerts.
- **Signal Templates**: Includes specialized formatting for `AI TRADE SIGNALS` with color-coded "BUY/SELL" embeds, confidence scores, and price triggers.
- **Rich Embeds**: Uses Discord's embed system to provide detailed "footer" metadata and timestamping for audit trails.

### 4. Notification Hub & Router (`notification_manager.py`)
The intelligent logic layer that determines *how* and *where* a message is delivered based on its priority.
- **Priority Routing Matrix**:
    - **CRITICAL**: Dispatched via SMS, Push, Email, and System Console for maximum visibility.
    - **WARNING**: Sent via Push and Email.
    - **INFO**: Logged to the internal dashboard and console only.

## Dependencies
- `sendgrid` / `boto3`: Underlying API drivers for professional email providers.
- `google-api-python-client`: Powers the personal Gmail integration.
- `smtplib`: Standard Python library for SMTP fallback.

## Usage Examples

### Dispatching a Managed Alert
```python
from services.communication.notification_manager import get_notification_manager, AlertPriority

notifier = get_notification_manager()

# This will trigger SMS, Push, and Email based on CRITICAL priority
notifier.send_alert(
    message="RISK ALERT: Portfolio volatility exceeded 2.5% threshold.",
    priority=AlertPriority.CRITICAL
)
```

### Sending a Trade Signal to Discord
```python
from services.communication.discord_webhook import get_discord_webhook

webhook = get_discord_webhook(url="https://discord.com/api/webhooks/...")

await webhook.send_trade_signal(
    ticker="NVDA",
    side="buy",
    price=650.25,
    confidence=0.88
)
```


---

## Source: service_community.md

# Backend Service: Community

## Overview
The **Community Service** facilitates collaborative intelligence and peer-to-peer engagement within the Sovereign OS ecosystem. It provides the infrastructure for structured financial discussion forums and a verified **Expert Q&A** system, enabling users to share insights, validate strategies, and access domain experts directly.

## Core Components

### 1. Expert Q&A System (`expert_qa_service.py`)
A high-integrity channel for direct consultation with financial specialists.
- **Intelligent Routing**: Automatically matches incoming user questions to verified experts based on category and specialty.
- **Answer Quality Lifecycle**:
    - **Open**: Question is active and awaiting expert input.
    - **Answered**: An expert has responded.
    - **Best Answer**: The user has selected a definitive response, which closes the question and updates the system's knowledge base.
- **Verification Logic**: Maintains registry of expert credentials and specialties to ensure high-signal responses.

### 2. Community Forum Service (`forum_service.py`)
The social architecture for collaborative investing.
- **Thread Management**: Supports multi-category discussion threads (e.g., "Macro," "Equities," "DeFi") with full title and content indexing.
- **Engagement Mechanics**:
    - **Nested Replies**: Enables structured, threaded conversations with parent/child relationships.
    - **Upvoting System**: Implements a popularity and quality discovery mechanism, allowing top-tier insights to surface to the community dashboard.
- **Activity Tracking**: Real-time monitoring of reply counts and "Last Active" timestamps to maintain forum vibrancy.

## Dependencies
- `pydantic`: Enforces schemas for `ForumThread`, `ThreadReply`, and `ExpertQuestion`.
- `services.system.cache_service`: Provides high-speed persistence for active discussions and Q&A threads.
- `services.communication.notification_service`: Triggers alerts for user mentions or expert responses.

## Usage Examples

### Creating a Category-Based Forum Thread
```python
from services.community.forum_service import get_forum_service

forum = get_forum_service()

thread = await forum.create_thread(
    user_id="user_vanguard_1",
    category="Macro",
    title="Impact of 2026 Yield Curve Inversion",
    content="How is the sovereign OS positioning for the upcoming rate hike cycle?"
)

print(f"Thread Live: {thread.thread_id} in {thread.category}")
```

### Routing a Question to an Expert
```python
from services.community.expert_qa_service import get_expert_qa_service

qa_service = get_expert_qa_service()

question = await qa_service.create_question(
    user_id="user_vanguard_1",
    title="Tax Implication of Tokenized Real Estate",
    content="What are the K-1 requirements for fractionalized REITS in the EU?",
    category="Tax_Law"
)

print(f"Question Routed to Expert: {question.expert_id}")
```


---

## Source: service_compliance.md

# Backend Service: Compliance

## Overview
The **Compliance Service** (internally known as "The Compliance Shield") is the platform's multi-layered regulatory and ethical governance engine. It operates across 49 specialized components to ensure every trade, transfer, and agent action adheres to SEC, FINRA, and fiduciary standards.

## Core Functional Pillars

### 1. The Compliance Engine (`compliance_engine.py`)
The central orchestrator for real-time violation detection.
- **Rule Verification**: Checks transactions against a dynamic library of SEC and FINRA rules.
- **Severity Scoring**: Categorizes violations into `LOW`, `MEDIUM`, or `HIGH` severity for prioritized response.
- **Persistence**: Logs all detected anomalies to the `AuditService` and `RecordVault` for permanent audit trails.

### 2. Market Integrity & Restrictions
- **Wash-Sale Detector (`compliance_service.py`, `wash_sale.py`)**: Analyzes the last 30 days of trading history to prevent the purchase of securities previously sold at a loss, ensuring compliance with IRS tax rules.
- **Insider Trading & Rule 144 (`insider_trading_svc.py`)**: 
    - **Volume Limits**: Calculates 1% of outstanding shares vs. 4-week average weekly volume for affiliate selling.
    - **Lock-Up Validator**: Monitors post-IPO or meta-acquisition lock-up windows.
    - **Compliant Selling Plans**: Validates Rule 10b5-1 selling plans.

### 3. Fiduciary & Trust Governance
- **Solvency Validator (`solvency_validator.py`)**: Ensures asset transfers into Asset Protection Trusts (APTs) are not fraudulent conveyances by performing Balance Sheet and Cash Flow tests.
- **HEMS Validator (`hems_validator.py`)**: Verifies that trust distributions match the legal "Health, Education, Maintenance, and Support" standard.
- **Spendthrift Firewall (`spendthrift_firewall.py`)**: Protects trust assets from external creditor claims by enforcing distribution caps.

### 4. Forensic & Evidence Layer
- **Record Vault (`record_vault.py`)**: A WORM (Write Once, Read Many) style storage system for all compliance-sensitive metadata.
- **Evidence Locker (`evidence_locker.py`)**: Secures snapshots of market states at the time of trade execution for later regulatory defense.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Compliance Dashboard** | Violation Feed | `compliance_engine.get_violations()` |
| **Trade Terminal** | Pre-Flight Modal | `compliance_service.check_wash_sale()` |
| **Strategist / Estate** | APT Solvency Tool | `solvency_validator.generate_solvency_affidavit()` |
| **Insider Workstation** | Role 144 Calculator | `insider_trading_svc.calculate_sellable_volume()` |
| **Audit Center** | Forensic Viewer | `record_vault.get_records_by_type()` |

## Dependencies
- `pydantic`: For robust schema validation of rules and violations.
- `utils.database_manager`: Direct PostgreSQL access for persisting legal affidavits.
- `services.system.cache_service`: For rapid rule-matching and transient state monitoring.

## Usage Examples

### Running a Pre-Trade Wash-Sale Check
```python
from services.compliance.compliance_service import get_compliance_service
from datetime import datetime

compliance = get_compliance_service()

check = compliance.check_wash_sale(ticker="TSLA", trade_date=datetime.now())
if check["is_wash_sale"]:
    print(f"Compliance Block: {check['reason']}")
```

### Validating Insider Sale Volume
```python
from services.compliance.insider_trading_svc import InsiderTradingService

insider_svc = InsiderTradingService()

compliance_report = insider_svc.validate_sale_compliance(
    ticker="NVDA",
    shares_to_sell=50000,
    outstanding_shares=1000000000,
    avg_weekly_volume=30000,
    lockup_expiry=datetime.date(2025, 12, 31)
)

if not compliance_report["compliant"]:
    print(f"SEC RULE 144 FAILURE: {compliance_report['reason']}")
```


---

## Source: service_coordination.md

# Backend Service: Coordination

## Overview
The **Coordination Service** is the platform's inter-departmental orchestration layer. It is designed to align the actions of diverse stakeholders—such as Financial Advisors, CPAs, Attorneys, and AI Agents—around a unified set of client objectives, ensuring that complex financial strategies (like estate planning or tax-loss harvesting) are executed in sync.

## Core Components

### 1. Shared Goals Manager (`shared_goals.py`)
A centralized registry for multi-stakeholder objectives.
- **Stakeholder Mapping**: Explicitly tracks which entities (e.g., `ADVISOR`, `CPA`, `ATTORNEY`) are responsible for portions of a top-level goal.
- **Atomic Goal Tracking**: Maintains the lifecycle of coordinated tasks from `OPEN` to completion.
- **Audit Logging**: Emits `COORDINATION_LOG` events to the system's observability stack, capturing exactly when and how goals are modified across different departments.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Mission Control** | Coordinated Timeline | `shared_goals_service.goals` (filtered by client) |
| **Collaboration Hub** | Shared Objectives Feed | `shared_goals_service.add_coordinated_goal()` |
| **Advisor Workstation** | Stakeholder Progress Panel | `shared_goals_service.goals` |
| **Client Portal** | Unified Roadmap | `shared_goals_service.goals` |

## Dependencies
- `logging`: Standard system logging for cross-stakeholder audit trails.

## Usage Examples

### Adding a Coordinated Tax Strategy Goal
```python
from services.coordination.shared_goals import SharedGoalsService

coord_svc = SharedGoalsService()

# Coordinate a ROTH conversion between the Advisor and CPA
goal = coord_svc.add_coordinated_goal(
    client_id="client_vanguard_88",
    goal_desc="Execute $50k ROTH Conversion for 2026 Tax Year",
    stakeholders=["ADVISOR", "CPA"]
)

print(f"Goal Coordinated: {goal['description']} with status {goal['status']}")
```


---

## Source: service_core.md

# Backend Service: Core

## Overview
The **Core Service** houses the platform's highest level of system abstraction and unification. Its primary role is to serve as the "Ghost in the Machine," aggregating various specialized modules—Finance, Sovereignty, Singularity, and Space—into a single, unified system status and directive interface.

## Core Components

### 1. OmegaGeist Unification Engine (`omega_geist.py`)
The final aggregation layer of the Sovereign OS implementation (Phase 215.3).
- **Epoch Monitoring**: Performs deep-health checks across all major architectural "Epochs" (e.g., FinTech, Sovereignty, Singularity).
- **System Awareness**: Monitors the high-level operational state and "Awareness" level of the collective AI workforce.
- **Master Directive**: Ensures all sub-systems are aligned with the core system directive: `PRESERVE_AND_GROW`.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **System BIOS** | Initialization Console | `omega_geist.awaken()` |
| **Mission Control** | System Health Matrix | `omega_geist.awaken()` (Status fields) |
| **Warden / Security** | Epoch Pulse Monitor | `omega_geist.awaken()` |
| **Developer Sandbox** | Unification Trace | `omega_geist.modules` registry |

## Dependencies
- `logging`: Standard system logging for master system event tracking.
- `time`: Used for simulated system hardware spin-up and synchronization during initialization.

## Usage Examples

### Initializing System Unification
```python
from services.core.omega_geist import OmegaGeistService

geist = OmegaGeistService()

# Perform master system check
sys_status = geist.awaken()

if sys_status["Awareness"] == "HIGH":
    print(f"System Unification Successful. Directive: {sys_status['Directive']}")
```


---

## Source: service_credit.md

# Backend Service: Credit

## Overview
The **Credit Service** is a dual-purpose financial engine. It manages personal credit health (monitoring, improvement, and simulation) while providing institutional-grade risk analysis for private credit and direct lending portfolios. It ensures that both the user's credit profile and the platform's credit-based investments are optimized for maximum yield and stability.

## Core Components

### 1. Consumer Credit intelligence
- **Credit Monitoring (`credit_monitoring_service.py`)**: 
    - **Score Tracking**: Monitors FICO/VantageScore trends across multiple timeframes.
    - **Factor Analysis**: Deconstructs credit scores into weighted factors (Payment History, Utilization, etc.) to identify specific areas of weakness.
- **Improvement Engine (`credit_improvement_service.py`)**:
    - **Personalized Recommendations**: Generates actionable items (e.g., "Set up autopay," "Request limit increase") with estimated impact scores.
    - **Score Simulator**: Projects future credit scores based on completed action items and projected timeframes.

### 2. Institutional Private Credit
- **Credit Risk Engine (`credit_risk_engine.py`)**: 
    - **Net Yield Calibration**: Calculates the expected net yield for direct lending by adjusting gross spreads for base rates, annual default probabilities, and recovery rates.
    - **Risk Status Classification**: Automatically flags portfolios as `STABLE` or `WATCHLIST` based on expected loss thresholds.
- **Loan Tape Ingestion (`loan_tape_svc.py`)**: Processes raw institutional loan tapes (Principal, Counterparty, Maturity) into unified portfolio committed-capital metrics.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Credit Dashboard** | Score Trend Graph | `credit_monitoring_service.get_credit_history()` |
| **Credit Dashboard** | Impact Simulator | `credit_improvement_service.simulate_score_improvement()` |
| **Credit Dashboard** | Action Center | `credit_improvement_service.generate_recommendations()` |
| **Private Credit Workstation** | Yield Calculator | `credit_risk_engine.calculate_expected_net_yield()` |
| **Private Credit Workstation** | Tape Ingestion Portal | `loan_tape_svc.ingest_tape()` |

## Dependencies
- `decimal`: Used for high-precision financial math in the yield engine.
- `pydantic`: Enforces schemas for `CreditScore`, `CreditRecommendation`, and `CreditProjection`.
- `services.system.cache_service`: Persists recent snapshots of credit scores and projections.

## Usage Examples

### Simulating a Credit Score Improvement
```python
from services.credit.credit_improvement_service import get_credit_improvement_service

improvement_svc = get_credit_improvement_service()

# user_id identifies the specific credit profile
projection = await improvement_svc.simulate_score_improvement(
    user_id="user_vanguard_99",
    recommendations=[rec1, rec2] # recommendation objects from generate_recommendations()
)

print(f"Projected Score: {projection.projected_score} by {projection.projected_date}")
```

### Calculating Expected Net Yield for Private Credit
```python
from services.credit.credit_risk_engine import CreditRiskEngine
from decimal import Decimal

risk_engine = CreditRiskEngine()

stats = risk_engine.calculate_expected_net_yield(
    gross_spread_bps=450,
    base_rate=Decimal("0.0525"),
    default_prob_annual=Decimal("0.015"),
    recovery_rate=Decimal("0.65")
)

print(f"Net Yield: {stats['net_yield_pct']}% (Status: {stats['risk_status']})")
```


---

## Source: service_crm.md

# Backend Service: CRM

## Overview
The **CRM (Customer Relationship Management)** service provides the platform's relationship intelligence layer. It is responsible for categorizing the user's client base into distinct tiers based on Assets Under Management (AUM) and strategic institutional status, ensuring that high-value opportunities and support resources are allocated with maximum efficiency.

## Core Components

### 1. Priority Scorer (`client_priority.py`)
A policy-driven engine that determines client importance and service levels (Phase 173.1).
- **Tiering Logic**:
    - **TIER_1_SFO (Priority 1)**: Single Family Offices (SFOs) or clients with **$50M+** in AUM. These represent the highest strategic priority.
    - **TIER_2_UHNW (Priority 2)**: Ultra-High-Net-Worth individuals with **$5M+** in AUM. Includes "Qualified Purchaser" status flagging for regulatory access to private funds.
    - **TIER_3_RETAIL (Priority 3)**: Standard retail clients.
- **Regulatory Profiling**: Automatically determines if a client meets the SEC "Qualified Purchaser" threshold, which is critical for restricted investment participation.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **CRM Dashboard** | Client List | `priority_scorer.calculate_priority()` (Tier labels) |
| **CRM Dashboard** | AUM Distribution Plot | `priority_scorer.calculate_priority()` |
| **Deal Center** | Allocation Modal | `priority_scorer.calculate_priority()` (Priority sorting) |
| **Client Onboarding** | Eligibility Wizard | `priority_scorer.calculate_priority()` (QP Status) |

## Dependencies
- `logging`: Records CRM logic events for institutional relationship audit trails.

## Usage Examples

### Calculating Client Priority and QP Status
```python
from services.crm.client_priority import PriorityScorer

scorer = PriorityScorer()

# Calculate tier for an institutional prospect
client_profile = scorer.calculate_priority(
    aum=120_000_000, 
    is_sfo=True
)

print(f"Client Tier: {client_profile['tier']}")
print(f"Qualified Purchaser: {client_profile['is_qualified_purchaser']}")
```


---

## Source: service_crypto.md

# Backend Service: Crypto

## Overview
The **Crypto Service** is the platform's portal to the digital asset ecosystem. It provides a unified, cross-chain interface for managing self-custody wallets (Ethereum, Solana, Bitcoin, Polygon), institutional exchange accounts (Coinbase Advanced), and decentralized finance (DeFi) interactions. It handles the complexity of gas optimization, signature verification, and multi-chain balance aggregation.

## Core Components

### 1. Multi-Chain Wallet Orchestration (`wallet_service.py`)
The central hub for user-controlled assets.
- **Cross-Chain Aggregation**: Consolidates balances across disparate networks (ETH, SOL, BTC) into a single `CryptoPortfolio` view.
- **Ownership Verification**: Implements EIP-191 style message signing and verification to securely link on-chain addresses to platform users.
- **Address Validation**: Provides chain-specific regex and checksum validation for preventing loss of funds due to invalid destination addresses.

### 2. Blockchain & Exchange Clients
- **Network Clients (`ethereum_client.py`, `solana_client.py`)**: Direct RPC integrations for fetching native and token (ERC-20, SPL) balances, price feeds, and transaction statuses.
- **Institutional Gateway (`coinbase_client.py`, `coinbase_custody.py`)**: Programmatic access to Coinbase Advanced Trading and Vaults, enabling seamless transition between centralized and decentralized liquidity.

### 3. Gas & Fee Optimization (`gas_service.py`)
Ensures cost-effective on-chain execution.
- **Real-Time Monitoring**: Tracks gas prices on Ethereum, Polygon, and Arbitrum.
- **Optimal Window Detection**: Analyzes historical volatility to recommend low-fee execution windows (e.g., finding periods where gas is <3 std dev from the 24h mean).
- **Transaction Queuing**: Allows users to "Set and Forget" transactions that execute automatically when gas hits a target Gwei threshold.

### 4. Advanced Security (`shamir_secret.py`)
- **Key Sharding**: Implements Shamir's Secret Sharing (SSS) to shard sensitive master keys or recovery phrases across multiple encrypted storage nodes, eliminating single points of failure in key management.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Crypto Terminal** | Portfolio Overview | `wallet_service.get_aggregated_portfolio()` |
| **Wallet Connect** | Auth Modal | `wallet_service.verify_ownership()` (Signature) |
| **Trade Modal** | Gas Fee Estimator | `gas_service.get_current_gas()` |
| **Trade Modal** | Execution Scheduler | `gas_service.get_optimal_execution_window()` |
| **DeFi Hub** | Yield Aggregator | `lp_tracker_service.py` (Liquidity metrics) |

## Dependencies
- `web3`: For Ethereum JSON-RPC communication and signature recovery.
- `pydantic`: For strictly-typed models like `Balance` and `CryptoPortfolio`.
- `services.system.secret_manager`: Securely retrieves RPC URLs and API credentials.

## Usage Examples

### Fetching a Unified Cross-Chain Portfolio
```python
from services.crypto.wallet_service import get_wallet_service

wallet_svc = get_wallet_service()

# Aggregates ETH, SOL, and others into a single USD-denominated view
portfolio = await wallet_svc.get_aggregated_portfolio(user_id="user_vanguard_1")

print(f"Total Crypto Value: ${portfolio.total_usd_value:,.2f}")
for balance in portfolio.balances:
    print(f"- {balance.amount} {balance.token} on {balance.chain}")
```

### Scheduling a Low-Fee Transaction
```python
from services.crypto.gas_service import GasService

gas_svc = GasService()

# Check if now is a good time to execute
if await gas_svc.detect_spike("ethereum"):
    # Find the next cheap window instead
    window = await gas_svc.get_optimal_execution_window()
    print(f"Gas Spike Detected! Optimal window: {window.start_time}")
else:
    print("Gas levels stable. Executing now.")
```


---

## Source: service_custody.md

# Backend Service: Custody

## Overview
The **Custody Service** is the platform's asset safeguarding and title verification layer. It is designed to ensure that the user's financial assets are held in the safest possible registration formats—primarily shifting from "Street Name" brokered positions to **Direct Registration (DRS)** with transfer agents. Additionally, it maintains the primary **Immutable Ledger**, providing cryptographic proof of every transaction on the platform.

## Core Components

### 1. DRS Transfer Manager (`drs_transfer_mgr.py`)
Automates the legal transition of asset ownership.
- **Direct Registration (DRS)**: Provides an automated workflow for moving shares from a broker (Source) to a Transfer Agent (Destination). This places the legal title of the security directly in the client's name.
- **Title Verification**: Includes logic for verifying the registration status of any asset (e.g., `DRS`, `PHYSICAL`, `ISSUER_DIRECT`) to determine the level of direct ownership.

### 2. Immutable Ledger Service (`ledger_service.py`)
Provides the "Truth Machine" for platform activity.
- **Cryptographic Chaining**: Uses SHA-256 hashing to chain every transaction to the previous entry, ensuring that any modification to historical data is detectable.
- **Integrity Validation**: Periodically audits the entire chain of ledger entries to ensure there have been no modifications or corruption.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Portfolio Terminal** | Registration Status Ribbon | `drs_transfer_manager.verify_legal_title()` |
| **Asset Detail Page** | DRS Transfer Wizard | `drs_transfer_manager.initiate_drs_transfer()` |
| **Vault / Audit Center** | Transaction History Ledger | `ledger_service.verify_chain_integrity()` |
| **Trust Workstation** | Title Evidence Locker | `drs_transfer_manager.verify_legal_title()` |

## Dependencies
- `hashlib`: Standard Python library for ledger checksumming and transaction chaining.
- `schemas.platform_ledger`: Defines the data structure for consistent ledger serialization.

## Usage Examples

### Initiating a DRS Transfer for Asset Protection
```python
from services.custody.drs_transfer_mgr import DRSTransferManager
from uuid import uuid4

drs_mgr = DRSTransferManager()

# Transfer 100 shares of an asset (UUID) to the Transfer Agent
ticket = drs_mgr.initiate_drs_transfer(
    asset_id=uuid4(),
    broker_id=uuid4(),
    share_quantity=100
)

print(f"DRS Transfer Ticket {ticket['transfer_ticket_id']} has status {ticket['status']}")
```

### Verifying Ledger Integrity
```python
from services.custody.ledger_service import LedgerService

ledger = LedgerService()

# entries: List[PlatformLedger] fetched from DB
is_valid = ledger.verify_chain_integrity(entries)

if not is_valid:
    print("CRITICAL ALERT: Ledger chain integrity failure detected!")
```


---

## Source: service_data.md

# Backend Service: Data

## Overview
The **Data Service** is the platform's high-fidelity ingestion and normalization hub. It aggregates raw financial data from over a dozen external providers (Alpha Vantage, FRED, Polygon, Google Trends, etc.) and fuses them into a unified mathematical "Market State Tensor." This ensures that both human users and AI agents have a consistent, normalized view of market volatility, sentiment, and macroeconomic health.

## Core Components

### 1. Data Fusion Engine (`data_fusion_service.py`)
The primary orchestrator for cross-domain data normalization.
- **Market State Tensor**: Fuses Price Momentum, Retail Sentiment, Options Flow (Smart Money), and Macro Health into a 0.0–1.0 scaled tensor.
- **Validation & Quarantine**: Implements data integrity checks (staleness, impossible values) and "quarantines" suspicious data to prevent AI agents from acting on corrupted signals.
- **Sigmoid Normalization**: Uses mathematical sigmoid functions to map disparate metrics (like Z-scores or basis points) into a consistent range.

### 2. External Data Providers
- **Equity Intelligence (`alpha_vantage.py`, `polygon_service.py`)**: Fetches real-time quotes, historical OHLCV bars, and institutional earnings calendars. Features robust rate-limiting via the `APIGovernor`.
- **Macroeconomic Engine (`fred_service.py`)**: Monitors the Federal Reserve's economic data (Yield Curve, CPI, Unemployment). 
    - **Regime Analysis**: Automatically classifies the economic state into categories like `EXPANSION`, `SLOWDOWN`, or `RECESSION_WARNING`.
- **Sentiment & Alternatives (`google_trends.py`, `reddit_service.py`)**: Ingests retail interest and social volume to quantify "herd behavior" and market fear/greed.

### 3. Options & Flow (`options_service.py`)
- **Smart Money Tracking**: Monitors Put/Call ratios and whale movement in the options market to identify directional bias before it reflects in spot prices.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Market Terminal** | Advanced Charts (OHLCV) | `alpha_vantage.get_intraday()` |
| **Market Terminal** | Sentiment Meter | `google_trends.get_trend_score()` |
| **Macro Dashboard** | Yield Curve Visualizer | `fred_service.get_yield_curve_data()` |
| **Macro Dashboard** | Regime Pulse | `fred_service.get_macro_regime()` |
| **AI Strategy Hub** | Tensor Heatmap | `data_fusion_service.get_market_state_tensor()` |
| **Earnings Center** | Calendar Timeline | `alpha_vantage.get_earnings_calendar()` |

## Dependencies
- `httpx`: High-performance asynchronous HTTP client for parallel API fetching.
- `numpy`: Used for multi-dimensional tensor calculations and normalization.
- `pydantic`: Enforces schemas for `Quote`, `OHLCV`, `MacroRegime`, and `Earnings`.
- `services.system.api_governance`: Manages API keys and tier-based rate limits.

## Usage Examples

### Generating a Market State Tensor for TSLA
```python
from services.data.data_fusion_service import DataFusionService

fusion = DataFusionService()

# Generates a normalized 0-1 set of metrics
state = fusion.get_market_state_tensor(symbol="TSLA")

print(f"Aggregate Market Score: {state['aggregate_score']}")
print(f"Retail Sentiment: {state['tensor']['retail_sentiment']}")
```

### Fetching Economic Regime from FRED
```python
from services.data.fred_service import get_fred_service

fred = get_fred_service()

regime = await fred.get_macro_regime()
print(f"Economic Status: {regime.status}")
print(f"Health Score: {regime.health_score}/100")
```


---

## Source: service_deal.md

# Backend Service: Deal

## Overview
The **Deal Service** manages the lifecycle of private investment opportunities, specifically focusing on private equity syndication and "Club Deals." It is the platform's mechanism for handling oversubscribed investment capacity, ensuring that scarce deal flow is distributed according to institutional priorities and regulatory tiers.

## Core Components

### 1. Deal Allocation Engine (`deal_allocation_srv.py`)
The platform's priority enforcement layer for investment capacity.
- **Priority Tiering**: Implements a strict allocation policy:
    1. **SFO (Single Family Office)**: Receives first-priority full-fill where possible.
    2. **UHNW (Ultra-High-Net-Worth)**: Receives pro-rata allocation of the remaining capacity.
    3. **HNW (High-Net-Worth)**: Allocated only if capacity remains, otherwise moved to the waitlist.
- **Pro-Rata Logic**: Automatically calculates fractional allocations when total client demand exceeds available deal capacity.

### 2. Club Deal Manager (`club_deal_manager.py`)
A tool for formation and syndication of private investment groups.
- **Syndication Calculations**: Determines the "Syndication Gap" (Total Deal Size vs. Core Platform Commitment).
- **Private Tease Dispatch**: Automates the distribution of deal "teasers" to a selected circle of private participants via the platform's messaging/Kafka bus.

### 3. Waitlist & Interest Manager (`waitlist_manager.py`)
Captures and ranks early-stage interest.
- **First-Look Timestamping**: Logs client interest with high-precision timestamps to maintain a fair "First-Look" order within priority buckets.
- **Priority Bucketing**: Automatically sorts waitlisted participants by client tier (e.g., placing SFOs at the head of the queue regardless of arrival time).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Private Deal Center** | Opportunities List | `club_deal_manager.create_club_deal()` (View deals) |
| **Deal Detail View** | Commitment Button | `waitlist_manager.log_interest()` |
| **Deal Detail View** | My Allocation Card | `deal_allocation_srv.allocate_oversubscribed_deal()` |
| **Admin Panel** | Allocation Resolver | `deal_allocation_srv.allocate_oversubscribed_deal()` |
| **SFO Dashboard** | Exclusive Access Ribbons | `waitlist_manager.log_interest()` (Priority status) |

## Dependencies
- `uuid`: Generates unique identifiers for deals, participants, and transfer tickets.
- `decimal`: Used for precision financial calculations in volume-based allocations.

## Usage Examples

### Resolving an Oversubscribed Deal Allocation
```python
from services.deal.deal_allocation_srv import DealAllocationService
from decimal import Decimal

alloc_svc = DealAllocationService()

# 10M Capacity, 15M Demand
commitments = [
    {"user_id": "sfo_1", "tier": "SFO", "amount": Decimal("8,000,000")},
    {"user_id": "uhnw_1", "tier": "UHNW", "amount": Decimal("5,000,000")},
    {"user_id": "uhnw_2", "tier": "UHNW", "amount": Decimal("2,000,000")},
]

results = alloc_svc.allocate_oversubscribed_deal(
    total_capacity=Decimal("10,000,000"),
    commitments=commitments
)

for res in results:
    print(f"User: {res['user_id']} | Status: {res['status']} | Allocated: ${res['allocated']:,.2f}")
```

### Logging Waitlist Interest
```python
from services.deal.waitlist_manager import WaitlistManager

wm = WaitlistManager()

# Log interest for a highly anticipated deal
result = wm.log_interest(
    deal_id="PE-SERIES-B-AI",
    user_id="client_uhnw_88",
    amount=500_000,
    tier="UHNW"
)

print(f"Waitlist Status: {result['status']} (Position: {result['waitlist_position']})")
```


---

## Source: service_debate.md

# Backend Service: Debate

## Overview
The **Debate Service** acts as the platform's "Decision Forensics" layer. It is responsible for recording the complete, immutable reasoning trail behind every AI-driven investment decision. By capturing the granular votes, dissenting opinions, and logical justifications of the multi-agent workforce, it provides the transparency required for institutional-grade AI governance.

## Core Components

### 1. Forensics Logger (`forensics_logger.py`)
The platform's "Black Box" recorder for agentic reasoning.
- **Decision Persistence**: Captures every investment proposal, the final decision (Buy/Sell/Hold), and the specific JSON-serialized votes of every agent involved in the debate.
- **Dissent Tracking**: Specifically records dissenting votes and the reasoning behind them, which is critical for post-trade analysis and understanding "edge case" risks that a majority consensus might have overlooked.
- **Audit Trails**: Links debate records to `proposal_id` and `symbol` for quick retrieval during compliance audits or performance reviews.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Admin Audit Console** | Decision Timeline | `forensics_logger.log_debate()` (Retrieved via DB) |
| **Market Terminal** | Agent Dissent Heatmap | `forensics_logger.log_debate()` |
| **Portfolio Detail** | "Why did we buy this?" Modal | `debate_logs` (Forensics retrieval) |
| **Compliance Station** | Regulatory Reporting | `forensics_logger.log_debate()` |

## Dependencies
- `utils.database_manager`: Handles the persistence of debate records to the central Postgres `debate_logs` table.
- `json`: Used to serialize complex multi-agent voting structures into queryable JSONB fields.

## Usage Examples

### Recording a Multi-Agent Decision Trail
```python
from services.debate.forensics_logger import forensics_logger

# Example multi-agent vote results
votes = [
    {"agent": "Strategist", "vote": "BUY", "confidence": 0.9, "reason": "Undervalued FCF"},
    {"agent": "Risk_Mgr", "vote": "HOLD", "confidence": 0.6, "reason": "Macro tailwinds unclear"},
    {"agent": "Market_Analyst", "vote": "BUY", "confidence": 0.85, "reason": "Bullish RSI breakout"}
]

# Log the outcome to the forensics database
forensics_logger.log_debate(
    proposal_id="PROP-7721-AAPL",
    symbol="AAPL",
    decision="BUY",
    votes=votes,
    metadata={"market_volatility": "Low", "model_version": "v2.1.0"}
)
```


---

## Source: service_economics.md

# Backend Service: Economics

## Overview
The **Economics Service** provides specialized macroeconomic and behavioral modeling tailored for the Ultra-High-Net-Worth (UHNW) segment. It moves beyond standard retail metrics (like CPI) to track the **CLEW Index** (Cost of Living Extremely Well) and provides structural insights into **Social Class Maintenance (SCM)**, ensuring that investment strategies account for the actual "lifestyles of the extremely wealthy" inflation.

## Core Components

### 1. CLEW Index Service (`clew_index_svc.py`)
Proprietary inflation tracking for the 0.1%.
- **UHNW Basket**: Tracks a specialized inflation basket including:
    - **Private Aviation**: Fuel, hangarage, and crew cost volatility.
    - **Tuition**: Historical 7% CAGR of Ivy League and elite primary education.
    - **Concierge Staff**: Wages for domestic staff and wealth management offices.
    - **Luxury Real Estate**: Maintenance and tax inflation for prime property holdings.
- **Inflation Delta**: Automatically calculates the spread between standard CPI and the CLEW Index to provide a "Real Yield" adjusted for high-end lifestyle maintenance.

### 2. Social Class Maintenance (SCM) Service (`scm_service.py`)
Predictive modeling for inter-generational wealth retention.
- **SCM Score**: A critical metric calculated as: `(Portfolio Yield - CLEW Inflation) / Lifestyle Burn`.
    - **Score > 1.0**: The family's wealth is expanding relative to their social class costs.
    - **Score < 1.0**: "Social Dilution" is occurring; the lifestyle is currently unsustainable by current portfolio performance.
- **Lifestyle Burn Projection**: Models how current spending will compound over 5, 10, and 20 years when adjusted for high-beta luxury inflation.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **UHNW Life Dashboard** | Personal Inflation Pulse | `clew_index_service.get_uhnwi_inflation_rate()` |
| **Strategist Station** | Social Class Health Meter | `scm_service.calculate_scm_score()` |
| **Planning Station** | Burn Projection Plot | `scm_service.project_lifestyle_burn()` |
| **Estate Detail** | Basket Allocator | `clew_index_service.calculate_personal_inflation()` |

## Dependencies
- `decimal`: Essential for high-precision inflation compounding and financial score calculations.
- `logging`: Records structural economic shifts for the platform's macro-agent history.

## Usage Examples

### Calculating an SCM Score for a SFO
```python
from services.economics.scm_service import SCMService
from decimal import Decimal

scm = SCMService()

# Portfolio yields 12%, Lifestyle burn is 4% of AUM
# CLEW Inflation is calculated internally (typically 6-8%)
score = scm.calculate_scm_score(
    portfolio_yield_pct=Decimal("0.12"),
    lifestyle_burn_pct=Decimal("0.04")
)

if score > 1.0:
    print(f"Status: Growth. SCM Score: {score}")
else:
    print(f"Status: Dilution Risk. SCM Score: {score}")
```

### Projecting Future Lifestyle Costs
```python
from services.economics.clew_index_svc import get_clew_index_service
from decimal import Decimal

clew_svc = get_clew_index_service()
current_spend = Decimal("2500000") # $2.5M annual burn

# Project spend in 10 years adjusted for CLEW inflation
rate = Decimal(str(clew_svc.get_uhnwi_inflation_rate()))
projected = current_spend * ((1 + rate) ** 10)

print(f"Current Spend: ${current_spend:,.2f}")
print(f"Projected Spend (10yrs): ${projected:,.2f} at {rate:.2%} CLEW rate")
```


---

## Source: service_education.md

# Backend Service: Education

## Overview
The **Education Service** is the platform's knowledge transfer and financial literacy layer. It provides a comprehensive suite of tools ranging from institutional-grade **Learning Management Systems (LMS)** to automated **529 Education Savings** planning. It is specifically designed to support multi-generational wealth stewardship through specialized training for heirs and family office participants.

## Core Components

### 1. Learning Management System (LMS) (`learning_management_service.py`)
The foundational engine for educational content delivery.
- **Course Lifecycle**: Manages the creation, enrollment, and completion status of educational modules.
- **Progress Tracking**: Monitors lesson-level activity and calculates completion percentages in real-time.
- **Automated Certification**: Issues verifiable completion certificates once a curriculum assessment threshold is met.

### 2. Heir Training Portal (`heir_lms.py`)
Specialized curriculum tracking for multi-generational wealth.
- **Governance Training**: Tracks mandatory participation in modules like "Family Board Governance" and "Strategic Philanthropy."
- **Performance Thresholds**: Enforces a "Certified" status only for heirs who pass assessments with high scores, ensuring competence before significant wealth transitions.

### 3. Education Savings Automation (`glide_path_529.py`)
Financial planning logic for future tuition costs.
- **Dynamic Glide Paths**: Automatically shifts portfolio allocations from aggressive (90% Equity) to conservative (50% Cash) based on the "Years to Enrollment" metric.
- **529 Optimization**: Recommends risk-adjusted buckets specifically for the 529 education savings vehicle.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Education Hub** | My Courses Dashboard | `learning_management_service.enroll_user()` |
| **Education Hub** | Lesson Viewer | `learning_management_service.update_progress()` |
| **Family Office Station** | Heir Training Tracker | `heir_lms.record_progress()` |
| **Education Planner** | 529 Glide Path Chart | `glide_path_recommender_529.recommend_allocation()` |
| **Profile / Awards** | Certificate Wallet | `learning_management_service.issue_certificate()` |

## Dependencies
- `pydantic`: For strictly-typed education models (`Course`, `Enrollment`, `Certificate`).
- `services.system.cache_service`: Provides high-speed persistence for progress tracking and certificate storage.

## Usage Examples

### Tracking Heir Training Progress
```python
from services.education.heir_lms import HeirLMSService
from uuid import uuid4

heir_svc = HeirLMSService()

# Record a score for a mandatory governance module
result = heir_svc.record_progress(
    heir_id=uuid4(),
    course_id="GOV-201",
    score=88
)

print(f"Certification Status: {result['certified']}")
print(f"LMS Message: {result['status']}")
```

### Retrieving 529 Allocation Recommendations
```python
from services.education.glide_path_529 import GlidePathRecommender529

recommender = GlidePathRecommender529()

# child is 10 years away from college
allocation = recommender.recommend_allocation(years_to_enrollment=10)

print("Target 529 Allocation:")
for asset_class, weight in allocation.items():
    print(f"- {asset_class}: {weight*100}%")
```


---

## Source: service_energy.md

# Backend Service: Energy

## Overview
The **Energy Service** manages the platform's transition into the physical energy and deep-tech sectors. It provides dual-layer capabilities: (1) real-time operational management of renewable energy assets (Solar, Battery Storage) and grid arbitrage, and (2) high-frontier investment research focusing on breakthroughs in fusion energy and proprietary patent analysis.

## Core Components

### 1. Grid Arbitrage & Battery Hub (`battery_mgr.py`)
Optimizes energy storage assets for profitability.
- **Dynamic Grid Arbitrage**: Monitors real-time grid prices and automatically triggers "CHARGE" cycles during off-peak periods (<$0.10) and "DISCHARGE" cycles during peak periods (>$0.40).
- **Asset Health**: Monitors charge levels and remaining runtime for residential/commercial battery banks (e.g., Tesla Powerwalls).

### 2. High-Frontier Energy Tech
- **Fusion Reactor Simulation (`fusion_sim.py`)**: Provides high-fidelity telemetry for fusion energy investments. Tracks critical metrics like **Plasma Temperature**, **Magnetic Confinement Stability**, and the **Q-factor** (Energy Gain vs. Input).
- **Patent Discovery Bot (`patent_bot.py`)**: A "Deep Tech" aggregator that scans USPTO, WIPO, and EPO databases for keywords like "Low Energy Nuclear Reactions (LENR)," "Zero Point," and "Solid State." Includes a "Scientific Validity" scoring layer to filter high-potential disruptions from noise.

### 3. Physical Asset Monitoring
- **Solar Monitor (`solar_monitor.py`)**: Tracks real-time photovoltaic output and efficiency.
- **Generator Service (`generator_svc.py`)**: Manages backup and peaking generator assets.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Energy Station** | Grid Price Arbitrage Table | `battery_manager.optimize_cycle()` |
| **Energy Station** | Facility Battery Health | `battery_manager.get_status()` |
| **Deep Tech Research** | Fusion Reactor Telemetry | `fusion_reactor_sim.get_telemetry()` |
| **Deep Tech Research** | New Patent Alerts | `patent_aggregator.scan_patents()` |
| **Strategist Station** | Asset Replacement Value | `solar_monitor.py` (Efficiency metrics) |

## Dependencies
- `random`: Used in simulations to model plasma fluctuations and technical volatility.
- `logging`: Records structural energy events, including "SCRAM" emergency shutdowns and patent flags.

## Usage Examples

### Executing Grid Arbitrage Optimization
```python
from services.energy.battery_mgr import BatteryManagerService

battery = BatteryManagerService()

# Simulate a peak price event ($0.45/kWh)
decision = battery.optimize_cycle(grid_price=0.45)

if decision == "DISCHARGE":
    print("Action: Selling energy back to the grid at peak rates.")
    print(f"Current Charge: {battery.get_status()['charge_level']}")
```

### Scanning for Fusion Energy Breakthroughs
```python
from services.energy.patent_bot import PatentAggregatorService

bot = PatentAggregatorService()

# Scan global databases for new filings
findings = bot.scan_patents()

for patent in findings:
    analysis = bot.analyze_patent(patent['id'])
    if analysis['market_potential'] == "DISRUPTIVE":
        print(f"ALERT: Disruptive energy technology detected: {patent['title']}")
```


---

## Source: service_enterprise.md

# Backend Service: Enterprise

## Overview
The **Enterprise Service** provides the structural framework for institutional and B2B clients. It enables the creation of complex organizational hierarchies, multi-level team management, and granular resource sharing. This service is the foundation for collaborative wealth management, allowing multiple stakeholders (e.g., family members, advisors, and trustees) to securely interact with shared portfolios and reports.

## Core Components

### 1. Enterprise Management Engine (`enterprise_service.py`)
Handles the "bones" of corporate and family office structures.
- **Organizational Hierarchies**: Supports nested organizations, allowing a parent holding company to manage multiple sub-entities or family branches.
- **Team Management**: Facilitates the creation of functional teams (e.g., "Investment Committee," "Tax Planning Team") within an organization.
- **Role-Based Membership**: Maps users to teams with specific roles (e.g., `Admin`, `Member`, `Contributor`), integrated with the platform's RBAC (Role-Based Access Control) system.

### 2. Multi-User Collaboration (`multi_user_service.py`)
The sharing and permissions layer for institutional assets.
- **Shared Resources**: Enables portfolios, custom reports, and dashboards to be shared across an entire team or organization.
- **Granular Permissions**: Supports fine-grained access control (Read/Write/Execute) on a per-resource, per-team basis.
- **Activity Logging**: (Inferred) Tracks modifications to shared resources to maintain a collaborative audit trail.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Enterprise Console** | Organization Tree | `enterprise_service.create_organization()` |
| **Enterprise Console** | Team Member List | `enterprise_service.add_team_member()` |
| **Portfolio Terminal** | Share Portfolio Modal | `multi_user_service.share_resource()` |
| **Resource Library** | Shared Documents Grid | `multi_user_service.get_shared_resources()` |
| **Settings / Roles** | Permission Matrix | `enterprise_service.add_team_member()` (Role management) |

## Dependencies
- `schemas.enterprise`: Defines the Pydantic models for `Organization`, `Team`, and `SharedResource`.
- `services.system.cache_service`: Provides long-term persistence for organizational structures and sharing records.
- `RBACService`: (Integration) Enforces the actual access boundaries defined by enterprise roles.

## Usage Examples

### Building a Family Office Hierarchy
```python
from services.enterprise.enterprise_service import get_enterprise_service

enterprise = get_enterprise_service()

# Create a master Family Office org
mfo = await enterprise.create_organization(name="East-West Multi-Family Office")

# Create a specialized Investment Team
inv_team = await enterprise.create_team(
    organization_id=mfo.organization_id, 
    team_name="Investment Committee"
)

# Add a Senior Advisor
await enterprise.add_team_member(
    team_id=inv_team.team_id,
    user_id="user_advisor_123",
    role="SENIOR_ADVISOR"
)
```

### Sharing a Portfolio with a Team
```python
from services.enterprise.multi_user_service import get_multi_user_service

mu_svc = get_multi_user_service()

# Share a specific portfolio with "ReadOnly" permissions for the whole team
shared_ref = await mu_svc.share_resource(
    resource_type="portfolio",
    resource_id="port_aggress_growth_01",
    team_id="team_family_office_A",
    permissions={"read": True, "write": False}
)

print(f"Resource shared successfully. ID: {shared_ref.resource_id}")
```


---

## Source: service_estate.md

# Backend Service: Estate

## Overview
The **Estate Service** is the platform's legacy preservation and multi-generational transfer engine. It enables clients to architect complex estate plans, simulate inheritance outcomes across decades, and enforce idiosyncratic trust stipulations (e.g., spendthrift clauses, milestone-based payouts). It includes specialized calculators for estate taxes, probate fees, and generation-skipping transfer (GST) impacts.

## Core Components

### 1. Estate Planning Engine (`estate_planning_service.py`)
The central orchestrator for legacy architecture.
- **Beneficiary Management**: Manages primary and contingent beneficiaries with precise allocation percentages.
- **Tax Optimization**: Automatically calculates estimated Federal Estate Tax based on current exemptions ($12M+ in 2024) and progressive tax brackets (up to 40%).
- **Asset Allocation**: Maps the total portfolio value to specific beneficiary buckets in real-time.

### 2. Inheritance Simulator (`inheritance_simulator.py`)
A predictive tool for long-term legacy visualization.
- **Wealth Projection**: Simulates the compound growth of an estate (defaulting to 6% CAGR) over 10-30 years.
- **After-Tax Projections**: Calculates the actual "net-to-heir" inheritance after accounting for spousal exemptions and potential inheritance taxes.
- **Scenario Modeling**: Allows users to compare different estate architectures (e.g., "Full Trust" vs. "Direct Transfer") side-by-side.

### 3. Trust Stipulations & Clauses (`stipulation_service.py`)
Enforces the specific "rules of the legacy."
- **Clause Management**: Stores and retrieves behavioral stipulations for trusts, such as "Crummey" notices or "Spendthrift" provisions.
- **Milestone Triggers**: Supports condition-based distributions (e.g., distributions triggered by reaching a certain age or graduating from an accredited university).

### 4. Beneficiary Waterfall (`beneficiary_tree.py`)
- **Primary & Contingent Logic**: Validates that beneficiary waterfalls sum to 100% and correctly handle contingent paths if primary beneficiaries are unavailable.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Estate Dashboard** | Beneficiary Waterfall Tree | `beneficiary_tree.validate()` |
| **Estate Dashboard** | Tax Liability Pulse | `estate_planning_service.calculate_estate_tax()` |
| **Inheritance View** | Multi-Decade Projection Chart | `inheritance_simulator.simulate_inheritance()` |
| **Trust Setup Wizard** | Clause Library | `stipulation_service.get_stipulations()` |
| **Planning Station** | Scenario Comparison Grid | `inheritance_simulator.compare_scenarios()` |

## Dependencies
- `schemas.estate`: Defines the complex Pydantic models for `EstatePlan`, `Beneficiary`, and `InheritanceProjection`.
- `services.portfolio.portfolio_aggregator`: Streams real-time portfolio value as the baseline for estate calculations.
- `services.system.cache_service`: Provides low-latency storage for active estate plans and simulation results.

## Usage Examples

### Running a 20-Year Inheritance Simulation
```python
from services.estate.inheritance_simulator import get_inheritance_simulator

sim = get_inheritance_simulator()

# Project current estate plan 20 years into the future
projections = await sim.simulate_inheritance(
    plan_id="estate_plan_jones_001",
    projection_years=20
)

for p in projections:
    print(f"Beneficiary: {p.beneficiary_id}")
    print(f"Estimated Pre-Tax: ${p.projected_inheritance:,.2f}")
    print(f"Estimated After-Tax: ${p.after_tax_inheritance:,.2f}")
```

### Adding a Milestone-Based Stipulation
```python
from services.estate.stipulation_service import StipulationService
from uuid import uuid4

stip_svc = StipulationService()
trust_id = uuid4()

# Add a university graduation requirement
stip_svc.add_stipulation(
    trust_id=trust_id,
    clause_type="MILESTONE",
    description="Recipient must graduate from an accredited university before first payout.",
    trigger_condition="degree_verification == True"
)
```


---

## Source: service_evolution.md

# Backend Service: Evolution

## Overview
The **Evolution Service** is the platform's self-improvement and optimization laboratory. It utilizes genetic algorithms to evolve investment strategies by treating agent parameters as "genes." By performing crossover, mutation, and hybrid splicing, the service ensures that the platform's alpha-generating logic adapts to changing market regimes rather than remaining static.

## Core Components

### 1. Genetic Architect (`gene_logic.py`)
The foundational layer for strategy mutation and hybridization.
- **Crossover & Splice**: Combines "genomes" from two successful parent agents to create a hybrid offspring. It uses uniform crossover to inherit successful parameters from both sides.
- **Gene Mutation**: Applies subtle random variations to strategy parameters (e.g., tweaking an RSI threshold from 30 to 32) within safe mathematical bounds.
- **Gene Pulse**: Calculates the internal "vitality" of an agent. It tracks how often specific genes are activated in decisions and flags "volatile" genes that may be prone to drifting into unprofitable behavior.

### 2. Chronological Auditor (`playback_service.py`)
Facilitates the validation of evolved strategies in a virtual sandbox.
- **Genome Playback**: Maps genetic markers back to actionable strategy parameters and re-runs historical market cycles to see how a "mutated" agent would have performed.
- **Strategy Sandboxing**: Integrates with the `BacktestEngine` to provide a risk-free environment for testing "Generation Zero" hybrid agents before they are deployed to production environments.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Evolution Lab** | Gene Splicer Wizard | `gene_logic.splice_agents()` |
| **Evolution Lab** | Mutation Risk Heatmap | `gene_logic.get_gene_pulse()` |
| **Strategy Detail** | "Replay Master" (Backtest) | `playback_service.run_playback()` |
| **Agent Performance** | Genetic Lineage Tree | `gene_logic.splice_agents()` (Parent ID links) |
| **Research Station** | Pulse Vitality Meter | `gene_logic.get_gene_pulse()` |

## Dependencies
- `services.analysis.genetic_distillery`: Provides the base `Genome` schema for all agentic genetic material.
- `services.analysis.backtest_engine`: Used by the playback service for historical simulation.
- `uuid`: Generates unique identifiers for newly "born" hybrid agents.

## Usage Examples

### Splicing Two Successful Agents
```python
from services.evolution.gene_logic import get_gene_splicer

splicer = get_gene_splicer()

# Splicing "Strategist_V1" and "Risk_Mgr_V2"
child = splicer.splice_agents(
    parent1_id="AG-STRAT-01",
    parent2_id="AG-RISK-02",
    parent1_genes={"rsi_period": 14, "momentum_thresh": 0.8},
    parent2_genes={"stop_loss": 0.05, "rsi_period": 12},
    bounds={"rsi_period": (10, 20), "stop_loss": (0.02, 0.1)}
)

print(f"Hybrid Agent Created: {child['id']}")
print(f"Inherited Genes: {child['genes']}")
```

### Checking an Agent's Genetic Vitality
```python
from services.evolution.gene_logic import GeneSplicer

splicer = GeneSplicer()
genes = {"rsi_buy": 30, "rsi_sell": 70, "vol_spike": 1.5}

pulse = splicer.get_gene_pulse(agent_id="AGENT-X44", genes=genes)

print(f"Agent Vitality Score: {pulse['overall_vitality']*100:.1f}%")
for entry in pulse['pulse']:
    print(f"Gene: {entry['gene']} | Status: {entry['status']} (Instability: {entry['instability']})")
```


---

## Source: service_execution.md

# Backend Service: Execution

## Overview
The **Execution Service** is the platform's high-fidelity trading and settlement hub. It is responsible for transforming high-level investment decisions into optimal market orders while minimizing slippage, hiding institutional intent (IcebergING), and adhering to specific execution benchmarks like **VWAP** (Volume-Weighted Average Price) and **TWAP** (Time-Weighted Average Price).

## Core Components

### 1. Smart Execution Engine (`smart_execution_service.py`)
The platform's dedicated algorithm suite for trade optimization.
- **VWAP / TWAP Execution**: Automatically slices large parent orders into child orders based on historical volume profiles (U-Shape) or fixed time intervals to achieve benchmark targets.
- **Implementation Shortfall**: Provides a "Patient-to-Urgent" slider logic that balances the risk of market impact (slippage) against the risk of delayed execution.

### 2. Smart Order Router (SOR) (`smart_sor.py`)
Determines the *how* and *where* of order routing.
- **Iceberg Orders**: Automatically fragments orders exceeding specified thresholds (e.g., 500 shares) to hide the true size of institutional trades from public order books.
- **Volatility-Aware Routing**: Switches between **Limit Orders** (to protect price in high-volatility regimes) and **Market Orders** (for immediate liquidity in stable regimes).

### 3. Algo Engine (`algo_execution.py`)
The mathematical generator for execution schedules.
- **Volume Profiling**: Utilizes a tiered "bucket" approach to model intraday liquidity, ensuring that order intensity matches expected market volume (e.g., morning and close intensity).

### 4. Philanthropy Execution (`philanthropy_service.py`)
- **Impact Trades**: Manages the specialized execution of trades intended for charitable impact, potentially involving tax-efficient "In-Kind" asset donations and specialized settlement workflows.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trading Terminal** | Order Ticket (Advanced) | `smart_sor.determine_order_strategy()` |
| **Trading Terminal** | Execution Progress Pulse | `smart_execution_service.execute_twap()` |
| **Order History** | Slippage Auditor | `execution_result.market_impact` |
| **Impact Hub** | Charitable Trade Wizard | `philanthropy_service` (Trade settlement) |
| **Admin Panel** | Algo Baseline Config | `algo_engine.DEFAULT_VOLUME_PROFILE` |

## Dependencies
- `schemas.orders`: Defines the standard `ExecutionStrategy` and `ExecutionResult` types.
- `services.system.cache_service`: Maintains real-time state for active execution schedules.
- `MarketDataService`: (Integration) Supplies real-time volatility and volume metrics for SOR decisions.

## Usage Examples

### Dispatching a VWAP Execution Schedule
```python
from services.execution.smart_execution_service import get_smart_execution_service

exec_svc = get_smart_execution_service()

# Execute 10,000 shares of SPY over 2 hours using VWAP
executions = await exec_svc.execute_vwap(
    symbol="SPY",
    total_quantity=10000,
    time_window_minutes=120
)

for ex in executions:
    print(f"Slice Filled: {ex.filled_quantity} @ ${ex.average_price:.2f} | Strategy: {ex.execution_strategy}")
```

### Determining Optimal Order Strategy via SOR
```python
from services.execution.smart_sor import get_sor

sor = get_sor()

# 5,000 shares in a high-volatility market (4%)
strategy = sor.determine_order_strategy(
    symbol="TSLA",
    quantity=5000,
    volatility=0.04
)

print(f"Routing Style: {strategy['execution_style']}") # Likely ICEBERG
print(f"Order Type: {strategy['order_type']}")         # Likely LIMIT
print(f"Reason: {strategy.get('reason', 'N/A')}")
```


---

## Source: service_external.md

# Backend Service: External

## Overview
The **External Service** acts as the platform's universal bridge to the outside world. It provides specialized **Adapters** that integrate niche alternative asset classes—such as luxury watches and blue-chip art—into the platform's unified portfolio view. Additionally, it integrates with institutional ecosystems like **Salesforce** to synchronize high-fidelity relationship data and deal-sourcing signals.

## Core Components

### 1. Alternative Asset Adapters
- **Chrono24 Adapter (`chrono24_adapter.py`)**: A valuation feed for the luxury watch market. It tracks pricing for elite references (e.g., Rolex, Patek Philippe) to ensure that a client's physical "Wrist Portfolio" is marked-to-market alongside their liquid assets.
- **Masterworks Adapter (`masterworks_adapter.py`)**: Connects to the fractional art secondary market. It fetches current appraisal values and market pricing for high-value artwork held by the platform's UHNW clients.

### 2. Enterprise CRM Integration
- **Salesforce Adapter (`salesforce_adapter.py`)**: The data bridge for institutional relationships.
    - **Contact Synchronization**: Automatically pulls contacts tagged as "Institutional" or "UHNW" into the platform's internal network graph.
    - **Deal Signal Extraction**: Scans activity logs for keywords like "Pitch Deck" or "Investment Opportunity" to proactively flag potential deal flow for the internal investment committee.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Alternative Assets** | Watch Collection List | `chrono24_adapter.fetch_watch_value()` |
| **Alternative Assets** | Art Valuation Card | `masterworks_adapter.fetch_artwork_value()` |
| **Network Hub** | Salesforce Sync Panel | `salesforce_adapter.sync_contacts()` |
| **Deal Sourcing** | CRM Signal Feed | `salesforce_adapter.fetch_deal_signal()` |
| **Portfolio Detail** | Physical Asset Breakdown | All Alternative Adapters |

## Dependencies
- `uuid`: Used for mapping external contacts and assets to internal platform identifiers.
- `random`: Utilized in mock adapters as "Valuation Perturbators" (simulating market fluctuations in testing environments).

## Usage Examples

### Sourcing a Deal Signal from Salesforce
```python
from services.external.salesforce_adapter import SalesforceAdapter

sf = SalesforceAdapter()

# Scan for activity from a high-priority institutional contact
signal = sf.fetch_deal_signal(contact_name="Sarah Venture")

if signal['signal_strength'] == "HIGH":
    print(f"ALERT: Significant deal signal detected from {signal['contact']}")
    print(f"Recent Activity: {signal['recent_activity']}")
```

### Valuation of a Luxury Asset
```python
from services.external.chrono24_adapter import Chrono24Adapter

chrono = Chrono24Adapter()

# Fetch latest valuation for a specific reference
valuation = chrono.fetch_watch_value(brand="Patek Philippe", reference="5711/1A")

print(f"Current Market Value: ${valuation['market_value_usd']:,.2f}")
print(f"Source: {valuation['source']} | Condition: {valuation['condition_grade']}")
```


---

## Source: service_finance.md

# Backend Service: Finance

## Overview
The **Finance Service** provides the platform's quantitative mathematical chassis. It handles specialized institutional-grade calculations ranging from **Mortgage Amortization** and equity gain tracking to the deep-dive analysis of **Total Cost of Ownership (TCO)** and **Fee Margins**. It is designed to expose the "hidden costs" of investment strategies, such as tax and cash drag, and compare them against passive "Beta" benchmarks.

## Core Components

### 1. Amortization Tracker (`amortization.py`)
Tracks the paydown of collateralized debt.
- **Equity Gain Logic**: Automatically updates the equity value of a real estate asset or business loan by resolving the monthly principal/interest split.
- **Paydown Analysis**: Integrates with the platform's balance sheet to provide an accurate "Net Worth" pulse as liabilities decrease.

### 2. Fee Margin Engine (`fee_margin_calc.py`)
Architects transparency for institutional fee structures.
- **Profitability Analysis**: Calculates the net operational margin on AUM fees after subtracting management costs and the inherent **Cost of Beta** (benchmarked at 3 bps / 0.03%).
- **Margin Thresholds**: Flags "Pressured" vs. "High" profitability strategies for Multi-Family Offices (MFOs) managing complex fee splits.

### 3. TCO & Opportunity Cost (`op_cost_calculator.py`)
Exposes the structural efficiency of investment strategies.
- **Total Cost of Ownership (TCO)**: Aggregates Management Fees, Bid-Ask Spreads, Tax Drag, and Cash Drag into a single, unified efficiency percentage.
- **Efficiency Gap**: Quantifies the delta between a custom strategy and a standard low-cost index (Cost of Beta), helping advisors justify active management premiums.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Real Estate Detail** | Equity Growth Meter | `amortization_tracker.get_equity_gain()` |
| **Family Office Station** | Strategy Margin Ledger | `fee_margin_calculator.calculate_margin()` |
| **Portfolio Audit** | TCO Transparency Card | `op_cost_calculator.calculate_tco()` |
| **Investment Planner** | "Gap vs Beta" Sparklines | `op_cost_calculator.compare_to_beta()` |
| **Wealth Dashboard** | Debt-to-Equity Pulse | `amortization_tracker` (Balance updates) |

## Dependencies
- `logging`: Records structural margin changes and efficiency flags for the platform's financial history.

## Usage Examples

### Calculating the TCO of an Active Growth Strategy
```python
from services.finance.op_cost_calculator import OperationalCostCalculator

calc = OperationalCostCalculator()

# Calculate TCO: 1% fee, 0.2% spread, 0.5% tax drag, 0.1% cash drag
tco = calc.calculate_tco(
    strategy_name="Aggressive Growth Aggregator",
    management_fee=0.0100,
    avg_spread=0.0020,
    tax_drag=0.0050,
    cash_drag=0.0010
)

gap = calc.compare_to_beta(strategy_tco=tco)
print(f"Total Cost of Ownership: {tco:.2%}")
print(f"Efficiency Gap vs Passive Beta: {gap*10000:.0f} bps")
```

### Analyzing Institutional Profitability
```python
from services.finance.fee_margin_calc import FeeMarginCalculator

fmc = FeeMarginCalculator()

# 0.75% Gross Fee, 0.20% Admin/Op Cost
analysis = fmc.calculate_margin(gross_fee=0.0075, operational_cost=0.0020)

print(f"Net Operational Fee: {analysis['net_fee_pct']:.2%}")
print(f"Surplus vs Beta Benchmark: {analysis['margin_vs_beta_bps']} bps")
print(f"Strategic Viability: {analysis['profitability']}")
```


---

## Source: service_fraud.md

# Backend Service: Fraud

## Overview
The **Fraud Service** serves as the platform's independent security and integrity auditor. Its primary mission is to detect reporting anomalies and structural fraud patterns (e.g., Ponzi schemes) that might otherwise be obscured by traditional performance metrics. By enforcing strict data-provenance rules and analyzing return volatility, it protects clients from third-party advisor malpractice.

## Core Components

### 1. Anti-Madoff Guard (`anti_madoff_guard.py`)
A specialized detection engine for reporting-based fraud.
- **Statement Source Validation**: Implements a "Zero-Trust" policy for financial data. It mandates that any statement or valuation data must originate directly from a **Qualified Custodian**, flagging any data provided solely by an investment advisor as a high-risk security violation.
- **Return Striation Detection**: Uses statistical analysis (standard deviation) to identify suspiciously "smooth" return profiles. If a manager reports consistent positive monthly returns with a volatility threshold below 0.1% (Standard Deviation < 0.001) over a 12-month period, the service triggers a `MADOFF_PATTERN` alert.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Institutional Audit** | Fraud Alert Table | `anti_madoff_guard.detect_return_striation()` |
| **Custodian Hub** | Data Provenance Shield | `anti_madoff_guard.validate_statement_source()` |
| **Manager Detail** | Volatility Consistency Meter | `anti_madoff_guard.detect_return_striation()` |
| **Compliance Station** | System Security Pulse | All Fraud alerts |

## Dependencies
- `numpy`: Used for high-precision statistical standard deviation calculations over return series.

## Usage Examples

### Detecting Suspiciously Consistent Returns
```python
from services.fraud.anti_madoff_guard import AntiMadoffGuard

guard = AntiMadoffGuard()

# 12 months of "too good to be true" 1% monthly returns
fake_returns = [0.0101, 0.0099, 0.0102, 0.01, 0.0098, 0.0101, 0.0102, 0.01, 0.0099, 0.0101, 0.01, 0.0102]

is_fraudulent = guard.detect_return_striation(returns=fake_returns)

if is_fraudulent:
    print("CRITICAL ALERT: Potential Ponzi pattern detected (Low Volatility Striation)")
```

### Validating Statement Provenance
```python
from services.fraud.anti_madoff_guard import AntiMadoffGuard

guard = AntiMadoffGuard()

# Scenario: Advisor uploads a PDF they authored themselves
is_valid = guard.validate_statement_source(
    provider_name="Jones Wealth Advisor LLC",
    custodian_name="Fidelity Institutional"
)

if not is_valid:
    print("ACTION BLOCKED: Data must originate from a verified custodian source.")
```


---

## Source: service_funds.md

# Backend Service: Funds

## Overview
The **Funds Service** manages the platform's institutional pooled investment products. It handles the lifecycle of index funds, tracks massive capital flows (In/Out) across the platform, and provides a sophisticated **Tradability Classification** layer that ensures large institutional trades are only executed in sufficiently liquid markets with manageable geopolitical risk.

## Core Components

### 1. Index Fund Master (`index_fund_service.py`)
The central registry for the platform's fund offerings.
- **Product Management**: Handles the registration of new index products (ETFs/Mutual Funds) and manages their metadata (Ticker, Name, Fund Type).
- **AUM Tracking**: Dynamically updates the current Assets Under Management (AUM) for each fund, which serves as the baseline for liquidity and fee calculations.

### 2. Capital Flow Processor (`flow_processor.py`)
Monitors the "circulatory system" of institutional capital.
- **Net Flow Analysis**: Tracks daily net inflows and outflows at the ticker level.
- **Outflow Alerts**: Automatically flags "Significant Outflows" (threshold: -$1B) to warn the investment committee of potential institutional flight.
- **Market Impact Multipliers**: Calculates the expected multiplier effect of capital flows on a fund's underlying market cap.

### 3. Tradability Classifier (`tradability_classifier.py`)
An institutional risk guardrail for trade execution.
- **Liquidity Tiering**: Categorizes assets into `HIGHLY_LIQUID`, `LIQUID`, `MODERATE`, or `ILLIQUID` tiers based on the ratio of Average Daily Volume (ADV) to total fund AUM.
- **Geopolitical Risk Filter**: Factors in "Country Repatriation Risk" to identify restricted markets where capital may be trapped or liquidity may evaporate.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Fund Supermarket** | Index Catalog Grid | `index_fund_service.list_funds()` |
| **Mission Control** | Whale Flow Radar | `flow_processor.process_flow()` (Outflow alerts) |
| **Trading Terminal** | Liquidity Shield | `tradability_classifier.calculate_tradability_score()` |
| **Admin Station** | AUM Management Console | `index_fund_service.update_aum()` |
| **Institutional Station** | Restricted Market Map | `tradability_classifier` (Country risk flags) |

## Dependencies
- `schemas.index_fund`: Defines the Pydantic models for `IndexFund` and `IndexFundCreate`.
- `logging`: Records structural fund events, specifically "Significant Outflow" alerts.

## Usage Examples

### Classifying an Emerging Market Index Fund
```python
from services.funds.tradability_classifier import TradabilityClassifier

classifier = TradabilityClassifier()

# Example: EEM (Emerging Markets) with moderate country risk
classification = classifier.calculate_tradability_score(
    ticker="EEM",
    avg_volume=50_000_000,
    aum=25_000_000_000,
    country_risk=6 # Scale 0-10
)

print(f"Ticker: {classification['ticker']} | Tier: {classification['tier']}")
print(f"Tradability Score: {classification['score']}/100")
if classification['is_restricted']:
    print("WARNING: Capital controls detected. Trading limited.")
```

### Processing a Whale Inflow
```python
from services.funds.flow_processor import FlowProcessor

fp = FlowProcessor()

# $500M inflow into SPY
flow_report = fp.process_flow({
    "ticker": "SPY",
    "net_flow_usd": 500_000_000
})

print(f"Net Flow: ${flow_report['net_flow']:,.2f}")
print(f"Estimated Market Impact: ${flow_report['impact_on_market_cap']:,.2f}")
```


---

## Source: service_growth.md

# Backend Service: Growth

## Overview
The **Growth Service** is the platform's primary engine for modeling and tracking private equity and venture capital investments. It handles the complex mathematics of cap-table management, funding round dilution, and exit waterfalls, enabling institutional and UHNW clients to forecast the longitudinal growth of their private "Venture" holdings.

## Core Components

### 1. Venture Modeling Engine (`venture_service.py`)
The platform's dedicated calculator for private market liquidity events.
- **Exit Waterfall Logic**: Automatically resolves the distribution of proceeds during a liquidity event (M&A/IPO). It accounts for **Liquidation Preferences** (1x, 2x, etc.), **Participating Preferred** rights, and the remaining common pool.
- **Dilution Simulator**: Models the impact of new funding rounds on existing shareholders. It calculates pre/post-money valuations, price-per-share increments, and the resulting dilution percentages for early-stage investors.
- **Share Class Management**: Defines the specific rights and preferences of different investment series (e.g., Series A, Seed, Common).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Growth/Venture Station** | Exit Waterfall Simulator | `venture_service.calculate_waterfall()` |
| **Growth/Venture Station** | Cap-Table Dilution Tool | `venture_service.simulate_dilution()` |
| **Portfolio Detail** | Private Round Timeline | `venture_service` (Round history) |
| **Strategist Station** | Potential Exit Valuation | `venture_service.calculate_waterfall()` |

## Dependencies
- `pydantic`: Uses `ShareClass` models to enforce structure on investment terms.

## Usage Examples

### Running an Exit Waterfall Calculation
```python
from services.growth.venture_service import get_venture_service, ShareClass

growth_svc = get_venture_service()

# 50M Exit Scenario
cap_table = [
    ShareClass(name="Series A", shares=1_000_000, price_per_share=5.0, liquidation_preference=1.0, is_participating=True),
    ShareClass(name="Seed", shares=500_000, price_per_share=2.0, is_preferred=True)
]

waterfall = growth_svc.calculate_waterfall(
    exit_value=50_000_000,
    cap_table=cap_table,
    common_shares=5_000_000
)

print(f"Distributable Proceeds: ${waterfall['exit_value']:,.2f}")
for name, payout in waterfall['payouts'].items():
    print(f"{name}: Total Payout ${payout['total_payout']:,.2f}")
```

### Simulating a Series B Dilution
```python
from services.growth.venture_service import VentureService

vs = VentureService()

# 10M new investment on 40M pre-money
round_sim = vs.simulate_dilution(
    current_shares=10_000_000,
    new_investment=10_000_000,
    pre_money_valuation=40_000_000
)

print(f"Post-Money Valuation: ${round_sim['post_money']:,.2f}")
print(f"Dilution to Existing: {round_sim['dilution_percentage']:.2f}%")
print(f"New Share Price: ${round_sim['price_per_share']:.2f}")
```


---

## Source: service_hr.md

# Backend Service: HR

## Overview
The **HR Service** is a specialized personnel management engine tailored for the unique requirements of **Family Offices**. Unlike traditional corporate HR systems, this service focuses on "Heir Governance," institutional role management for descendants, and the balancing of hard performance KPIs with familial discretion. It is designed to track "Social Maintenance" value and identify structural nepotism within the family's enterprise holdings.

## Core Components

### 1. Heir Governance Engine (`heir_governance_svc.py`)
Manages the employment and compensation lifecycle for family descendants.
- **Productivity Evaluation**: Audits heir roles by comparing their discretionary salary against market-rate averages. It enforces a transparency policy that flags any role with a >1.5x pay premium as a "Cushey Job" (Nepotism), allowing for clear distinction between market-aligned roles and family support roles.
- **Discretionary KPI Overrides**: Implements a nuanced performance scoring system that balances "Hard KPIs" (40% weight) with "Family Discretion" (60% weight). This allows family principals to maintain executive control over internal performance metrics for family members.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Governance Hub** | Heir Productivity Audit | `heir_governance_svc.evaluate_role_productivity()` |
| **Governance Hub** | KPI Discretion Slider | `heir_governance_svc.apply_discretionary_kpi_override()` |
| **Family Ops Detail** | Staff Premium Ledger | `heir_governance_svc.evaluate_role_productivity()` |
| **Admin Station** | Nepotism Risk Heatmap | `heir_governance_svc` (Status flags) |

## Dependencies
- `logging`: Records audit logs of role flags (Nepotism) and discretionary overrides for historical governance transparency.

## Usage Examples

### Auditing an Heir's Role Premium
```python
from services.hr.heir_governance_svc import HeirGovernanceService
from uuid import uuid4

hr_svc = HeirGovernanceService()
heir_id = uuid4()

# Evaluate an "Executive VP" role paying 300k vs 150k market average
audit = hr_svc.evaluate_role_productivity(
    heir_id=heir_id,
    role_title="Executive VP of Lifestyle",
    salary=300000.0,
    market_rate_avg=150000.0
)

print(f"Role Status: {audit['status']}")
print(f"Pay Premium: {audit['pay_premium_pct']}% above market")
print(f"Social Maintenance Value: {audit['social_maintenance_value']}")
```

### Applying a Family Discretion Override
```python
from services.hr.heir_governance_svc import HeirGovernanceService

hr_svc = HeirGovernanceService()

# staff_001 achieved 40% on hard math, but principal grants 90% discretion
final_score = hr_svc.apply_discretionary_kpi_override(
    staff_id="HEIR_STAFF_001",
    hard_kpi_score=40.0,
    family_discretion=90.0
)

print(f"Final Governance-Adjusted Score: {final_score}")
```


---

## Source: service_impact.md

# Backend Service: Impact

## Overview
The **Impact Service** is the platform's verifiable philanthropy and ESG infrastructure. It transforms charitable giving into a high-fidelity, data-driven operation. By utilizing **Impact Oracles** for off-chain verification and **Smart Contracts** for automated grant issuance, it ensures that philanthropic capital is deployed only when real-world KPIs are met. It also features a **Quadratic Voting** system for family councils to democratically prioritize impact initiatives.

## Core Components

### 1. Impact Verification Oracle (`impact_oracle.py`)
The platform's truth layer for real-world social impact.
- **KPI Verification**: Integrates with off-chain data sources—including satellite imagery, IoT sensors, and government APIs—to confirm that social or environmental milestones (e.g., carbon recapture, school enrollment) have been achieved.
- **Confidence Scoring**: Assigns a confidence metric to verified events based on the reliability and redundancy of the source data.

### 2. Grant Smart Contracts (`grant_smart_contract.py`)
Automates the lifecycle of philanthropic funding.
- **On-Chain Proposals**: Creates formal grant proposals on public or private ledgers (Ethereum/Solana), binding the fund release to specific verifiable KPIs.
- **Conditional Fund Release**: Automatically triggers the disbursement of funds once the Impact Oracle confirms KPI achievement, eliminating administrative delays and ensuring transparency.

### 3. Quadratic Voting Service (`voting_svc.py`)
Empowers democratic decision-making within Family Councils.
- **Quadratic Logic**: Implements a voting mechanism where the cost of power increases by the square of the votes (Cost = Power²). This encourages members to put more weight on initiatives they are truly passionate about while preventing a single dominant member from controlling the entire philanthropic budget.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Impact Tracker** | KPI Verification Pulse | `impact_oracle.verify_kpi()` |
| **Philanthropy Hub** | Grant Creation Wizard | `grant_smart_contract.propose_grant()` |
| **Council Station** | Quadratic Voting Terminal | `voting_service.cast_vote()` |
| **Philanthropy Hub** | Grant Settlement Ledger | `grant_smart_contract.release_funds()` |
| **Impact Tracker** | Oracle Source Timeline | `impact_oracle.verified_sources` |

## Dependencies
- `math`: Used for calculating vote power (square roots) in the quadratic voting engine.
- `logging`: Records oracle verifications, grant proposals, and voting results for auditability.

## Usage Examples

### Verifying a Philanthropic KPI via Oracle
```python
from services.impact.impact_oracle import ImpactOracleService

oracle = ImpactOracleService()

# Verify if a clean water project KPI (ID: CW_202) has been met
result = oracle.verify_kpi(kpi_id="CW_202", kpi_type="Water_Purity_IoT")

if result['verified']:
    print(f"KPI Verified via {result['source']} with {result['confidence']:.1%} confidence.")
else:
    print("KPI Verification Failed. Grant funds held.")
```

### Casting a Quadratic Vote
```python
from services.impact.voting_svc import VotingService

voting = VotingService()

# Alice spends 25 credits to get 5 votes on "AI Safety Research" (Prop ID: 2)
vote_result = voting.cast_vote(user="Alice", proposal_id=2, credits_spent=25)

print(f"Votes Cast: {vote_result['votes_cast']}")
print(f"Remaining Governance Credits: {vote_result['remaining_credits']}")
```


---

## Source: service_indicators.md

# Backend Service: Indicators

## Overview
The **Indicators Service** provides the platform's technical analysis and signal generation layer. It specializes in volatility-based metrics that help traders and automated agents determine historical and current market ranges. Its primary tool is the **ATR (Average True Range) Calculator**, which is essential for placing "Noise-Resistant" stop-loss orders in volatile markets.

## Core Components

### 1. ATR Calculator (`atr_calc.py`)
A quantitative utility for measurement of price volatility.
- **Average True Range Logic**: Computes the ATR over a configurable period (default: 14) by analyzing the range between high, low, and previous close for each candle. 
- **Volatility-Adjusted Stop Padding**: Provides a precision tool for risk management. Instead of using arbitrary percentages, it calculates stop-loss levels based on market volatility (e.g., placing a stop 1.5x ATR away from a swing high or low). This ensures that trades are not "stopped out" by normal intraday price fluctuations.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trading Terminal** | Technical Indicators Chart | `atr_calc.calculate_atr()` |
| **Trading Terminal** | "Padded Stop" Assistant | `atr_calc.get_padded_stop()` |
| **Risk Station** | Volatility Heatmap | `atr_calc.calculate_atr()` |
| **Order Ticket** | Smart Stop Level Slider | `atr_calc.get_padded_stop()` |

## Dependencies
- `decimal`: Used for precision financial calculations within the stop-padding logic.
- `logging`: Records the calculation of significant volatility shifts.

## Usage Examples

### Calculating ATR for Stop-Loss Placement
```python
from services.indicators.atr_calc import ATRCalculator

calc = ATRCalculator()

# Mock 14-period candle data
candles = [
    {"high": 105, "low": 95, "close": 100},
    {"high": 110, "low": 102, "close": 108},
    # ... (12 more candles)
]

atr = calc.calculate_atr(candles=candles, period=14)

# Place a Long stop 1.5x ATR below a swing low of $102
stop_price = calc.get_padded_stop(
    swing_level=102.0,
    atr=atr,
    direction="LONG",
    padding_mult=1.5
)

print(f"Current ATR: {atr:.4f}")
print(f"Volatility-Adjusted Stop Price: ${stop_price}")
```

### Dynamic Risk Padding for Short Positions
```python
from services.indicators.atr_calc import ATRCalculator

atr = 2.45 # Current volatility measure
swing_high = 450.50

# Place a Short stop 2.0x ATR ABOVE the swing high
padded_stop = ATRCalculator.get_padded_stop(
    swing_level=swing_high,
    atr=atr,
    direction="SHORT",
    padding_mult=2.0
)

print(f"Padded Short Stop: ${padded_stop}")
```


---

## Source: service_infrastructure.md

# Backend Service: Infrastructure

## Overview
The **Infrastructure Service** is the foundation upon which the entire Sovereign OS is built. It provides the "Global Nervous System" (Event Bus) for inter-service communication, high-performance caching for AI operations, and the orchestration of the platform's self-hosted, ZFS-backed **Private Cloud**. It ensures low-latency response times, data redundancy, and unified state management across the distributed architecture.

## Core Components

### 1. Global Event Bus (`event_bus.py`)
The architectural backbone for reactive, event-driven logic.
- **Pub/Sub Orchestration**: Allows asynchronous communication between services. For example, the discovery of a "Liquidity Crisis" in the risk service can be broadcast to the trading terminal and notifications engine simultaneously.
- **Topic-Based Routing**: Facilitates specialized subscription channels for high-priority signals (e.g., Geopolitical Shocks, System Heartbeats).

### 2. Agent Response Cache (`cache_service.py`)
Optimizes AI latency and operational costs.
- **MD5-Based Persistence**: Generates unique cryptographic keys for every agent-prompt pair, storing the resulting LLM responses in a persistent JSON cache.
- **Latency Reduction**: Automatically hits the cache for repeated queries, ensuring that "Agentic Thinking" is instantaneous for known scenarios.

### 3. Private Cloud Manager (`private_cloud.py`)
Manages the platform's physical data sovereignty.
- **ZFS Integration**: Interfaces with self-hosted storage tanks (RAID-Z2) to provide high-redundancy document storage.
- **Quota Monitoring**: Dynamically tracks available TBs and storage health, ensuring that the platform's large-scale data logs and document archives have sufficient headroom.
- **Sovereign Sync**: Handles the encrypted upload of sensitive financial documents to a private Nextcloud instance.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **System Monitor** | Event Bus Feed | `event_bus_service.publish()` (Signal log) |
| **Settings Panel** | Storage Quota Ring | `private_cloud_service.check_storage_quota()` |
| **Admin Panel** | Cache Hit/Miss Pulse | `agent_response_cache.get()` |
| **Document Vault** | Sovereign Cloud Sync Status| `private_cloud_service.sync_document()` |
| **Mission Control** | System Health Sparklines | `telemetry_service` (Heartbeats) |

## Dependencies
- `hashlib`: Generates unique keys for the agent response cache.
- `ZFS / Nextcloud`: (Infrastructure) The underlying storage and cloud technology stacks.
- `json`: Standard persistence format for local state and lightweight caching.

## Usage Examples

### Publishing a Geopolitical Shock Signal
```python
from services.infrastructure.event_bus import EventBusService

bus = EventBusService()

# Broadcast a major market event
bus.publish(
    topic="GEOPOLITICAL_SHOCK",
    payload={
        "region": "MIDDLE_EAST",
        "severity": "CRITICAL",
        "timestamp": "2026-02-06T12:00:00Z"
    }
)
```

### Retrieving an AI Completion from Cache
```python
from services.infrastructure.cache_service import get_agent_cache

cache = get_agent_cache()

# Attempt to fetch a previous completion
cached_response = cache.get(
    agent_id="STRATEGIST_AG_01",
    prompt="Summarize the impact of 5% interest rates on growth equity."
)

if cached_response:
    print(f"CACHE HIT: {cached_response[:100]}...")
```

### Checking Cloud Storage Health
```python
from services.infrastructure.private_cloud import PrivateCloudService

cloud = PrivateCloudService()

stats = cloud.check_storage_quota()
print(f"Cloud Status: {stats['status']} | Free Space: {stats['free_tb']} TB")
print(f"Redundancy: {stats['redundancy']}")
```


---

## Source: service_ingestion.md

# Backend Service: Ingestion

## Overview
The **Ingestion Service** is the platform's "Digital Collector." It manages the high-bandwidth pipelines required to source alternative and traditional market data. From the granular "Dark Pool" tape to satellite-derived port congestion counts and SEC filing scrapers, this service ensures that the platform has a information edge by aggregating signals that are often invisible to retail and standard institutional players.

## Core Components

### 1. Dark Pool Tape Engine (`dark_tape.py`)
Tracks the "Invisible Hand" of institutional liquidity.
- **Off-Exchange Filtering**: Specifically targets "Dark Prints" (Exchange Code 'D') which represent 40%+ of global equity volume.
- **Block Cluster Detection**: Analyzes identical-size trade prints to identify "Split Block" orders, revealing the entry and exit points of institutional whales.
- **Dark Level Identification**: Pinpoints price levels with anomalous dark volume, which serve as institutional support and resistance zones.

### 2. SEC & Financial Scraper (`sec_scraper.py`)
The foundational layer for valuation modeling.
- **Live Financial Extraction**: Pulls real-time Free Cash Flow (FCF), ROIC, and Operating Margins via market data APIs (`yfinance`) to feed the platform's DCF (Discounted Cash Flow) engines.
- **Filing Discovery**: Provides a framework for automated EDGAR retrieval, allowing the system to monitor 10-K and 10-Q filings for fundamental sentiment shifts.

### 3. Alternative Telemetry Ingestors
- **Satellite Port Telemetry (`port_congestion.py`)**: Sinks visual ship counts from major global ports (e.g., Long Beach, Rotterdam) to provide leading indicators for supply chain bottlenecks and inflationary pressure.
- **Federal Reserve Balance Tracker (`fed_balance.py`)**: Monitors the "Size of the Fed" as a primary signal for macro liquidity conditions (QE/QT).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Whale Watch Terminal** | Dark Print Ticker | `dark_pool_tape.filter_dark_prints()` |
| **Whale Watch Terminal** | Institutional Level Heatmap | `dark_pool_tape.get_significant_levels()` |
| **Supply Chain Hub** | Port Congestion Gauge | `port_congestion.get_ship_count()` |
| **Fundamental Station** | Income/Cash Flow Ledger | `sec_scraper.get_financials()` |
| **Strategist Station** | Fed Balance Pulse | `fed_balance.py` (Telemetry feed) |

## Dependencies
- `yfinance`: Powers the immediate retrieval of live institutional-grade financials.
- `logging`: Records the discovery of "Split Block" clusters and satellite ingestion events.

## Usage Examples

### Detecting Institutional "Block Clusters" in Dark Pools
```python
from services.ingestion.dark_tape import DarkPoolTapeService

tape = DarkPoolTapeService()

# Mock tape data containing some identical 10,000 share chunks
mock_tape = [
    {"symbol": "NVDA", "price": 450.50, "size": 10000, "exchange": "D"},
    {"symbol": "NVDA", "price": 450.55, "size": 10000, "exchange": "D"},
    {"symbol": "NVDA", "price": 450.45, "size": 10000, "exchange": "D"}
]

clusters = tape.detect_block_clusters(dark_prints=mock_tape)

for c in clusters:
    print(f"Detected {c['count']}x {c['size']} share prints | Total Volume: {c['total_volume']}")
```

### Retrieving Live Valuation Metrics
```python
from services.ingestion.sec_scraper import SECScraper

scraper = SECScraper()

# Fetch valuation metrics for Microsoft
metrics = scraper.get_financials(ticker="MSFT")

print(f"Market Cap: ${metrics['market_cap'] / 1e12:.2f}T")
print(f"Free Cash Flow: ${metrics['free_cash_flow'] / 1e9:.2f}B")
print(f"ROIC: {metrics['roic']:.2%}")
```


---

## Source: service_institutional.md

# Backend Service: Institutional

## Overview
The **Institutional Service** is the platform's multi-tenant engine for financial advisors, banks, and family offices. It provides the infrastructure necessary to manage thousands of client relationships, configure **White-Label** branding for different organizations, and generate high-fidelity **Professional Reports**. It also features an integrated relationship graph (Neo4j) to track advisor-client hierarchies and advanced analytics for revenue forecasting and risk profiling.

## Core Components

### 1. Client & Organization Management (`institutional_service.py`)
The central orchestrator for institutional operations.
- **Advisor-Client Graph**: Utilizes Neo4j to maintain a persistent graph of which advisors manage which clients, enabling complex access control and organizational reporting.
- **White-Label Configuration**: Allows organizations to customize their logo, color palettes, and custom domains, ensuring the platform feels like a native institutional app.
- **Institutional Analytics**: Generates real-time metrics including **Fee Forecasts**, **Churn Probability**, and **KYC Risk Scores** to help advisors manage their business at scale.
- **Risk & Health Profiling**: Continuously monitors client accounts for institutional risk breaches (volatility/drawdown thresholds) and generates proactive health alerts.

### 2. Professional Reporting Terminal (`professional_tools_service.py`)
Handles the generation of high-fidelity documentation for allocators.
- **Advanced Report Engine**: Facilitates the creation of custom reports (e.g., GP/LP quarterly updates, performance audits) that are persisted in the platform's document cache.
- **Mandate Compliance**: Ensures that reports are generated contextually based on the specified institutional mandate and report type.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Advisor Console** | Client Management Grid | `institutional_service.get_clients_for_advisor()` |
| **Advisor Console** | Revenue Forecast Chart | `institutional_service.get_revenue_forecast()` |
| **White Label Settings**| Branding Preview | `institutional_service.configure_white_label()` |
| **Client Detail** | Risk Profile Pulse | `institutional_service.get_client_risk_profile()` |
| **Reporting Terminal** | Report Generator Wizard | `professional_tools_service.generate_professional_report()` |
| **Document Hub** | e-Signature Tracker | `institutional_service.get_signature_status()` |

## Dependencies
- `neo4j`: Powers the institutional relationship graph.
- `services.system.cache_service`: Provides persistent storage for client data, configurations, and reports.
- `schemas.institutional`: Defines the core Pydantic models for `Client`, `WhiteLabelConfig`, and `ProfessionalReport`.

## Usage Examples

### Configuring White-Label Branding for a Family Office
```python
from services.institutional.institutional_service import get_institutional_service

inst_svc = get_institutional_service()

# Configure custom branding for 'Sovereign Wealth Management'
config = await inst_svc.configure_white_label(
    organization_id="org_sovereign_001",
    branding_name="Sovereign Wealth Portal",
    primary_color="#1a2b3c",
    logo_url="https://cdn.sovereign.net/logo.png"
)

print(f"Branding configured: {config.branding_name}")
```

### Generating an Institutional Revenue Forecast
```python
from services.institutional.institutional_service import InstitutionalService

svc = InstitutionalService()

# Fetch a 12-month revenue forecast for the entire advisory practice
forecast = await svc.get_revenue_forecast()

print(f"Current Monthly Fees: ${forecast['current_fees']:,.2f}")
print(f"Projected Annual Growth: {forecast['growth_rate']:.1%}")
for month in forecast['history'][-3:]:
    print(f"Month: {month['date']} | Revenue: ${month['amount']:,.2f}")
```

### Auditing a Client's Signature Compliance
```python
from services.institutional.institutional_service import get_institutional_service

inst_svc = get_institutional_service()

# Check which institutional onboarding docs are still pending
status = await inst_svc.get_signature_status(client_id="client_jdoe_123")

print(f"Compliance Completion: {status['completion_percentage']}%")
for doc in status['documents']:
    if doc['status'] == "Pending":
        print(f"MISSING: {doc['name']}")
```


---

## Source: service_insurance.md

# Backend Service: Insurance

## Overview
The **Insurance Service** manages the platform's specialized risk-wrapper and tax-alpha infrastructure. It is designed for UHNW and institutional clients utilizing **Private Placement Life Insurance (PPLI)**, **Corporate-Owned Life Insurance (COLI)**, and premium financing. The service optimizes asset placement by ranking investments based on their "Tax Drag," monitors the health of policy-backed loans, and proactively flags lapse risks to ensures the long-term structural integrity of the legacy plan.

## Core Components

### 1. PPLI Efficiency & Tax-Drag Ranking (`ppli_efficiency_svc.py`, `efficiency_ranker.py`)
Determines the optimal assets to place inside a tax-exempt insurance wrapper.
- **Tax-Drag Analysis**: Calculates the impact of ordinary income, short-term capital gains, and high turnover on an asset's net performance.
- **Priority Placement**: Automatically ranks a client's portfolio, flagging assets with a high "Efficiency Gap" as "CRITICAL" candidates for PPLI wrapping (e.g., credit-heavy funds or high-turnover hedge strategies).

### 2. Policy Loan & Lapse Tracker (`loan_tracker.py`)
The monitoring layer for insurance-collateralized liquidity.
- **Wash Loan Management**: Logs and verifies "Wash Loans" where borrowing costs are offset by policy credits, enabling tax-free access to capital.
- **Lapse Risk Projection**: Continuously monitors the ratio of loan balance to cash value. It calculates the remaining years of "Cost of Insurance" (COI) coverage, triggering high-severity alerts if a policy is projected to lapse within 5 years.

### 3. Withdrawal & Distribution Modeling (`ppli_withdrawal.py`)
- **Tax-Free Distributions**: Models distributions via the "FIFO" (Basis First) principle and subsequent loans to maintain the policy's tax-favored status under IRS Section 7702.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Insurance Station** | PPLI Wrapper Optimizer | `ppli_efficiency_svc.rank_assets_by_tax_drag()` |
| **Insurance Station** | Lapse Risk Countdown | `ppli_loan_tracker.calculate_lapse_risk()` |
| **Portfolio Detail** | Tax-Drag Impact Card | `efficiency_ranker.rank_assets()` |
| **Document Hub** | Policy Ledger (Loans) | `ppli_loan_tracker.log_loan_transaction()` |
| **Planning Station** | PPLI Withdrawal Preview | `ppli_withdrawal.py` (Withdrawal math) |

## Dependencies
- `decimal`: Used for all high-precision financial math involving tax rates, yields, and loan interest.
- `logging`: Records structural events like "High Lapse Risk" and "PPLI Priority Shifts."

## Usage Examples

### Ranking Assets for a PPLI Shield
```python
from services.insurance.efficiency_ranker import TaxEfficiencyRanker
from decimal import Decimal

ranker = TaxEfficiencyRanker()

# Sample assets: High-yield bond vs Low-yield tech
assets = [
    {"ticker": "HYG", "yield": 0.08, "turnover": 0.40, "type": "BOND"},
    {"ticker": "AAPL", "yield": 0.01, "turnover": 0.05, "type": "EQUITY"}
]

# Assume 37% ordinary income tax rate
ranking = ranker.rank_assets(assets=assets, ord_rate=Decimal('0.37'), st_rate=Decimal('0.37'))

for r in ranking:
    print(f"Asset: {r['ticker']} | Tax Drag: {r['tax_drag_bps']} bps | Priority: {r['ppli_priority']}")
```

### Checking the Lapse Risk of a Policy Loan
```python
from services.insurance.loan_tracker import PPLILoanTracker
from decimal import Decimal

tracker = PPLILoanTracker()

# Scenario: $2M Cash Value, $1.8M Loan, $50k Annual Cost of Insurance
years_rem = tracker.calculate_lapse_risk(
    cash_value=Decimal('2000000'),
    loan_balance=Decimal('1800000'),
    annual_coi=Decimal('50000')
)

print(f"Policy Health: {years_rem} years of coverage remaining.")
if years_rem < 5:
    print("ACTION REQUIRED: Strategy re-funding or loan repayment recommended.")
```


---

## Source: service_integration.md

# Backend Service: Integration

## Overview
The **Integration Service** serves as the platform's universal connector hub. It provides a standardized **Framework** for linking the Sovereign OS with external financial ecosystems (e.g., Mint, YNAB, Quicken) and enterprise toolsets. By utilizing OAuth-based authentication and structured sync scheduling, it ensures that external data is seamlessly mapped and transformed into the platform's internal schemas.

## Core Components

### 1. Integration Framework (`integration_framework.py`)
The foundational infrastructure for external connectivity.
- **Provider Registry**: Maintains a list of supported third-party applications and their respective connectivity protocols.
- **OAuth Orchestration**: Handles the secure lifecycle of external connections, managing authentication tokens and connection states (`CONNECTED`, `DISCONNECTED`, `PENDING`).
- **Data Mapping Foundation**: Provides the base logic for transforming external JSON payloads into platform-compliant models.

### 2. Synchronization Engine (`integration_service.py`)
Orchestrates the movement of data between external apps and the platform.
- **Sync Job Management**: Handles the scheduling and execution of `full` and `incremental` data refreshes. It tracks the status of each job, including start/end times and the count of records successfully synchronized.
- **Conflict Resolution**: (Framework level) Provides the logic for resolving data discrepancies between external feeds and the platform's local state.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Integrations Hub** | App Store / Connector Grid | `integration_framework.get_supported_apps()` |
| **Integrations Hub** | Connection Wizard | `integration_framework.create_integration()` |
| **Sync Monitor** | Real-time Sync Pulse | `integration_service.sync_data()` |
| **Sync Monitor** | Historical Job Ledger | `integration_service.get_sync_status()` |
| **Settings Panel** | Linked Accounts Card | `integration_framework` (Connection status) |

## Dependencies
- `services.system.cache_service`: Persists integration states and synchronization logs.
- `schemas.integration`: Defines the standard `Integration` and `SyncJob` Pydantic models.
- `OAuthService`: (External) Handles the actual token exchange and refreshing.

## Usage Examples

### Linking a New External App (Mint)
```python
from services.integration.integration_framework import get_integration_framework

framework = get_integration_framework()

# User initiates a connection to Mint with a successful OAuth token
integration = await framework.create_integration(
    user_id="user_vanderbilt_001",
    app_name="mint",
    oauth_token="0x_MOCK_OAUTH_TOKEN_ABC"
)

print(f"Integration Created: {integration.integration_id}")
print(f"Current Status: {integration.status}")
```

### Triggering an Incremental Data Sync
```python
from services.integration.integration_service import get_integration_service

sync_service = get_integration_service()

# Run an incremental update for an existing YNAB connection
job = await sync_service.sync_data(
    integration_id="integration_user_001_ynab",
    sync_type="incremental"
)

print(f"Sync Job {job.sync_job_id}: {job.status}")
print(f"Records Processed: {job.records_synced}")
```


---

## Source: service_integrations.md

# Backend Service: Integrations (Vertical Plugins)

## Overview
The **Integrations (Vertical Plugins) Service** manages niche and vertical-specific third-party API bridges. Unlike the core integration framework which handles broad financial data, this service focuses on high-specificity plugins such as **Real Estate Valuation (Zillow)** and the **Voice Command OS (Whisper)**. It serves as an internal "Marketplace Manager" where administrators can register, enable, and monitor specialized third-party dependencies.

## Core Components

### 1. Real Estate Valuation Bridge (`zillow.py`)
Provides mark-to-market capabilities for physical property assets.
- **Zestimate Integration**: Fetches real-time property valuations and one-month price shifts directly from Zillow. This allows physical real estate to be tracked alongside liquid equities in the platform's unified wealth dashboard.

### 2. Voice Command OS (`voice_cmd.py`)
Enables the platform's human-interface Layer via audio.
- **Speech-to-Intent Orchestration**: Interfaces with AI transcription services (e.g., Whisper) to convert verbal instructions into structured system commands. This allows principals to interact with their portfolio via natural language (e.g., "Show me my exposure to NVDA").

### 3. Integration Manager (`manager.py`)
The administrative registry for specialized plugins.
- **API Marketplace**: Manages the registration of third-party API keys, ensuring they are masked in logs for security.
- **Service Toggle**: Provides a centralized toggle system to enable or disable niche integrations without requiring a system restart.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Real Estate Detail**| Property Mark-to-Market Card | `zillow_service.get_zestimate()` |
| **Global UI** | Voice Command Pulse | `voice_os.process_audio()` |
| **Marketplace Station**| API Bridge Status List | `integration_manager.get_active_integrations()` |
| **Admin Station** | API Key Registrar | `integration_manager.register_integration()` |

## Dependencies
- `Zillow API`: (External) Source for real estate valuation telemetry.
- `Whisper API`: (External) Source for speech transcription and intent processing.
- `logging`: Records API fetch events and transcription successes/failures.

## Usage Examples

### Tracking Property Value via Zestimate
```python
from services.integrations.zillow import ZillowService

z_svc = ZillowService()

# Fetch latest valuation for a specific property ID
valuation = z_svc.get_zestimate(property_id="PROP_BEL_AIR_01")

print(f"Current Value: ${valuation['current_valuation']:,.2f}")
print(f"Monthly Change: ${valuation['one_month_change']:+, .2f}")
```

### Processing a Voice Instruction
```python
from services.integrations.voice_cmd import VoiceOS

voice = VoiceOS()

# Simulate receiving audio from the user's mobile device
# "Show my exposure to Apple"
intent = voice.process_audio(audio_data=b"binary_audio_payload")

print(f"Detected System Intent: {intent}")
# Logic would then route "SHOW_EXPOSURE_AAPL" to the Exposure Service
```

### Registering a New Marketplace Integration
```python
from services.integrations.manager import IntegrationManager

manager = IntegrationManager()

# Register a specialized data bridge
manager.register_integration(
    name="REUTERS_MACRO",
    api_key="SK_ABC_123_SECRET_KEY",
    enabled=True
)

print(f"Active Integrations: {manager.get_active_integrations()}")
```


---

## Source: service_international.md

# Backend Service: International

## Overview
The **International Service** is the platform's geopolitical and cross-border risk engine. It is designed to navigate the structural complexities of global markets, focusing on the identification of **State-Owned Enterprises (SOEs)** and the monitoring of **Index Skew** in international markets. It provides institutional-grade risk ratings for emerging and developed market exposures, ensuring that portfolios aren't silently concentrated in sanctioned regions or single-company dominated indices.

## Core Components

### 1. International Concentration Analyzer (`concentration_analyzer.py`)
Monitors structural skews within global equity indices.
- **Index Skew Detection**: Automatically flags international indices where a single ticker holds >20% weight (e.g., TSMC's dominance in the Taiwan market). This prevents the "Passive Concentration" trap where an investor believes they are diversified across a country but are actually highly leveraged to a single firm's idiosyncratic risk.

### 2. State-Owned Enterprise (SOE) Classifier (`soe_classifier.py`)
The geopolitical risk layer for global mandates.
- **Ownership Analysis**: Classifies companies as SOEs based on government ownership thresholds (>50%) or the presence of strategic sovereign entities (e.g., SASAC, Temasek, Mubadala).
- **Geopolitical Risk Rating**: Assigns risk levels based on the entity's status and its region. SOEs in sanctioned or high-friction regions (e.g., RU, CN) are flagged as "CRITICAL" or "HIGH" risk, while those in stable partner regions are rated "LOW."

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Geopolitical Station**| Global SOE Exposure Map | `soe_classifier.classify_soe()` |
| **Geopolitical Station**| Country Skew Alert Feed | `intl_concentration_analyzer.analyze_index_skew()` |
| **Portfolio Detail** | Regulatory Risk Rating Card| `soe_classifier.get_risk_rating()` |
| **Strategist Station** | Sanctioned Entity Ledger | `soe_classifier.py` (Risk logic) |

## Dependencies
- `logging`: Records the discovery of significant index skews and high-risk SOE classifications for the audit trail.

## Usage Examples

### Detecting a Structural Skew in an Emerging Market Index
```python
from services.international.concentration_analyzer import IntlConcentrationAnalyzer

analyzer = IntlConcentrationAnalyzer()

# Mock holdings for the Taiwan Index
taiwan_holdings = [
    {"ticker": "TSMC", "weight": 0.28}, # 28% weight
    {"ticker": "HON_HAI", "weight": 0.05},
    {"ticker": "MEDIATEK", "weight": 0.04}
]

skew_report = analyzer.analyze_index_skew(index_name="Taiwan_TAIEX", holdings=taiwan_holdings)

if skew_report['is_skewed']:
    print(f"Index {skew_report['index_name']} is SKEWED.")
    print(f"Top Holding {skew_report['top_ticker']} accounts for {skew_report['top_weight']:.1%} of index.")
```

### Classifying an Entity as a State-Owned Risk
```python
from services.international.soe_classifier import SOEClassifier

classifier = SOEClassifier()

# Classify an entity controlled by SASAC (State-owned Assets Supervision and Administration Commission)
is_soe = classifier.classify_soe(ownership_pct=0.15, controlling_entity="SASAC")

risk_rating = classifier.get_risk_rating(is_soe=is_soe, country_code="CN")

print(f"SOE Classification: {is_soe}")
print(f"Geopolitical Risk Rating: {risk_rating}")
```


---

## Source: service_journal.md

# Backend Service: Journal

## Overview
The **Journal Service** is the platform's behavioral auditing and strategy optimization layer. It transforms standard trade logs into actionable insights by analyzing the psychological and structural patterns of an investor's performance. By identifying statistically dominant "Setups" and highlighting temporal performance skews (e.g., specific days of the week), it helps traders refine their edge and eliminate sub-optimal behaviors.

## Core Components

### 1. Journal Pattern Analyzer (`analyzer.py`)
The quantitative core of the trading diary.
- **Temporal PnL Analysis**: Aggregates trade performance by the day of the week. This allows investors to identify biological or psychological patterns (e.g., high fatigue on Fridays leading to poor decision-making).
- **Setup Leaderboard**: Evaluates different trading strategies (e.g., Mean Reversion, Momentum, Pullback) based on their average **R-Multiple**. It identifies which "Setup" is statistically most profitable for the account, enabling the investor to focus capital on their strongest competitive advantages.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trader Station** | Setup Efficiency Leaderboard | `journal_analyzer.get_best_setup()` |
| **Trader Station** | Day-of-Week PnL Heatmap | `journal_analyzer.analyze_by_day()` |
| **Portfolio Detail** | Behavioral Consistency Score | `journal_analyzer.analyze_by_day()` |
| **Strategist Station** | Strategy Drift Audit | `journal_analyzer` (Historical r-multiples) |

## Dependencies
- `logging`: Records the extraction of significant strategic insights from the trade journal.

## Usage Examples

### Identifying the Most Profitable Trading Setup
```python
from services.journal.analyzer import JournalAnalyzer

analyzer = JournalAnalyzer()

# Historical trades with R-Multiple performance
history = [
    {"setup": "BREAKOUT", "r_multiple": 3.5},
    {"setup": "MEAN_REVERSION", "r_multiple": 1.2},
    {"setup": "BREAKOUT", "r_multiple": 4.0},
    {"setup": "PULLBACK", "r_multiple": 2.1}
]

best = analyzer.get_best_setup(trades=history)
print(f"Statistically Dominant Setup: {best}")
```

### Analyzing PnL Distribution by Day
```python
from services.journal.analyzer import JournalAnalyzer

analyzer = JournalAnalyzer()

trades = [
    {"day": "Monday", "pnl": 1200.0},
    {"day": "Monday", "pnl": -500.0},
    {"day": "Friday", "pnl": -2500.0},  # Significant loss on Friday
    {"day": "Wednesday", "pnl": 800.0}
]

daily_stats = analyzer.analyze_by_day(trades=trades)

for day, pnl in daily_stats.items():
    print(f"Day: {day} | Cumulative Net PnL: ${pnl:,.2f}")
```


---

## Source: service_journaling.md

# Backend Service: Journaling (Real-Time Behavioral)

## Overview
The **Journaling (Real-Time Behavioral) Service** is the platform's qualitative event-capture layer. Unlike the trade-focused `Journal` service, this service focuses on the **Present State** of the user. It logs emotional triggers, captured sentiment, and instances where system guardrails have intervened to prevent impulsive or sub-optimal decisions. This data is critical for building a longitudinal map of a user's psychological relationship with their assets.

## Core Components

### 1. Behavioral Log Engine (`behavioral_log.py`)
The high-fidelity recorder for human-system interaction.
- **Event Journaling**: Captures specific behavioral events (e.g., "Impulse Buy Attempt", "Panic Sell Blocked", "Revenge Trade Flagged") with detailed qualitative context.
- **Sentiment Tracking**: Assigns a numeric **Sentiment Score** to each event, allowing the system's behavioral agents to monitor for patterns of emotional distress or over-excitement that could lead to financial risk.
- **Intervention Ledger**: Maintains a permanent record of every time a "Prevented Trade" was triggered by the platform's risk or behavioral layers, allowing for subsequent post-mortem analysis.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Psychology Hub** | Emotional Sentiment Pulse | `behavioral_log.log_event()` |
| **Psychology Hub** | Intervention History Ticker| `behavioral_log.get_recent_logs()` |
| **Whale Watch Terminal** | User Stability Meter | `behavioral_log` (Sentiment aggregate) |
| **Admin Station** | Behavioral Audit Ledger | `behavioral_log.logs` |

## Dependencies
- `datetime`: Provides ISO-standard timestamps for event traceability.
- `logging`: Mirrors behavioral events to the system logs for cross-referencing with trade execution errors.

## Usage Examples

### Logging an Impulsive Execution Attempt
```python
from services.journaling.behavioral_log import BehavioralLog

log_svc = BehavioralLog()

# Capture an event where the user tried to FOMO into a volatile crypto asset
log_svc.log_event(
    event_type="FOMO_GUARD_TRIGGERED",
    details="User attempted to buy DOGE after 40% spike. Execution blocked by Behavioral Guardrail.",
    sentiment_score=-8 # High emotional intensity / Low rational score
)

print(f"Logged {len(log_svc.logs)} behavioral events.")
```

### Retrieving Recent Tactical Interventions
```python
from services.journaling.behavioral_log import BehavioralLog

log_svc = BehavioralLog()

# (Simulated) Fetching the last 5 interventions for the 'Intervention History' widget
interventions = log_svc.get_recent_logs(limit=5)

for entry in interventions:
    print(f"[{entry['timestamp']}] {entry['type']}: {entry['details']}")
```


---

## Source: service_kafka.md

# Backend Service: Kafka (Real-Time Streaming)

## Overview
The **Kafka Service** is the high-throughput asynchronous backbone of the Sovereign OS. It facilitates the real-time movement of "Market Bytes" and "Agent Signals" across the distributed architecture. By utilizing a robust **Base Consumer** framework with integrated circuit breakers, the service ensures that the platform can process tens of thousands of price updates, order book shifts, and inter-agent communications every second with minimal latency and high fault tolerance.

## Core Components

### 1. Unified Consumer Framework (`consumer.py`)
The platform's standardized entry point for event-driven logic.
- **Base Consumer Class**: Implements background polling, threading, and deserialization for all agents. It features a built-in **Circuit Breaker** that halts consumption if more than 10 consecutive errors occur, protecting the system from cascading failures during network instability.
- **Domain Consumers**: Provides specialized listeners for `market.vix` (Volatility Update), `market.equity` (Price Feed), and `agent.signals` (Inter-Agent Messaging).

### 2. High-Fidelity Orderbook Streamer (`orderbook_consumer.py`)
Processes Level 2 Depth-of-Book data in real-time.
- **Liquidity Analysis**: Aggregates bid/ask depth to identify significant imbalances (e.g., >50% sell-side pressure).
- **Market Microstructure**: Forwards high-fidelity book summaries to risk engines and the trading terminal, enabling precision execution based on available liquidity.

### 3. Graph Correlation Bridge (`graph_bridge.py`)
Synchronizes the streaming layer with the relationship graph (Neo4j).
- **Dynamic Correlation Engine**: Consumes price updates for FX and Equity pairs and recalculates Pearson correlation coefficients on-the-fly using a rolling history window.
- **Graph Persistence**: Updates the "Edge Weights" (Correlation Strength) in the Neo4j graph, allowing the platform to visualize the real-time "Nervous System" of the global market.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trading Terminal** | Level 2 Orderbook Depth | `orderbook_consumer.latest_books` |
| **Market Intelligence** | Real-time Correlation Graph | `graph_bridge.process_message()` (Edge weights) |
| **System Monitor** | Consumer Health Pulse | `base_consumer.health_check()` |
| **Whale Watch Terminal** | Institutional Block Signal Feed| `kafka.consumer` (Signals) |
| **Mission Control** | Volatility (VIX) Ticker | `vix_consumer.process_message()` |

## Dependencies
- `confluent-kafka`: High-performance Python client for Apache Kafka.
- `Neo4j`: Used by the Graph Bridge to persist market correlations.
- `json`: Standard format for event serialization/deserialization.

## Usage Examples

### Implementing a Custom Market Data Consumer
```python
from services.kafka.consumer import BaseConsumer, ConsumerConfig

class MyAlphaConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers=None):
        config = ConsumerConfig(
            topics=['market.alpha.signals'],
            group_id='alpha-detection-team'
        )
        super().__init__(config, bootstrap_servers)

    def process_message(self, message):
        print(f"NEW ALPHA SIGNAL: {message['signal_id']} for {message['ticker']}")

consumer = MyAlphaConsumer()
consumer.start() # Runs in background thread
```

### Checking the Health of the Kafka Infrastructure
```python
from services.kafka.orderbook_consumer import orderbook_consumer

# Inspect the health status of the high-fidelity depth consumer
status = orderbook_consumer.health_check()

if status['healthy']:
    print(f"Depth Consumer is active on: {status['topics']}")
else:
    print(f"CRITICAL: Consumer halted after {status['error_count']} errors.")
```

### Visualizing Real-time Market Imbalance
```python
from services.kafka.orderbook_consumer import orderbook_consumer

# Fetch the latest processed book for NVIDIA
book = orderbook_consumer.get_book("NVDA")

if book:
    print(f"NVDA Bid Size: {book['total_bid_size']}")
    print(f"NVDA Ask Size: {book['total_ask_size']}")
```


---

## Source: service_legacy.md

# Backend Service: Legacy (Generational Stewardship)

## Overview
The **Legacy (Generational Stewardship) Service** is the platform's engine for ultra-long-term wealth preservation and multi-generational data archival. Unlike traditional portfolio services that focus on 5-10 year horizons, the Legacy service operates on a **100-year timescale**. It manages the hyper-durable asset allocations required for inter-generational survival and provides specialized tools like "Digital Time Capsules" to preserve family wisdom and institutional state for descendants through the next century.

## Core Components

### 1. Century Planner (`century_planner.py`)
The 100-year strategic allocator.
- **Hyper-Durable Allocation**: Focuses on assets with extreme longevity: physical gold, arable land, clean water rights, and Bitcoin (Cold Storage). It generates a "Century Plan" that prioritizes core wealth preservation over short-term market alpha.
- **Inter-Generational Horizon**: Sets a dynamic target (e.g., Year 2126) and provides rebalancing prescriptions meant to be followed across multiple generations.

### 2. Digital Time Capsule (`time_capsule.py`)
Long-term data archival on resilient physical media.
- **Archival Hashing**: Hashes and prepares critical family or institutional data for etching on high-durability media such as **Quartz Glass (5D memory)** or M-DISC.
- **Unlock Protocols**: Establishes "Sealed" archival states with specific unlock dates, effectively creating a cryptographically-secured bridge to the future.

### 3. Perpetual System Monitor (`perpetual.py`)
Stewardship of the Sovereign OS state across the system's lifecycle.
- **System Post-Mortem & Perpetual State**: Tracks the entire operational history of the AI Investor system. It maintains a ledger of major milestones and phases, ensuring that the "Ancestral State" of the system is preserved for future operators.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Legacy Station** | 100-Year Century Planner | `century_planner.generate_100_year_plan()` |
| **Legacy Station** | Digital Time Capsule Seal | `time_capsule.seal_capsule()` |
| **Governance Hub** | Perpetual System Status | `perpetual.generate_post_mortem()` |
| **Legacy Station** | Durable Asset Heatmap | `century_planner.target_allocation` |
| **Admin Panel** | System Milestone Ledger | `perpetual.record_milestone()` |

## Dependencies
- `hashlib`: Used for generating archival hashes for time capsules.
- `datetime`: Tracks system inception and generational target dates.
- `logging`: Records the sealing of capsules and the generation of multi-century plans.

## Usage Examples

### Generating a 100-Year Wealth Preservation Plan
```python
from services.legacy.century_planner import CenturyPlannerService

planner = CenturyPlannerService()

# Generate a plan for a $100M Family Office AUM
plan = planner.generate_100_year_plan(current_wealth=100_000_000.0)

print(f"Plan Horizon: {plan['horizon']}")
print(f"Goal: {plan['primary_goal']}")
for asset, amount in plan['allocation_usd'].items():
    print(f"{asset}: ${amount:,.2f}")
```

### Sealing a Generational Time Capsule
```python
from services.legacy.time_capsule import TimeCapsuleService

capsule_svc = TimeCapsuleService()

# Prepare family council mission statement for the year 2076
capsule = capsule_svc.seal_capsule(
    content_description="Family Constitution & Mission Statement",
    unlock_date="2076-01-01"
)

print(f"Capsule ID: {capsule['capsule_id']}")
print(f"Storage Medium: {capsule['media_type']}")
print(f"Physical Target: {capsule['location']}")
```

### Recording an Institutional Milestone for Perpetual History
```python
from services.legacy.perpetual import PerpetualLegacy

legacy = PerpetualLegacy()

# Record the completion of Phase 100 Deployment
legacy.record_milestone("Sovereign OS reached Perpetual Operation state.")
status = legacy.generate_post_mortem()

print(f"System Legacy Mode: {status['legacy_mode']}")
print(f"Total Captured Milestones: {status['total_milestones']}")
```


---

## Source: service_legal.md

# Backend Service: Legal

## Overview
The **Legal Service** is the platform's multi-layered defensive and structural infrastructure. It provides institutional-grade "Legal-as-a-Service" (LaaS) for UHNW families and family offices. The service automates the analysis of complex contracts for dangerous clauses, tracks residency thresholds to prevent "Accidental Tax Residency," monitors global court dockets for litigation risks, and resolves complex ownership hierarchies across trusts, LLCs, and individualholdings.

## Core Components

### 1. Contract Analysis Engine (`contract_analyzer.py`)
Autonomous review of legal documents to flag structural risks.
- **Risk Scoring**: Uses keyword analysis and intent mapping to score contracts based on aggressive indemnification, arbitration, or perpetual exclusivity clauses.
- **Clause Flagging**: Automatically identifies and extracts "High-Risk" text, providing a summary and recommendation (Approve/Reject) for legal counsel review.

### 2. Citizenship & Mobility Hedging (`citizenship_hedging_svc.py`)
Stewardship of "Plan B" residency and visa compliance.
- **Residency Threshold Tracking**: Monitors days spent in specific jurisdictions to ensure compliance with the 183-day rule, preventing unintended tax residency recognition.
- **Visa Compliance Audit**: Validates the holding period and investment status of "Golden Visa" or residency-by-investment assets, tracking the progress towards citizenship eligibility.

### 3. Litigation Radar (`litigation_radar.py`)
Proactive monitoring for legal threats.
- **Docket Scraping**: Interfaces with court dockets (e.g., PACER/CourtListener) to monitor filings involving family members, trusts, or holding companies.
- **Jurisdictional Risk Profiling**: Evaluates the legal protection levels of different jurisdictions (e.g., Nevada, Cook Islands) to assist in asset protection planning.

### 4. Ownership & Entity Resolver (`ownership_resolver.py`)
Orchestrates the legal and tax status of diverse account types.
- **Tax Entity Mapping**: Automatically resolves whether an account/asset is owned by an individual (pass-through), a revocable/irrevocable trust, or a business entity. It identifies which structures require separate tax filings and which are legally distinct layers.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Legal Command** | Contract Risk Scorer | `contract_analysis_service.analyze_document()` |
| **Legal Command** | Global Residency Pulse | `citizenship_hedging_svc.track_residency_threshold()` |
| **Legal Command** | Litigation Docket Monitor | `litigation_radar_service.scan_dockets()` |
| **Trust Station** | Entity Ownership Graph | `legal_ownership_resolver.resolve_tax_entity()` |
| **Governance Hub** | Golden Visa Vesting Progress| `citizenship_hedging_svc.validate_visa_investment_hold()`|

## Dependencies
- `hashlib / json`: Used by internal metadata and archival layers.
- `datetime / date`: Tracks residency thresholds and visa investment timers.
- `logging`: Records structural alerts such as "Risk of Tax Recognition" or "Critical Litigation Found."

## Usage Examples

### Running an Autonomous Contract Risk Audit
```python
from services.legal.contract_analyzer import ContractAnalysisService

analyzer = ContractAnalysisService()

# Run an AI audit on a new Private Equity Subscription Agreement
audit = analyzer.analyze_document(file_path="/vault/contracts/PE_Sub_Agreement.pdf")

print(f"Risk Score: {audit['risk_score']}/100")
print(f"Recommendation: {audit['assessment']}")
for clause in audit['flagged_clauses']:
    print(f"FLAG: {clause['clause']} is {clause['risk']} risk")
```

### Tracking Global Residency for Tax Optimization
```python
from services.legal.citizenship_hedging_svc import CitizenshipHedgingService

hedging_svc = CitizenshipHedgingService()

# Check threshold for the UK after a 120-day summer residence
threshold = hedging_svc.track_residency_threshold(country_code="UK", days_present=120)

print(f"Status in {threshold['country']}: {threshold['status']}")
print(f"Days remaining until Tax Residency: {threshold['days_remaining_to_resident']}")
```

### Resolving Account Ownership for Tax Reporting
```python
from services.legal.ownership_resolver import LegalOwnershipResolver

resolver = LegalOwnershipResolver()

# Resolve status for an Irrevocable Asset Protection Trust
res = resolver.resolve_tax_entity(account_type="IRREVOCABLE_TRUST")

print(f"Legal Entity Type: {res['entity_type']}")
print(f"Requires Separate Tax Return: {res['requires_separate_tax_filing']}")
```


---

## Source: service_lending.md

# Backend Service: Lending

## Overview
The **Lending Service** manages the platform's institutional-grade debt and liquidity infrastructure. It allows UHNW clients to unlock liquidity from concentrated asset positions without triggering immediate tax events. The service provides specialized volatility-adjusted **Loan-to-Value (LTV)** modeling, tax-aware decision logic to compare borrowing costs against capital gains hits ("Borrow vs. Sell"), and generates automated **Interest-Only (IO)** payment schedules for multi-million dollar credit facilities.

## Core Components

### 1. Stock-Based Lending Engine (`stock_lending_svc.py`)
Optimizes liquidity extraction from concentrated equity positions.
- **Volatility-Adjusted LTV**: Automatically calculates maximum borrowing capacity based on ticker volatility. Lower volatility assets (e.g., indices or mega-caps) receive higher LTVs (up to 50%), while high-volatility assets are restricted to ensure collateral stability.
- **Tax-Aware Decision Logic**: Conducts a "Borrow vs. Sell" analysis. It calculates the one-time capital gains tax cost of selling a position versus the annual interest cost of borrowing against it. If the tax hit is significantly higher than 3 years of interest, it recommends a "Borrow" strategy to preserve basis and defer taxes.

### 2. Credit Facility Manager (`payment_sched.py`)
Orchestrates the lifecycle of UHNW debt structures.
- **Interest-Only (IO) Scheduler**: Generates precision repayment schedules for interest-only credit lines. This is the standard structure for UHNW liquidity, allowing the principal to remain invested while only addressing the cost of capital on a monthly basis.
- **Balance Tracking**: Monitors the remaining principal and due dates for monthly interest payments.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Liquidity Station** | Borrowing Power Calculator | `stock_lending_svc.calculate_borrowing_power()` |
| **Liquidity Station** | Borrow vs. Sell Decision Tool| `stock_lending_svc.analyze_borrow_vs_sell()` |
| **Portfolio Detail** | Collateral LTV Status | `stock_lending_svc.calculate_borrowing_power()` |
| **Lending Panel** | IO Payment Schedule | `payment_schedule_tracker.generate_io_schedule()` |
| **Document Hub** | Credit Agreement Summary | `lending` logic (Interest rates/Terms) |

## Dependencies
- `decimal`: Used for all high-precision financial math (LTV, tax rates, and interest payments).
- `datetime / timedelta`: Orchestrates the monthly due dates for loan repayment schedules.
- `logging`: Records structural events like "Significant Borrowing Capacity Identified" or "Loan vs. Sell Recommendations."

## Usage Examples

### Calculating Max Borrowing Power for a Concentrated Holder
```python
from services.lending.stock_lending_svc import StockLendingService
from decimal import Decimal

lending = StockLendingService()

# Client holds $10M of a ticker with 25% volatility
capacity = lending.calculate_borrowing_power(
    symbol="NVDA",
    position_value=Decimal("10000000.00"),
    volatility_pct=25.0
)

print(f"Asset: {capacity['symbol']}")
print(f"Max LTV: {capacity['max_ltv']:.1%}")
print(f"Available Liquidity: ${capacity['available_liquidity']:,.2f}")
```

### Performing a "Borrow vs. Sell" Tax Break-Even Analysis
```python
from services.lending.stock_lending_svc import StockLendingService
from decimal import Decimal

lending = StockLendingService()

# Evaluate selling $1M vs borrowing at 6% interest
res = lending.analyze_borrow_vs_sell(
    position_value=Decimal("1000000.00"),
    cost_basis=Decimal("100000.00"),
    cap_gains_rate=Decimal("0.238"), # 23.8% rate
    loan_interest_rate=Decimal("0.06") # 6% interest
)

print(f"One-Time Tax Cost of Sale: ${res['one_time_tax_cost']:,.2f}")
print(f"Annual Interest Cost: ${res['annual_loan_interest']:,.2f}")
print(f"Break-even: {res['breakeven_years']} years")
print(f"Strategy Recommendation: {res['recommendation']}")
```

### Generating an 12-Month Interest-Only Schedule
```python
from services.lending.payment_sched import PaymentScheduleTracker
from decimal import Decimal

tracker = PaymentScheduleTracker()

# Generate a 1-year IO schedule for a $5M draw
schedule = tracker.generate_io_schedule(
    principal=Decimal("5000000.00"),
    rate_pct=6.25,
    months=12
)

for payment in schedule[:3]: # Show first 3 months
    print(f"Period {payment['period']} | Due: {payment['due_date']} | Interest: ${payment['interest_payment']:,.2f}")
```


---

## Source: service_lifestyle.md

# Backend Service: Lifestyle (Social Class Maintenance)

## Overview
The **Lifestyle Service** (internally known as **SCM - Social Class Maintenance**) manages the platform's luxury expenditure and inter-generational stability infrastructure. It goes beyond simple expense tracking by modeling **Personal Inflation (CLEW Index)**—the divergence of luxury goods/services from standard CPI—and projecting the impact of family growth on wealth-per-head across multiple generations. Its primary objective is to quantify and mitigate the risk of "Social Class Dilution."

## Core Components

### 1. CLEW Index & Personal Inflation (`scm_service.py`)
Tracks the real cost of maintaining a UHNW lifestyle.
- **Luxury Inflation (CLEW)**: Models the inflation rates of weighted luxury components: Services (security/staff), Private Aviation, Elite Education, and Collectibles. It calculates a "Luxury Inflation Alpha"—the gap between standard consumer inflation and the actual cost increase for a high-net-worth individual.

### 2. Generational Dilution Tracker (`scm_service.py`)
Predicts the sustainability of a legacy across family branches.
- **Wealth-per-Heir Projection**: Projects total wealth and wealth-per-person across N generations based on family growth assumptions (heirs per branch). It helps family offices understand the required "Internal Rate of Return" (IRR) to maintain a specific social standing as the family tree expands.

### 3. Class Risk & Stability Simulator (`scm_service.py`)
A quantitative audit of lifestyle sustainability.
- **Class Stability Monte Carlo**: Simulates the probability of maintaining a current social class across a client's life expectancy. It accounts for the annual "Burn Rate," net worth, and luxury inflation skews to determine if a lifestyle is "SECURE" or "AT RISK" of degrading the principal over time.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Lifestyle Station**| CLEW Index Pulse | `scm_service.calculate_clew_index()` |
| **Legacy Station** | Generational Dilution Graph | `scm_service.project_wealth_dilution()` |
| **Governance Hub** | Class Maintenance Probability| `scm_service.run_class_risk_sim()` |
| **Lifestyle Station**| Sustainable Burn Monitor | `scm_service.run_class_risk_sim()` |
| **Portfolio Detail** | Luxury Inflation Alpha Card | `scm_service.calculate_clew_index()` |

## Dependencies
- `decimal`: Used for all precision math involving inflation rates, burn rates, and generational wealth distributions.
- `logging`: Records structural insights like "High Wealth Dilution Detected" or "Class Stability Probability Shifts."

## Usage Examples

### Calculating the CLEW Index (Personal Inflation)
```python
from services.lifestyle.scm_service import SCMService
from decimal import Decimal

scm = SCMService()

# Luxury cost inputs (e.g., Private flights inflated 12%, Education 9%)
input_rates = {
    "PRIVATE_FLIGHTS": Decimal("0.12"),
    "ELITE_EDUCATION": Decimal("0.09")
}

stats = scm.calculate_clew_index(components=input_rates)

print(f"Personal Inflation Rate (CLEW): {stats['clew_index_rate']:.2%}")
print(f"Lux Inflation Alpha: {stats['lux_inflation_alpha']:.2%}")
```

### Projecting Wealth Dilution Across 3 Generations
```python
from services.lifestyle.scm_service import SCMService
from decimal import Decimal

scm = SCMService()

# Starting wealth $500M, 3 heirs per generation, over 3 generations
dilution = scm.project_wealth_dilution(
    net_worth=Decimal("500000000.00"),
    heirs=3,
    generations=3
)

for d in dilution:
    print(f"Gen {d['generation']} | Total: ${d['total_wealth']:,.0f} | Per Heir: ${d['wealth_per_heir']:,.0f}")
```

### Running a Class Maintenance Simulator
```python
from services.lifestyle.scm_service import SCMService
from decimal import Decimal

scm = SCMService()

# $50M Net Worth, $2.5M Annual Lifestyle Burn, 7% Luxury Inflation
sim = scm.run_class_risk_sim(
    net_worth=Decimal("50000000.00"),
    annual_burn=Decimal("2500000.00"),
    clew_rate=0.07
)

print(f"Stability Status: {sim['status']}")
print(f"Probability of Class Persistence: {sim['probability']:.0%}")
print(f"Recommended Sustainable Burn: ${sim['sustainable_annual_burn']:,.2f}")
```


---

## Source: service_logging.md

# Backend Service: Logging (Internal Telemetry)

## Overview
The **Logging Service** (specifically the **Warden Health Log**) serves as the platform's diagnostic persistence layer. It is responsible for capturing and storing the results of automated system health checks performed by the **Warden Service**. By providing a structured ledger of infrastructure stability and component availability, it enables real-time monitoring and historical analysis of the Sovereign OS's operational uptime.

## Core Components

### 1. Warden Health Log (`health_log.py`)
The system's diagnostic recorder.
- **Check-Result Persistence**: Processes and logs the detailed output of the Warden's health checks (e.g., Database connectivity, API latency, Memory usage).
- **Status Ledgering**: Standardizes check results into an `OVERALL_STATUS` (e.g., HEALTHY, DEGRADED, CRITICAL) for simplified frontend visualization and alerting.
- **Audit Traceability**: Provides a historical trace for infrastructure troubleshooting, allowing engineers to correlate system errors with specific health-check failures.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **System Monitor** | Warden Infrastructure Pulse | `health_log.log_check()` |
| **Admin Station** | Diagnostic Success Ledger | `health_log.log_check()` (Status tags) |
| **Warden Command** | Stability Trend-Line | `health_log` (Historical results) |
| **Global UI** | System Status Badge | `health_log` (Current status state) |

## Dependencies
- `datetime`: Provides micro-second precision timestamps for diagnostic event correlation.
- `logging`: Mirrors health-check results to the application-level logs for centralized log management (e.g., ELK Stack / Datadog).

## Usage Examples

### Logging a Successful System Health Check
```python
from services.logging.health_log import HealthLog

logger_svc = HealthLog()

# Mock result from the Warden service
result = {
    "timestamp": "2026-02-06T23:55:00Z",
    "overall_status": "HEALTHY",
    "services": {
        "postgres": "UP",
        "redis": "UP",
        "neo4j": "UP"
    }
}

logger_svc.log_check(check_result=result)
# Console: WARDEN_CHECK_LOG: HEALTHY - {'timestamp': ...}
```

### Logging a Degraded System State
```python
from services.logging.health_log import HealthLog

logger_svc = HealthLog()

# Mock result indicating memory pressure
result = {
    "timestamp": "2026-02-06T23:58:00Z",
    "overall_status": "DEGRADED",
    "alerts": ["JVM Memory Pressure on Searcher Agent 04"]
}

logger_svc.log_check(check_result=result)
```


---

## Source: service_market.md

# Backend Service: Market (Tactical Intelligence)

## Overview
The **Market Service** is the platform's core tactical data and sentiment infrastructure. It processes high-frequency "Market Bytes," normalizing heterogeneous Level 2 order depth from multiple liquidity providers into a consistent internal format. Beyond raw data, the service provides advanced quantitative metrics such as **VWAP-for-Size** (execution price estimation), **Orderflow Toxicity (VPIN)** for liquidity crash prediction, and a composite **Fear & Greed Index** to gauge macro-sentiment regimes.

## Core Components

### 1. Level 2 Orderbook Parser (`level2_parser.py`)
The system's high-fidelity data bridge.
- **Normalization Engine**: Transforms raw depth payloads from disparate providers into a standardized snapshot featuring sorted Bids/Asks, mid-prices, and spread calculations. It ensures that all tactical agents operate on a unified view of the market's limit order book.

### 2. Liquidity Aggregator (`depth_aggregator.py`)
Computes execution-quality and depth metrics.
- **VWAP-for-Size**: Estimates the actual fill price for a specific order size by traversing the order book levels (essential for non-slippage trading).
- **Volume Imbalance**: Calculates the net volume bias within a specific price range (e.g., ±5 pips) to detect hidden selling pressure or "Bid Walls."

### 3. Fear & Greed Sentiment Service (`fear_greed_service.py`)
The platform's psychological barometer.
- **Composite Sentiment**: Merges VIX (Volatility) contribution with momentum proxies to generate a score from 0-100 (Extreme Fear to Extreme Greed).
- **Regime Classification**: Categorizes the market into sentiment buckets, allowing risk-management agents to proactively adjust exposure based on the prevailing psychological regime.

### 4. Toxicity Monitor (`toxicity_monitor.py`)
Detects impending liquidity crises via Orderflow Toxicity.
- **VPIN (Volume-synchronized Probability of Informed Trading)**: Measures the imbalance between buy/sell volume relative to total volume. Significant spikes in VPIN ("Toxicity Alerts") indicate that informed traders may be overwhelming market markers, signaling an impending liquidity vacuum or price crash.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trading Terminal** | Real-Time Depth Visualizer | `level2_parser.parse_depth_event()` |
| **Trading Terminal** | Slippage Estimator (VWAP) | `depth_aggregator.get_vwap_for_size()` |
| **Market Intelligence** | Fear & Greed Dial | `fear_greed_service.get_latest()` |
| **System Monitor** | Liquidity Toxicity Alert | `toxicity_monitor.calculate_vpin_status()` |
| **Portfolio Detail** | Sentiment Component Table | `fear_greed_service.calculate_score()` |

## Dependencies
- `math / random`: Generates sentiment simulations and composite weightings.
- `datetime`: Provides micro-second precision for high-frequency pricing data.
- `logging`: Records structural events like "Significant Liquidity Imbalance" or "Extreme Toxicity Detected."

## Usage Examples

### Normalizing a Raw Level 2 Depth Event
```python
from services.market.level2_parser import Level2Parser

parser = Level2Parser()

# Raw feed from a liquidity provider
raw_msg = {
    "symbol": "BTC/USD",
    "timestamp": "2026-02-06T23:55:00Z",
    "bids": [{"price": 42000.50, "size": 1.5}, {"price": 41999.00, "size": 10}],
    "asks": [{"price": 42001.00, "size": 2.1}, {"price": 42002.50, "size": 5.0}]
}

book = parser.parse_depth_event(payload=raw_msg)
print(f"Mid: {book['mid']} | Spread: {book['spread']} | Depth: {book['depth_levels']} levels")
```

### Estimating Fill Price (VWAP) for a Large SELL Order
```python
from services.market.depth_aggregator import DepthAggregator

aggregator = DepthAggregator()

# book comes from parser...
size_to_sell = 10.0
vwap = aggregator.get_vwap_for_size(book=book, size=size_to_sell, direction="SELL")

print(f"Projected Fill Price for {size_to_sell} units: ${vwap:,.2f}")
```

### Checking for Orderflow Toxicity
```python
from services.market.toxicity_monitor import ToxicityMonitor

monitor = ToxicityMonitor()

# Input: 500 Buy units, 2500 Sell units in a single volume bucket
status = monitor.calculate_vpin_status(buy_volume=500, sell_volume=2500, avg_vpin=0.20)

if status['toxicity_alert']:
    print(f"TOXICITY ALERT! Score: {status['vpin_score']} | Risk: {status['liquidity_risk']}")
```


---

## Source: service_market_data.md

# Backend Service: Market Data (Structural Flow Intelligence)

## Overview
The **Market Data Service** (internally known as **Structural Flow Intelligence**) is the platform's deep-intelligence layer. It focuses on identifying structural imbalances and institutional movements that aren't visible in raw price tick data. The service follows sophisticated quantitative theses, such as **Michael Green's "Forced Seller"** model (passive index fragility), tracks **Whale Selling Pressure** via 13F filing deltas, and monitors **Volume Promo Spikes** to identify social-media-driven pumps that create artificial exit liquidity for insiders.

## Core Components

### 1. Forced Seller & Passive Fragility Tracker (`forced_seller_svc.py`)
Analyzes the structural risks of passive indexing.
- **Passive Concentration Index**: Scores tickers based on their percentage of passive ownership. High passive concentration indicates structural "inelasticity"—where mandatory buying/selling by index funds can cause violent price swings independent of fundamentals.
- **Liquidity Trap Detector**: Monitors bid/ask spread expansion relative to historical averages. It triggers a "Halt" signal if the spread expands by >2.5x, indicating a liquidity vacuum where active trading becomes dangerous.

### 2. Whale Flow & Crowding Analyzer (`fund_flow_service.py`)
Tracks the footprints of institutional capital.
- **Whale Selling Tracker**: Analyzes 13F and institutional filing data to detect "Agitator Selling"—aggressive exit pressure (>1M shares) by major hedge funds or asset managers.
- **Sector Overcrowding Engine**: Identifies when specific sectors (e.g., Tech, Energy) become structurally overcrowded by institutional "Long" mandates, signaling a higher risk of a sharp multi-trader exit.

### 3. Volume & Promo Monitor (`volume_monitor.py`)
Detects artificial activity and sentiment spikes.
- **Promo Spike Detector**: Cross-references volume spikes (>2x average) with extreme social media sentiment to identify "Promotional Pumping." This is a critical indicator for detecting efforts to create sellable volume for Rule 144 affiliate sales or institutional exits.
- **Weekly Volume Baseline**: Establishes a 4-week moving average of trading volume to provide a stable baseline for anomaly detection.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Whale Watch Terminal** | Institutional Exit Feed | `fund_flow_service.track_whale_selling()` |
| **Whale Watch Terminal** | Passive Fragility Heatmap | `forced_seller_svc.monitor_passive_flow()` |
| **Market Intelligence** | Sector Overcrowding Dial | `fund_flow_service.detect_sector_overcrowding()` |
| **System Monitor** | Liquidity Trap Warning | `forced_seller_svc.detect_liquidity_trap()` |
| **Governance Hub** | Promo/Hype Alert Ticker | `volume_monitor.detect_promo_spike()` |

## Dependencies
- `decimal`: Used for all high-precision calculations involving ownership percentages and flow velocities.
- `json / logging`: Manages the ingestion of Kafka-based volume alerts and records structural risk events.

## Usage Examples

### Detecting Structural Fragility in an Index Heavyweight
```python
from services.market_data.forced_seller_svc import ForcedSellerService

fs_svc = ForcedSellerService()

# Ticker with 75% passive ownership (e.g., a core S&P 500 component)
report = fs_svc.monitor_passive_flow(ticker="AAPL", passive_ownership_pct=75.0)

print(f"Ticker: {report['ticker']} | Fragility Score: {report['fragility_score']}")
print(f"Risk Level: {report['risk_level']}")
if report['risk_level'] == "CRITICAL":
    print("WARNING: Price is structurally inelastic to active supply/demand.")
```

### Tracking Aggressive 'Whale' Exit Pressure
```python
from services.market_data.fund_flow_service import FundFlowService

whale_svc = FundFlowService()

# Latest filing deltas for a specific stock
deltas = [
    {"holder": "WHALE_FUND_A", "change": -2500000}, # Sold 2.5M shares
    {"holder": "WHALE_FUND_B", "change": -1200000}
]

report = whale_svc.track_whale_selling(ticker="TSLA", filing_data=deltas)

print(f"Signal: {report['signal']} | Major Sellers: {', '.join(report['major_sellers'])}")
print(f"Total Institutional Pressure: {report['total_whale_sold']:,} shares")
```

### Identifying a Social-Media-Driven Volume Spike
```python
from services.market_data.volume_monitor import VolumeMonitor

monitor = VolumeMonitor()

# Input: Current Vol 5M vs Avg Vol 1M, with extremely positive social hype (0.95)
spike = monitor.detect_promo_spike(
    ticker="PUMP_TICKER", 
    current_vol=5000000, 
    avg_vol=1000000, 
    social_sentiment_score=0.95
)

if spike['is_promo_spike']:
    print(f"FLAGGED: {spike['ticker']} is undergoing a PROMO SPIKE.")
    print(f"Action: {spike['action']}")
```


---

## Source: service_marketplace.md

# Backend Service: Marketplace

## Overview
The **Marketplace Service** is the platform's ecosystem and extensibility infrastructure. It provides a standardized **Extension Framework** that allows third-party developers and institutions to build, validate, and deploy plugins and strategies within the Sovereign OS environment. The service manages the entire lifecycle of an extension—from sandboxed development and security validation to public listing, user reviews, and secure installation.

## Core Components

### 1. Extension Framework (`extension_framework.py`)
The foundational layer for third-party contributions.
- **Sandboxed Development**: Enables developers to create and test extensions in a secure, isolated environment before submission.
- **Security Validation Pipeline**: Performs automated security and code-quality checks on submitted extensions to ensure they comply with the platform's Zero-Trust architecture.
- **Extension Registry**: Manages versioning and metadata for all available plugins, ensuring that users always have access to stable and authenticated code.

### 2. Marketplace Orchestration (`marketplace_service.py`)
The consumer-facing layer for strategy and tool discovery.
- **Discovery & Listing**: Provides a searchable catalog of extensions categorized by functionality (e.g., Risk, Trading, Reporting).
- **Reputation & Feedback**: Manages a granular review and rating system, allowing the community to vet the effectiveness of various third-party strategies.
- **Installation Management**: Orchestrates the secure deployment of extensions into a user's local instance, maintaining a ledger of active installations and subscription states.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Marketplace Station**| Extension Grid / Catalog | `marketplace_service.get_extension_reviews()` |
| **Marketplace Station**| Review & Rating Form | `marketplace_service.add_review()` |
| **Marketplace Station**| Extension Detail View | `extension_framework.cache_service` |
| **Developer Console** | Extension Creation Wizard | `extension_framework.create_extension()` |
| **Developer Console** | Security Audit Results | `extension_framework.validate_extension()` |
| **System Settings** | Installed Plugins Ledger | `marketplace_service.install_extension()` |

## Dependencies
- `services.system.cache_service`: Persists extension metadata, reviews, and installation records.
- `schemas.marketplace`: Defines the standard `Extension`, `ExtensionStatus`, and `ExtensionReview` models.
- `SecurityService`: (External) Performs deep-packet inspection of extension code during validation.

## Usage Examples

### Creating a New Developer Extension
```python
from services.marketplace.extension_framework import get_extension_framework

framework = get_extension_framework()

# Developer submits a new Momentum Alpha strategy
extension = await framework.create_extension(
    developer_id="dev_black_swann_001",
    extension_name="Hyper-Momentum-V2",
    description="Captures volatility breakout signals in G10 FX pairs.",
    version="1.0.0",
    category="Trading Strategy"
)

print(f"Extension Registered: {extension.extension_id} (Status: {extension.status})")
```

### Validating an Extension for Production
```python
from services.marketplace.extension_framework import get_extension_framework

framework = get_extension_framework()

# (Simulated) Run the validation pipeline
# extension comes from the framework
report = await framework.validate_extension(extension=extension)

if report['valid']:
    print(f"Security Audit PASSED. Timestamp: {report['timestamp']}")
else:
    print(f"Audit FAILED: {report['security']['errors']}")
```

### Installing a Strategy for a Client
```python
from services.marketplace.marketplace_service import get_marketplace_service

marketplace = get_marketplace_service()

# Client installs the strategy to their instance
install = await marketplace.install_extension(
    extension_id="ext_dev_001_123456789",
    user_id="user_vanderbilt_001"
)

print(f"Installation Success: {install['installation_id']}")
print(f"Status: {install['status']} | Active since: {install['installed_date']}")
```


---

## Source: service_memory_service.md

# Backend Service: Memory Service (Long-Term Agent Memory)

## Overview
The **Memory Service** is the platform's "Hippocampus"—providing the infrastructure for agents to store and recall long-term experiences. It enables experiential learning by transforming textual agent logs into high-dimensional semantic vectors. These vectors are indexed in a high-performance vector database (Postgres + `pgvector`), allowing agents to perform RAG (Retrieval-Augmented Generation) on their own past successes and failures. Crucially, the service includes a "Scrubber" layer to ensure that all stored memories are redacted of sensitive PII/PHI before being permanented.

## Core Components

### 1. Semantic Embedding Engine (`memory_service.py`)
Transformers agent actions into searchable vectors.
- **Model Orchestration**: Utilizes the `nomic-ai/nomic-embed-text-v1.5` model to generate 768-dimensional embeddings. It uses specific prefixes (`search_document:` vs `search_query:`) to optimize the vector space for retrieval tasks.
- **Lazy Loading**: The model is lazily loaded only when a memory operation is performed, optimizing system memory for lightweight agent instances.

### 2. Experience Archival & Scrubbing (`memory_service.py`)
Ensures safe and permanent retention of agent history.
- **PII/PHI Scrubber**: Before any experience is vectorized, it is passed through the `scrubber` utility to redact names, addresses, and sensitive financial identifiers, ensuring compliance with privacy standards even in long-term storage.
- **pgvector Persistence**: Stores memories in a specialized `agent_memories` table with HNSW indexing for sub-millisecond similarity search.

### 3. Semantic Recall System (`memory_service.py`)
Enables agents to "remember" relevant context.
- **Similarity Search**: Performs a cosine similarity search (`<=>` operator) against the stored vector space to retrieve the top-N memories most relevant to a current query or task.
- **Similarity Thresholding**: Allows for fine-grained control over recall quality by filtering results below a certain similarity score (e.g., 0.70).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Agent Command** | Memory Frequency Pulse | `memory_service.store_experience()` |
| **Agent Command** | Knowledge Retrieval Terminal| `memory_service.recall_memories()` |
| **System Admin** | Vector Index Status | `memory_service.pgvector_context` |
| **Governance Hub** | Redaction Audit Ledger | `memory_service.scrubber` |
| **Portfolio Detail** | Agent Experience Tooltip | `memory_service.recall_memories()` |

## Dependencies
- `sentence-transformers`: The core engine for generating semantic embeddings.
- `numpy`: Used for internal vector manipulation.
- `pgvector`: (Database Extension) Provides vector-specific indices and operators in Postgres.
- `utils.scrubber`: Redacts sensitive information from experiences.

## Usage Examples

### Storing a New Agent Experience
```python
from services.memory_service import memory_service

# Agent records a successful trade execution strategy
await memory_service.store_experience(
    dept_id=1, # Trading Dept
    mission_id="mission_123",
    content="Successfully avoided slippage by splitting orders across 4 liquidity providers.",
    metadata={"strategy": "VWAP_SPLIT", "success": True}
)
```

### Recalling Relevant Memories for a Current Task
```python
from services.memory_service import memory_service

# Agent is planning a new large order and wants to 'recall' past experiences
query = "How to minimize slippage on large block trades?"
memories = await memory_service.recall_memories(
    query=query,
    limit=3,
    min_similarity=0.75
)

for m in memories:
    print(f"[{m['similarity']:.2f}] Memory: {m['content']}")
    print(f"Metadata: {m['metadata']}")
```


---

## Source: service_meta_optimizer.md

# Backend Service: Meta Optimizer (Sovereign Singularity)

## Overview
The **Meta Optimizer Service** (internally designated as **Mission 200: The Sovereign Singularity**) is the platform's self-architecting engine. It represents the highest level of system autonomy, where the AI Investor analyzes its own department-wide performance to self-optimize and propose new strategic missions. By auditing "Alpha Reports," the Meta Optimizer identifies structural winning streaks and failures, generating actionable proposals to scale up dominant mission fleets, trim underperforming exposure, and spawn cross-sector "Arb-Missions" to capture emerging inefficiencies.

## Core Components

### 1. Optimization Cycle Engine (`meta_optimizer.py`)
Orchestrates the system's self-improvement loops.
- **Alpha Performance Audit**: Decrypts and analyzes the Secure EOD (End of Day) reports from the Alpha Reporting service. it maps ROI across all sectors (e.g., Tech, Energy, Crypto) to identify the current "Alpha Dominant" sector.
- **Dynamic Fleet Scaling**: Generates reinforcement proposals for winning sectors (scaling mission fleets by +20%) and risk mitigation proposals for negative-alpha sectors (reducing exposure by 50%).

### 2. Meta-Mission Discovery (`meta_optimizer.py`)
The system's R&D and "Strategy Spawning" logic.
- **Arb-Mission Spawning**: Detects high-variance gaps between the best and worst-performing sectors. It proposes new "Meta-Missions" designed to arbitrage these price inefficiencies, treating the system's own performance discrepancies as a high-fidelity trade signal.
- **Proposal Persistence**: Maintains a historical ledger of all "Sovereign Strategy Proposals," allowing human operators (and higher-level governor agents) to audit the system's self-modification logic over time.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Sovereign Singularity** | Optimization Cycle Pulse | `meta_optimizer_service.run_optimization_cycle()` |
| **Sovereign Singularity** | Active Strategy Proposals | `meta_optimizer_service.get_proposal_history()` |
| **Sovereign Singularity** | Reinforcement Rationale Card| `meta_optimizer_service.proposal_history` |
| **Governance Hub** | System Evolution Ledger | `meta_optimizer_service.proposal_history` |
| **Mission Control** | Proposed Arb-Missions | `meta_optimizer_service.run_optimization_cycle()` |

## Dependencies
- `services.analytics.alpha_reporting`: Provides the primary performance data used for system audits.
- `json / logging`: Manages the generation and recording of sovereign strategy proposals.

## Usage Examples

### Executing an Autonomous Optimization Cycle
```python
from services.meta_optimizer import get_meta_optimizer_service

optimizer = get_meta_optimizer_service()

# Run the 'Sovereign Singularity' audit after market close
proposals = optimizer.run_optimization_cycle()

print(f"Cycle Complete. Generated {len(proposals)} Proposals.")

for p in proposals:
    print(f"[{p['type']}] Action: {p['action']}")
    print(f"Rationale: {p['rationale']}")
```

### Auditing the History of System Self-Optimizations
```python
from services.meta_optimizer import get_meta_optimizer_service

optimizer = get_meta_optimizer_service()

# Retrieve all previously generated strategy proposals
history = optimizer.get_proposal_history()

for prop in history:
    print(f"Recorded Proposal ID: {prop['id']} for Sector: {prop['target']}")
```


---

## Source: service_mfo.md

# Backend Service: MFO (Multi-Family Office)

## Overview
The **MFO (Multi-Family Office) Service** provides the administrative and lifestyle infrastructure required to manage multiple high-net-worth families within a single institutional framework. It enables shared office operations by automating the allocation of overhead costs (Staff, Tech, Rent), orchestrating professional concierge and expert network requests, and aggregating group spending to unlock institutional-grade vendor discounts and leverage that individual families could not achieve alone.

## Core Components

### 1. Shared Concierge & Expert Router (`concierge_srv.py`)
Centralized management of lifestyle and professional requests.
- **Lifestyle Ticketing**: Routes and prioritizes requests (from travel and jets to urgent security) into a shared MFO concierge queue. It identifies VIP priority based on the nature and urgency of the request.
- **Expert Network Access**: Interfaces with a vetted professional network (via Neo4j) to locate specialists in domains like legal, tax, or fine art, ensuring MFO-wide discount rates are applied.

### 2. Overhead Expense Allocator (`expense_allocator.py`)
Automates the splitting of MFO operational costs.
- **Pro-Rata AUM Allocation**: Default methodology that splits shared costs (e.g., Bloomberg terminals, shared office rent) proportionally based on each family's Assets Under Management (AUM).
- **Fixed Split Allocation**: Alternative methodology that applies an equal fixed-cost burden across all participating families regardless of size.

### 3. Vendor Leverage Aggregator (`spend_aggregator.py`)
Pools family spending to achieve institutional benefits.
- **Group Negotiation Power**: Aggregates the total spending of all member families with specific vendors. If the aggregate spend exceeds specific thresholds (e.g., >$1M), it automatically unlocks "Tier 1" institutional discounts, providing group leverage that benefits every participating family.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Concierge Hub** | Active Lifestyle Tickets | `concierge_service.create_lifestyle_request()` |
| **MFO Admin Panel** | Overhead Allocation Table | `mfo_expense_allocator.split_monthly_overhead()` |
| **MFO Admin Panel** | Vendor Leverage Tracker | `mfo_spend_aggregator.calculate_group_leverage()` |
| **Governance Hub** | Vetted Expert Directory | `concierge_service.fetch_expert_access()` |
| **System Settings** | MFO Billing Summary | `mfo_expense_allocator` (Allocation results) |

## Dependencies
- `decimal`: Used for all precision math involving overhead splits and aggregate spending.
- `uuid`: Generates unique identifiers for family accounts and concierge tickets.
- `logging`: Records structural MFO events like "Threshold Reached for Vendor Discount" or "Overhead Allocation Finalized."

## Usage Examples

### Creating a High-Priority Concierge Request
```python
from services.mfo.concierge_srv import ConciergeService
import uuid

concierge = ConciergeService()
family_id = uuid.uuid4()

# Client requests an urgent private jet charter
req = concierge.create_lifestyle_request(
    family_id=family_id,
    req_type="TRAVEL",
    detail="URGENT: Need private charter from London to Zurich for Family Council."
)

print(f"Ticket: {req['ticket_id']} | Priority: {req['priority']} | Team: {req['assigned_team']}")
```

### Allocating MFO Overhead via Pro-Rata AUM
```python
from services.mfo.expense_allocator import MFOExpenseAllocator
from decimal import Decimal

allocator = MFOExpenseAllocator()

# Shared office overhead for the month: $250k
overhead = Decimal("250000.00")

# Families and their current AUMs
aums = {
    "Family_Vanderbilt": Decimal("1200000000.00"),
    "Family_Astor": Decimal("800000000.00")
}

splits = allocator.split_monthly_overhead(total_overhead=overhead, family_aums=aums)

for s in splits:
    print(f"Family: {s['family_id']} | Share: ${s['amount']:,} (Method: {s['method']})")
```

### Unlocking Group Leverage via Spend Aggregation
```python
from services.mfo.spend_aggregator import MFOSpendAggregator

aggregator = MFOSpendAggregator()

# Total spends at a specific provider (e.g., Wheels Up) across all MFO families
provider_spends = [400000, 350000, 300000] # Total > $1M

leverage = aggregator.calculate_group_leverage(vendor_name="GlobalAero", family_spends=provider_spends)

print(f"Vendor: {leverage['vendor']} | Aggregate Spend: ${leverage['aggregate_spend']:,.2f}")
print(f"Discount Unlocked: {leverage['group_discount_pct']}% | Status: {leverage['status']}")
```


---

## Source: service_middleware.md

# Backend Service: Middleware (Sovereign Kernel)

## Overview
The **Middleware Service** (also known as the **Sovereign Kernel**) operates as the gatekeeper for the entire platform. It enforces the system's "Zero-Trust" security model by intercepting every HTTP request before it reaches business logic. Its most critical component is the **Sovereign Signature Enforcement**, which mandates that all state-mutating operations (writes/edits) must be cryptographically signed by a hardware authenticator (WebAuthn/YubiKey/TouchID), preventing unauthorized changes even if a session token is hijacked. Additionally, it handles high-performance caching (Redis) and rate-limiting to protect external API quotas.

## Core Components

### 1. Sovereign Signature Enforcement (`sovereign_signature_middleware.py`)
the "Nuclear Keys" of the platform.
- **Biometric Write-Protection**: Intercepts `POST`, `PUT`, and `DELETE` requests to critical endpoints (e.g., `v1/ledger`, `v1/orders`). It rejects any request that lacks a valid `X-Sovereign-Signature` header.
- **Challenge-Response Protocol**: Verifies that the signature was generated using a private key held on the user's physical device (Passkey) and matches the specific command payload, preventing replay attacks.
- **Authorization Bypass (Dev Mode)**: Includes a strict "Dev-Only" bypass for local testing, which must be disabled in production.

### 2. API Gateway Cache (`cache_layer.py`)
Reduces latency and external costs.
- **Response Caching**: Caches idempotent `GET` requests (e.g., market data quotes, portfolio summaries) in Redis. This prevents redundant calls to expensive external providers like AlphaVantage or Bloomberg, significantly reducing API costs.
- **Smart Invalidation**: (Planned) Automatically invalidates cache entries when underlying data changes (e.g., a new trade clears).

### 3. Failover & Rate Limiter (`failover.py`, `rate_limiter.py`)
Ensures system resilience.
- **Circuit Breaker**: Detects when a primary data provider (e.g., primary exchange feed) is down and automatically routes requests to a backup provider.
- **Quota Enforcer**: Tracks API usage against defined limits (e.g., "5 calls/min to AlphaVantage"). It queues or rejects excess requests to prevent account bans.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Global** | API Client (`apiClient.js`) | `cache_layer` | **Partially Implemented** (Basic caching headers present) |
| **All Write Forms** | "Sign & Submit" Modal | `sovereign_signature_middleware` | **Missing / Backend Only** |
| **System Monitor** | Gateway Health Status | `rate_limiter` | **Missing / Backend Only** |

> [!WARNING]
> **Frontend Gap Identifier**: The `Sovereign-Signature` header is currently enforced on the backend but is **NOT yet implemented** in the frontend `apiClient.js`. Write operations will currently fail with `401 Unauthorized` until the frontend functionality for WebAuthn signing is built.

## Dependencies
- `fastapi`: Provides the dependency injection framework for attaching middleware to routes.
- `services.auth.sovereign_auth_service`: Performs the actual cryptographic verification of the signatures.
- `redis`: (Implied) Backing store for cache and rate-limit counters.

## Usage Examples

### Protecting a Critical Route with Sovereign Signature
```python
from fastapi import APIRouter, Depends
from services.middleware.sovereign_signature_middleware import require_sovereign_signature

router = APIRouter()

@router.post("/ledger/transfer", dependencies=[Depends(require_sovereign_signature)])
async def execute_transfer(transfer_request: TransferSchema):
    # This code ONLY executes if the request has a valid cryptographic signature
    # matching the transfer_request body.
    return ledger.process_transfer(transfer_request)
```

### Checking Rate Limits before External Call
```python
from services.middleware.rate_limiter import GatewayRateLimiter

limiter = GatewayRateLimiter()

if limiter.is_allowed(provider="OPENAI"):
    # Safe to call API
    response = call_openai_gpt4()
else:
    # Rate limit exceeded
    raise HTTPException(status_code=429, detail="Rate limit exceeded for AI provider")
```


---

## Source: service_mission_service.md

# Backend Service: Mission Service (Autonomous Squads)

## Overview
The **Mission Service** is the platform's operational commander. It transforms high-level user objectives (e.g., "Find M&A Targets" or "Liquidate Crypto Assets") into executable, multi-agent workflows. By utilizing a "Template Registry," the service allows users to deploy pre-configured squads of agents with specific roles, budgets, and risk parameters. It orchestrates the lifecycle of these missions—from configuration and budget allocation to the asynchronous dispatch of jobs via the ARQ task queue.

## Core Components

### 1. Mission Template Registry (`mission_service.py`)
The catalog of available autonomous operations.
- **Template Loading**: Ingests mission definitions from `config/mission_templates.json`. Each template defines the mission's goal, required departments (e.g., Wealth + Intelligence), outcome logic hash, and default constraints.
- **Example Missions**:
    - **M&A Scout**: Deploys Wealth and Intelligence agents to find acquisition targets.
    - **Crash Protocol**: Triggers Security and Finance agents for emergency asset liquidation.
    - **Shadow Mirror**: Runs a red-team security audit on internal infrastructure.

### 2. Autonomous Deployment Engine (`mission_service.py`)
Instantiates and dispatches mission squads.
- **Squad Configuration**: Merges the static template with dynamic user overrides (e.g., "Increase budget to $5,000" or "Set Time-to-Live to 2 hours").
- **ARQ Job Dispatch**: Converts the mission parameters into asynchronous jobs (`run_agent_logic`) and pushes them to the Redis-backed ARQ worker pool. This ensures that agents execute in parallel, non-blocking processes.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mission Control** | Mission Library Grid | `mission_service.get_all_templates()` | **Implemented** |
| **Mission Control** | Launch Configuration Modal| `mission_service.deploy_mission()` | **Implemented** |
| **Mission Overview** | Active Mission Tracker | `mission_service` (Job Status) | **Implemented** |
| **Orchestrator** | Visual Mission Flow | `mission_service` (Dept Dependencies) | **Implemented** |

> [!NOTE]
> **Integration Status**: The Mission Service is deeply integrated into the frontend. The `MissionControl.jsx` page provides a full UI for browsing the template library, configuring parameters, and visually monitoring the real-time status of deployed agent squads.

## Dependencies
- `config.mission_templates.json`: The source of truth for all available mission definitions.
- `arq`: The asynchronous task queue used to dispatch agent jobs to background workers.
- `uuid`: Generates unique Mission IDs (`mssn_...`) for tracking execution across the distributed system.

## Usage Examples

### Listing Available Missions for a Specific Sector
```python
from services.mission_service import get_mission_service

svc = get_mission_service()

# specific templates for 'Security' sector missions
security_missions = svc.get_all_templates(sector="Security")

for m in security_missions:
    print(f"ID: {m['id']} | Name: {m['name']}")
    print(f"Goal: {m['goal']}")
```

### Deploying a 'Crash Protocol' Mission via Code
```python
from services.mission_service import get_mission_service

svc = get_mission_service()

# Deploy emergency liquidation with elevated budget
result = await svc.deploy_mission(
    template_id="mission_002", # Crash Protocol
    config={
        "budget": 5000, # Override default $1000
        "ttl": 300 # 5 minutes max execution time
    },
    arq_pool=redis_pool_connection
)

print(f"Mission Launched: {result['mission_id']}")
print(f"Active Jobs: {len(result['jobs'])}")
```


---

## Source: service_ml.md

# Backend Service: ML (Machine Learning Pipeline)

## Overview
The **ML Service** provides the end-to-end MLOps infrastructure for the platform. It manages the complete lifecycle of predictive models—from data ingestion and training to versioning, A/B testing, and production deployment. The service is designed to support both classical ML (XGBoost, RandomForest) and deep learning workflows, ensuring that the AI Investor's decision-making engines are continuously retrained and improved without downtime.

## Core Components

### 1. Training Pipeline Orchestrator (`training_pipeline.py`)
Manages the model creation lifecycle.
- **Job Scheduling**: Creates and tracks training jobs with specific datasets and hyperparameter configurations. It maintains a ledger of all training attempts (`PENDING` -> `RUNNING` -> `COMPLETED`) to ensure reproducibility.
- **Model Versioning**: Automatically fingerprints and versions every trained model artifact. This ensures that the system can always roll back to a previous "Golden Master" if a newer model shows performance degradation.

### 2. Model Deployment Service (`model_deployment_service.py`)
Handles the transition from training to inference.
- **Gradual Rollouts**: Supports "Canary Deployments" where a new model version is rolled out to only a small percentage (e.g., 5%) of inference requests. This allows for safe A/B testing against live market data.
- **Performance Monitoring**: Tracks key metrics like inference latency, throughput, and accuracy in real-time.
- **Instant Rollback**: Provides a "Kill Switch" to immediately revert to the previous stable model version if the error rate spikes.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **System Monitor** | Tensor Monitor | `model_deployment_service.monitor_performance()` | **Implemented** (`TensorMonitor.jsx`) |
| **Admin Console** | Model Version Grid | `training_pipeline.get_job()` | **Missing** |
| **Admin Console** | Deployment Rollout Slider | `model_deployment_service.deploy_model()` | **Missing** |

> [!NOTE]
> **Integration Status**: While the `TensorMonitor` widget exists for visualizing model performance, the administrative controls for triggering training jobs or managing deployment rollouts are currently **Backend-Only**. These operations must be performed via API or CLI.

## Dependencies
- `schemas.ml_training`: Defines standard models for `TrainingJob`, `ModelVersion`, and `TrainingStatus`.
- `services.system.cache_service`: Persists job status and deployment configurations.

## Usage Examples

### Starting a New Training Job
```python
from services.ml.training_pipeline import get_training_pipeline

pipeline = get_training_pipeline()

# Launch a training run for the "Price_Predictor_v2" model
job = await pipeline.create_training_job(
    model_name="Price_Predictor_LSTM",
    dataset_id="dataset_market_2025_Q4",
    hyperparameters={"epochs": 50, "batch_size": 32, "learning_rate": 0.001}
)

# Start the job (Async)
started_job = await pipeline.start_training(job_id=job.job_id)
print(f"Training Started: {started_job.job_id} at {started_job.started_date}")
```

### Deploying a Canary Version (10% Traffic)
```python
from services.ml.model_deployment_service import get_model_deployment_service

deployment_svc = get_model_deployment_service()

# Deploy model version 'v1.2.5' to 10% of users
result = await deployment_svc.deploy_model(
    model_version=my_model_object,
    rollout_percentage=10.0
)

print(f"Deployment Active: {result['deployment_id']}")
print(f"Rollout: {result['rollout_percentage']}%")
```

### Emergency Rollback
```python
from services.ml.model_deployment_service import get_model_deployment_service

svc = get_model_deployment_service()

# Revert to previous stable version
success = await svc.rollback_model(model_id="Price_Predictor_LSTM")

if success:
    print("Rollback successful. Traffic redirected to previous version.")
```


---

## Source: service_mobile.md

# Backend Service: Mobile (Quick Actions)

## Overview
The **Mobile Service** is a lightweight compatibility layer designed to optimize the Sovereign OS experience for smaller screens. Its primary function is to expose **Quick Actions**—high-leverage, macro commands that allow a user to perform complex portfolio operations with a single tap. This is crucial for "on-the-go" management, where full dashboard interactivity is limited.

## Core Components

### 1. Quick Action Executor (`quick_actions.py`)
The command hub for mobile inputs.
- **Macro Command Logic**: Maps simple string commands (e.g., `CLOSE_ALL`) to complex backend workflows.
- **Defined Actions**:
    - **CLOSE_ALL**: Emergency liquidation of all open speculative positions.
    - **HEDGE**: Immediately buys OTM puts or short futures to delta-neutralize the portfolio.
    - **REDUCE_50**: Halves the size of every active position to reduce risk exposure.
    - **STOP_TRADING**: Activates "Zen Mode," halting all algorithmic trading bots.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mobile Layout** | Floating Action Button (FAB) | `quick_actions.execute()` | **Partial / Disconnected** |

> [!WARNING]
> **Integration Gap**: A `QuickActions.jsx` component exists in the frontend codebase, but it currently relies on hardcoded default actions (`Quick Trade`, `Deposit`) rather than the backend's defined macros (`CLOSE_ALL`, `HEDGE`). The wiring to the backend `execute()` endpoint is **not yet implemented**.

## Dependencies
- `typing`: Standard library for type safety.
- `logging`: Records mobile command execution for audit trails.

## Usage Examples

### Executing a 'Panic' Hedge Command
```python
from services.mobile.quick_actions import QuickActions

# User taps "HEDGE" on mobile app
action_result = QuickActions.execute("HEDGE")

if action_result["success"]:
    print(f"Command Executed: {action_result['description']}")
else:
    print("Invalid Mobile Command")
```

### Flattening the Portfolio (Emergency Close)
```python
from services.mobile.quick_actions import QuickActions

# User taps "CLOSE ALL"
result = QuickActions.execute("CLOSE_ALL")
# Backend would trigger OrderExecutionService to send liquidating market orders
print(result) 
# Output: {'success': True, 'action': 'CLOSE_ALL', 'description': 'Close all positions'}
```


---

## Source: service_modes.md

# Backend Service: Modes (System States)

## Overview
The **Modes Service** manages the high-level operational states of the Sovereign OS. Unlike simple configuration flags, "Modes" are systemic regimes that fundamentally alter how the platform behaves. This includes **Zen Mode** (which filters out tactical noise to focus on long-term compounding), **Shield Mode** (which locks down capital during extreme risk), and **GEX Regimes** (which adjust trading logic based on market maker gamma exposure).

## Core Components

### 1. Zen Mode Controller (`zen_mode.py`, `tactical_noise_filter.py`)
The "Homeostasis" engine for psychological safety.
- **Noise Filtering**: When activated, the `TacticalNoiseFilter` suppresses high-frequency alerts, news tickers, and PnL volatility updates. This prevents "chart staring" and FOMO-driven errors.
- **Long-Term Focus**: Shifts the dashboard UI to emphasize "Goal Progress" and "Retirement Horizons" rather than daily price action.

### 2. Volatility Regime Setter (`gex_regime.py`)
Adapts system logic to market structure.
- **Gamma Exposure (GEX) Analysis**: Calculates the total GEX of the market to determine the current volatility regime.
    - **Positive GEX**: Implies mean-reverting behavior (buy dips, sell rips).
    - **Negative GEX**: Implies correlation breakdown and crash acceleration (switch to breakout/momentum logic).

### 3. Shield Logic (`shield_logic.py`)
The global kill-switch and defense mechanism.
- **System Lockdown**: A Redis-backed state that, when active, overrides all other services to block capital outflows and new risk-taking. It is triggered by "Black Swan" events or manual intervention.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Zen Station** | Homeostasis Overlay | `zen_mode.activate()` | **Implemented** (`HomeostasisOverlay.jsx`) |
| **Zen Station** | Retirement Gauge | `zen_mode` (Goal Tracking) | **Implemented** (`RetirementGauge.jsx`) |
| **Market Dashboard** | GEX Profile Chart | `gex_regime.determine_regime()` | **Implemented** (`GEXProfile.jsx`) |
| **Global Header** | Shield Status Indicator| `shield_logic.is_active()` | **Partially Implemented** |

## Dependencies
- `redis`: Persists the Shield Mode state across system restarts.
- `logging`: Critical for auditing state transitions (e.g., "Why did the system enter Shield Mode at 03:00 AM?").

## Usage Examples

### Activating Zen Mode to Prevent Panic Selling
```python
from services.modes.zen_mode import ZenMode
from services.modes.tactical_noise_filter import TacticalNoiseFilter

zen = ZenMode()
noise_filter = TacticalNoiseFilter()

# User engages "Zen Mode" after a 5% market drop
zen.activate(reason="High stress detected. Focusing on 20-year horizon.")

# Backend suppresses all intraday price alerts
noise_filter.enable_zen()

print(f"System State: {zen.get_status()}") 
# Output: {'active': True, 'reason': 'High stress detected...'}
```

### Adjusting Strategy based on GEX Regime
```python
from services.modes.gex_regime import GEXRegimeSetter

gex_setter = GEXRegimeSetter()

# Total Market GEX (in billions)
current_gex = -2500000000.0 # -$2.5B (High Volatility Danger Zone)

regime = gex_setter.determine_regime(total_gex=current_gex)

if regime == "HIGH_VOL_CRASH_ACCELERATION":
    print("WARNING: Negative Gamma Environment. Hedging requirements doubled.")
    # Trigger hedging logic...
```


---

## Source: service_monitoring.md

# Backend Service: Monitoring (System Vitals)

## Overview
The **Monitoring Service** is the platform's "Central Nervous System," providing real-time observability into the health, performance, and security of the Sovereign OS. It aggregates metrics from all other services, tracking CPU/RAM usage, API latency, and application errors. It also serves as the dispatch hub for critical alerts, routing them to the appropriate human channels (Slack, PagerDuty, SMS) based on severity.

## Core Components

### 1. Alert Manager (`alert_manager.py`)
The unified notification dispatcher.
- **Multi-Channel Routing**: Intelligent logic that routes alerts based on severity:
    - **INFO/WARNING** -> Slack Channels.
    - **ERROR** -> Email + Slack.
    - **CRITICAL** -> PagerDuty + SMS + All Channels.
- **Context Enrichment**: automatically attaches timestamps, metadata, and stack traces to every alert payload.

### 2. Error Tracker (`error_tracker.py`)
Production-grade exception monitoring.
- **Sentry Integration**: Wraps the Python application with the Sentry SDK to capture unhandled exceptions, performance transactions, and breadcrumbs.
- **PII Scrubbing**: Configured to strip sensitive financial data from error logs before they leave the secure enclave.

### 3. Health & Latency Monitors (`health_monitor.py`, `latency_monitor.py`)
Real-time system pulse tracking.
- **Resource Vitals**: Tracks CPU, Memory, and Disk usage to detect "Zombie Services" or memory leaks via `psutil`.
- **E2E Latency**: Measures the round-trip time for critical market events (Redpanda Ingest -> Postgres Commit), alerting if processing lag exceeds 200ms.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **System Monitor** | DB Health Gauges | `health_monitor.get_system_vitals()` | **Implemented** (`DatabaseGauges.jsx`) |
| **System Monitor** | Data Source Pulse | `latency_monitor.get_average_latency()` | **Implemented** (`DataSourceHealth.jsx`) |
| **Sentry Station** | Audit Log Stream | `error_tracker` (via API logs) | **Implemented** (`SentryAudit.jsx`) |
| **Sentry Station** | Security Vault Status | `health_monitor.check_service_health()`| **Implemented** (`SentryVault.jsx`) |

## Dependencies
- `psutil`: Cross-platform library for retrieving information on running processes and system utilization.
- `sentry_sdk`: The official Python client for Sentry.io.
- `twilio`: (Optional) Library for sending SMS alerts for critical failures.

## Usage Examples

### Dispatching a Critical System Alert
```python
from services.monitoring.alert_manager import get_alert_manager, AlertLevel

alerter = get_alert_manager()

# Database connection lost - Wake up the admin!
alerter.send_alert(
    message="CRITICAL: Primary Postgres Connection Failed [ECONNREFUSED]",
    level=AlertLevel.CRITICAL,
    channels=None, # Auto-selects PagerDuty + SMS
    context={"node": "worker-01", "retry_count": 5}
)
```

### Checking System Health Vitals
```python
from services.monitoring.health_monitor import get_health_monitor

physician = get_health_monitor()
vitals = physician.get_system_vitals()

if vitals["status"] == "CRITICAL_LOAD":
    print(f"WARNING: CPU at {vitals['cpu_percent']}% | RAM at {vitals['memory_percent']}%")
else:
    print(f"System Healthy. CPU: {vitals['cpu_percent']}%")
```


---

## Source: service_neo4j.md

# Backend Service: Neo4j (Knowledge Graph)

## Overview
The **Neo4j Service** transforms the platform from a simple database into a **Knowledge Graph**. While Postgres stores *what* happened (transactions, balances), Neo4j stores *why* it matters (relationships, ownership, influence, risk contagion). It serves as the "Master Brain," merging disjointed data domains (Legal, Tax, Finance, Personal) into a single, queryable semantic network.

## Core Components

### 1. Master Graph Orchestrator (`master_graph.py`)
The unified query engine.
- **Global Unification**: Periodically runs Cypher queries to link isolated nodes (e.g., connecting a `Trust` in the Legal domain to a `Portfolio` in the Finance domain via a `BENEFICIARY_OF` relationship).
- **Reflexivity Engine**: Simulates "financial contagion." If an asset collapses, the `trigger_reflexivity_shock()` method traverses the graph to identify every downstream entity (Trust, LLC, Family Member) that gets hit, calculating a "Contagion Velocity."

### 2. Graph-Ledger Sync (`graph_ledger_sync.py`)
Ensures "Dual-State Consistency."
- **Real-Time Mirroring**: Listens for Postgres ledger commits and immediately updates the corresponding Graph nodes.
- **SLA**: Targets a <100ms sync latency to ensure that if a user buys a stock (Postgres), the Risk Graph (Neo4j) reflects the new exposure instantly.
- **Integrity Check**: The `verify_graph_ledger_integrity()` method audits both databases to ensure zero variance in account balances or entity counts.

### 3. Neo4j Driver (`neo4j_service.py`)
High-performance connection pooling.
- **Singleton Pattern**: Manages the Bolt driver connection lifecycle, ensuring efficient reuse across thousands of async requests.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Estate Planner** | Entity Graph Visualizer | `master_graph.get_graph_data()` | **Implemented** (`EntityGraph.jsx`) |
| **Orchestrator** | Network Map | `master_graph.get_search_entities()` | **Implemented** (`NetworkMap.jsx`) |
| **System Health** | Neo4j Vitals | `neo4j_service.driver.verify_connectivity()`| **Implemented** (`Neo4jHealthVitals.jsx`) |
| **Risk Dashboard** | Contagion Sim | `master_graph.trigger_reflexivity_shock()` | **Partial** (`OrchestratorGraph.jsx`) |

## Dependencies
- `neo4j`: The official Python driver for Neo4j.
- `decimal`: Required for high-precision financial calculations during sync.
- `networkx`: (Implicit/Future) usage for complex graph algorithms like centrality or max-flow.

## Usage Examples

### Triggering a "Black Swan" Simulation
```python
from services.neo4j.master_graph import MasterGraph

brain = MasterGraph()

# Simulate a 50% collapse in a Commercial Real Estate holding
shock_result = brain.trigger_reflexivity_shock(
    asset_id="asset_cre_tower_1",
    magnitude=0.50 
)

print(f"Contagion Velocity: {shock_result['contagion_velocity']}")
for victim in shock_result['affected_nodes']:
    print(f"Impacted: {victim['group']} | Loss Est: ${victim['impact']:,.2f}")
```

### Querying Global Risk Exposure
```python
from services.neo4j.master_graph import MasterGraph

# "How much are we exposed to 'Geopolitical Instability' across ALL trusts?"
results = brain.query_global_exposure(risk_factor="Geopolitical_Zone_B")

total_exposure = sum(r['exposure'] for r in results)
print(f"Total Geopolitical Risk: ${total_exposure:,.2f}")
```


---

## Source: service_news.md

# Backend Service: News (Sentiment Engine)

## Overview
The **News Service** acts as the platform's sensory organ for unstructured market data. It aggregates news from multiple providers, filters it for relevance to the user's portfolio, and applies Natural Language Processing (NLP) to generate quantitative sentiment scores. This allows the AI Investor to react not just to price action, but to the narrative driving the market.

## Core Components

### 1. News Aggregator (`news_aggregation_service.py`)
The ingestion pipeline.
- **Multi-Source Fetching**: logic to pull headlines from various APIs (currently mocked, designed for simple integration with vendors like NewsAPI or Alpha Vantage).
- **Relevance Engine**: Filters the firehose of global news down to articles that matter for the specific symbols in the user's Watchlist vs Portfolio. It boosts the "Relevance Score" based on recency and keyword matches.

### 2. Sentiment Analyzer (`sentiment_analysis_service.py`)
The NLP scoring engine.
- **Article Scoring**: Scans article titles and content for positive/negative keywords (e.g., "gain", "profit" vs "drop", "loss").
    - *Current Implementation*: Heuristic keyword counting.
    - *Architecture*: Plug-and-play compatible with advanced transformers (BERT/FinBERT).
- **Market Impact Assessment**: Combines sentiment score with "Confidence" (based on article volume) to predict potential price movement direction and magnitude.
- **Sector Heatmap**: Aggregates individual stock sentiment to gauge the mood of entire sectors (e.g., "Tech is Very Bullish," "Energy is Bearish").

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Market Dashboard** | News Feed | `news_aggregation_service.fetch_news()` | **Implemented** (`NewsFeed.jsx`) |
| **Analytics** | Sentiment Chart | `sentiment_analysis_service.get_symbol_sentiment()` | **Implemented** (`SentimentChart.jsx`) |
| **Market Overview** | Sector Heatmap | `sentiment_analysis_service.get_all_sectors_sentiment()`| **Implemented** (via `FearGreedGauge.jsx` logic) |

## Dependencies
- `textblob` or `vaderSentiment`: (Future) Libraries for upgraded sentiment analysis.
- `cache_service`: Caches API responses to prevent rate-limit exhaustion and reduce latency.

## Usage Examples

### Fetching & Analyzing News for 'AAPL'
```python
from services.news.sentiment_analysis_service import get_sentiment_analysis_service

sentiment_svc = get_sentiment_analysis_service()

# Get aggregated sentiment for the last 24 hours
sentiment = await sentiment_svc.get_symbol_sentiment(symbol="AAPL", hours_back=24)

print(f"Sentiment: {sentiment.sentiment_label} ({sentiment.overall_sentiment:.2f})")
print(f"Based on {sentiment.article_count} articles.")
print(f"Bullish/Bearish Ratio: {sentiment.bullish_count}/{sentiment.bearish_count}")
```

### Assessing Market Impact
```python
impact = await sentiment_svc.assess_market_impact(symbol="TSLA")

if impact.impact_score > 0.5:
    print(f"High Impact Alert: {impact.expected_direction.upper()} move expected.")
    print(f"Magnitude: ~{impact.expected_magnitude}%")
```


---

## Source: service_notifications.md

# Backend Service: Notifications (Omnichannel Dispatch)

## Overview
The **Notifications Service** manages the outbound communication layer of the Sovereign OS. It abstracts away the complexity of integrating with various providers (Slack, Twilio, SendGrid, PagerDuty), allowing other services to simply "send a message" without worrying about the delivery mechanism. It also enforces user preferences, ensuring that alerts are delivered to the right device at the right time.

## Core Components

### 1. Preference Manager (`notification_preferences.py`)
The user control plane.
- **Channel Opt-In**: Manages the `enabled/disabled` state for each channel (SMS, Email, Slack).
- **Verification**: Handles the "Verify Phone Number" OTP flow to prevent spam.

### 2. FOMO Alert Engine (`fomo_alert.py`)
Urgency driver for deal flow.
- **Scarcity Logic**: Monitors "remaining capacity" in private deals. When allocation drops below a threshold, it triggers high-priority alerts to TIER_1 and TIER_2 clients to drive immediate action.

### 3. Provider Adapters (`slack_service.py`, `twilio_service.py`, etc.)
The delivery infrastructure.
- **Unified Interface**: Each adapter implements a standard `send()` method, allowing the calling service to be agnostic of the underlying API.
- **Mock Mode**: The `SlackClient` includes a simulation mode for development, allowing devs to see "fake" messages in the logs without spamming real channels.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Settings** | SMS Config | `notification_preferences.update_sms_preferences()` | **Implemented** (`SMSSettings.jsx`) |
| **Settings** | Discord/Slack Config | `slack_service.get_channels()` | **Implemented** (`DiscordSettings.jsx`) |
| **Deal Room** | Capacity Alert Badge | `fomo_alert` (triggered via socket) | **Partial** |

## Dependencies
- `twilio`: SMS and Voice API client.
- `sendgrid`: Transactional Email API client.
- `slack_sdk`: (Future) Official Slack client.

## Usage Examples

### Configuring User Preferences
```python
from services.notifications.notification_preferences import get_notification_preferences

prefs = get_notification_preferences()

# Enable SMS for "Margin Calls" only
prefs.update_sms_preferences(
    enabled=True,
    phone="+15550199",
    alert_types=["margin_call", "liquidation"]
)
```

### Triggering a Deal Scarcity Alert (FOMO)
```python
from services.notifications.fomo_alert import FOMOAlertService

fomo = FOMOAlertService()

# Push alert to TIER_1 SFO clients
fomo.push_scarcity_alert(
    deal_name="SpaceX Secondary Series N",
    remaining_capacity=500000.00, # $500k left
    recipient_tier="TIER_1_SFO"
)
```


---

## Source: service_operations.md

# Backend Service: Operations (Efficiency Engine)

## Overview
The **Operations Service** is the "Cyborg" component of the Sovereign OS, designed to optimize the mix of human capital and automated systems. It provides quantitative frameworks for "Buy vs. Build" decisions (e.g., "Should we hire a Controller or use an outsourced firm?") and tracks the "Return on Effort" for various investment strategies to ensure scalability.

## Core Components

### 1. Outsource Calculator (`outsource_calc.py`)
The Hiring ROI logic.
- **Cost Comparison**: Maintains a database of industry standard salaries for Family Office roles (Controller, Accountant, Analyst) adjusting for benefits and overhead.
- **Volume-Based Tiers**: Compares internal fixed costs against variable outsourced vendor costs based on transaction volume.
- **Decision Engine**: Outputs a clear `HIRE_INTERNAL` vs `OUTSOURCE_FUNCTION` recommendation.

### 2. Workload Tracker (`workload_tracker.py`)
The Scalability Monitor.
- **Seat Management**: Tracks active licenses for expensive terminals (Bloomberg at $2,400/mo, Refinitiv at $1,800/mo) to identify unused assets.
- **Effort Scoring**: Aggregates "Research Hours" + "Monitoring Hours" + "Trading Minutes" per strategy.
    - *Scalability Heuristic*: If a strategy requires >20 hours/month of human intervention, it is flagged as `is_scalable: False`.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Admin Console** | Resource Utilization | `workload_tracker.get_monthly_tech_burn()` | **Missing** |
| **Ops Dashboard** | Hiring vs Outsourcing ROI | `outsource_calc.evaluate_hiring_choice()` | **Missing** |

> [!NOTE]
> **Integration Status**: This service is currently a **Backend-Only** utility. Its logic is used for internal reporting and optimization but has not yet been exposed via a dedicated frontend dashboard.

## Dependencies
- `decimal`: For precise currency calculations in ROI modeling.
- `typing`: Standard type hinting.

## Usage Examples

### Evaluating a Hiring Decision
```python
from services.operations.outsource_calc import OperationsOutsourceCalculator

ops_calc = OperationsOutsourceCalculator()

# Evaluate hiring a Controller for a firm with 5,000 annual transactions
decision = ops_calc.evaluate_hiring_choice(
    function_name="CONTROLLER",
    transaction_vol=5000
)

print(f"Recommendation: {decision['recommendation']}")
print(f"Internal Cost: ${decision['estimated_internal_cost']:,.2f}")
print(f"Vendor Cost: ${decision['estimated_vendor_cost']:,.2f}")
```

### Checking Software Burn Rate
```python
from services.operations.workload_tracker import OperationalWorkloadService

tracker = OperationalWorkloadService()

# Assign seats
tracker.assign_seat(user_id="analyst_01", platform="BLOOMBERG")
tracker.assign_seat(user_id="pm_01", platform="REFINITIV")

# Calculate burn
monthly_burn = tracker.get_monthly_tech_burn()
print(f"Monthly Tech Fixed Costs: ${monthly_burn:,.2f}")
```


---

## Source: service_optimization.md

# Backend Service: Optimization (Quant Engine)

## Overview
The **Optimization Service** is the mathematical core of the investment process. It translates high-level strategic goals (e.g., "Maximize Sharpe Ratio") into precise asset allocation weights using advanced quantitative models like Mean-Variance Optimization (MVO), Black-Litterman, and Risk Parity. It also actively monitors portfolios for drift and generates tax-efficient rebalancing orders.

## Core Components

### 1. Portfolio Optimizer (`portfolio_optimizer_service.py`)
The Math Kernel.
- **Supported Models**:
    - **Mean-Variance (Markowitz)**: The classic approach to finding the Efficient Frontier.
    - **Risk Parity**: Allocates capital such that each asset contributes equally to overall portfolio risk (great for all-weather portfolios).
    - **Minimum Variance**: Seeks the absolute lowest volatility portfolio.
- **Constraint Handling**: Supports real-world constraints like `long_only` (no shorting), `position_limits` (e.g., max 5% per stock), and `sector_exposure`.

### 2. Rebalancing Engine (`rebalancing_service.py`)
The Drift Corrector.
- **Drift Monitoring**: Continuously compares Current Weights vs. Target Weights. If the deviation exceeds a threshold (default 5%), it flags the portfolio for rebalancing.
- **Trade Generation**: Auto-calculates the precise BUY/SELL orders needed to restore alignment.
- **Approval Workflow**: Enforces a safety check—if total trade value > $10,000, it requires explicit user approval before execution.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategist Workstation** | Rebalance Tool | `rebalancing_service.generate_rebalancing_recommendation()` | **Implemented** (`StrategistRebalance.jsx`) |
| **Brokerage** | Tax Lot Optimizer | `rebalancing_service._estimate_tax_impact()` | **Implemented** (`TaxLotOptimizer.jsx`) |
| **Institutional** | Allocation Wheel | `portfolio_optimizer_service.optimize()` | **Implemented** (`AssetAllocationWheel.jsx`) |

## Dependencies
- `numpy`: Matrix operations and linear algebra.
- `scipy.optimize`: The solver engine (SLSQP method) for minimization problems.
- `cvxpy`: (Future) For more complex convex optimization problems.

## Usage Examples

### Optimizing a Portfolio for Max Sharpe
```python
from services.optimization.portfolio_optimizer_service import get_optimizer_service

optimizer = get_optimizer_service()

result = await optimizer.optimize(
    portfolio_id="pf_growth_aggr",
    objective="maximize_sharpe",
    method="mean_variance",
    risk_model="historical"
)

for symbol, weight in result.optimal_weights.items():
    print(f"{symbol}: {weight*100:.1f}%")

print(f"Exp Return: {result.expected_return:.2%}")
print(f"Exp Volatility: {result.expected_risk:.2%}")
```

### Checking for Drift
```python
from services.optimization.rebalancing_service import get_rebalancing_service

rebalancer = get_rebalancing_service()

# Check if portfolio has drifted > 3%
needs_rebalance = await rebalancer.check_rebalancing_needed(
    portfolio_id="pf_retirement",
    threshold=0.03
)

if needs_rebalance:
    rec = await rebalancer.generate_rebalancing_recommendation("pf_retirement")
    print(f"Drift Detected: {rec.drift_percentage:.2f}%")
    print(f"Recommended Trades: {len(rec.recommended_trades)}")
```


---

## Source: service_options.md

# Backend Service: Options (Derivatives Engine)

## Overview
The **Options Service** provides the "Hedge Fund" capabilities of the Sovereign OS. It goes beyond simple price tracking to analyze second-order derivatives (Greeks) and market structure (Gamma Exposure). It enables the system to detect "Dealer Hedging Pressure" (GEX), price complex strategies (Straddles, Iron Condors), and visualize implied volatility surfaces.

## Core Components

### 1. GEX Calculator (`gex_calculator.py`)
The Market Structure Engine.
- **Gamma Exposure (GEX)**: Calculates the total dollar value of Gamma dealers must hedge for every 1% move in the underlying.
- **Gamma Flip Detection**: Identifies the precise price level where dealers switch from being "Long Gamma" (stabilizing flows, buy-the-dip) to "Short Gamma" (accelerating flows, sell-the-rip).
- **Regime Identification**: Classifies the market state as `LONG_GAMMA` (Low volatility expected) or `SHORT_GAMMA` (High volatility danger zone).

### 2. Options Analytics (`options_analytics_service.py`)
The Pricing Kernel.
- **Real-Time Greeks**: Calculates Delta, Gamma, Theta, Vega, and Rho for individual options and complex multi-leg strategies using the Black-Scholes model.
- **Probability of Profit (PoP)**: Estimates the statistical likelihood of a trade ending In-The-Money (ITM) based on current Implied Volatility (IV).
- **P&L Simulation**: Projects profit/loss across different price and time horizons (e.g., "What if SPY drops 2% tomorrow vs. next week?").

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Market Dashboard** | GEX Profile | `gex_calculator.calculate_gex()` | **Implemented** (`GEXProfile.jsx`) |
| **Trading Terminal** | Options Analysis | `options_analytics_service.analyze_strategy()` | **Implemented** (`OptionsChainWidget.jsx`) |
| **Flow Monitor** | Unusual Whales | `options_analytics_service` (Flow data aggregator) | **Implemented** (`OptionsFlowTable.jsx`) |

## Dependencies
- `scipy.stats.norm`: Used for Cumulative Distribution Functions (CDF) in Black-Scholes pricing.
- `numpy`: Vectorized calculations for efficient pricing of entire option chains.

## Usage Examples

### Calculating Gamma Exposure for SPY
```python
from services.options.gex_calculator import GEXCalculator

# Mock Option Chain Data
chain = [
    {'strike': 450, 'gamma': 0.05, 'open_interest': 15000, 'type': 'CALL'},
    {'strike': 450, 'gamma': 0.04, 'open_interest': 12000, 'type': 'PUT'},
    # ... more contracts
]

gex_result = GEXCalculator.calculate_gex(spot_price=452.50, options_chain=chain)

print(f"Total Dealer GEX: ${gex_result['total_gex']:,.0f}")
print(f"Gamma Flip Level: ${gex_result['gamma_flip_price']:.2f}")
print(f"Market Regime: {gex_result['market_regime']}")
```

### Analyzing an Iron Condor Strategy
```python
from services.options.options_analytics_service import get_options_analytics_service
from schemas.options import OptionsStrategy, OptionLeg

analytics = get_options_analytics_service()

# Define Strategy
condor = OptionsStrategy(legs=[
    OptionLeg(symbol="SPY", strike=440, option_type="put", action="sell", quantity=1),
    OptionLeg(symbol="SPY", strike=435, option_type="put", action="buy", quantity=1),
    OptionLeg(symbol="SPY", strike=460, option_type="call", action="sell", quantity=1),
    OptionLeg(symbol="SPY", strike=465, option_type="call", action="buy", quantity=1)
])

# Get Greeks & P&L
analysis = await analytics.analyze_strategy(
    strategy=condor,
    underlying_price=450.00,
    days_to_expiration=30,
    volatility=0.18
)

print(f"Total Theta: {analysis.greeks.total_theta:.4f}")
print(f"Max Profit probability: {analysis.probability_profit:.1%}")
```


---

## Source: service_payment.md

# Backend Service: Payment (Trust Administration)

## Overview
The **Payment Service** (singular) is a specialized module for **Trust Administration**. Unlike general bill pay, this service handles the complex, compliance-heavy outflows required for Irrevocable Life Insurance Trusts (ILITs) and Special Needs Trusts (SNTs). It ensures that every dollar leaving these entities follows strict legal protocols to preserve tax benefits and government aid eligibility.

## Core Components

### 1. ILIT Flow Manager (`ilit_flow.py`)
The Estate Tax Shield.
- **Workflow Enforcement**: detailed logic to ensure the "Crummey" process is followed:
    1.  Grantor Gifts cash to Trust.
    2.  Trustees send "Crummey Notices" to beneficiaries (giving them a window to withdraw).
    3.  Trust pays the Insurance Carrier.
- **Audit Trail**: Logs every step to prove to the IRS that the gift was "present interest," qualifying for the annual exclusion.

### 2. Vendor Direct (`vendor_direct.py`)
The SNT Guardian.
- **SSI/Medicaid Protection**: Ensures payments are made **directly to vendors** (e.g., paying a landlord or phone company) rather than giving cash to the beneficiary. This prevents the beneficiary from losing government benefits due to "income" rules.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Bill Pay** | Trust Payment Portal | `vendor_direct.process_vendor_payment()` | **Implemented** (`BillPaymentDashboard.jsx`) |
| **Estate Admin** | Crummey Tracker | `ilit_flow.process_premium_cycle()` | **Missing** (Backend logic exists, UI pending) |

## Dependencies
- `logging`: Critical for audit trails in legal defense.
- `typing`: Type enforcement for financial safety.

## Usage Examples

### Processing an ILIT Premium
```python
from services.payment.ilit_flow import ILITFlowService

ilit_svc = ILITFlowService()

# 1. Grantor gifts $50k
# 2. Notices sent...
# 3. Time to pay the carrier
result = ilit_svc.process_premium_cycle(
    ilit_id="ilit_dynasty_01",
    premium_amount=50000.00
)

print(f"Workflow Status: {result['workflow_status']}")
for step in result['audit_trail']:
    print(f"- {step['step']}: {step['status']}")
```

### Paying a Vendor from an SNT
```python
from services.payment.vendor_direct import VendorDirectPayment

snt_pay = VendorDirectPayment()

# Pay Rent directly to Landlord (Approved Expense)
receipt = snt_pay.process_vendor_payment(
    trust_id="snt_beneficiary_01",
    vendor_id="landlord_llc",
    amount=2500.00,
    category="SHELTER"
)

print(f"Payment ID: {receipt['payment_id']}")
print(f"Status: {receipt['status']}")
```


---

## Source: service_payments.md

# Backend Service: Payments (Fintech Gateway)

## Overview
The **Payments Service** (plural) acts as the integration hub for external financial APIs. Unlike the "Payment" service (which handles internal trust flows), this service wraps third-party SDKs into a unified interface for the rest of the Sovereign OS. It enables the system to See (Plaid), Earn (Stripe), and Trade (Coinbase/Robinhood).

## Core Components

### 1. Plaid Connector (`plaid_service.py`)
The Bank Bridge.
- **Link Token Exchange**: Manages the multi-step Oauth flow to securely connect users' bank accounts without ever touching their credentials.
- **Micro-Deposit Verification**: (Mocked) logic for validating ACH routing numbers.

### 2. Stripe Manager (`stripe_service.py`)
The Revenue Engine.
- **Subscription Management**: Handles SaaS billing for the platform itself (if monetized) or for collecting tenant rents.
- **Checkout Sessions**: Generates secure payment links for one-off transactions.

### 3. Crypto/Brokerage Bridges (`coinbase_service.py`, `robinhood_service.py`)
The Execution Rails.
- **Unified Trading Interface**: Abstracts away the differences between crypto (Coinbase) and equity (Robinhood) orders, allowing the `OrderExecutionService` to simply call `buy(symbol, qty)`.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Banking Dashboard** | Link Account Btn | `plaid_service.create_link_token()` | **Implemented** (`PlaidLinkModal.jsx`) |
| **Crypto Wallet** | Trade Panel | `coinbase_service.place_order()` | **Implemented** (`CoinbaseTrade.jsx`) |
| **Brokerage** | Account Connect | `robinhood_service.link_account()` | **Implemented** (`RobinhoodConnect.jsx`) |

## Dependencies
- `plaid-python`: Official Plaid SDK.
- `stripe`: Official Stripe SDK.
- `coinbase-advanced-py`: (Future) Coinbase Advanced Trade API client.

## Usage Examples

### Linking a New Bank Account
```python
from services.payments.plaid_service import get_plaid_client

plaid = get_plaid_client()

# 1. Frontend requests a Link Token
token_response = await plaid.create_link_token(user_id="user_123")
print(f"Link Token: {token_response['link_token']}")

# 2. Frontend launches Plaid Link... sends back public_token
# 3. Backend exchanges for Access Token
access_data = await plaid.exchange_public_token("public-sandbox-123")
print(f"Access Token: {access_data['access_token']}")
```

### Creating a Stripe Checkout Session
```python
from services.payments.stripe_service import get_stripe_client

stripe = get_stripe_client()

session = await stripe.create_checkout_session(
    user_id="tenant_01",
    plan_id="price_monthly_rent"
)

print(f"Redirect User to: {session['url']}")
```


---

## Source: service_pe.md

# Backend Service: Private Equity (Deal Engine)

## Overview
The **Private Equity (PE) Service** provides the financial modeling infrastructure for illiquid investments. It mimics the analytical capabilities of a PE associate, enabling the autonomous system to evaluate "buyout" opportunities, project returns (IRR/MOIC), and manage complex distribution waterfalls between General Partners (GPs) and Limited Partners (LPs).

## Core Components

### 1. LBO Engine (`lbo_engine.py`)
The Buyout Calculator.
- **Return Projection**: Calculates Internal Rate of Return (IRR) and Multiple on Invested Capital (MOIC) based on entry/exit multiples, leverage ratios, and operational improvements.
- **Deleveraging Model**: Simulates the pay-down of debt using free cash flow over the hold period.

### 2. Waterfall Engine (`waterfall_engine.py`)
The Distribution Manager.
- **Tiered Splits**: Implements standard PE waterfall logic:
    1.  **Return of Capital**: LPs get 100% of cash flow until they recover their initial investment.
    2.  **Preferred Return**: LPs get a "hurdle rate" (e.g., 8%).
    3.  **GP Catch-up**: The Deal Sponsor gets their share.
    4.  **Carried Interest**: Splits remaining profits (e.g., 80/20).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Brokerage** | P&L Waterfall | `waterfall_engine.calculate_distributions()` | **Implemented** (`PLWaterfall.jsx`) |
| **Deal Room** | LBO Model | `lbo_engine.project_deal_returns()` | **Missing** (Logic exists, UI pending) |

## Dependencies
- `decimal`: **Critical** for financial precision. Floating point errors in waterfall calculations are legally unacceptable.

## Usage Examples

### Projecting an LBO Return
```python
from services.pe.lbo_engine import LBOEngine
from decimal import Decimal

lbo = LBOEngine()

# Project returns for a $10M EBITDA company bought at 10x
result = lbo.project_deal_returns(
    entry_ebitda=Decimal('10000000'),
    entry_multiple=Decimal('10.0'),
    equity_contribution_pct=Decimal('0.40'), # 40% Equity / 60% Debt
    exit_multiple=Decimal('12.0'),           # Ops Improvement
    years=5,
    revenue_growth_pct=Decimal('0.05')       # 5% YoY Growth
)

print(f"Projected MOIC: {result['moic']}x")
print(f"Projected IRR: {result['irr_pct']}%")
```

### Calculating GP/LP Distributions
```python
from services.pe.waterfall_engine import WaterfallEngine

distributor = WaterfallEngine()

# Distribute $500k of cash flow from a portfolio company
payout = distributor.calculate_distributions(
    distributable_cash=Decimal('500000'),
    invested_capital=Decimal('2000000')
)

print(f"LP Share: ${payout['total_lp_dist']:,.2f}")
print(f"GP Promote: ${payout['total_gp_dist']:,.2f}")
```


---

## Source: service_performance.md

# Backend Service: Performance (The Scoreboard)

## Overview
The **Performance Service** is the "Meritocracy Engine" of the Sovereign OS. It goes beyond simple P&L to answer the question: *"Was this skill or luck?"* It calculates risk-adjusted returns (True Sharpe), measures distinctiveness from the index (Active Share), and attributes profits to specific investment professionals (Staff Attribution) to determine bonuses.

## Core Components

### 1. Staff Attribution Engine (`staff_attribution.py`)
The Bonus Calculator.
- **Alpha Attribution**: Tracks exactly how much "Alpha" (excess return over benchmark) was generated by each specific employee (Agent or Human).
- **Role Benchmarking**: Compares performance against industry standards for the role (e.g., "Did this Analyst beat the average Analyst base + bonus?").
- **Audit Trail**: Provides the data backing for discretionary bonus pools.

### 2. True Sharpe Calculator (`true_sharpe.py`)
The Private Asset Truth Teller.
- **Volatility Unsmoothing**: Private assets (PE, VC) often look artificially stable because they are not marked-to-market daily. This component mathematically "unsmooths" the return series to reveal the *actual* volatility, preventing false confidence.
- **Risk-Adjusted Return**: Calculates Sharpe Ratio using this "True Volatility".

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Auditor Workstation** | Attribution Table | `staff_attribution.calculate_professional_alpha()` | **Implemented** (`AuditorAttribution.jsx`) |
| **Portfolio Analytics** | Sector Brinson | `attribution_service._sector_attribution()` | **Implemented** (`SectorAttribution.jsx`) |
| **Risk Dashboard** | True Sharpe | `true_sharpe.calculate_true_sharpe()` | **Implemented** (`AdvancedRiskDashboard.jsx`) |

## Dependencies
- `decimal`: Required for precise financial performance reporting.

## Usage Examples

### Calculating Alpha for a Portfolio Manager
```python
from services.performance.staff_attribution import StaffAttributionEngine
from decimal import Decimal

attribution = StaffAttributionEngine()

# PM generated 12% return vs 8% benchmark on $50M AUM
result = attribution.calculate_professional_alpha(
    staff_id="pm_tech_fund",
    actual_return=Decimal('0.12'),
    benchmark_return=Decimal('0.08'),
    aum_managed=Decimal('50000000')
)

print(f"Alpha Generated: {result['alpha_bps']} bps")
print(f"Dollar Value Created: ${result['alpha_dollar_value']:,.2f}")
```

### Calculating True Sharpe for a VC Fund
```python
from services.performance.true_sharpe import TrueSharpeCalculator

scorer = TrueSharpeCalculator()

# Fund returned 25%, but with "smoothed" volatility of only 10%
# We estimate True Volatility is actually 25%
metrics = scorer.calculate_true_sharpe(
    annual_return=0.25,
    risk_free_rate=0.04,
    true_volatility=0.25
)

print(f"True Sharpe Ratio: {metrics['true_sharpe']}")
```


---

## Source: service_philanthropy.md

# Backend Service: Philanthropy (The "Enough" Engine)

## Overview
The **Philanthropy Service** enforces the Sovereign Individual's "Enough" philosophy. It automatically sweeps capital above a defined Net Worth threshold (e.g., $3M) into charitable causes using tax-efficient structures. It integrates with crypto-native donation platforms (The Giving Block) and charity rating agencies (Charity Navigator) to ensure high-impact giving.

## Core Components

### 1. Donation Service (`donation_service.py`)
The Sweeper.
- **Excess Calculation**: `max(0, Current_Net_Worth - Threshold)`.
- **Routing Logic**: Splits excess capital according to user-defined allocations (e.g., "50% Climate, 30% Education, 20% Health").
- **Tax Optimization**: Tracks potential tax savings from donations to offset capital gains in other services.

### 2. Charity Client (`charity_client.py`)
The Connector.
- **The Giving Block**: Interface for executing crypto donations (ETH/BTC) directly to non-profits, avoiding capital gains tax on the appreciation.
- **Charity Navigator**: Fetches "Financial Health" and "Transparency" scores to gatekeep donations (no scams allowed).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Impact Dashboard** | Donation Router | `donation_service.route_excess_alpha()` | **Implemented** (`DonationRouter.jsx`) |
| **Philanthropy** | Charity Search | `charity_client.get_charity_rating()` | **Partially Implemented** (Mock data in `ImpactDashboard.jsx`) |

## Dependencies
- `httpx`: Async HTTP client for external API calls.
- `dataclasses`: Structuring donation records and allocation objects.

## Usage Examples

### Sweeping Excess Capital
```python
from services.philanthropy.donation_service import get_donation_service

service = get_donation_service()

# Assume net worth is $3.5M and threshold is $3.0M
excess = await service.calculate_excess_alpha(
    current_net_worth=3500000.0,
    threshold=3000000.0
)

if excess > 0:
    print(f"Excess Capital Detected: ${excess:,.2f}")
    
    # Route to causes
    record = await service.route_excess_alpha(
        amount=excess,
        allocations=[
            {"category": "Climate", "percentage": 50},
            {"category": "Education", "percentage": 50}
        ]
    )
    
    print(f"Donation Executed: {record.id}")
    print(f"Est. Tax Savings: ${record.tax_savings_est:,.2f}")
```

### Checking Charity Health
```python
from services.philanthropy.charity_client import CharityNavigatorClient

client = CharityNavigatorClient()

rating = await client.get_charity_rating("Doctors Without Borders")

print(f"Score: {rating['score']}/100")
print(f"Transparency: {rating['transparency']}")
```


---

## Source: service_physical.md

# Backend Service: Physical (Security Grid)

## Overview
The **Physical Security Service** connects the digital brain of the Sovereign OS to the physical world. It manages the hardware layer of defense, including biometric access control systems, CCTV surveillance with computer vision, and autonomous drone patrols. It ensures that the servers running the AI and the assets stored in the vault are physically protected.

## Core Components

### 1. Access Control (`access_control.py`)
The Gatekeeper.
- **Biometric Logging**: Tracks all entries and exits from secure zones (Server Room, Vault) using methods like Retina Scan, Fingerprint, and NFC.
- **Audit Trail**: Immutable logs of who went where and when, critical for post-incident forensics.

### 2. CCTV Engine (`cctv_engine.py`)
The Eyes.
- **AI Analytics**: Runs object detection (YOLOv8) on video streams to identify unauthorized persons or vehicles in restricted areas.
- **Retention Policy**: Manages storage rotation for video evidence (default 30 days).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mission Control** | Defcon Status | `defcon_svc.get_current_level()` | **Implemented** (`MissionControl.jsx`) |
| **Security Dashboard** | Camera Feed | `cctv_engine.analyze_frame()` | **Missing** (Backend logic exists, UI pending) |

## Dependencies
- `random`: Used for simulating sensor noise and detection events in the current mock implementation.

## Usage Examples

### Logging a Retina Scan Entry
```python
from services.physical.access_control import AccessControlService

security = AccessControlService()

# User scans retina at Server Room door
log = security.log_access_attempt(
    user_id="admin_01",
    zone="Server Room",
    method="RETINA_SCAN",
    success=True
)

print(f"Access Status: {log['status']}")
```

### Analyzing a CCTV Frame
```python
from services.physical.cctv_engine import CCTVEngine

cctv = CCTVEngine()

# Process frame from the Gate Camera
result = cctv.analyze_frame("Cam-01-Gate")

if result['detections']:
    print(f"ALERT: {len(result['detections'])} objects detected!")
    for det in result['detections']:
        print(f"- Detected {det['label']} (Confidence: {det['confidence']:.2f})")
```


---

## Source: service_physicist.md

# Backend Service: Physicist (Quant Lab)

## Overview
The **Physicist Service** is the specialized research arm of the system, dedicated to advanced derivatives pricing and market thermodynamics. While the `options` service handles general flow and strategy P&L, the **Physicist** focuses on the raw mathematics of volatility, offering a high-performance Black-Scholes-Merton engine optimized for real-time Greeks and Implied Volatility (IV) surface calibration.

## Core Components

### 1. Options Pricing Engine (`options_pricing_service.py`)
The Speed Demon.
- **Black-Scholes-Merton**: Implementation of the standard pricing model for European options.
- **Real-Time Greeks**: Calculates secondary risk metrics (Rho, Vega per 1% vol change) efficiently.
- **Newton-Raphson Solver**: Solves for Implied Volatility (IV) given a market price, essential for constructing surface maps.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Physicist Workstation** | Expected Move | `options_pricing_service.black_scholes()` | **Implemented** (`PhysicistExpectedmove.jsx`) |
| **Physicist Workstation** | Volatility Surface | `options_pricing_service.calculate_implied_volatility()` | **Implemented** (`PhysicistMorphing.jsx`) |

## Dependencies
- `scipy.stats.norm`: For Gaussian cumulative distribution functions.
- `math`: Standard library used for maximum speed (avoiding numpy overhead for single-contract pricing).

## Usage Examples

### Pricing a Call Option
```python
from services.physicist.options_pricing_service import get_options_pricing_service

pricer = get_options_pricing_service()

# Price a Call: Spot=100, Strike=100, Time=1 year, RiskFree=5%, Vol=20%
result = pricer.black_scholes(
    S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.20, option_type="call"
)

print(f"Theoretical Price: ${result['price']:.2f}")
print(f"Delta: {result['delta']:.4f}")
print(f"Gamma: {result['gamma']:.4f}")
```

### Solving for Implied Volatility
```python
# If the market price is $10.50, what is the Implied Vol?
iv = pricer.calculate_implied_volatility(
    market_price=10.50,
    S=100.0, K=100.0, T=1.0, r=0.05, option_type="call"
)

print(f"Implied Volatility: {iv:.2%}")
```


---

## Source: service_planning.md

# Backend Service: Planning (The CFO)

## Overview
The **Planning Service** creates the roadmap for financial independence. It uses goal-based investing principles to reverse-engineer the required savings rates and asset allocations needed to hit specific life milestones (Retirement, Home Purchase, Philanthropy). It also includes a "Tough Love" module (`spending_analyzer.py`) to detect lifestyle creep.

## Core Components

### 1. Financial Planning Engine (`financial_planning_service.py`)
The Architect.
- **Goal Projection**: Calculates the future value of current savings + projected contributions to see if a goal is "On Track."
- **Asset Allocation**: Recommends a specific mix (Equity/Fixed Income/Cash) based on the *time horizon* of each goal (e.g., 80/20 for retirement in 20 years, but 20/80 for a house down payment in 2 years).
- **Contribution Optimization**: Solves for the *minimum* monthly savings needed to hit all goals, or prioritizes goals if capacity is limited.

### 2. Spending Analyzer (`spending_analyzer.py`)
The Auditor.
- **Waste Detection**: Flags spending categories that exceed peer-group benchmarks (e.g., "Dining > $1,000/mo") or indicate inefficiency (e.g., "Subscriptions > $200/mo").
- **Savings Rate Calculation**: Tracks the most important metric in personal finance: `(Savings / (Expenses + Savings))`.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Financial Plan** | Goal Timeline | `financial_planning_service.project_goal_timeline()` | **Implemented** (`FinancialPlanningDashboard.jsx`) |
| **Zen Mode** | Retirement Gauge | `financial_planning_service` (Progress %) | **Implemented** (`RetirementGauge.jsx`) |
| **Cash Flow** | Spending Audit | `spending_analyzer.analyze_patterns()` | **Partially Implemented** (Mock logic in dashboard) |

## Dependencies
- `numpy`: Used for financial math (FV, PV, PMT functions).
- `schemas.financial_planning`: Pydantic models for strict type validation of financial goals.

## Usage Examples

### Creating a Retirement Plan
```python
from services.planning.financial_planning_service import get_financial_planning_service

planner = get_financial_planning_service()

# Define a goal: Retire with $5M in 20 years
plan = await planner.create_financial_plan(
    user_id="user_01",
    goals=[{
        "name": "Retirement",
        "target_amount": 5000000.0,
        "current_amount": 500000.0,
        "target_date": datetime(2046, 1, 1)
    }],
    monthly_contribution_capacity=10000.0
)

# Check if on track
projection = await planner.project_goal_timeline(plan.goals[0])
print(f"On Track: {projection.on_track}")
print(f"Projected Completion: {projection.projected_date}")
```

### Analyzing Monthly Spend
```python
from services.planning.spending_analyzer import SpendingAnalyzer
from schemas.spending import SpendingCategory

auditor = SpendingAnalyzer()

report = auditor.analyze_patterns(
    SpendingCategory(
        user_id="user_01",
        subscriptions=250.0, # Flagged as high
        food_dining=800.0,
        total_spending=8000.0,
        savings_contributions=2000.0
    )
)

print(f"Savings Rate: {report['savings_rate']:.1%}")
for opp in report['opportunities']:
    print(f"Alert: {opp['message']}")
```


---

## Source: service_portfolio.md

# Backend Service: Portfolio (The Ledger)

## Overview
The **Portfolio Service** is the central source of truth for the Sovereign Individual's Net Worth. It solves the "fragmentation problem" by aggregating real-time positions from multiple brokerage APIs (Alpaca, Robinhood, IBKR) and combining them with manually tracked illiquid assets (Real Estate, Art, PE). It provides the unified data layer that powers all higher-level analytics (Risk, Performance, Planning).

## Core Components

### 1. Portfolio Aggregator (`portfolio_aggregator.py`)
The Unifier.
- **Multi-Broker Connectivity**: Polling engine that fetches positions from connected exchange APIs.
- **Unified Schema**: Normalizes different API responses (e.g., Alpaca's `qty` vs IBKR's `position`) into a standard `Position` object with standardized cost basis and P&L calculations.
- **Caching**: Reduces API rate limits by caching the aggregated view for a short duration (e.g., 60s).

### 2. Assets Service (`assets_service.py`)
The Illiquid Manager.
- **Manual CRUD**: Simple database (JSON-backed) for tracking assets that don't have APIs (Homes, Cars, Angel Investments).
- **Valuation Updates**: Allows users to manually update the estimated value of these assets to keep Net Worth accurate.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Institutional Dashboard** | Allocation Wheel | `portfolio_aggregator.calculate_unified_gains()` | **Implemented** (`AssetAllocationWheel.jsx`) |
| **All Pages** | Total Net Worth | `portfolio_aggregator.get_portfolio()` | **Implemented** (Global Store) |
| **Illiquid Assets** | Asset Editor | `assets_service.add_asset()` | **Partially Implemented** (`Assetlist` pending) |

## Dependencies
- `collections.defaultdict`: Used for efficient aggregation of positions across multiple accounts (e.g., summing AAPL shares from Robinhood and Alpaca).
- `services.brokerage`: heavily relies on the Brokerage Service clients.

## Usage Examples

### Fetching the Unified Portfolio
```python
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator

aggregator = get_portfolio_aggregator()

# Get combined view of Crypto, Equities, and Cash
portfolio = await aggregator.aggregate_positions(
    user_id="user_01",
    include_alpaca=True,
    include_robinhood=True,
    include_ibkr=False
)

print(f"Total Net Worth: ${portfolio['total_current_value']:,.2f}")
print(f"Unrealized Gain: ${portfolio['total_unrealized_gain']:,.2f}")

for pos in portfolio['positions']:
    print(f"- {pos['symbol']}: {pos['quantity']} shares via {pos['sources']}")
```

### Adding a Physical Asset
```python
from services.portfolio.assets_service import assets_service

# Add a rental property
assets_service.add_asset({
    "name": "Downtown Condo",
    "category": "Real Estate",
    "value": 450000.00,
    "location": "Austin, TX",
    "purchaseDate": "2023-06-15"
})

print(f"Updated Illiquid Value: ${assets_service.get_total_valuation():,.2f}")
```


---

## Source: service_pricing.md

# Backend Service: Pricing (The Ticker)

## Overview
The **Pricing Service** manages the granular details of market data. It has two main responsibilities: ensuring mathematical precision (rounding, pip calculations) to prevent floating-point errors in financial transactions, and high-frequency storage of incoming price ticks into a specialized Time-Series Database (TimescaleDB).

## Core Components

### 1. Precision Engine (`pricing/precision_engine.py`)
The Normalizer.
- **Decimal Enforcement**: Ensures all prices and quantities are stored as `Decimal` objects, not floats.
- **Pip/Tick Calculation**: Converts raw price differences into standardized "Pips" for FX or "Ticks" for Futures based on symbol-specific configs.
- **Display Formatting**: Guarantees that JPY pairs show 3 decimal places while EURUSD shows 5, matching standard trading terminals.

### 2. Price Telemetry Service (`price_telemetry_service.py`)
The Tape.
- **High-Frequency Ingestion**: Writes thousands of price updates per second (Ticks) into a hypertable.
- **TimescaleDB Integration**: Uses efficient SQL for time-series queries (e.g., "Get the last known price").

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **System Health** | Telemetry Stream | `price_telemetry_service.get_latest_price()` | **Implemented** (`Telemetry.jsx`) |
| **Trade Ticket** | Price Formatter | `precision_engine.format_for_display()` | **Implicit** (Used in various inputs) |

## Dependencies
- `decimal`: **Mandatory** for all internal math.
- `sqlalchemy`: Connectivity to the TimescaleDB instance.

## Usage Examples

### Normalizing a Price for Display
```python
from services.pricing.precision_engine import PrecisionEngine

# Raw float input from API
raw_price = 1.09214567 

# Normalize for EUR/USD (5 decimals)
norm_price = PrecisionEngine.normalize_price("EURUSD", raw_price)
display_str = PrecisionEngine.format_for_display("EURUSD", raw_price)

print(f"Stored: {norm_price} (Type: {type(norm_price)})")
print(f"Displayed: {display_str}")
```

### Storing a Market Tick
```python
from services.price_telemetry_service import PriceTelemetryService

telemetry = PriceTelemetryService()

# Store a new tick from WebSocket
telemetry.store_tick(
    symbol="BTC-USD",
    price=42069.50,
    volume=0.5,
    source="COINBASE"
)

# Retrieve latest
latest = telemetry.get_latest_price("BTC-USD")
print(f"Latest BTC Price: ${latest:,.2f}")
```


---

## Source: service_private_banking.md

# Backend Service: Private Banking (The Velvet Rope)

## Overview
The **Private Banking Service** strictly manages the exclusivity of the platform. It acts as the "Bouncer," automatically upgrading users to higher tiers of service based on their Net Worth and assigning them human Relationship Managers (RMs) to handle complex manual needs. It distinguishes the platform from a retail brokerage by offering "White Glove" support logic.

## Core Components

### 1. Client Qualifier (`qualifier.py`)
The Gatekeeper.
- **Tier Logic**:
    - **PRIVATE**: > $10M Net Worth.
    - **ULTRA**: > $50M Net Worth.
    - **FAMILY_OFFICE**: > $100M Net Worth.
- **Automatic Upgrades**: Monitors net worth changes to trigger upgrade workflows (e.g., notifying the Concierge team).

### 2. RM Load Balancer (`rm_load_balancer.py`)
The Assigner.
- **Human Resource Management**: Assigns a human Relationship Manager to a new client based on capacity.
- **Capacity Limits**: Enforces hard caps (e.g., 50 clients per RM for Ultra High Net Worth) to ensure service quality remains high.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Settings** | Account Tier | `qualifier.qualify_client()` | **Implemented** (Implicit in `departmentRegistry.js`) |
| **Concierge** | Chat to RM | `rm_load_balancer.assign_next_available_rm()` | **Missing** (UI not found) |

## Dependencies
- `uuid`: For unique client and RM identification.

## Usage Examples

### Qualifying a Client
```python
from services.private_banking.qualifier import PrivateBankingQualifier

qualifier = PrivateBankingQualifier()

# User just hit $55M Net Worth
status = qualifier.qualify_client(
    user_id="user_whale_01",
    net_worth=55000000.00
)

print(f"Qualified Tier: {status['tier']}") # Should be ULTRA
print(f"Is Qualified: {status['qualified']}")
```

### Assigning a Relationship Manager
```python
from services.private_banking.rm_load_balancer import RMLoadBalancer

balancer = RMLoadBalancer()

managers = [
    {"id": "rm_alice", "current_count": 48},
    {"id": "rm_bob", "current_count": 12} # Bob is open
]

assigned_rm = balancer.assign_next_available_rm(
    client_tier="ULTRA",
    managers=managers
)

print(f"Assigned RM: {assigned_rm}")
```


---

## Source: service_private_markets.md

# Backend Service: Private Markets (The Illiquidity Engine)

## Overview
The **Private Markets Service** manages the valuation and risk assessment of assets that cannot be sold instantly (Private Equity, Venture Capital, Real Estate). Its primary job is to ensure the **Illiquidity Premium** is captured—meaning the user is adequately compensated (typically +300-500 bps) for locking up their capital for years.

## Core Components

### 1. Premium Optimizer (`premium_optimizer.py`)
The Reality Check.
- **Illiquidity Premium Calculator**: Compares the expected Internal Rate of Return (IRR) of a private deal against a public market equivalent (Public Market Equivalent - PME). If the spread is < 300bps, the deal is rejected.
- **Return Unsmoothing**: Private assets often report artificially stable returns (e.g., "Up 2% every quarter") because they are appraised infrequently. This component uses the **Geltner Formula** to reverse-engineer the *true* volatility, ensuring the Risk Parity models don't overweight these assets due to false low-volatility signals.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Asset Entry** | Valuation Form | `premium_optimizer.calculate_illiquidity_premium()` | **Implemented** (`PrivateEntry.jsx`) |
| **Risk Dashboard** | True Volatility | `premium_optimizer.unsmooth_returns()` | **Implicit** (Data flows to Risk Engine) |

## Dependencies
- `decimal`: Required for precise IRR spread calculations.

## Usage Examples

### Evaluating a PE Fund
```python
from services.private_markets.premium_optimizer import PremiumOptimizer
from decimal import Decimal

optimizer = PremiumOptimizer()

# PE Fund offers 15% IRR, while S&P 500 expects 10%
evaluation = optimizer.calculate_illiquidity_premium(
    private_irr=Decimal('0.15'),
    public_equiv_irr=Decimal('0.10')
)

print(f"Premium: {evaluation['premium_bps']} bps")
print(f"Is Sufficient? {evaluation['is_sufficient']}") # True (500 > 300)
```

### Unsmoothing Real Estate Returns
```python
# Quarterly appraisals show very low volatility
smoothed_returns = [0.02, 0.021, 0.019, 0.022]

# Reveal the true volatility (assuming 0.5 autocorrelation)
true_returns = optimizer.unsmooth_returns(smoothed_returns, rho=0.5)

print(f"Smoothed: {smoothed_returns}")
print(f"True Vol: {true_returns}") 
# Result will be much more volatile
```


---

## Source: service_public_api.md

# Backend Service: Public API ( The Open Door)

## Overview
The **Public API Service** enables the Sovereign OS to be extensible. It allows external developers (or secondary autonomous agents) to interact with the platform programmatically. It handles the "Business of APIs"—issuing keys, enforcing rate limits, and tracking billable usage—so the core services can focus on logic, not infrastructure.

## Core Components

### 1. Public API Service (`public_api_service.py`)
The Gateway.
- **Key Management**: Issues cryptographically secure API keys (`sk_...`) tied to specific users and usage tiers.
- **Rate Limiting**: Enforces quotas based on tiers:
    - **Free**: 100 req/day
    - **Pro**: 1,000 req/day
    - **Enterprise**: 10,000+ req/day
- **Usage Tracking**: Logs every request (endpoint, latency, status) for billing and analytics.

### 2. Developer Portal Service (`developer_portal_service.py`)
The Librarian.
- **Documentation**: Generates OpenAPI specs for the exposed endpoints.
- **SDK Generation**: (Mocked) Provides ready-to-use client libraries for Python and JavaScript to lower the barrier to entry.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Developer Settings** | Key Vault | `public_api_service.create_api_key()` | **Implemented** (`KeyVault.jsx`) |
| **API Dashboard** | Usage Graph | `public_api_service.get_api_usage()` | **Implemented** (`ApiUsage.jsx`) |
| **Marketplace** | Docs Viewer | `developer_portal_service.get_api_documentation()` | **Implemented** (`APIMarketplace.jsx`) |

## Dependencies
- `secrets`: Cryptographically strong random number generation for API keys.
- `schemas.public_api`: Pydantic models for request/response validation.

## Usage Examples

### issuing a New API Key
```python
from services.public_api.public_api_service import get_public_api_service

gateway = get_public_api_service()

# Grant "Pro" access to a user
new_key = await gateway.create_api_key(
    user_id="dev_user_99",
    tier="pro"
)

print(f"Secret Key: {new_key.api_key}")
print(f"Rate Limit: {new_key.rate_limit} req/day")
```

### Tracking a Request
```python
# Middleware calls this largely transparently
await gateway.track_usage(
    api_key_id="key_123",
    endpoint="/api/v1/portfolio",
    response_time_ms=45.2,
    status_code=200
)
```


---

## Source: service_quantitative.md

# Backend Service: Quantitative (The Quant Lab)

## Overview
The **Quantitative Service** is the mathematical engine of the platform. It houses 21 specialized calculators for generating alpha, assessing risk-adjusted returns, and detecting market anomalies. It enables the system to grade its own performance (Sharpe, Alpha) and identify structural market risks (Passive Bubble, Reflexivity).

## Core Components (Selected)

### 1. Alpha Calculator (`alpha_calculator.py`)
- **Simple Alpha**: `Portfolio Return - Benchmark Return`.
- **Jensen's Alpha**: Risk-adjusted outperformance accounting for Beta, using the CAPM formula.

### 2. Sharpe Ratio Calculator (`sharpe_calculator.py`)
- **Formula**: `(Rp - Rf) / σp`
- Annualizes daily returns (252 trading days) and volatility.

### 3. Reflexivity Engine (`reflexivity_engine.py`)
- **Passive Saturation Check**: Flags tickers where "Big Three" (BlackRock, Vanguard, State Street) hold > 40% of shares, indicating extreme fragility to index rebalancing flows.
- **Inelastic Flow Impact**: Models how passive inflows move prices non-linearly.

### Other Key Modules
- `sortino_calculator.py`: Sharpe variant that only penalizes *downside* volatility.
- `correlation_calculator.py`: Tracks portfolio diversification.
- `rolling_metrics.py`: Time-windowed performance snapshots.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategist** | Alpha/Beta Dashboard | `alpha_calculator.calculate_jensens_alpha()` | **Implemented** (`StrategistAlphabeta.jsx`) |
| **Portfolio Analytics** | Performance Radar | `sharpe_calculator.calculate()` | **Implemented** (`AdvancedPortfolioAnalytics.jsx`) |
| **Risk Monitor** | Reflexivity Alert | `reflexivity_engine.check_passive_saturation()` | **Implicit** (Feeds into Risk Dashboard) |

## Dependencies
- `numpy`: Foundation for all statistical calculations (mean, std, sqrt).
- `decimal`: Used in `reflexivity_engine.py` for precise percentage calculations.

## Usage Examples

### Calculating Jensen's Alpha
```python
from services.quantitative.alpha_calculator import AlphaCalculator

calc = AlphaCalculator()

# My portfolio returned 15%, S&P 500 returned 10%
# Risk-free rate is 2%, my Beta is 1.1
alpha = calc.calculate_jensens_alpha(
    portfolio_ret=0.15,
    benchmark_ret=0.10,
    rf_rate=0.02,
    beta=1.1
)
print(f"Jensen's Alpha: {alpha:.2%}") # Outperformance vs. expected
```

### Calculating Sharpe Ratio
```python
from services.quantitative.sharpe_calculator import SharpeRatioCalculator

calc = SharpeRatioCalculator()

daily_returns = [0.001, -0.002, 0.003, 0.001, -0.001] # Sample
sharpe = calc.calculate(daily_returns, risk_free_rate=0.02)

print(f"Sharpe Ratio: {sharpe}")
```

### Checking Passive Bubble Risk
```python
from services.quantitative.reflexivity_engine import ReflexivityEngine

engine = ReflexivityEngine()

# AAPL: Big Three own 6B shares, 15B total outstanding
report = engine.check_passive_saturation("AAPL", 6_000_000_000, 15_000_000_000)

print(f"Passive Ownership: {report['passive_ownership_pct']}%")
print(f"Reflexivity Risk: {report['inelasticity_rank']}")
```


---

## Source: service_real_estate.md

# Backend Service: Real Estate (The Property Empire)

## Overview
The **Real Estate Service** manages direct property investments and syndicated real estate deals. It tracks K-1 distributions, calculates depreciation recapture for tax purposes, and monitors capital raise progress for GP/LP structures.

## Core Components

### 1. Syndication Service (`syndication_service.py`)
- **Capital Raise Tracker**: Monitors "soft circle" commitments from investors before a deal closes.
- **K-1 Distribution Tracker**: Records distributions and adjusts cost basis for "Return of Capital" events.
- **Depreciation Recapture Calculator**: At sale, calculates the portion of gain subject to depreciation recapture (taxed at 25%) vs. long-term capital gains.

### 2. Supporting Modules
- `rental_yield.py`: Cap rate and cash-on-cash return calculations.
- `timer_service.py`: Manages 1031 exchange deadlines.
- `liquidity_model.py`: Estimates time-to-exit for illiquid property holdings.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Real Estate Portfolio** | Syndication Manager | `syndication_service.get_raise_status()` | **Partially Implemented** |
| **Tax Planning** | Recapture Estimator | `syndication_service.calculate_tax_recapture()` | **Missing** |

## Usage Example

```python
from services.real_estate.syndication_service import SyndicationService
from decimal import Decimal

service = SyndicationService()

# Track a soft commitment
service.soft_circle("DEAL_123", "INVESTOR_A", Decimal("100000"))

# Check capital raise progress
status = service.get_raise_status("DEAL_123", Decimal("1000000"))
print(f"Raise Progress: {status['pct_complete']}%")
```


---

## Source: service_reconciliation.md

# Backend Service: Reconciliation (The Auditor)

## Overview
The **Reconciliation Service** ensures that the platform's internal records match external sources of truth (brokerages, banks). It detects "drift" caused by missed transactions, API errors, or data corruption.

## Core Components

### 1. Consistency Checker (`consistency_checker.py`)
- **Ledger Verification**: Compares internal balance against broker-reported balance.
- **Drift Detection**: Flags discrepancies greater than $0.01 as reconciliation failures, triggering alerts.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Admin Dashboard** | Reconciliation Status | `consistency_checker.verify_ledger()` | **Implicit** (Runs as background job) |

## Usage Example

```python
from services.reconciliation.consistency_checker import ConsistencyChecker
from decimal import Decimal

checker = ConsistencyChecker()

# Compare internal vs. broker balance
is_ok, drift = checker.verify_ledger(
    internal_balance=Decimal("125000.45"),
    broker_balance=Decimal("125000.43")
)

print(f"Consistent: {is_ok}, Drift: ${drift}")
```


---

## Source: service_reits.md

# Backend Service: REITs (The Property Stock Lab)

## Overview
The **REITs Service** provides specialized analytics for Real Estate Investment Trusts. It calculates the key metrics that differ from traditional equity analysis: FFO (Funds From Operations) and AFFO (Adjusted FFO).

## Core Components

### 1. FFO Calculator (`ffo_calculator.py`)
- **FFO**: Adds back non-cash depreciation to net income and subtracts gains on property sales.
- **AFFO**: Further adjusts FFO by subtracting recurring capital expenditures, providing a truer picture of sustainable cash flow.

### 2. Supporting Modules
- `payout_validator.py`: Checks if the REIT's dividend payout ratio is sustainable.
- `property_classifier.py`: Categorizes REITs by sector (Residential, Industrial, Retail, etc.).
- `sector_yield_tracker.py`: Compares yields across REIT sectors.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **REIT Analyzer** | FFO Comparison | `ffo_calculator.calculate_ffo()` | **Missing** (Data powers Research) |

## Usage Example

```python
from services.reits.ffo_calculator import FFOCalculator

calc = FFOCalculator()

# Calculate FFO for a REIT
ffo = calc.calculate_ffo(
    net_income=50_000_000,
    depreciation=20_000_000,
    gains_on_sales=5_000_000
)

# Calculate AFFO (truer cash flow)
affo = calc.calculate_affo(ffo, recurring_cap_ex=8_000_000)

print(f"FFO: ${ffo:,.2f}, AFFO: ${affo:,.2f}")
```


---

## Source: service_reporting.md

# Backend Service: Reporting (The Family Office Statement)

## Overview
The **Reporting Service** generates consolidated reports for high-net-worth individuals and family offices. It aggregates assets across complex structures (trusts, insurance wrappers, private placements) into a single "Total Wealth" view.

## Core Components

### 1. Total Wealth Calculator (`total_wealth.py`)
- **Unified Balance Sheet**: Combines liquid assets, trust assets, insurance cash value (PPLI), and private placements.
- **Liquidity Scoring**: Calculates the percentage of assets that can be converted to cash quickly.
- **Qualification Status**: Flags clients as "Qualified Purchaser" (> $5M) for regulatory access to certain investments.

### 2. Supporting Modules
- `global_risk_aggregator.py`: Summarizes risk exposure across all entities.
- `trust_vs_probate.py`: Compares estate costs with and without trust structures.
- `survival_score.py`: Calculates a client's "runway" (months of expenses covered by liquid assets).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Wealth Dashboard** | Net Worth Summary | `total_wealth.aggregate_net_worth()` | **Implemented** (Global Store) |
| **Reports Page** | PDF Export | Various reporting modules | **Partially Implemented** |

## Usage Example

```python
from services.reporting.total_wealth import TotalWealthCalculator
from decimal import Decimal

calc = TotalWealthCalculator()

report = calc.aggregate_net_worth(
    liquid_assets=Decimal("5000000"),
    trust_assets=Decimal("10000000"),
    insurance_cash_value=Decimal("2000000"),
    private_placements=Decimal("3000000")
)

print(f"Total Net Worth: ${report['total_net_worth']:,.2f}")
print(f"Alternative Exposure: {report['alternative_exposure_pct']}%")
print(f"Status: {report['status']}")
```


---

## Source: service_reputation.md

# Backend Service: Reputation (The Guardian)

## Overview
The **Reputation Service** protects the digital identity of Ultra High Net Worth (UHNW) families. It detects deepfakes, monitors online sentiment, and automates legal takedown requests.

## Core Components

### 1. Deepfake Detector (`deepfake_detect.py`)
- **Media Scanning**: Analyzes videos/audio for manipulation artifacts (e.g., lip sync mismatches).
- **DMCA Automation**: Issues takedown notices for unauthorized AI clones of protected identities.

### 2. Supporting Modules
- `sentiment_radar.py`: Monitors online mentions of family members.
- `seo_shield.py`: Suppresses negative search results.
- `ghost_writer.py`: AI-generated reputation repair content.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Security Dashboard** | Deepfake Alerts | `deepfake_detect.scan_media()` | **Missing** |

## Usage Example

```python
from services.reputation.deepfake_detect import DeepfakeDetectorService

detector = DeepfakeDetectorService()

result = detector.scan_media("https://suspicious-site.com/fake_interview.mp4")
if result["is_deepfake"]:
    detector.issue_takedown(result["url"])
```


---

## Source: service_research.md

# Backend Service: Research (The Analyst Desk)

## Overview
The **Research Service** generates comprehensive research reports by combining qualitative analysis (SEC filings, moat scoring) with quantitative valuation (DCF models). It produces PDF-ready documents for portfolio analysis, company research, and market outlook.

## Core Components

### 1. Research Service (`research_service.py`)
- **Portfolio Reports**: Aggregates performance, risk metrics, and recommendations.
- **Company Research**: Integrates `FilingAnalyzer` (qualitative) and `DCFEngine` (quantitative) to produce actionable investment theses.
- **Caching**: Reports are cached for 365 days.

### 2. Report Generator (`report_generator.py`)
- Handles PDF export formatting.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Research Dashboard** | Company Deep Dive | `research_service.generate_company_research()` | **Implemented** (`ResearchWidget.jsx`) |
| **Reports Page** | PDF Export | `report_generator` | **Partially Implemented** |

## Usage Example

```python
from services.research.research_service import get_research_service

service = get_research_service()

report = await service.generate_company_research(
    user_id="user_01",
    symbol="NVDA"
)

print(f"Report: {report.title}")
print(f"Content: {report.content}")
print(f"Fair Value: ${report.data['fair_value']}")
```


---

## Source: service_retirement.md

# Backend Service: Retirement (The Glide Path)

## Overview
The **Retirement Service** provides the core financial planning engine for retirement projections. It uses **Monte Carlo simulations** (10,000 runs) to calculate the probability of a successful retirement based on savings rate, expected returns, and withdrawal strategy.

## Core Components

### 1. Retirement Projection Service (`retirement_projection_service.py`)
- **Monte Carlo Engine**: Runs thousands of simulations to model uncertainty.
- **Scenario Comparison**: Allows comparison of multiple retirement scenarios (e.g., retiring at 60 vs. 65).
- **Year-by-Year Timeline**: Generates a deterministic projection for visualization.

### 2. Supporting Modules (18 total)
- `glide_path_engine.py`: Automatically de-risks asset allocation as retirement approaches.
- `safe_withdrawal.py`: Implements the classic 4% rule and variants.
- `sequence_risk.py`: Models the risk of bad returns early in retirement.
- `match_calculator.py`: Calculates optimal 401(k) contributions to maximize employer match.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Retirement Dashboard** | Monte Carlo Chart | `retirement_projection_service.project_retirement()` | **Implemented** (`RetirementGauge.jsx`) |
| **Planning Widget** | Scenario Comparator | `retirement_projection_service.compare_scenarios()` | **Implemented** |

## Usage Example

```python
from services.retirement.retirement_projection_service import get_retirement_projection_service
from schemas.retirement import RetirementScenario

service = get_retirement_projection_service()

scenario = RetirementScenario(
    scenario_name="Early Retirement",
    current_age=40,
    retirement_age=55,
    life_expectancy=90,
    current_savings=500000.0,
    annual_contribution=30000.0,
    expected_return=0.07,
    withdrawal_rate=0.035,
    inflation_rate=0.03
)

projection = await service.project_retirement(scenario)
print(f"Probability of Success: {projection.probability_of_success:.1%}")
print(f"Projected Savings at Retirement: ${projection.projected_retirement_savings:,.0f}")
```


---

## Source: service_risk.md

# Backend Service: Risk (The Control Tower)

## Overview
The **Risk Service** is the largest and most critical service in the platform, with **45 specialized modules** designed to protect capital. It enforces hard limits on trading activity, monitors portfolio health in real-time, and automatically halts operations when thresholds are breached.

## Core Components (Selected)

### 1. Circuit Breaker (`circuit_breaker.py`)
The Emergency Brake.
- **Global Kill Switch**: Halts ALL trading immediately upon manual trigger.
- **Portfolio Freeze**: Automatically freezes trading if daily drawdown exceeds -3%.
- **Asset Kill Switch**: Halts trading on a specific asset if it drops >10% from its high.

### 2. Stress Testing Service (`stress_testing_service.py`)
- Simulates portfolio behavior under historical crash scenarios (2008, COVID, Black Monday).

### 3. Margin Service (`margin_service.py`)
- Calculates buying power and tracks margin usage to prevent forced liquidations.

### 4. Position Sizer (`position_sizer.py`)
- Implements Kelly Criterion and volatility-scaled position sizing.

### Other Key Modules
- `geopolitical_risk_svc.py`: Tracks exposure to politically unstable regions.
- `concentration_detector.py`: Flags when a single position dominates the portfolio.
- `liquidity_validator.py`: Ensures trades can be executed without excessive slippage.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Risk Dashboard** | Kill Switch Control | `circuit_breaker.is_halted()` | **Implemented** (`MissionControl.jsx`) |
| **Trade Ticket** | Position Sizer | `position_sizer.calculate_size()` | **Implemented** |
| **Stress Testing** | Scenario Analyzer | `stress_testing_service` | **Implemented** (`StressTest.jsx`) |

## Usage Example

```python
from services.risk.circuit_breaker import get_circuit_breaker

breaker = get_circuit_breaker()

# Check if trading is halted
if breaker.is_halted():
    print(f"Trading is HALTED. Reason: {breaker.freeze_reason}")
else:
    # Check daily P&L
    daily_pnl = -0.025 # -2.5%
    is_frozen = breaker.check_portfolio_freeze(daily_pnl)
    if not is_frozen:
        print("Trading is active.")

# Manual emergency halt
breaker.trigger_global_kill_switch("Flash crash detected manually.")
```


---

## Source: service_security.md

# Backend Service: Security (The Vault)

## Overview
The **Security Service** is the platform's defensive perimeter, containing **28 specialized modules** for identity management, encryption, and emergency protocols. It protects UHNW clients from both cyber threats and real-world incapacity scenarios.

## Core Components (Selected)

### 1. Dead Man Switch (`dead_man_switch.py`)
Digital Inheritance Protocol.
- **Check-In System**: Requires periodic user verification.
- **Trigger Threshold**: If 30 days pass without check-in, releases crypto keys/shards to designated beneficiaries.

### 2. Encryption Service (`encryption_service.py`)
- AES-256 encryption for data at rest.
- Key rotation and secure key storage.

### 3. KYC Service (`kyc_service.py`)
- Know Your Customer compliance for onboarding.
- Identity verification and sanction screening.

### 4. Supporting Modules
- `shamir_sharing.py`: Splits secret keys into shards.
- `pqc_keygen.py`: Post-Quantum Cryptography key generation.
- `geofence_service.py`: Location-based access restrictions.
- `panic_service.py`: Emergency lockout and asset freeze.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Security Settings** | Dead Man Switch | `dead_man_switch.check_in()` | **Missing** |
| **Vault** | Key Manager | `shamir_sharing`, `encryption_service` | **Partially Implemented** |

## Usage Example

```python
from services.security.dead_man_switch import DeadManSwitchService

switch = DeadManSwitchService()

# User confirms they are alive
switch.check_in()

# Check status
status = switch.verify_status()
print(f"Switch Status: {status['status']}")
print(f"Days Until Trigger: {status.get('days_until_trigger', 'N/A')}")
```


---

## Source: service_sfo.md

# Backend Service: SFO (Single Family Office Hub)

## Overview
The **SFO Service** provides the economic justification and governance framework for Ultra High Net Worth (UHNW) families considering the transition from external advisors to a dedicated Single Family Office.

## Core Components

### 1. SFO Justification Engine (`sfo_justification.py`)
- **Breakeven Analysis**: Compares external RIA fees (~1% AUM) against internal staffing costs (~$1M base).
- **Complexity Premium**: Adds cost for every $100M over $1B AUM.
- **Viability Score**: Returns whether an SFO is economically justified.

### 2. Supporting Modules
- `governance.py`: Governance policies and voting structures.
- `dark_asset_service.py`: Tracks off-the-books or undisclosed assets.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Family Office Dashboard** | Breakeven Calculator | `sfo_justification.run_breakeven_analysis()` | **Missing** |

## Usage Example

```python
from services.sfo.sfo_justification import SFOJustificationEngine
from decimal import Decimal

engine = SFOJustificationEngine()

result = engine.run_breakeven_analysis(Decimal("500000000")) # $500M AUM

print(f"External Fees: ${result['external_annual_fees']:,.2f}")
print(f"Internal Costs: ${result['internal_operating_est']:,.2f}")
print(f"Is SFO Viable? {result['is_sfo_economically_viable']}")
```


---

## Source: service_simulation.md

# Backend Service: Simulation (The What-If Engine)

## Overview
The **Simulation Service** runs "what-if" scenarios to stress-test trading strategies and portfolios. It contains **17 specialized simulators** covering Monte Carlo projections, geopolitical shocks, liquidity crises, and reflexivity dynamics.

## Core Components (Selected)

### 1. Monte Carlo Simulator (`monte_carlo_sim.py`)
- **Trade Sequence Simulation**: Projects a strategy's win rate and R-multiples forward over 1,000+ trades.
- **Ruin Detection**: Stops simulation if equity drops 50%, flagging the strategy as high-risk.
- **Max Drawdown Tracking**: Records the deepest equity dip.

### 2. Class Risk Simulator (`class_risk_sim.py`)
- Simulates correlated drawdowns across asset classes.

### 3. Geopolitical Simulator (`geopolitical_sim_engine.py`)
- Models the impact of war, sanctions, or regime change on portfolio exposure.

### Other Key Modules
- `reflexivity_sim.py`: Models passive fund flow dynamics.
- `power_law_sim.py`: Simulates fat-tail events (Black Swans).
- `liquidity_crisis.py`: Models forced selling spirals.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategy Lab** | Monte Carlo Chart | `monte_carlo_sim.run_simulation()` | **Implemented** (`MonteCarlo.jsx`) |
| **Risk Dashboard** | Scenario Analyzer | `geopolitical_sim_engine` | **Partially Implemented** |

## Usage Example

```python
from services.simulation.monte_carlo_sim import MonteCarloSimulator

result = MonteCarloSimulator.run_simulation(
    win_rate=0.55,       # 55% win rate
    avg_win_r=2.0,       # Win 2R on average
    avg_loss_r=1.0,      # Lose 1R on average
    initial_balance=100000,
    risk_per_trade_pct=0.01, # Risk 1% per trade
    num_trades=1000
)

print(f"Final Equity: ${result['final_equity']:,.2f}")
print(f"Max Drawdown: {result['max_drawdown_pct']}%")
print(f"Ruin Occurred: {result['ruin_occurred']}")
```


---

## Source: service_singularity.md

# Backend Service: Singularity (The Self-Improving AI)

## Overview
The **Singularity Service** contains the platform's most advanced AI capabilities: self-training, autonomous code refactoring, and emergent agent behaviors. It has **16 modules** designed for a future where the system can improve itself.

## Core Components (Selected)

### 1. Training Orchestrator (`training_orchestrator.py`)
- **LoRA/QLoRA Fine-Tuning**: Manages local GPU fine-tuning jobs for custom models.
- **Job Queue**: Tracks active training runs and GPU allocation.

### 2. Auto-Refactor (`auto_refactor.py`)
- AI-powered code analysis and improvement suggestions.

### 3. Bug Hunter (`bug_hunter.py`)
- Autonomous bug detection and fix generation.

### 4. Other Key Modules
- `rag_core.py`: Retrieval-Augmented Generation for contextual AI responses.
- `mind_upload.py`: Captures user decision patterns for persona modeling.
- `inference_engine.py`: Local inference for fine-tuned models.
- `defi_sniper.py`: Autonomous DeFi yield optimization.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mission Control** | Training Status | `training_orchestrator.get_job_status()` | **Missing** |
| **Evolution Dashboard** | Agent Hall of Fame | Various evolution modules | **Implemented** (`EvolutionDashboard.jsx`) |

## Usage Example

```python
from services.singularity.training_orchestrator import TrainingOrchestrator

orchestrator = TrainingOrchestrator()

job = orchestrator.submit_job(
    model_name="llama-3-8b-family-office",
    dataset_path="/data/family_office_qa.jsonl",
    params={"epochs": 3, "lora_rank": 16}
)

print(f"Job Status: {job['status']}")

# Check later
status = orchestrator.get_job_status(job["submitted_at"][:36])
print(f"Progress: {status.get('progress', 'N/A')}")
```


---

## Source: service_social.md

# Backend Service: Social (The Crowd Radar)

## Overview
The **Social Service** monitors online communities for trading sentiment and ticker mentions. It scrapes Discord, Reddit, StockTwits, Facebook, and YouTube to quantify "hype" and detect emerging momentum plays before they hit mainstream news.

## Core Components

### 1. Discord Bot (`discord_bot.py`)
- **Channel Monitoring**: Listens to configurable channels for ticker mentions.
- **Hype Scoring**: Calculates velocity (mentions/hour) and growth percentage.
- **Sentiment Tagging**: Labels messages as Bullish/Bearish/Neutral.

### 2. StockTwits Client (`stocktwits_client.py`)
- Fetches message streams and sentiment ratios for tickers.

### 3. Reddit Service (`reddit_service.py`)
- Monitors subreddits like r/wallstreetbets for unusual activity.

### Other Modules
- `facebook_hype_service.py`: Tracks public investment groups.
- `youtube_client.py`: Monitors financial YouTuber mentions.
- `inertia_cache.py`: Shared cache for cross-platform sentiment aggregation.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Social Sentiment** | Discord Feed | `discord_bot.get_recent_mentions()` | **Implemented** (`StockTwitsFeed.jsx`) |
| **Community Dashboard** | Hype Leaderboard | `discord_bot.get_hype_score()` | **Partially Implemented** |

## Usage Example

```python
from services.social.discord_bot import get_discord_bot
import asyncio

bot = get_discord_bot()

async def main():
    await bot.connect()
    mentions = await bot.get_recent_mentions("NVDA")
    for msg in mentions:
        print(f"[{msg['channel']}] {msg['author']}: {msg['content']}")

asyncio.run(main())
```


---

## Source: service_social_trading.md

# Backend Service: Social Trading (The Mirror)

## Overview
The **Social Trading Service** enables users to automatically replicate the trades of other investors. It provides the infrastructure for "copy trading," where a follower's portfolio mirrors the positions of a leading trader, adjusted by risk parameters.

## Core Components

### 1. Copy Trading Service (`copy_trading_service.py`)
- **Config Management**: Creates and manages copy relationships between followers and traders.
- **Proportional Allocation**: Scales trade size based on follower's chosen percentage of capital.
- **Risk Multiplier**: Allows followers to amplify or reduce the copied position size.
- **Execution Engine**: Automatically mirrors trades for all active followers.

### 2. Social Trading Service (`social_trading_service.py`)
- Manages trader profiles and leaderboards.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Social Trading Dashboard** | Copy Button | `copy_trading_service.create_copy_config()` | **Implemented** |
| **Leaderboards** | Top Traders | `social_trading_service` | **Implemented** |

## Usage Example

```python
from services.social_trading.copy_trading_service import get_copy_trading_service
import asyncio

service = get_copy_trading_service()

async def main():
    # Start copying a trader
    config = await service.create_copy_config(
        follower_id="user_123",
        trader_id="trader_alpha",
        allocation_percentage=25.0,  # Use 25% of my capital
        risk_multiplier=0.5          # Take half-sized positions
    )
    print(f"Copying {config.trader_id} with config {config.config_id}")

asyncio.run(main())
```


---

## Source: service_sovereignty.md

# Backend Service: Sovereignty (The Private Channel)

## Overview
The **Sovereignty Service** provides secure, private communication infrastructure for the platform's users and agents. It's the foundation for a self-hosted, off-grid messaging capability.

## Core Components

### 1. Chat Server (`chat_server.py`)
- Minimal implementation for private, secure messaging.
- Designed for internal agent-to-agent or user-to-advisor communication.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Advisor Chat** | Message Window | `chat_server` | **Missing** |

## Notes
This is a minimal service, likely a placeholder for future expansion into Matrix/Signal-based secure communications.


---

## Source: service_space.md

# Backend Service: Space (The Final Frontier)

## Overview
The **Space Service** monitors risks that originate beyond Earth's atmosphere. This is a forward-looking module designed for clients with significant space-related assets (satellites, SpaceX allocations) or for continuity planning in extreme scenarios.

## Core Components

### 1. Space Weather Service (`space_weather.py`)
- **Solar Flare Monitoring**: Tracks Kp-index and solar wind speed.
- **CME Alerting**: Warns of Coronal Mass Ejections that could disrupt communications.
- **Shielding Protocol**: Triggers hardware protection when solar storm risk is high.

### 2. Supporting Modules
- `astro_vault.py`: Secure storage for off-world contingency keys.
- `dsn_monitor.py`: Monitors Deep Space Network status.
- `terraforming_engine.py`: (Future) Long-term planetary colonization ROI models.
- `uplink_manager.py`: Manages satellite communication links.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Space Dashboard** | Solar Weather | `space_weather.scan_hazards()` | **Missing** |

## Usage Example

```python
from services.space.space_weather import SpaceWeatherService

svc = SpaceWeatherService()

report = svc.scan_hazards()
print(f"Status: {report['status']}")
print(f"Solar Wind: {report['solar_wind_speed']}")
print(f"Kp Index: {report['kp_index']}")
```


---

## Source: service_storage.md

# Backend Service: Storage (The Archive)

## Overview
The **Storage Service** provides secure document storage via AWS S3. All files are encrypted at rest (AES-256) and accessed via time-limited presigned URLs. It supports multipart uploads for large files and organizes documents by category.

## Core Components

### 1. S3 Service (`s3_service.py`)
- **Category Buckets**: Separate buckets for `tax`, `kyc`, `report`, `user_upload`, and `general` documents.
- **Encryption**: All objects are encrypted at rest using AWS S3-managed keys (AES-256).
- **Presigned URLs**: Secure, time-limited (default 1 hour) download links.
- **Multipart Upload**: Efficient upload of large files (>5MB) in chunks.
- **Checksum Verification**: SHA-256 checksums for data integrity.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Documents Page** | File Uploader | `s3_service.upload_file()` | **Partially Implemented** |
| **Tax Center** | Document Viewer | `s3_service.generate_presigned_url()` | **Implicit** |

## Usage Example

```python
from services.storage.s3_service import get_s3_service
import asyncio

s3 = get_s3_service()

async def main():
    # Upload a tax document
    with open("W2_2025.pdf", "rb") as f:
        content = f.read()
    
    result = await s3.upload_file(
        user_id="user_123",
        filename="W2_2025.pdf",
        content=content,
        category="tax"
    )
    
    print(f"Uploaded as: {result.s3_key}")
    
    # Generate download URL
    url = s3.generate_presigned_url(result.s3_key, category="tax")
    print(f"Download URL: {url}")

asyncio.run(main())
```


---

## Source: service_strategies.md

# Backend Service: Strategies (The Playbook)

## Overview
The **Strategies Service** contains **14 pre-built trading strategies** that the platform can deploy. These range from regime-aware allocation to political alpha (Pelosi tracking) to risk parity. Each strategy is a modular "recipe" that the Strategy Execution Engine can run.

## Core Components (Selected)

### 1. Regime Detector (`regime_detector.py`)
- **Trend Filter**: Uses SPY vs. 200-day SMA to classify market regime.
- **Volatility Filter**: Uses VIX level to confirm regime.
- **Regimes**: BULL (above SMA, low VIX), BEAR (below SMA or high VIX), TRANSITION.

### 2. Other Key Strategies
- `pelosi_copy.py`: Tracks and mirrors congressional trade disclosures.
- `risk_parity.py`: Allocates based on volatility contribution.
- `quality_tilt.py`: Overweights high-quality stocks.
- `smart_rebalance.py`: Intelligent portfolio rebalancing.
- `zone_filter.py`: Technical support/resistance-based filtering.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategy Builder** | Regime Selector | `regime_detector.detect_current_regime()` | **Implemented** |
| **Political Alpha** | Pelosi Tracker | `pelosi_copy` | **Implemented** (`PoliticalAlpha.jsx`) |

## Usage Example

```python
from services.strategies.regime_detector import RegimeDetector

detector = RegimeDetector()

regime = detector.detect_current_regime("SPY")

print(f"Current Regime: {regime['name']}")
print(f"Confidence: {regime['confidence']}")
print(f"SPY Position: {regime['spy_pos']}")
print(f"Risk-Off Mode: {regime['is_risk_off']}")
```


---

## Source: service_strategy.md

# Backend Service: Strategy (The Execution Engine)

## Overview
The **Strategy Service** is the runtime environment for trading strategies. It takes the "recipes" defined in the Strategies service and actually executes them live, with risk controls, performance monitoring, and drift detection.

## Core Components

### 1. Strategy Execution Service (`strategy_execution_service.py`)
- **Lifecycle Management**: Start, stop, and pause strategies.
- **Rule Execution**: Evaluates conditions and executes actions based on priority.
- **Performance Tracking**: Calculates win rate, P&L, Sharpe, and drawdown.
- **Drift Detection**: Calculates statistical drift between backtested expectations and live performance using chi-square and KS tests.

### 2. Supporting Modules
- `strategy_builder_service.py`: Creates and configures strategies.
- `strategy_compiler.py`: Compiles strategy rules into executable form.
- `tax_harvester.py`: Automated tax-loss harvesting logic.
- `dynamic_allocator.py`: Adjusts allocations based on market conditions.
- `rebalance_engine.py`: Triggers rebalancing when drift exceeds thresholds.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategy Dashboard** | Run/Stop Controls | `strategy_execution_service.start_strategy()` | **Implemented** |
| **Performance Tab** | Drift Monitor | `strategy_execution_service.calculate_model_drift()` | **Partially Implemented** |

## Usage Example

```python
from services.strategy.strategy_execution_service import get_strategy_execution_service
import asyncio

service = get_strategy_execution_service()

async def main():
    # Start a strategy
    strategy = await service.start_strategy(
        strategy_id="strat_001",
        portfolio_id="portfolio_main"
    )
    print(f"Strategy {strategy.strategy_id} is now {strategy.status.value}")
    
    # Check for drift
    drift = await service.calculate_model_drift("strat_001")
    print(f"Drift Score: {drift.drift_score:.2%} - Status: {drift.status}")

asyncio.run(main())
```


---

## Source: service_streaming.md

# Backend Service: Streaming (The Event Bus)

## Overview
The **Streaming Service** provides real-time data pipelines using Kafka. It consumes messages from department-specific topics (events, metrics, agent status) and relays them to WebSocket clients, enabling live dashboard updates.

## Core Components

### 1. Kafka Department Consumer (`kafka_dept_consumer.py`)
- **Topic Subscription**: Subscribes to per-department topics for events, metrics, and agent status.
- **Fallback Simulation**: If Kafka is unavailable, simulates realistic department updates for development.
- **WebSocket Relay**: Integrates with `DepartmentBroadcaster` to push messages to frontend clients.

### Topic Structure
| Topic Pattern | Purpose | Retention |
| :--- | :--- | :--- |
| `dept.{id}.events` | Department events | 7 days |
| `dept.{id}.metrics` | Performance metrics | 24 hours |
| `dept.{id}.agents` | Agent status updates | 1 hour |
| `telemetry.stream` | Global telemetry | 24 hours |
| `system.alerts` | System-wide alerts | 7 days |

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mission Control** | Live Metrics | `kafka_dept_consumer` → WebSocket | **Implemented** |
| **Agent Monitor** | Status Panel | `topic: dept.{id}.agents` | **Implemented** |

## Usage Example

```python
from services.streaming.kafka_dept_consumer import start_dept_consumer
import asyncio

async def main():
    consumer = await start_dept_consumer()
    
    def my_broadcast(dept_id, topic_type, message):
        print(f"Dept {dept_id} [{topic_type}]: {message}")
    
    consumer.set_broadcast_callback(my_broadcast)
    
    # Let it run
    await asyncio.sleep(60)
    await consumer.stop()

asyncio.run(main())
```


---

## Source: service_system.md

# Backend Service: System (The Operating Core)

## Overview
The **System Service** contains **24 foundational modules** that power the platform's infrastructure. It manages caching, secrets, health checks, authentication, and cross-cutting concerns that all other services depend on.

## Core Components (Selected)

### 1. Cache Service (`cache_service.py`)
- **Redis Backend**: Uses Redis for high-performance distributed caching.
- **In-Memory Fallback**: Automatically falls back to in-memory cache if Redis is unavailable.
- **TTL Support**: All cached items have configurable time-to-live.

### 2. Secret Manager (`secret_manager.py`)
- Environment variable loading with `.env` support.

### 3. Vault Secret Manager (`vault_secret_manager.py`)
- HashiCorp Vault integration for production secrets.

### 4. Other Key Modules
- `totp_service.py`: Time-based One-Time Password generation for MFA.
- `health_check_service.py`: Liveness and readiness probes.
- `social_auth_service.py`: OAuth2 flows for Google, Discord, etc.
- `tracing_service.py`: Distributed tracing for debugging.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Settings** | MFA Setup | `totp_service` | **Implemented** |
| **Health Monitor** | Status Page | `health_check_service` | **Implemented** (`HealthToast.jsx`) |

## Usage Example

```python
from services.system.cache_service import get_cache_service

cache = get_cache_service()

# Set a value with 1-hour TTL
cache.set("user:123:preferences", {"theme": "dark"}, ttl=3600)

# Get a value
prefs = cache.get("user:123:preferences")
print(prefs)  # {"theme": "dark"}
```


---

## Source: service_tax.md

# Backend Service: Tax (The Tax Shelter)

## Overview
The **Tax Service** is the largest service in the platform with **49 specialized modules** dedicated to tax optimization, compliance, and planning. It handles everything from tax-loss harvesting to estate tax calculations, ensuring maximum after-tax returns for UHNW clients.

## Core Components (Selected)

### 1. Tax Optimization Service (`tax_optimization_service.py`)
- **Lot Selection**: FIFO, LIFO, Highest Cost, Lowest Cost, Specific Lot.
- **Year-End Projection**: Projects tax liability based on realized gains.
- **Withdrawal Sequencing**: Optimizes withdrawal order (taxable → tax-deferred → tax-free).

### 2. Harvest Services (`harvest_service.py`, `enhanced_tax_harvesting_service.py`)
- **Tax-Loss Harvesting**: Identifies losing positions to realize losses.
- **Wash Sale Protection**: Prevents wash sale violations.

### 3. Other Key Modules
- `qoz_service.py`: Qualified Opportunity Zone capital gains deferral.
- `section121_validator.py`: Primary residence sale exclusion ($250k/$500k).
- `exit_tax_engine.py`: Expatriation tax calculations.
- `backdoor_roth_procedure.py`: Mega Backdoor Roth IRA conversions.
- `crt_deduction.py`: Charitable Remainder Trust deductions.
- `gst_calculator.py`: Generation-Skipping Transfer Tax.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Tax Dashboard** | Harvest Opportunities | `harvest_service` | **Implemented** (`TaxOptimizer.jsx`) |
| **Tax Projection** | Year-End Estimate | `tax_optimization_service.project_year_end_tax()` | **Implemented** |
| **Withdrawal Planner** | Sequence Optimizer | `tax_optimization_service.optimize_withdrawal_sequence()` | **Partially Implemented** |

## Usage Example

```python
from services.tax.tax_optimization_service import get_tax_optimization_service
import asyncio

service = get_tax_optimization_service()

async def main():
    # Optimize lot selection for selling AAPL
    result = await service.optimize_lot_selection(
        portfolio_id="portfolio_001",
        symbol="AAPL",
        quantity=100,
        method="highest_cost"  # Minimize taxes on gains
    )
    
    print(f"Tax Impact: ${result['tax_impact']['tax_impact']:.2f}")
    print(f"Gain/Loss: ${result['gain_loss']:.2f}")

asyncio.run(main())
```


---

## Source: service_trading.md

# Backend Service: Trading (The Execution Floor)

## Overview
The **Trading Service** contains **22 modules** for order execution, risk management, and trading simulation. It provides both live trading infrastructure and a realistic paper trading environment for strategy development.

## Core Components (Selected)

### 1. Paper Trading Service (`paper_trading_service.py`)
- **Virtual Portfolios**: Simulated portfolios with configurable starting capital.
- **Realistic Execution**: Slippage, commissions, and partial fills.
- **Performance Tracking**: Returns, drawdown, and position analytics.

### 2. FX Service (`fx_service.py`)
- Multi-currency trading and exposure management.

### 3. Option Hedge Service (`option_hedge_service.py`)
- Protective put and covered call strategies.

### Other Key Modules
- `trailing_stop.py`: Dynamic trailing stop-loss orders.
- `slippage_estimator.py`: Estimates execution slippage by order size.
- `defensive_protocol.py`: Risk-off protocols for market crashes.
- `ipo_tracker.py`: Tracks IPO allocations and lock-up periods.
- `beneficiary_blocker.py`: Prevents trades that violate beneficiary restrictions.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Paper Trading** | Portfolio View | `paper_trading_service.get_portfolio_performance()` | **Implemented** (`PaperTrading.jsx`) |
| **Order Ticket** | Execute Button | `paper_trading_service.execute_paper_order()` | **Implemented** |
| **FX Dashboard** | Currency Exposure | `fx_service` | **Implemented** (`FXOverview.jsx`) |

## Usage Example

```python
from services.trading.paper_trading_service import get_paper_trading_service
import asyncio

service = get_paper_trading_service()

async def main():
    # Create a paper trading portfolio
    portfolio = await service.create_virtual_portfolio(
        user_id="user_123",
        portfolio_name="My Test Strategy",
        initial_cash=100000.0
    )
    
    # Execute a paper trade
    order = await service.execute_paper_order(
        portfolio_id=portfolio.portfolio_id,
        symbol="AAPL",
        quantity=100,
        order_type="market"
    )
    
    print(f"Filled at ${order.filled_price:.2f}")
    print(f"Commission: ${order.commission:.2f}")
    print(f"Slippage: ${order.slippage:.4f}")

asyncio.run(main())
```


---

## Source: service_treasury.md

# Backend Service: Treasury (The Cash Desk)

## Overview
The **Treasury Service** manages corporate cash and liquidity across the family office. It optimizes idle cash placement and manages sweep accounts.

## Core Components

### 1. Cash Management Service (`cash_management_service.py`)
- **Cash Position Tracking**: Monitors cash across all accounts.
- **Sweep Rules**: Defines when and where to move excess cash.

### 2. Idle Sweeper (`idle_sweeper.py`)
- **Automatic Sweep**: Moves idle cash to money market funds overnight.
- **Threshold Management**: Only sweeps amounts above a minimum balance.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Treasury Dashboard** | Cash Status | `cash_management_service` | **Missing** |

## Notes
This is a smaller service focused on operational treasury functions. Larger investment decisions are handled by the Planning and Strategy services.


---

## Source: service_trusts.md

# Backend Service: Trusts (The Estate Vault)

## Overview
The **Trusts Service** manages Charitable Remainder Trusts (CRTs) and other trust structures for estate planning. It handles distributions, remainder calculations, and tax benefits.

## Core Components

### 1. CRT Service (`crt_service.py`)
- **Distribution Management**: Calculates annual distributions based on trust type.
- **Remainder Tracking**: Monitors the remainder interest for charitable beneficiaries.

### 2. CRT Distribution (`crt_distribution.py`)
- Calculates specific payout amounts based on unitrust or annuity trust rules.

### 3. Remainder Trigger (`remainder_trigger.py`)
- Monitors when the remainder interest passes to charity.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Estate Planning** | CRT Calculator | `crt_service` | **Partially Implemented** |

## Notes
CRTs provide income streams to donors while benefiting charities, with significant tax advantages.


---

## Source: service_validators.md

# Backend Service: Validators (The Gatekeeper)

## Overview
The **Validators Service** provides data validation utilities, currently focused on Kafka message validation.

## Core Components

### 1. Kafka Validators (`kafka_validators.py`)
- Validates incoming Kafka messages against expected schemas.
- Ensures data integrity before processing.

## Notes
This is a utility service used internally by streaming and messaging components.


---

## Source: service_valuation.md

# Backend Service: Valuation (The Appraisal Desk)

## Overview
The **Valuation Service** calculates intrinsic value using valuation models. Its centerpiece is a 2-stage Discounted Cash Flow (DCF) engine powered by live financial data.

## Core Components

### 1. DCF Engine (`dcf_engine.py`)
- **Data Integration**: Fetches financials via SEC Scraper.
- **2-Stage DCF Model**: Projects cash flows for 5 years, then calculates terminal value.
- **Margin of Safety**: Compares fair value to current price.

### 2. Supporting Modules
- `safe_calc.py`: SAFE note conversion calculations.
- `secondary_market.py`: Pre-IPO secondary share valuation.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Research Dashboard** | Fair Value Badge | `dcf_engine.calculate_intrinsic_value()` | **Implemented** |

## Usage Example

```python
from services.valuation.dcf_engine import DCFEngine

engine = DCFEngine()

result = engine.calculate_intrinsic_value("AAPL")

print(f"Current Price: ${result['current_price']:.2f}")
print(f"Fair Value: ${result['fair_value']:.2f}")
print(f"Margin of Safety: {result['margin_of_safety_pct']:.1f}%")
```


---

## Source: service_vc.md

# Backend Service: VC (The Deal Flow)

## Overview
The **VC Service** provides venture capital investment analysis tools, including deal scoring and contrarian opportunity detection.

## Core Components

### 1. Tier 1 Scorer (`tier1_scorer.py`)
- Scores deals based on team quality, market size, and traction.

### 2. Deal Aggregator (`deal_aggregator.py`)
- Aggregates deal flow from multiple syndicate sources.

### 3. Contrarian Detector (`contrarian_detector.py`)
- Identifies overlooked opportunities in unpopular sectors.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **VC Dashboard** | Deal Pipeline | `deal_aggregator` | **Missing** |


---

## Source: service_venture.md

# Backend Service: Venture (The Cap Table)

## Overview
The **Venture Service** manages capitalization tables for startup investments, tracking ownership stakes, dilution, and vesting schedules.

## Core Components

### 1. Cap Table Service (`cap_table_service.py`)
- **Ownership Tracking**: Records share classes, options, and SAFEs.
- **Dilution Modeling**: Projects dilution from future funding rounds.
- **Exit Scenarios**: Calculates payout under different exit valuations.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Venture Dashboard** | Cap Table View | `cap_table_service` | **Missing** |


---

## Source: service_warden.md

# Backend Service: Warden (The Scheduler)

## Overview
The **Warden Service** manages scheduled jobs and automated routines. It acts as the platform's internal job scheduler, running background tasks on defined intervals.

## Core Components

### 1. Scheduler (`scheduler.py`)
- **Cron-like Scheduling**: Triggers jobs at specified intervals.
- **Job Registry**: Maintains a list of registered background tasks.

### 2. Routine Runner (`routine_runner.py`)
- Executes registered routines sequentially or in parallel.

### 3. Circuit Breaker (`circuit_breaker.py`)
- Halts job execution if failures exceed a threshold.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Ops Dashboard** | Job Monitor | `scheduler` | **Missing** |


---

## Source: service_watchlist.md

# Backend Service: Watchlist (The Radar)

## Overview
The **Watchlist Service** allows users to track symbols of interest across multiple organized lists. It supports alerts and integrates with market data for real-time updates.

## Core Components

### 1. Watchlist Service (`watchlist_service.py`)
- **CRUD Operations**: Create, read, update, delete watchlists.
- **Symbol Management**: Add and remove symbols from lists.
- **Multi-Watchlist Support**: Users can have multiple named watchlists.

### 2. Alert Service (`alert_service.py`)
- **Price Alerts**: Triggers when a symbol hits a target price.
- **Volume Alerts**: Triggers on unusual volume.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Sidebar** | Watchlist Panel | `watchlist_service` | **Implemented** |
| **Alerts Page** | Alert Manager | `alert_service` | **Partially Implemented** |

## Usage Example

```python
from services.watchlist.watchlist_service import get_watchlist_service
import asyncio

service = get_watchlist_service()

async def main():
    watchlist = await service.create_watchlist(
        user_id="user_123",
        watchlist_name="Tech Giants",
        symbols=["AAPL", "MSFT", "GOOGL"]
    )
    
    await service.add_symbol(watchlist.watchlist_id, "NVDA")
    print(f"Symbols: {watchlist.symbols}")

asyncio.run(main())
```


---

## Source: service_wealth.md

# Backend Service: Wealth (The Net Worth Engine)

## Overview
The **Wealth Service** is a comprehensive wealth management hub with **26 modules** covering net worth tracking, asset allocation homeostasis, and specialized financial planning tools for UHNW families.

## Core Components (Selected)

### 1. Homeostasis Engine (`homeostasis_engine.py`)
- **Portfolio Balance**: Maintains target ratios between liquid growth (50%), safe moat (30%), and speculative (20%).
- **Deviation Detection**: Flags when allocations drift more than 5% from targets.
- **Rebalancing Actions**: Recommends specific adjustments.

### 2. Other Key Modules
- `net_worth.py`: Consolidated net worth calculation.
- `ppli_forecaster.py`: Private Placement Life Insurance projections.
- `bond_ladder.py`: Bond maturity ladder construction.
- `concentration_alert.py`: Single-position concentration warnings.
- `enough_calculator.py`: "Enough" wealth threshold calculation.
- `estate_planner.py`: Estate transfer optimization.
- `inflation_hedge.py`: Inflation protection strategies.
- `illiquid_tracker.py`: Tracks illiquid asset exposure.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Net Worth Dashboard** | Total Value | `net_worth` | **Implemented** |
| **Asset Allocation** | Homeostasis Gauge | `homeostasis_engine.check_homeostasis()` | **Partially Implemented** |
| **Estate Planning** | Transfer Optimizer | `estate_planner` | **Missing** |

## Usage Example

```python
from services.wealth.homeostasis_engine import HomeostasisEngine

engine = HomeostasisEngine()

portfolio = {
    "liquid_growth": 600000,
    "safe_moat": 300000,
    "speculative": 100000
}

result = engine.check_homeostasis(portfolio)
print(f"Balanced: {result['is_balanced']}")
print(f"Actions: {result['actions_required']}")
```


---

## Source: service_workspace.md

# Backend Service: Workspace (The User Hub)

## Overview
The **Workspace Service** manages user preferences and personalization settings for the application.

## Core Components

### 1. User Preferences Service (`user_preferences_service.py`)
- **Theme Preferences**: Dark/light mode, color schemes.
- **Layout Settings**: Dashboard widget arrangement.
- **Notification Preferences**: Email, push, and in-app alert settings.
- **Default Account**: Sets default portfolio for trading actions.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Settings Page** | Preferences Panel | `user_preferences_service` | **Implemented** |


---

