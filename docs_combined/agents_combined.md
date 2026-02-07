# Agents - Combined Documentation
Auto-generated on: Sat 02/07/2026 07:18 AM

---

## Source: architect\lifecycle_modeler.md

# LifeCycle Modeler Agent (`architect/architect_agents.py`)

## Description
The `LifeCycleModelerAgent` (Agent 7.1) is responsible for long-term financial planning and multi-decade wealth projection. It helps the user model the path to Financial Independence (FI) and retirement.

## Role in Department
Acts as the "Strategic Visionary" in the Architect department, focusing on macro-level wealth goals rather than short-term trades.

## Input & Output
- **Input**: Net worth, current age, retirement target age, monthly savings rate, and expected annual returns.
- **Output**: Detailed projection data including year-over-year wealth accumulation, "Dead Simple" FI status, and estimated retirement year.

## Integration & Logic
- **Simulation**: Uses compound interest models to simulate financial health over 30-50 year horizons.
- **Goal Tracking**: Emits status updates comparing current progress against the "Retirement Goal" threshold.
- **Departmental Flow**: Provides the long-term context that informs the `Strategist`'s risk tolerance.


---

## Source: auditor\auditor_agents.md

# Auditor Department Agents (`auditor/auditor_agents.py`)

This folder contains agents responsible for verifying the integrity of the system's financial and decision-making processes.

## Reconciliation Bot Agent (Agent 9.5)
### Description
The `ReconciliationBotAgent` is an automated accountant that ensures the internal ledger precisely matches the reality of external bank balances.

### Role
Acts as the "Truth Verifier" for all cash positions.

### Integration
- **Treasury Service**: Fetches real-time bank balances.
- **Ledger System**: Compares balances against Postgres entries.
- **Alerting**: Discrepancies > $0.05 trigger an immediate high-priority audit event.

---

## Mistake Classifier Agent (Agent 9.6)
### Description
The `MistakeClassifierAgent` performs "Post-Mortem" analysis on losing trades to determine if they were the result of a bad strategy or emotional "Tilt."

### Role
Acts as the "Psychologist" and "Compliance Officer" for the trading engine.

### Integration
- **Trade History**: Analyzes closed positions with negative P&L.
- **Scoring**: Assigns a "Tilt Score" (0.0 - 1.0). High tilt scores result in automatic circuit breaker triggers by the `ProtectorAgent`.


---

## Source: autocoder_agent.md

# Autocoder Agent (`autocoder_agent.py`)

## Description
The `AutocoderAgent` is an autonomous code generation and execution agent. It translates natural language prompts into Python code, validates the code for security, and executes it in a sandboxed environment.

## Role in Department
This agent acts as a "Technical specialist" that can be invoked by other agents to perform data analysis, strategy development, or automation tasks that require custom code.

## Input & Output
- **Input**: Natural language prompt (e.g., "Analyze the volatility of AAPL over the last 30 days") and optional context variables.
- **Output**: A dictionary containing the generated code, execution results (stdout/stderr), and any errors encountered.

## Pipelines & Integration
- **LLM**: Uses `gpt-4o` for high-fidelity code generation.
- **Sandbox**: Integrates with `SandboxExecutor` which uses AST parsing to detect dangerous operations (like `os.system`) and executes code in an isolated subprocess.
- **Event Bus**: Listens for `code_generation_request` events on the Kafka stream.

## Security Features
- **AST Validation**: Prevents execution of dangerous functions and blocked imports.
- **Subprocess Isolation**: Code runs in a temporary environment with a set timeout.
- **Whitelist/Blacklist**: Strict control over available libraries.


---

## Source: backtest_agent.md

# Backtest Agent (`backtest_agent.py`)

## Description
The `BacktestAgent` is the primary validator for trading strategies. It runs historical simulations on OHLCV data to calculate performance metrics and ensure a strategy is viable before deployment.

## Role in Department
It serves as the final barrier in the Quant Lab (Strategist department), providing the "K-Factor" validation required by the Sovereign OS roadmap.

## Input & Output
- **Input**: Strategy definition, date range, initial capital, and ticker symbol.
- **Output**: `BacktestResult` including Sharpe Ratio, Max Drawdown, Win Rate, and the critical `k_factor`.

## Pipelines & Integration
- **Database**: Pulls historical time-series data from Postgres.
- **Monte Carlo**: Provides data for k-factor validation (k > 1.05 required for deployment).
- **Execution Workflow**: Signals from the `Strategist` department are routed here for historical verification.

## Key Metrics
- **K-Factor**: A multiplier representing profit expectancy. Sustainable growth requires `k > 1.0`.
- **Max Drawdown**: Crucial for ensuring the strategy doesn't violate tail-risk constraints.


---

## Source: base_agent.md

# Base Agent (`base_agent.py`)

## Description
The `BaseAgent` is the abstract base class (ABC) for all agents within the Sovereign OS. It defines the mandatory interface and provides core functionalities such as state management, observability (tracing), LLM integration, and tool execution.

## Role in Department
As an abstract base, it doesn't belong to a specific department but serves as the DNA for every agent in the system. It ensures that all agents follow the same lifecycle (start/stop/health) and communication protocols.

## Input & Output
- **Input**: `Dict[str, Any]` (Typically a Kafka event payload or a direct invocation request).
- **Output**: `Optional[Dict[str, Any]]` (Response or action to be taken).

## Pipelines & Integration
- **State Management**: Integrates with `StateManagerService` (Redis-backed FSM) to persist and restore agent states.
- **Observability**: Uses `SocketManager` for live HUD updates and `DatabaseManager` for persistent audit logs of every action.
- **LLM Routing**: Connects to `ModelManager` to provide LLM-agnostic completion capabilities.
- **Tool Execution**: Integrates with `ToolRegistry` to execute specialized tools with Pydantic validation and sector isolation checks.

## Key Methods
- `transition_to(new_state, reason)`: Managed state transitions with FSM validation.
- `emit_trace(label, content, type, metadata)`: Real-time observability and logging.
- `get_completion(prompt, system_message)`: LLM completion interface with caching.
- `execute_tool(tool_name, tool_args)`: Secure tool execution with sector isolation.
- `process_event(event)`: Abstract method to be implemented by child agents.


---

## Source: chaos_agent.md

# Chaos Agent (`chaos_agent.py`)

## Description
The `ChaosAgent` is the "Joker" of the system, responsible for resilience testing. It proactively injects faults into the Sovereign OS to verify that high-availability and self-healing mechanisms are functional.

## Role in Department
Acts as a security and infrastructure auditor, simulating real-world failures to ensure the "Sovereign Kernel" can survive hardware or network instability.

## Input & Output
- **Input**: Stress test triggers (e.g., `start_stress_test`).
- **Output**: Trace events indicating the type of fault injected and the system's reaction.

## Capabilities
- **Latency Injection**: Simulates network jitter or slow API responses.
- **Consumer Lag**: Mocks Kafka lag to test the `TrafficControllerAgent`'s backpressure logic.
- **Process Termination**: Simulates container crashes (e.g., "killing" an analyst agent) to verify automatic restarts.

## Integration
- **Docker API**: In a production environment, this agent interacts with Docker to kill containers or throttle resources.
- **Observability**: Every "Chaos Event" is traced so engineers can correlate system behavior with the injected fault.


---

## Source: columnist\columnist_agents.md

# Columnist Department Agents (`columnist/columnist_agents.py`)

The Columnist department is the "Intelligence Agency" of the Sovereign OS, responsible for ingestion and sentiment analysis of news, rumors, and catalysts.

## Scraper General Agent (Agent 2.1)
### Description
The `ScraperGeneralAgent` is a high-bandwidth ingestion engine that monitors RSS feeds, Twitter (X), and financial news portals.

### Integration
- **Ticker Extraction**: Automatically identifies mentions of $TICKER symbols in news text.
- **Preprocessing**: Cleans and stores news articles for the `SentimentAnalystAgent`.

---

## Sentiment Analyst Agent (Agent 2.2)
### Description
The `SentimentAnalystAgent` assigns quantitative sentiment scores to news articles.

### Integration
- **Scoring**: Maps articles to a score of -1.0 (Bearish) to +1.0 (Bullish).
- **Pipelines**: Feeds synthesized sentiment scores to the `StackerAgent` for trade weighting.

---

## Anomaly Scout Agent (Agent 2.4)
### Description
The `AnomalyScoutAgent` monitors price feeds for statistical outliers (exceeding 4σ variance).

### Integration
- **Trigger**: High-volatility detections are pushed to the `LayoutMorphologistAgent` to update the user HUD.

---

## Macro Oracle Agent (Agent 2.5)
### Description
The `MacroOracleAgent` analyzes high-level economic indicators such as CPI, GDP, and Fed interest rate decisions.

---

## Catalyst Mapper Agent (Agent 2.6)
### Description
The `CatalystMapperAgent` builds a timeline of upcoming market events (Earnings, FDA approvals, Halvings).

### Integration
- **Neo4j**: Maps catalysts to specific assets in the knowledge graph.


---

## Source: consensus\consensus_agents.md

# Consensus Department Agents (`consensus/`)

The Consensus department manages the multi-agent voting system used to authorize high-value decisions.

## Consensus Engine (`consensus_engine.py`)
### Description
The `ConsensusEngine` evaluates votes from different agents to determine if a proposal has sufficient support to proceed.

### Role
Acts as the "Democracy Matrix" of the Sovereign OS.

### Logic
- **Weighted Voting**: Agents with higher historical accuracy (reputation) or seniority have higher vote weights.
- **Thresholds**: Requires a minimum number of voters and a weighted majority to approve a trade.

---

## Vote Aggregator (`vote_aggregator.py`)
### Description
The `VoteAggregator` is a service that tracks individual agent votes, their justifications (personas), and their weights for any given proposal ID.

### Integration
- **Debate Chamber**: Captures votes emitted during the adversarial debate process.
- **Persistence**: Final vote counts are logged for transparency and future auditing by the `Auditor` department.


---

## Source: conviction_analyzer.md

# Conviction Analyzer Agent (`conviction_analyzer_agent.py`)

## Description
The `ConvictionAnalyzerAgent` is a high-level strategic agent that identifies "Sure Thing" investment opportunities. It looks for fundamental moats, specific catalysts, and market dislocations.

## Role in Department
It acts as the "Architect" of aggressive plays, identifying opportunities that warrant leverage and higher position sizing.

## Input & Output
- **Input**: Symbol, news context, market data, and qualitative indicators (e.g., "technology lead", "government contract").
- **Output**: `ConvictionAnalysis` with a thesis, recommended leverage (up to 2x), and suggested allocation.

## Decision Criteria
- **Moat Detection**: Identifies "Technology Corner" (NVIDIA), "Network Effects" (Visa), and "Regulatory Capture" (PBMs).
- **Catalyst Detection**: Monitors for government contracts, market panic, or misread earnings.
- **Conviction Scoring**: Levels range from LOW to SURE_THING.

## Pipelines & Integration
- **Stacker Agent**: Feeds high-conviction signals to the `StackerAgent` for final trade aggregation.
- **Portfolio Manager**: Recommendations are used to adjust position sizing within the Aggressive vs. Defensive portfolios.


---

## Source: debate_chamber.md

# Debate Chamber Agent (`debate_chamber_agent.py`)

## Description
The `DebateChamberAgent` orchestrates adversarial debates between multiple AI personas (e.g., The Bull vs. The Bear). It synthesizes these arguments to reach a final consensus score for a given ticker or proposal.

## Role in Department
Acts as the central "Conflict Resolution" mechanism, ensuring that every trade is viewed from multiple perspectives before execution.

## Input & Output
- **Input**: Ticker symbol or trade proposal.
- **Output**: Full debate transcript and a consensus summary (Decision: BUY/SELL/HOLD, Confidence Score, Averaged Metrics).

## Integration points
- **Persona Agents**: Leverages specialized Bull and Bear personas to generate reasoning.
- **LLM**: Uses Anthropic's Claude for high-quality dialectical synthesis.
- **Frontend**: Results are stored in the `DebateStore` for visualization in the "Debate Chamber" UI.

## Logic Flow
1. **Request Bull Argument**: Highlights momentum and growth.
2. **Request Bear Argument**: Highlights risk and headwinds.
3. **Moderator Synthesis**: Acts as the judge, weighting arguments and calculating a confidence score.


---

## Source: department_agent.md

# Department Agent (`department_agent.py`)

## Description
The `DepartmentAgent` is a specialized subclass of `BaseAgent` designed to function within a specific department (e.g., "Strategist", "Trader", "Auditor"). It handles domain-specific event routing and uses tailored prompt templates.

## Role in Department
This is the workhorse class for categorized agents. It provides the boilerplate for department-specific behavior, such as updating telemetry and loading specialized prompts from the `agents/prompts/` directory.

## Input & Output
- **Input**: Department-specific events (e.g., `audit.reconcile`) and task payloads.
- **Output**: Telemetry updates and success/error responses from LLM invocations.

## Key Features
- **Prompt Isolation**: Loads system and user prompts specific to the agent's role (e.g., `department_agent_system.txt`).
- **Telemetry**: Automatically publishes status and performance metrics to the department's event topic (e.g., `dept.1.agents`).
- **Agnostic Invocation**: Can be directly invoked for specialized tasks with a standard payload.

## Pipelines & Integration
- **Event Bus**: Extensively uses `EventBusService` to broadcast its status across its department.
- **Prompt Loader**: Connects to the centralized prompt repository for consistency across 84+ agents.


---

## Source: front_office\front_office_agents.md

# Front Office Department Agents (`front_office/front_office_agents.py`)

The Front Office department acts as the "Administrative HQ," managing the CEO's (user's) focus and protecting them from technical and administrative noise.

## Inbox Gatekeeper Agent (Agent 14.1)
### Description
The `InboxGatekeeperAgent` is the digital assistant that triages incoming communications. It ensures that only critical, actionable items reach the user's primary "Heads-Up Display" (HUD).

### Role
Acts as the "Noise Shield" for the CEO.

### Integration
- **Inbox Service**: Syncs with emails and messages.
- **Classification**: Uses LLM-based triage to categorize items as `NOISE`, `ACTIONABLE`, or `FYI`.
- **Urgency Scoring**: Items with an urgency score of 7+ and classified as `ACTIONABLE` are promoted to the HUD.
- **Archiving**: Non-critical items are automatically archived with the triage metadata for later review.


---

## Source: guardian\guardian_agents.md

# Guardian Department Agents (`guardian/guardian_agents.py`)

The Guardian department is the "Financial Fortress," responsible for the automated treasury, cash flow management, and banking security.

## Bill Automator Agent (Agent 6.1)
### Description
The `BillAutomatorAgent` handles the ingestion and processing of utility and operational bills.
- **Acceptance Criteria**: 100% OCR accuracy on amounts and due dates.

### Integration
- **Treasury Service**: Uses specialized PDF OCR to extract line-item data.
- **Staging**: Bills are staged for payment after validation, ensuring no manual data entry.

---

## Flow Master Agent (Agent 6.2)
### Description
The `FlowMasterAgent` manages active cash flow and liquidity across multiple accounts.
- **Threshold**: Executes high-limit ACH sweeps (e.g., when checking > $5,000).

### Role
Acts as the "Liquidity Controller."

---

## Net Worth Auditor Agent (Agent 6.5)
### Description
The `NetWorthAuditorAgent` is the real-time truth-check for the total net worth.

### Integration
- **Reconciliation**: Reconciles the internal ledger with external external balances (discrepancies > $0.05 trigger alerts).
- **SLA**: Audits must be completed within 60 seconds of a sync request.


---

## Source: hunter\hunter_agents.md

# Hunter Department Agents (`hunter/hunter_agents.py`)

The Hunter department focuses on "Venture Growth," identifying private equity opportunities, venture deals, and modeling complex cap-table scenarios.

## Cap-Table Modeler Agent (Agent 10.2)
### Description
The `CapTableModelerAgent` is a specialized financial modeler that analyzes venture deal terms, dilution risks, and exit scenarios.

### Capabilities
- **Waterfall Analysis**: Simulates exit distributions (e.g., a $1B exit) across different share classes (Series A, B, Common).
- **Round Modeling**: Simulates dilution for upcoming funding rounds based on pre-money valuations and new investment amounts.

### Integration
- **Venture Service**: Leverages a deep math engine for price-per-share and post-money valuation calculations.
- **Reporting**: Emits high-fidelity "Dilution Reports" used for investment decision-making.


---

## Source: lawyer\lawyer_agents.md

# Lawyer Department Agents (`lawyer/lawyer_agents.py`)

The Lawyer department is the "Compliance Shield," ensuring that all system actions remain within regulatory and tax-efficient boundaries.

## Wash-Sale Watchdog Agent (Agent 8.1)
### Description
The `WashSaleWatchdogAgent` specifically monitors trade requests for potential IRS "Wash-Sale" rule violations.

### Role
Acts as a "Compliance Gatekeeper" for tax efficiency.

### Logic & Integration
- **Compliance Service**: Audits ticker trade history over the preceding and succeeding 30-day windows.
- **Blocking**: Automatically blocks trades that would trigger a violation, providing a detailed reason to the `ProtectorAgent`.
- **SLA**: Determines compliance status in real-time during the order creation pipeline.


---

## Source: orchestrator\orchestrator_agents.md

# Orchestrator Department Agents (`orchestrator/orchestrator_agents.py`)

The Orchestrator department is the "Sovereign Kernel," the central nervous system that manages communication, security, and the overall system state.

## Synthesizer Agent (Agent 1.1)
### Description
Aggregates activity logs from all 84 agents into a unified "State of the Union" daily briefing.
- **Accuracy**: Briefing totals must match ledger totals to 0.01%.

---

## Command Interpreter Agent (Agent 1.2)
### Description
Translates voice or text commands into structured JSON system calls.
- **Accuracy**: 99% accuracy on entity extraction (tickers, quantities, dates).

---

## Traffic Controller Agent (Agent 1.3)
### Description
The "Kafka Master" that manages message routing and backpressure.
- **Performance**: Maintains Kafka lag < 200ms even during 5k msg/sec spikes.

---

## Layout Morphologist Agent (Agent 1.4)
### Description
Predicatively manages the UI layout based on market events.
- **Trigger**: Automatically switches the HUD to "Trader Mode" within 500ms of high-volatility detection.

---

## Red-Team Sentry Agent (Agent 1.5)
### Description
The internal security officer monitoring for unsafe bytecode or syscalls.
- **Enforcement**: Issues an immediate `SIGKILL` on any agent attempting un-whitelisted `os.system` or `eval` calls.

---

## Context Weaver Agent (Agent 1.6)
### Description
Maintains Redis-based session memory to ensure 100% context injection during agent role-switches.


---

## Source: personas\persona_agents.md

# Persona Agents (`personas/`)

Persona agents are biased AI models that simulate specific market viewpoints. They are used in adversarial debates to challenge or support trade proposals.

## Bull Persona Agent (`bull_agent.py`)
### Description
The `BullAgent` is structurally biased toward long positions. It prioritizes momentum, growth narrative, and impulsive price action.

### Reasoning Style
- Focuses on trend continuation.
- Heavily weights "Buy the Dip" logic and breakout patterns.

---

## Bear Persona Agent (`bear_agent.py`)
### Description
The `BearAgent` is the "Skeptic." It looks for overextension, technical divergence, and macroeconomic headwinds.

### Reasoning Style
- Focuses on risk of reversal.
- Highlights daily resistance levels and overbought indicators (e.g., high RSI).


---

## Source: physicist\physicist_agents.md

# Physicist Department Agents (`physicist/physicist_agents.py`)

The Physicist department is the "Volatility Engine," managing complex mathematical layers of risk, Options Greeks, and tail-risk probability.

## Theta Collector Agent (Agent 5.1)
### Description
Monitors portfolio time-decay (Theta) and harvests yield.
- **SLA**: Daily P&L report must track Theta with <$1.00 variance.

---

## Volatility Surface Mapper Agent (Agent 5.2)
### Description
Generates 3D data meshes for vizualizing Implied Volatility across different strikes and expiries.
- **Performance**: Mesh generation must have <50ms latency.

---

## Delta Hedger Agent (Agent 5.4)
### Description
Calculates net portfolio Delta and stages rebalancing trades.
- **Enforcement**: Stages hedge trades when Delta drift exceeds 10% thresholds.

---

## Black-Scholes Solver Agent (Agent 5.5)
### Description
A dedicated compute agent for high-frequency Black-Scholes calculations (Option pricing and Greeks).

---

## Black-Swan Watcher Agent (Agent 5.6)
### Description
Monitors for "Tail-Risk" and extreme market events using IV heuristics.
- **Risk Levels**: Categorizes risk as NORMAL, ELEVATED, or EXTREME.


---

## Source: protector_agent.md

# Protector Agent (`protector_agent.py`)

## Description
Known as "The Warden," the `ProtectorAgent` is the final gatekeeper for all trade executions. It enforces rigid risk management protocols and the "Prime Directive" of capital preservation.

## Role in Department
Acts as the "Chief Risk Officer" for the entire system. No trade can reach the exchange without the Warden's approval.

## Input & Output
- **Input**: Trade execution requests (`VALIDATE_ORDER`) including amount, current balance, and daily loss meta-data.
- **Output**: `APPROVE` or `REJECT` decision with a clear reason.

## Risk Protocols enforced
- **Circuit Breaker**: Stops all trading if daily loss thresholds are exceeded or if the system detects excessive volatility.
- **1% Rule**: Prevents any single trade from risking more than 1% of the total account equity.
- **Validation**: Integrates with the `RiskManager` service for complex rule evaluation.

## Integration
- **Trader Department**: Sits at the end of the order routing pipeline.
- **Observability**: Emits high-priority traces on any security or risk violation.


---

## Source: research_agent.md

# Research Agent (`research_agent.py`)

## Description
The `ResearchAgent` is responsible for conducting external market research and gathering real-world intelligence using advanced search capabilities.

## Role in Department
Acts as the "Information Scout," providing qualitative data that complements quantitative signals from price scanners.

## Input & Output
- **Input**: Natural language research queries (e.g., "What is the current regulatory outlook for ARM-based chips in China?").
- **Output**: Detailed answers with citations and confidence levels.

## Integration & Strategy
- **Perplexity Client**: Uses the Perplexity API for high-accuracy, real-time web search and citation generation.
- **History Management**: maintains an in-memory history of queries and results to build context for multi-step research missions.
- **Synthesis**: Feeds citations and summaries back to the `Orchestrator` or `ConvictionAnalyzer` for decision support.

## Singleton Pattern
Uses a Singleton pattern to ensure that the `Perplexity` client and research history are consistently managed across the session.


---

## Source: searcher_agent.md

# Searcher Agent (`searcher_agent.py`)

## Description
Known as "The Scout," the `SearcherAgent` traverses the market and the system's internal knowledge graph (Neo4j) to identify high-liquidity paths and emerging trading opportunities.

## Role in Department
Operates as the front-line scanner for the `Trader` and `Strategist` departments, spotting patterns before the high-frequency engines engage.

## Input & Output
- **Input**: Scan triggers (sector, minimum liquidity, correlation thresholds).
- **Output**: A list of scored opportunities including symbols, identified patterns, and correlation data.

## Key Capabilities
- **Neo4j Graph Traversal**: Finds correlations and dependencies between assets (e.g., NVDA -> TSMC -> ASML).
- **Market Scanning**: Integrates with `MarketScannerService` to monitor major trading pairs in real-time.
- **Pattern Recognition**: Uses `PatternRecognition` engine to identify technical or structural market setups.

## Pipelines
- **Opportunity Scorer**: Every identified pattern is scored (0-100), and only those above a quality threshold (typically 50+) are emitted.
- **Stacker Integration**: Emitters results as `SCAN_COMPLETE` events which are picked up by the `StackerAgent`.


---

## Source: sentry\sentry_agents.md

# Sentry Department Agents (`sentry/sentry_agents.py`)

The Sentry department manages physical and digital security, geofencing, and biometric synchronization.

## Travel-Mode Guard Agent (Agent 11.3)
### Description
The `TravelGuardAgent` monitors for device divergence (e.g., your primary workstation vs. your mobile device) and triggers lockouts if security violations are detected.

### Capabilities
- **Geofencing**: Tracks device coordinates (lat/lon) via the `GeofenceService`.
- **Divergence Detection**: Calculates distance between trusted devices.
- **Enforcement**: Triggers a `LOCK_SYSTEM` action if devices diverge beyond a safe proximity threshold.

### Integration
- **Heartbeat Checks**: Validates device proximity in real-time during "Travel Mode."
- **Security Alerts**: Emits high-priority error traces on mismatch detection.


---

## Source: stacker_agent.md

# Stacker Agent (`stacker_agent.py`)

## Description
The `StackerAgent` is the central "Decision Aggregator" of the Sovereign OS. It weighs evidence from multiple disparate sources (Market Scanners, Macro Regimes, Options Flow, Sentiment) and only triggers a trade when a statistical confidence threshold is met.

## Role in Department
It acts as the "Jury" that evaluates the "Evidence" provided by other agents. It is the final decision point before the `ProtectorAgent` validates the risk.

## Aggregation Logic (The Stack)
Weights signals from various sources (defaults):
- **SearcherAgent**: 30%
- **HMM Engine (Macro)**: 35%
- **FFT Engine (Freq)**: 20%
- **Options Flow (Whale Detection)**: 25%
- **ProtectorAgent**: 15% (Negative signals/Risk warnings carry heavy weight)

## Input & Output
- **Input**: `SIGNAL` events, `OPTIONS_FLOW` events, and `MACRO_REGIME` updates.
- **Output**: `TRADE_SIGNAL` when the aggregate confidence exceeds the `CONFIDENCE_THRESHOLD` (typically 0.65).

## Integration & Persistence
- **Neo4j**: Persists Whale Flow and Macro Regimes as nodes in the global knowledge graph to build historical context.
- **Kafka**: Listens for signals across the entire system and emits high-confidence execution calls.


---

## Source: strategist\strategist_agents.md

# Strategist Department Agents (`strategist/strategist_agents.py`)

The Strategist department is the "Quant Lab," where trading strategies are defined, optimized, and stress-tested.

## Backtest Autopilot Agent (Agent 3.1)
### Description
High-performance vectorized backtesting engine using Polars.
- **Benchmark**: Executes a 10-year SMA cross strategy in <2 seconds.

---

## Optimizer Agent (Agent 3.2)
### Description
Runs grid searches and genetic algorithms to find optimal strategy parameters.
- **Performance**: Identifies top 5 parameter sets in <10 seconds.

---

## Correlation Detective Agent (Agent 3.3)
### Description
Builds and maintains the "Correlation Web" (Neo4j), identifying hidden dependencies between assets.

---

## Risk Manager Agent (Agent 3.4)
### Description
Calculates Value at Risk (VaR) and overall portfolio risk metrics.

---

## Alpha Researcher Agent (Agent 3.5)
### Description
Conducts factor analysis and discovers new alpha signals in historical data.

---

## Blueprint Architect Agent (Agent 3.6)
### Description
The visual strategy builder that manages `StrategyBlueprints` and validates them for logical consistency.


---

## Source: trader\trader_agents.md

# Trader Department Agents (`trader/trader_agents.py`)

The Trader department is the "Execution Layer," responsible for order routing, fill tracking, and algorithmic execution.

## Order General Agent (Agent 4.1)
### Description
The supreme commander of order flow, responsible for routing orders to optimal venues (NYSE, NASDAQ, etc.) using Smart Order Routing (SOR).
- **Latency**: SOR routing under 50ms.

---

## Fill Tracker Agent (Agent 4.2)
### Description
Monitors and reconciles all order fills in real-time.
- **Accuracy**: 100% reconciliation against broker records.
- **Positioning**: Updates the system’s net position immediately upon fill.

---

## Algo-Executor Agent (Agent 4.3)
### Description
Executes large orders using algorithmic profiles (TWAP, VWAP, Iceberg) to minimize market impact.

---

## Hedger Agent (Agent 4.4)
### Description
Monitors net portfolio exposure and executes automatic hedging trades (e.g., buying SQQQ if exposure is too long).

---

## Arbitrageur Agent (Agent 4.5)
### Description
Identifies and executes latency or cross-venue arbitrage opportunities.

---

## Market Maker Agent (Agent 4.6)
### Description
Provides two-sided liquidity and manages bid/ask spreads to minimize slippage on internal crossings.


---

