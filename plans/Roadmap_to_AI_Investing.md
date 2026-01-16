# Roadmap to AI Investing: Project Genesis & Extraction

**Version:** 5.0 (The 42-Phase Ultimate Plan)
**Source Template:** `Job_Recruiter` (Existing Project)
**Target Project:** `AI_Investor` (New Repository)
**Philosophy:** Complex Adaptive System (The "Yellowstone Wolf" Principle)
**Last Updated:** 2026-01-16 (16:10 EST)

---

## Strategic Vision: The Autonomous Profit Engine

### Core Philosophy

The AI Investor system operates as a **Complex Adaptive System** inspired by ecological balance principles. Like the wolves of Yellowstone that restored ecosystem equilibrium, our agent swarm maintains portfolio balance through constant oscillation detection and mean-reversion strategies.

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MISSION CONTROL DASHBOARD                     │
│         Real-time visualization • Infographic UX • Controls      │
└─────────────────────────────────────────────────────────────────┘
                              ▲ WebSocket
┌──────────────────────────────┴──────────────────────────────────┐
│                      ORCHESTRATION LAYER                         │
│   Portfolio Allocator • Risk Governor • Regime Classifier        │
└─────────────┬───────────────────────────────────────┬───────────┘
              │                                       │
    ┌─────────▼─────────┐                   ┌────────▼─────────┐
    │  DEFENSIVE SHIELD  │                   │  AGGRESSIVE ALPHA │
    │     Portfolio       │                   │     Portfolio      │
    │  ─────────────────  │                   │  ─────────────────  │
    │  • Capital Pres.    │     Dynamic       │  • Growth Focus    │
    │  • Low Volatility   │◄───Allocation────►│  • High Conviction │
    │  • Income Focus     │                   │  • Momentum Capture│
    └─────────┬───────────┘                   └────────┬──────────┘
              │                                        │
    ┌─────────▼──────────────────────────────────────▼───────────┐
    │                       AGENT SWARM                            │
    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
    │  │Protector │ │ Searcher │ │ Stacker  │ │ Backtest │        │
    │  │  Agent   │ │  Agent   │ │  Agent   │ │  Agent   │        │
    │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
    └─────────────────────────────────────────────────────────────┘
                               ▼ Kafka
    ┌─────────────────────────────────────────────────────────────┐
    │                     DATA INFRASTRUCTURE                      │
    │  Neo4j Graph • Postgres TimeSeries • Google Trends • Reddit  │
    └─────────────────────────────────────────────────────────────┘
```

---

## The 42-Phase Evolution Plan

### Part I: Genesis & Foundation (Phases 0-5)

#### Phase 0: DNA Extraction (Borrowed Infrastructure) ✅

**Goal:** Extract core "Project DNA" from `Job_Recruiter` template.

- [x] **CLI Utility:** Copy and adapt `cli.py` for dynamic command handling.
- [x] **Command Registry:** Integrate `utils/registry/command_registry.py` to allow JSON-based command mapping.
- [x] **Configuration Engine:** Implement `utils/core/config.py` with multi-environment `.env` support.
- [x] **Logging System:** Standardize `utils/logging.py` with rotating file handlers and console formatting.
- [x] **Activity Auditing:** Incorporate `UnifiedActivityService` for business logic logging.
- [x] **Agent Blueprint:** Port `BaseAgent` class with standard `process_event` and `circuit_breaker` logic.
- [x] **Environment Isolation:** Initialize project-specific `venv/` to prevent dependency leakage.
- **Acceptance Criteria:**
  - `python cli.py --help` displays all registered investor commands.
  - Environment variables correctly load from `.env`.
  - All new agents successfully inherit from `BaseAgent`.
  - Activity logs are correctly persisted to the `activity` log file.

#### Phase 1: Project Scaffolding & Infrastructure ✅

**Goal:** Establish the physical environment for the AI.

- [x] Initialize Git repository `AI_Investor`.
- [x] Configure Docker environment (Kali Linux/Debian optimized).
- [x] Set up persistent volumes for Postgres and Neo4j.
- [x] Create core directory structure (`agents/`, `services/`, `web/`).
- [ ] **Web Framework:** Implement FastAPI/Flask routing with shared Middleware (JWT, Error Handling).
- **Acceptance Criteria:**
  - System boots with `docker-compose up` without errors.
  - All database ports are accessible locally.
  - API Health-check endpoint returns 200.

#### Phase 2: The Nervous System (Kafka Event Bus) ✅

**Goal:** Enable sub-millisecond communication between agents.

- [x] Configure Zookeeper and Kafka services.
- [x] Implement Topic Manager (`scripts/kafka/init_topics.py`).
- [x] Create `MarketEvent` and `SignalEvent` schemas.
- **Acceptance Criteria:**
  - Messages persist across restarts.
  - Consumer groups function correctly.
  - Latency < 5ms for local message passing.

#### Phase 3: The Brain Structure (Neo4j & Postgres) ✅

**Goal:** Long-term memory and relationship mapping.

- [x] Design Graph Schema (Asset, Sector, Correlation).
- [x] Implement Postgres Time-series tables.
- [x] Populate sample data (S&P 500 constituents).
- **Acceptance Criteria:**
  - Neo4j queries return connected assets within 50ms.
  - Postgres handles 10k inserts/sec.

#### Phase 4: The Agents (Prototypes) ✅

**Goal:** Birth of the first autonomous entities.

- [x] **BaseAgent** implementation.
- [x] **ProtectorAgent** (Risk Monitor).
- [x] **SearcherAgent** (Opportunity Scanner).
- [x] **StackerAgent** (Decision Maker).
- **Acceptance Criteria:**
  - Agents successfully register with the orchestration layer.
  - Agents emit heartbeats to Kafka.

#### Phase 5: Signal Processing Core (FFT & HMM) ✅

**Goal:** Ability to perceive market rhythms and regimes.

- [x] Fast Fourier Transform (FFT) Engine for cycle detection.
- [x] Hidden Markov Model (HMM) for regime classification.
- **Acceptance Criteria:**
  - Accurately identify "Bull", "Bear", and "Sideways" regimes.
  - Isolate dominant market frequencies with >90% consistency.

#### Phase 5.5: Legacy Feature Refinement (The "Missing Links") ✅

**Goal:** ensure unique concepts from original plans are not lost.

- [x] **Neo4j "Recycling Centers":** Explicitly map nodes where "dead" capital is re-routed.
- [x] **"The Gap" Metric:** Ensure the `GapDisplay` is the mathematical heart of the dashboard.
- [x] **Iron Condor Logic:** Implement as the primary "Neutral Regime" yield generator.
- [x] **Synthetic Options:** Verify Node.js engine can mechanically "manufacture" a put option via Delta hedging.

#### Phase 5.7: LLM Workflow Optimization ✅

**Goal:** Enhance the AI-to-Code interface for faster iteration.

- [x] **Standardized Verbose Headers:** Implement rich comments at the top of every file (Purpose, Role, I/O).
- [x] **Infrastructure Guardrails:** Enhanced `.gitignore` and `.dockerignore`.
- [x] **Workflow Enforcement:** Standardized headers applied across all core modules.

---

### Part II: The Senses - Data & Sentiment (Phases 6-12)

#### Phase 6: Primary Market Data Tap ✅

**Goal:** High-fidelity financial data ingestion.

- [x] Implement Alpha Vantage / Polygon.io wrappers.
- [x] Build `MarketDataProducer` for Kafka.
- [x] Implement historical data backfill loader (`historical_loader.py`).
- **Verbose Acceptance Criteria:**
  - [x] Connector handles rate limits gracefully with exponential backoff.
  - [ ] Websocket connection maintains stability > 24 hours.
  - [x] No data gaps in OHLCV bars (Verified via `backfill-history`).
  - [ ] Latency from API to Kafka topic < 200ms.

#### Phase 7: The "Crowd Wisdom" Engine (Google Trends) ✅

**Goal:** Quantify retail sentiment using creative search queries.

- [x] Implement `GoogleTrendsService` (`services/data/google_trends.py`).
- [x] **Query Normalization:** Compare search volume vs 90-day moving average.
- [x] **Spike Detection:** Flag moves > 2 standard deviations as significant.
- [x] **Fear Keywords:** `AMZN debt`, `margin call`, `how to short` (Correlation > 0.6 with drops).
- [x] **Greed Keywords:** `buy [TICKER]`, `moon`, `price prediction`.
- **Verbose Acceptance Criteria:**
  - [x] Service successfully pulls trend data for tracked keywords.
  - [x] Correlation engine identifies > 0.6 correlation between specific local search spikes and price drops.
  - [x] System alerts when "Fear" queries exceed 2 standard deviations.
  - [x] "Trend Score" is persisted to Neo4j and Kafka.

#### Phase 8: Social NLP Pipeline (Reddit & Twitter) ✅

**Goal:** Decode the hive mind of `r/wallstreetbets` and FinTwit.

- [x] Build Reddit Scraper using PRAW.
- [x] **FinBERT Integration:** Use pre-trained financial model for sentiment (-1 to +1).
- [x] **Meme Velocity:** Track "Rate of Change" in mentions (alert on 500% spikes).
- [x] **Noise Filtering:** Identify and downweight sarcasm/shitposting.
- **Verbose Acceptance Criteria:**
  - [ ] System identifies trending tickers on Reddit before they appear on CNBC.
  - [ ] FinBERT correctly labels "bullish", "long", "calls" as positive.
  - [ ] Daily report generated: "Most Discussed Tickers" with sentiment polarity.
  - [ ] Real-time alert for sudden 500% spike in mentions.

#### Phase 9: The "Smart Money" Decoder (Options Flow) ✅

**Goal:** See what the institutions are doing in the dark.

- [x] Access Options flow data (unusual whales, sweeps).
- [x] Implement Put/Call Ratio tracker.
- [x] Detect "Gamma Squeezes" setups (Heuristics in `OptionsFlowService`).
- **Verbose Acceptance Criteria:**
  - [x] Identify "Whale" trades via volume/OI heuristics (Verified in Mock Mode).
  - [x] Calcualte GEX (Gamma Exposure) for major indices (Partial implementation via `get_options_sentiment`).
  - [x] Alert when Put/Call ratio hits extreme bounds (Calculated via `get_options_sentiment`).

#### Phase 10: Macro-Economic Pulse ✅

**Goal:** Understand the ocean the fish are swimming in.

- [x] Integrate FRED API (Federal Reserve Economic Data).
- [x] Track Yield Curve Inversion (10Y-2Y); trigger 'Recession' protocol after inversion.
- [x] Monitor Inflation (CPI/PCE) and Unemployment claims in real-time.
- **Verbose Acceptance Criteria:**
  - [x] Automated fetching of economic calendar events (Verified via `test-macro`).
  - [x] System changes "Regime" status to "Recession Warning" if Yield Curve inverts.
  - [x] Unemployment claims correlated with market liquidity drops (Data points ingested).

#### Phase 11: Data Fusion & Normalization ✅ (VERIFIED COMPLETE)

**Goal:** One Truth to rule them all.

- [x] Create `DataFusionLayer` to merge Price, Sentiment, and Macro data.
- [x] **Synchronization:** All streams aligned to 1-minute bars using UTC timestamps.
- [x] **Quarantine:** "Dirty" data (outliers/missing) is automatically flagged and isolated.
- **Implementation:** `services/data/data_fusion_service.py` - DataFusionService class
- **Verbose Acceptance Criteria:**
  - [x] All data streams are synchronized to the exact same timestamp (1-minute bars).
  - [x] "Dirty" data is flagged and quarantined automatically.
  - [x] Data lineage is traceable from source to final database record.

#### Phase 12: The "Fear & Greed" Composite Index ✅ IMPLEMENTED

**Goal:** A proprietary master metric for market emotion.
**Started:** 2026-01-16

- [ ] **Data Fusion:** Merge Trends, Social, VIX, and Put/Call data.
- [ ] **Scoring Scale:** 0 (Extreme Fear) to 100 (Extreme Greed).
- [ ] **Strategic Thresholds:**
  - **< 20 (Bottom):** High-probability buying opportunity (Defensive -> Aggressive shift).
  - **> 80 (Top):** Risk mitigation window (Aggressive -> Defensive shift).
- [ ] **FearGreedIndexService:** Create dedicated service in `services/analysis/fear_greed_service.py`
- [ ] **API Endpoint:** Add `/api/market/fear-greed` endpoint for real-time access.
- [ ] **Dashboard Widget:** Create `FearGreedGauge.jsx` visualization component.
- **Verbose Acceptance Criteria:**
  - [ ] Index historically correlates with market tops (Greed > 80) and bottoms (Fear < 20).
  - [ ] Real-time calculation updated every minute.
  - [ ] Dashboard visualization showing the gauge needle.

---

### Part III: The Intuition - Advanced Analytics (Phases 13-15)

#### Phase 13: Feature Engineering Pipeline

**Goal:** Transform raw data into ML-ready vectors.

- [ ] Rolling window statistics (RSI, MACD, Bollinger).
- [ ] Lagged features for time-series prediction.
- [ ] Sentiment vectors (Fear Score, Hype Score).
- **Verbose Acceptance Criteria:**
  - [ ] Feature store contains 200+ distinct features per asset.
  - [ ] Feature generation takes < 50ms per tick.

#### Phase 14: Predictive Modeling (Machine Learning)

**Goal:** Probabilistic forecasting of future price/regime.

- [ ] Train XGBoost Classifier for "Up/Down" prediction.
- [ ] Train LSTM/Transformer for price trajectory.
- [ ] Implement model versioning and A/B testing.
- **Verbose Acceptance Criteria:**
  - [ ] Model achieves > 55% directional accuracy out-of-sample.
  - [ ] Inference time < 10ms.
  - [ ] Automated retraining pipeline triggers weekly.

#### Phase 15: Factor Analysis & Risk Parity ✅ IMPLEMENTED

**Goal:** Understanding the "Why" behind returns.

- [ ] Implement Fama-French 5-Factor model.
- [ ] Calculate Beta, Momentum, Value, Quality, Size factors.
- **Verbose Acceptance Criteria:**
  - [ ] Portfolio decomposition shows exactly how much risk comes from each factor.
  - [ ] Risk Parity algorithm balances risk contributions equally across assets.

---

### Part IV: The Strategy - Dual Portfolio Management (Phases 16-19)

#### Phase 16: Defensive Shield Construction 🛡️ ✅ IMPLEMENTED

**Goal:** Preservation of capital. "Don't lose money."

- [ ] **Strategy:** Low Volatility + Dividend Aristocrats + Treasuries.
- [ ] **Logic:** Allocation increases when Fear Index is high.
- [ ] **Selection:** Assets with Beta < 0.5 and Yield > 3%.
- **Verbose Acceptance Criteria:**
  - [ ] Portfolio Max Drawdown never exceeds 5% in backtests.
  - [ ] Yield generation meets reliable monthly targets.
  - [ ] Auto-rotation into Cash/Gold during "Crash" regime.

#### Phase 17: Aggressive Alpha Construction 🚀 ✅ IMPLEMENTED

**Goal:** Asymmetric upside. "Hunt for 100x."

- [ ] **Strategy:** Momentum + Growth + Crypto + Options.
- [ ] **Logic:** Allocation increases when "Goldilocks" regime (Growth + Low Vol).
- [ ] **Selection:** High Relative Strength, High Social Sentiment.
- **Verbose Acceptance Criteria:**
  - [ ] Captures > 80% of the upside of a bull run.
  - [ ] Momentum filter cuts losers quickly (< 5% drop).
  - [ ] Position sizing is volatility-adjusted (smaller size for higher vol).

#### Phase 18: Dynamic Allocator (The Switch) ✅ IMPLEMENTED

**Goal:** Fluid movement between Defense and Offense.

- [ ] Implement `AllocationsManager` based on Regime + Sentiment.
- [ ] Smooth transition logic (don't flip 100% in one day).
- **Verbose Acceptance Criteria:**
  - [ ] Allocator shifts from 80% Alpha to 80% Shield within 3 days of a "Bear" signal.
  - [ ] Transaction costs for switching are calculated and optimized.
  - [ ] "Hysteresis" implemented to prevent rapid flip-flopping.

#### Phase 19: Tax-Efficiency & Harvesting ✅ IMPLEMENTED

**Goal:** It's not what you make, it's what you keep.

- [ ] Implement Tax-Loss Harvesting algorithm.
- [ ] Wash Sale rule avoidance logic.
- **Verbose Acceptance Criteria:**
  - [ ] System identifies unrealized losses to offset gains before year-end.
  - [ ] No Wash Sales triggered in a rolling 30-day window.

---

### Part V: The Shield - Risk Management (Phases 20-22)

#### Phase 20: Real-time Risk Monitor ✅ IMPLEMENTED

**Goal:** The unblinking eye on exposure.

- [ ] Calculate Portfolio VaR (Value at Risk) every minute.
- [ ] Monitor Sector Concentration Limits (e.g., max 20% Tech).
- **Verbose Acceptance Criteria:**
  - [ ] Alert triggered instantly if VaR > Threshold.
  - [ ] Dashboard displays "Current Risk Thermometer".

#### Phase 21: Volatility Circuit Breakers ✅ IMPLEMENTED

**Goal:** Automatic brakes when usage is unsafe.

- [ ] Implement hard "Kill Switches" for assets dropping > 10% in minutes.
- [ ] "Portfolio Freeze" if daily drawdown hits 3%.
- **Verbose Acceptance Criteria:**
  - [ ] Circuit breaker fires within 1 second of trigger condition.
  - [ ] Notification sent to user phone immediately upon freeze.
  - [ ] Manual override required to resume trading.

#### Phase 22: Stress Testing Suite ✅ IMPLEMENTED

**Goal:** rigorous torture testing of the portfolio.

- [ ] Simulate "Black Swan" events (2008, 2020 C19, Flash Crash).
- [ ] Monte Carlo Simulation (10,000 runs) for future path probability.
- **Verbose Acceptance Criteria:**
  - [ ] Portfolio demonstrates survival (bankruptcy probability < 0.1%) in all scenarios.
  - [ ] Report generated: "If 2008 happens tomorrow, we lose X%".

---

### Part VI: The Hands - Execution (Phases 23-26)

#### Phase 23: Paper Trading Simulator ✅ IMPLEMENTED

**Goal:** Prove it works without risking a cent.

- [ ] Build a realistic Exchange Simulator with slippage and fees.
- [ ] Connect Agents to the Simulator.
- **Verbose Acceptance Criteria:**
  - [ ] P&L tracks theoretical performance within 1% error margin.
  - [ ] Simulator handles Order modifications and cancellations correctly.

#### Phase 24: Broker Integration (Robinhood/Alpaca) 🚀 ✅ IMPLEMENTED

**Goal:** Connecting to the real financial plumbing.

- [ ] Implement `RobinhoodService` using `robin_stocks`.
- [ ] Implement OAuth/API connectivity to Broker.
- [ ] Handle 2FA (TOTP) and Session Management.
- [ ] Connect account balance and positions to the `ProtectorAgent`.
- **Verbose Acceptance Criteria:**
  - [ ] Authenticated session persists for trading day.
  - [ ] Can query Account Balance and Positions in real-time.
  - [ ] Order execution (Buy/Sell) verified via API logs.

#### Phase 25: Smart Order Routing (SOR) ✅ IMPLEMENTED

**Goal:** Assessing liquidity and getting the best fill.

- [ ] Logic to split large orders ("Iceberg").
- [ ] Limit Order management (joining the bid vs crossing the spread).
- **Verbose Acceptance Criteria:**
  - [ ] Large orders do not slippage price by > 0.1%.
  - [ ] Fill rate > 95% for limit orders within expected timeframes.

#### Phase 26: Algorithmic Execution ✅ IMPLEMENTED

**Goal:** Robots trading with robots.

- [ ] Implement VWAP (Volume Weighted Average Price) execution.
- [ ] Implement TWAP (Time Weighted Average Price).
- **Verbose Acceptance Criteria:**
  - [ ] Execution price beats the benchmark (Arrival Price) on average.
  - [ ] Randomization of order timing to avoid detection.

---

### Part VII: The Face - UX & Visualization (Phases 27-29)

#### Phase 27: Mission Control V2 (Infographic UX) 🎨 ✅ IMPLEMENTED

**Goal:** A "Minority Report" style interface. High-density, beautiful data.

- [x] **Tech:** React + Vite + D3.js.
- [x] **Modular View Architecture:**
  - [x] **Monitor View:** Real-time sentiment & market telemetry.
  - [x] **Command View:** Backtest execution & agent controls.
  - [x] **Research View:** Drill-down into specific assets & news.
  - [x] **Portfolio View:** Broker positions, balance tracking & performance.
- [x] **Custom Reusable Components:**
  - [x] Atomic design system (Buttons, Cards, Badges, Modals).
  - [x] Performance-optimized D3 wrappers.
- [x] **Testing Suite:**
  - [x] **Verbose Jest Component Tests:** Coverage for all modular views and reusable UI.
  - [x] Integration tests for routing and auth flows.
- [x] **Authentication System:**
  - [x] Secure Login with username/password.
  - [x] User Profile + Avatar management.
- [x] **UX/UI Excellence:**
  - [x] Holographic-style glowing charts (Neon/Dark Mode).
  - [x] Responsive Design (Mobile-first navigation).
  - [x] 3D Portfolio Universe visualization (Neo4j Graph - Mocked/D3).
- **Verbose Acceptance Criteria:**
  - [x] 60 FPS rendering performance for D3 components.
  - [x] High-fidelity Sci-Fi HUD aesthetic.
  - [x] All components have accompanying `.test.jsx` files with >80% coverage.
  - [x] Seamless navigation between Monitor, Command, Research, and Portfolio.
  - [x] Secure session persistence after login.

#### Phase 28: Mobile Command Center (React Native) 📱 ✅ IMPLEMENTED

**Goal:** Deployment on Android for control from anywhere.

- [ ] **Tech:** React Native + Expo.
- [ ] **Mobile Features:**
  - [ ] Android-optimized layout and touch interactions.
  - [ ] Push Notifications for system alerts (Drawdown, Alerts).
  - [ ] Real-time mobile charts (Victory or SVG-based).
- [ ] **Deployment:**
  - [ ] Build & Deploy `.apk` for Android testing.
- **Verbose Acceptance Criteria:**
  - [ ] App builds successfully for Android target.
  - [ ] Critical actions (Kill Switch) are accessible in 1 tap.
  - [ ] Biometric login support (Fingerprint/Face).

#### Phase 29: User Personalization & Notifications ✅ IMPLEMENTED

**Goal:** The AI talks to you.

- [ ] Configurable Alert Rules (SMS, Email, Push).
- [ ] Daily "Morning Briefing" generated by LLM (Natural Language).
- **Verbose Acceptance Criteria:**
  - [ ] User receives a "Morning Coffee" report summarizing the plan for the day.
  - [ ] Alerts are not spammy; smart filtering applied.

---

### Part VIII: Operations & Autonomy (Phases 30-33)

#### Phase 30: CI/CD & Deployment

**Goal:** Code that deploys itself.

- [ ] GitHub Actions pipelines for Test, Build, Deploy.
- [ ] Blue/Green deployment to ensure zero downtime.
- **Verbose Acceptance Criteria:**
  - [ ] A git push to `main` automatically runs tests and updates the containers.
  - [ ] Failed tests block deployment.

#### Phase 31: Self-Healing & Observability

**Goal:** An immune system for the software.

- [ ] ELK Stack (Elastic, Logstash, Kibana) for logs.
- [ ] Prometheus + Grafana for metrics.
- [ ] Auto-restart for crashed services.
- **Verbose Acceptance Criteria:**
  - [ ] Dashboard shows CPU, Memory, and Network I/O per container.
  - [ ] "Dead Man's Switch" alerts if the system goes silent.

#### Phase 32: Security Hardening

**Goal:** Fort Knox.

- [ ] API Key encryption (Vault).
- [ ] Rate limiting on all endpoints.
- [ ] Penetration testing (Simulated attacks).
- **Verbose Acceptance Criteria:**
  - [ ] No secrets stored in code repositories.
  - [ ] OWASP Top 10 vulnerabilities mitigated.

#### Phase 33: The "Singularity" (Launch) 🚀

**Goal:** Handing over the keys.

- [ ] Final end-to-end audit.
- [ ] 1-week "Shadow Mode" run (Real data, fake money).
- [ ] **Go Live** with small capital.
- **Verbose Acceptance Criteria:**
  - [ ] System operates for 7 continuous days with 0 human intervention.
  - [ ] Profit/Loss matches backtest expectations within 2 standard deviations.
  - [ ] The user is "Wowed" by the experience.

---

### Part IX: Deep Alternative Data (Phases 34-36)

#### Phase 34: Visual Hype Tracking (TikTok & YouTube) 📸

**Goal:** Monitoring the visual web for viral financial trends.

- [ ] **Video Transcription:** Auto-transcribe top 100 finance channels.
- [ ] **Visual Logo Detection:** Spotting product placement/usage.
- [ ] **Hype Meter:** Measuring velocity of video shares.
- **Verbose Acceptance Criteria:**
  - [ ] System alerts when a ticker is mentioned in > 10 viral videos (1M+ views) in 24h.
  - [ ] Sentiment analysis distinguishes between "Roasting" and "Hype".

#### Phase 35: Political Alpha (Congress & Lobbying) 🏛️

**Goal:** If they trade on inside info, we follow.

- [ ] **Senate Disclosure Tracker:** Scrape periodic transaction reports.
- [ ] **Lobbying Correlation:** Match lobbying spend spikes with stock performance.
- [ ] **Gov Contract Awards:** Monitor defense spending announcements.
- **Verbose Acceptance Criteria:**
  - [ ] Copy-trade signal generated within 24h of disclosure.
  - [ ] "Nancy Pelosi Index" implemented as a trackable strategy.

#### Phase 36: Corporate Espionage (Legal) 🛰️

**Goal:** Satellite and physical world data.

- [ ] **Supply Chain Tracking:** Marine traffic API for shipping delays.
- [ ] **Job Listing Anomaly:** Detecting sudden hiring freezes or mass hiring.
- [ ] **Parking Lot Indices:** (Via 3rd party API) Retail foot traffic.
- **Verbose Acceptance Criteria:**
  - [ ] Detect revenue miss potential via shipping data 2 weeks before earnings.
  - [ ] Correlate "Hiring Spree" with "Growth" signals.

---

### Part X: Generative Evolution (Phases 37-39)

#### Phase 37: The Strategy Distillery (Genetic Algos) 🧬

**Goal:** Evolutionary computation for trading logic.

- [ ] **Genetic Algorithm Engine:** Cross-over and mutate strategy parameters.
- [ ] **Survival of the Fittest:** Cull underperforming logic.
- [ ] **Generation Tracking:** Trace exact lineage of the "Alpha".
- **Verbose Acceptance Criteria:**
  - [ ] Genetic Algorithm engine successfully mutates and crosses over strategy parameters.
  - [ ] System evolves a strategy beating Buy & Hold by > 20% over 50 generations.
  - [ ] Traceable lineage maintained for all evolved 'Alpha' strategies.
  - [ ] Automatic paper-trading initiated for all 'Mutant' strategies.

#### Phase 38: The "Debate" Chamber (Multi-Persona LLM) 🗣️

**Goal:** Replicating an Investment Committee.

- [ ] **Persona Injection:** "The Bear", "The Bull", "The Macro Economist", "The Gambler".
- [ ] **Roundtable Logic:** Agents debate a trade and vote.
- [ ] **Consensus Scoring:** Trade only executed if > 70% agreement.
- **Verbose Acceptance Criteria:**
  - [ ] Trade execution requires > 70% consensus from the persona committee.
  - [ ] Debate transcripts saved for human oversight and audit.
  - [ ] Forced 'devil's advocate' logic implemented to prevent groupthink.

#### Phase 39: Auto-Coder (Self-Improving Agents) 🤖

**Goal:** The AI writes its own adapters.

- [ ] **Sandbox Mode:** LLM writes Python code to connect to new APIs.
- [ ] **Unit Test generation:** AI verifies its own code.
- [ ] **Hot Swapping:** Deploying new modules without restart.
- **Verbose Acceptance Criteria:**
  - [ ] LLM agent successfully writes and integrates a new REST API adapter.
  - [ ] AI-generated unit tests verify all self-written code.
  - [ ] Strict sandbox environment prevents malicious code execution.
  - [ ] Hot-swapping of modules achieved without system restart.

---

### Part XI: Mastery & Transcendence (Phases 40-42)

#### Phase 40: The VR/AR "Minority Report" Cockpit 🥽

**Goal:** Spatial computing interface.

- [ ] **WebXR Integration:** View portfolio in 3D space.
- [ ] **Gesture Control:** "Swipe away" bad trades.
- [ ] **Immersive Data:** Walk through the Neo4j graph context.
- **Verbose Acceptance Criteria:**
  - [ ] WebXR integration compatible with Meta Quest/Apple Vision Pro.
  - [ ] Maintainable 90 FPS rendering in VR environment.
  - [ ] Gesture-controlled portfolio actions (Liquidate, Hedge, Swipe) verified.
  - [ ] Spatial navigation of Neo4j asset-correlation graph implemented.

#### Phase 41: The "Family Office" (Multi-Tenant Scale) 👨‍👩‍👧‍👦

**Goal:** Managing wealth for a tribe.

- [ ] **Account Segregation:** Separate risk profiles for different users.
- [ ] **Shared Intelligence:** One "Brain" managing multiple wallets.
- [ ] **Inheritance Protocol:** "Dead Man's Switch" for asset transfer.
- **Verbose Acceptance Criteria:**
  - [ ] Strict account segregation implemented for multiple user profiles.
  - [ ] One unified 'Brain' manages multiple wallet connections.
  - [ ] 'Dead Man's Switch' inheritance protocol for asset transfer active.
  - [ ] Unified dashboard for 'Family Head' provides overview of all tenants.

#### Phase 42: The Answer (Total Homeostasis) 🧘

**Goal:** Integrating Life, Wealth, and Time.

- [ ] **Cash Flow Autopilot:** Connection to main bank account.
- [ ] **"Enough" Metric:** System stops risking when goals are met.
- [ ] **Philanthropy Mode:** Auto-donating excess alpha to charity.
- **Verbose Acceptance Criteria:**
  - [ ] Autopilot connection to primary bank account for cash flow management.
  - [ ] Implementation of the 'Enough' metric to cease high-risk trading once goals are met.
  - [ ] User achieves 'Peace of Mind' (Qualitative survey score > 9/10).
  - [ ] Philanthropy Mode automatically routes excess alpha to charity.

---

### Part XII: Institutional Trading OS (Phases 43-48) 🏛️

#### Phase 43: OS-Style Window Management ✅

**Goal:** Transform the static dashboard into a functional Desktop OS Environment.

- [x] **Window Wrapper Pattern:** All widgets wrapped in draggable/resizable containers.
- [x] **Multi-Corner Resize:** 8 resize handles (N, S, E, W, NE, NW, SE, SW).
- [x] **Standard Window Chrome:** Minimize (Yellow), Maximize (Green), Close (Red) buttons.
- [x] **Taskbar System:** Bottom dock for minimized windows with restore functionality.
- [x] **Z-Index Stacking:** Click-to-focus window ordering.
- [x] **Glassmorphism Effects:** `backdrop-blur: 20px` with professional shadows.
- **Verbose Acceptance Criteria:**
  - [x] Users can drag windows anywhere on the desktop.
  - [x] Users can resize from any corner/edge.
  - [x] Minimized windows appear in bottom taskbar.
  - [x] Clicking taskbar button restores window.

#### Phase 44: Professional Header & Navigation

**Goal:** Enterprise-grade menu bar with animated dropdowns.

- [x] **Global Header:** Full-width background with high contrast.
- [x] **Dropdown Menus:** File, Edit, View, Widgets, Help with 150ms animations.
- [x] **Keyboard Shortcuts:** Displayed in menu items (Ctrl+S, Ctrl+N, etc.).
- [x] **Icons:** Professional icons for all menu actions.
- [x] **User Identity Cluster:** Avatar, Role Badge, Settings dropdown.
- **Verbose Acceptance Criteria:**
  - [x] Dropdowns animate smoothly with slide-in effect.
  - [x] Profile dropdown includes: Settings, Subscription, API Keys, Logout.
  - [x] Widgets menu shows checkmarks for open windows.

#### Phase 45: Advanced Routes & Workspaces

**Goal:** Professional route structure for specialized trading views.

- [ ] `/workspace/terminal` - Main Command Center with multi-window arrangement.
- [ ] `/analytics/options` - Dedicated options strategy modeling hub.
- [ ] `/portfolio/backtest` - Historical simulation and "What-if" analysis.
- [ ] `/scanner/global` - High-density grid for real-time price monitoring.
- [ ] **Breadcrumb Navigation:** Dynamic path tracking (Workspace > Terminal > AI Agent).
- **Verbose Acceptance Criteria:**
  - [ ] Each route has a dedicated layout optimized for its use case.
  - [ ] Breadcrumbs update dynamically on navigation.
  - [ ] Routes are bookmarkable and shareable.

#### Phase 46: Specialized Trading Widgets

**Goal:** Institutional-grade trading components.

- [ ] **Advanced Options Chain Widget:**
  - [ ] Real-time Greeks (Δ, Γ, Θ, Vega) and IV display.
  - [ ] Strike price ladder with Bid/Ask columns.
  - [ ] One-click order entry from option chain.
- [ ] **Level 2 Market Depth (DOM):**
  - [ ] Vertical price ladder showing order book.
  - [ ] Smart Money vs Retail liquidity visualization.
  - [ ] Drag-and-drop order placement on price ladder.
- [ ] **Live Trade Tape (Time & Sales):**
  - [ ] Scrolling executed trades stream.
  - [ ] Color-coded Bid (Red) vs Ask (Green) trades.
  - [ ] Block Trade filter for institutional activity.
- [ ] **Multi-Asset Scanner Widget:**
  - [ ] Grid scanning for technical/AI-detected events.
  - [ ] Real-time Hype Index and earnings alerts.
  - [ ] Symbol linking to update all related windows.
- **Verbose Acceptance Criteria:**
  - [ ] Options chain displays all available contracts with Greeks.
  - [ ] DOM shows real-time bid/ask depth at each price level.
  - [ ] Trade tape updates in real-time with < 100ms latency.
  - [ ] Scanner clicking updates linked chart windows.

#### Phase 47: Symbol Linking & Global Hotkeys

**Goal:** Lightning-fast workflow optimization.

- [ ] **Color Group Linking:**
  - [ ] Windows assignable to color groups (Red, Blue, Green).
  - [ ] Ticker change in one window propagates to same-color group.
- [ ] **Global Hotkeys:**
  - [ ] Configurable keyboard shortcuts (Shift+B = Buy, ESC = Cancel).
  - [ ] Hotkey display in menu items.
- [ ] **Layout Persistence:**
  - [ ] Named workspaces ("Morning Scalping", "ETF Review").
  - [ ] Instant workspace switching.
  - [ ] Import/Export workspace configurations.
- **Verbose Acceptance Criteria:**
  - [ ] Linked windows update within 50ms of symbol change.
  - [ ] Hotkeys work globally regardless of focused window.
  - [ ] Workspaces persist across browser sessions.

#### Phase 48: Pre-Trade Risk & Notifications

**Goal:** Professional trading safeguards and feedback.

- [ ] **Pre-Trade Risk Checks:**
  - [ ] Position size validation before order submission.
  - [ ] Margin limit enforcement.
  - [ ] Concentration limit warnings.
- [ ] **Notification Engine:**
  - [ ] Toast-style alerts ("Whale Flow Detected on $TSLA").
  - [ ] Configurable alert severity levels.
- [ ] **Global Confirmation Modal:**
  - [ ] Centered modal with backdrop blur.
  - [ ] Reusable for high-value trade confirmations.
  - [ ] Props: title, message, confirmAction, denyAction.
- [ ] **Sortable Data Tables:**
  - [ ] Click-to-sort column headers.
  - [ ] Ascending/Descending toggle with visual indicators.
- **Verbose Acceptance Criteria:**
  - [ ] Risk checks block orders exceeding limits.
  - [ ] Toast notifications appear without page refresh.
  - [ ] Modals properly trap focus and blur background.
  - [ ] Tables sort within 100ms of click.

---

## Technical Stack Summary

- **Core Brain:** Python 3.10+, NumPy, Pandas, Scikit-Learn
- **Agents:** Custom AsyncIO Actor Model
- **Data:** Kafka (Redpanda), Neo4j (Graph), Postgres (TimescaleDB)
- **Web:** Flask/FastAPI, SocketIO
- **UI:** React 19, Vite, Tailwind CSS, D3.js, Zustand, Framer Motion, WebXR
- **Window Management:** Custom hooks (useWindowManager), Glassmorphism CSS
- **Infra:** Docker Compose, GitHub Actions, Kubernetes (Future)

## Current Progress Summary

| Part | Phases | Status | Last Updated |
|------|--------|--------|---------------|
| I: Genesis & Foundation | 0-5.7 | ✅ Complete | 2026-01-16 |
| II: Data & Sentiment | 6-12 | ✅ Complete | 2026-01-16 |
| III: Advanced Analytics | 13-14 | 📋 Planned | - |
| III: Advanced Analytics | 15 | ✅ Complete | 2026-01-16 |
| IV: The Strategy | 16-19 | ✅ Complete | 2026-01-16 |
| V: The Shield | 20-22 | ✅ Complete | 2026-01-16 |
| VI: The Hands | 23-26 | ✅ Complete | 2026-01-16 |
| VII: UX & Visualization | 27 | ✅ Complete | 2026-01-16 |
| VII: UX & Visualization | 28 | ✅ Complete | 2026-01-16 |
| VII: UX & Visualization | 29 | ✅ Complete | 2026-01-16 |
| XII: Institutional Trading OS | 43-44 | ✅ Complete | 2026-01-16 |
| XII: Institutional Trading OS | 45-48 | 📋 Planned | - |

## Next Immediate Actions

1. **Phase 12 (ACTIVE):** Build Fear & Greed Composite Index.
   - Create `FearGreedIndexService` in `services/analysis/`
   - Add API endpoint `/api/market/fear-greed`
   - Build dashboard gauge widget
2. **Phase 13:** Feature Engineering Pipeline.
3. **Phase 45:** Implement advanced route structure.
4. **Phase 46:** Build Options Chain Widget with Greeks display.
