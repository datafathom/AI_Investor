# Agents - Combined Documentation
Auto-generated on: Sun 02/15/2026 03:11 AM

---

## Source: admin\admin_overseer.md

# Admin Overseer (Agent 0.1)

## ID: `admin_overseer`

## Role & Objective
The 'System Administrator'. Provides high-level oversight of all 19 departments and ensures the overall institutional health, security, and performance of the AI Investor OS.

## Logic & Algorithm
- **Departmental Pulse**: Aggregates the `primaryMetric` from all 19 departments to generate a "Total Institutional Health" score.
- **Resource Allocation**: Monitors CPU/Memory/Storage usage across all agents and microservices, triggering "Clean Build" or "Stop Process" commands if thresholds are exceeded.
- **Security Escalation**: Acts as the final authority for the Red Team Sentry and breach alerts, coordinating recovery paths.

## Inputs & Outputs
- **Inputs**:
  - `system_telemetry` (Data): Metrics from all active departments.
- **Outputs**:
  - `admin_status_report` (Dict): High-level system health and critical alerts.

## Acceptance Criteria
- Maintain system-wide uptime of 99.9%.
- Trigger institutional lockdown in < 1 second of a Level 10 breach detection.


---

## Source: architect\goal_priority_arbiter.md

# Goal Priority Arbiter (Agent 2.6)

## ID: `goal_priority_arbiter`

## Role & Objective
The strategic decision-maker. It acts as the final judge of competing financial priorities, determining how surplus capital should be allocated across the user's defined goals.

## Logic & Algorithm
1. **Priority Hierarchy**: Ranks user goals from "Essential" to "Luxury".
2. **Trade-Off Simulation**: Models the impact of prioritizing one goal over another (e.g., "Retiring 2 years early" vs "Buying a luxury car").
3. **Optimality Scoring**: Grades the current savings plan on its mathematical alignment with the user's weighted goals.

## Inputs & Outputs
- **Inputs**:
  - Goal List (Amount & Date)
  - Surplus Monthly Cash Flow
- **Outputs**:
  - Goal Alignment Score
  - Trade-Off Impact Map

## Acceptance Criteria
- Trade-off analysis must complete in under 500ms to allow interactive "What-If" sliders in the GUI.
- The arbiter must flag any "Essential" goals that are at risk based on the current burn rate.


---

## Source: architect\inflation_architect.md

# Inflation Architect (Agent 2.4)

## ID: `inflation_architect`

## Role & Objective
The "Real Value" validator. It ensures the system never treats future currency as equal to current currency. Every projection in the Sovereign OS is run through the Inflation Architect to show the user their actual future purchasing power.

## Logic & Algorithm
1. **Live Data Ingestion**: Constant monitoring of CPI (Consumer Price Index) and PCE (Personal Consumption Expenditures).
2. **Discounting Engine**: Applies compounding inflation rates to all future cash flows.
3. **GUI Sync**: Provides a global "Real vs Nominal" toggle for all financial charts.

## Inputs & Outputs
- **Inputs**:
  - Future Nominal Values
  - External Inflation Feeds
- **Outputs**:
  - Current Purchasing Power Equivalent (Real Dollars)

## Acceptance Criteria
- Inflation adjustments must match the latest government-reported CPI data within 24 hours of release.
- Real-dollar conversions must be applied to 100% of projections exceeding a 12-month horizon.


---

## Source: architect\inheritance_logic.md

# Inheritance Logic (Agent 2.3)

## ID: `inheritance_logic`

## Role & Objective
The legacy safeguard. It manages the complex rules governing wealth transfer to beneficiaries, ensuring the system's long-term plan is resilient to probate and estate tax liabilities.

## Logic & Algorithm
1. **Beneficiary Sequencing**: Monitors and validates heir percentages across all assets.
2. **Tax Liability Simulation**: Estimates potential estate taxes based on current jurisdictional laws.
3. **Gap Detection**: Identifies assets with missing or outdated beneficiary designations.

## Inputs & Outputs
- **Inputs**:
  - Estate Plan (Percentage Splits)
  - Asset Valuations
- **Outputs**:
  - Legacy Readiness Score (0-100)
  - Beneficiary Gap Report

## Acceptance Criteria
- 100% of assets must be mapped to at least one primary beneficiary.
- Estate tax estimates must be updated annually or upon major legislative changes.


---

## Source: architect\life_cycle_modeler.md

# Life-Cycle Modeler (Agent 2.1)

## ID: `life_cycle_modeler`

## Role & Objective
The "North Star" of the Sovereign OS. The Life-Cycle Modeler is responsible for long-term financial forecasting and determining the exact moment of Financial Independence (FI). It models wealth accumulation over a 40-50 year horizon.

## Logic & Algorithm
1. **Simulation Engine**: Uses the `LifeCycleService` to run deterministic and Monte Carlo simulations of net worth growth.
2. **Burn Rate Analysis**: Factors in inflation-adjusted living expenses.
3. **Success Rate Calculation**: Determines the probability that the current investment strategy will sustain the user through retirement without depleting the principal.

## Inputs & Outputs
- **Inputs**:
  - Current Net Worth
  - Monthly Savings & Burn Rate
  - Expected Portfolio Return
  - Inflation Assumptions
- **Outputs**:
  - FI Year & Age
  - Portfolio Success Rate (%)

## Acceptance Criteria
- FI projections must update in under 1 second during live parameter adjustments.
- Monte Carlo simulations must run at least 1,000 iterations for statistical significance.


---

## Source: architect\real_estate_amortizer.md

# Real Estate Amortizer (Agent 2.5)

## ID: `real_estate_amortizer`

## Role & Objective
The property debt specialist. It manages the intricate mathematics of real estate leverage, tracking equity growth, mortgage amortization, and rental yield.

## Logic & Algorithm
1. **Amortization Modeling**: Tracks the exact split of principal vs interest for all property debt.
2. **Equity Curve Generation**: Maps future equity build-up based on scheduled payments and regional appreciation.
3. **IRR Calculation**: Determines the Internal Rate of Return for properties including leverage impacts.

## Inputs & Outputs
- **Inputs**:
  - Mortgage Terms (Principal, Rate, Length)
  - Current Property Appraisals
  - Rental Cash Flow Data
- **Outputs**:
  - Equity Build-up Curve
  - Cash-on-Cash Return Metrics

## Acceptance Criteria
- Principal/Interest splits must be accurate to the cent compared to official bank statements.
- Equity projections must include at least three scenarios (Bear, Base, Bull appreciation).


---

## Source: architect\stacker_agent.md

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

## Source: architect\tax_location_optimizer.md

# Tax Location Optimizer (Agent 2.2)

## ID: `tax_location_optimizer`

## Role & Objective
The efficiency engine for the portfolio. It determines the most tax-efficient placement of assets across Taxable (Brokerage), Tax-Deferred (401k/IRA), and Tax-Exempt (Roth) accounts to maximize after-tax wealth.

## Logic & Algorithm
1. **Asset Classification**: Tags every asset as high-yield (tax-heavy) or growth-oriented (tax-light).
2. **Account Matching**: Maps high-tax assets (REITs, Corporate Bonds) to tax-advantaged accounts.
3. **Alpha Estimation**: Calculates the "Tax Alpha" or additional return generated solely through optimized placement.

## Inputs & Outputs
- **Inputs**:
  - Account Map (Tax Status per ID)
  - Asset List (Yield & Growth projections)
  - User Tax Bracket
- **Outputs**:
  - Proposed Asset Swaps
  - Estimated Annual Tax Savings (USD)

## Acceptance Criteria
- Tax Alpha optimization must be recalculated within 2 seconds of any major portfolio rebalance.
- Proposed swaps must account for any potential realized gains from the move itself (Wash-sale avoidance).


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

## Source: auditor\behavioral_analyst.md

# Behavioral Analyst (Agent 12.2)

## ID: `behavioral_analyst`

## Role & Objective
The 'Self-Reflection' engine. Grades the system's performance on rule adherence versus impulsive deviations, ensuring the "Sovereign OS" remains disciplined.

## Logic & Algorithm
- **Variance Audit**: Compares executed trades against the Strategist's "Golden Rules" (e.g., max position size).
- **Rule Grader**: Assigns an "Impulse Score" to any trade that breaks pre-defined logic but was forced through.
- **Sentiment Correlation**: Cross-references the user's "Readiness Score" (from Wellness Sync) with system-driven rule violations.

## Inputs & Outputs
- **Inputs**:
  - `system_configuration` (Rules): The defined trading constraints.
  - `execution_stream` (Data): Chronological list of trade events.
- **Outputs**:
  - `discipline_grade` (A-F): Overall rating of system adherence to policy.

## Acceptance Criteria
- Identify 100% of "Rule Breaking" events within 1 hour of execution.
- Maintain a cumulative "System Integrity" score of > 95%.


---

## Source: auditor\benchmarker.md

# Benchmarker (Agent 12.3)

## ID: `benchmarker`

## Role & Objective
The 'Standard Bearer'. Compares total portfolio performance against external indices like the S&P 500, BTC, or Gold to determine true alpha.

## Logic & Algorithm
- **Time-Weighted Returns**: Calculates the TWR of the total portfolio across all accounts.
- **Relative Performance**: Subtracts index returns from portfolio returns to isolate "Manager Skill" (Alpha).
- **Correlation Mapping**: Identifies if the portfolio is becoming "Too Beta" (moving 1:1 with the market) vs its intended uncorrelated strategy.

## Inputs & Outputs
- **Inputs**:
  - `total_account_equity` (Stream): The current net worth.
  - `market_index_prices` (Stream): Prices for SPY, QQQ, BTC, etc.
- **Outputs**:
  - `alpha_beta_report` (Dict): Relative performance metrics.

## Acceptance Criteria
- Calculate daily relative performance vs standard benchmarks by market close.
- Flag any 5-day period where "Alpha" becomes negative while the market is rising.


---

## Source: auditor\fee_forensic_agent.md

# Fee Forensic Agent (Agent 12.4)

## ID: `fee_forensic_agent`

## Role & Objective
The 'Leakage Finder'. Scans institutional statements for incorrect commission tiering, hidden fees, or "PFOF" (Payment for Order Flow) leakage.

## Logic & Algorithm
- **Commission Audit**: Compares actual fees charged against the brokerage's published "Active Trader" tiered schedule.
- **Hidden Fee Detection**: Identifies "SEC Fees" or "ADR Fees" that weren't disclosed in the pre-trade estimates.
- **Arbitrage Check**: Verifies that the Flow Master's sweeps aren't being offset by excessive transfer fees.

## Inputs & Outputs
- **Inputs**:
  - `brokerage_statements` (PDF/Data): Institutional billing documents.
- **Outputs**:
  - `fee_leakage_report` (float): Total USD lost to excessive or incorrect fees.

## Acceptance Criteria
- Reconcile 100% of trading commissions against the published tier schedule.
- Identify overcharges of > $5 within 30 days for recovery requests.


---

## Source: auditor\mistake_classifier.md

# Mistake Classifier (Agent 12.6)

## ID: `mistake_classifier`

## Role & Objective
The 'Memory Optimizer'. Tags every loss with a specific mistake type for the Historian, turning failures into educational data points.

## Logic & Algorithm
- **Taxonomy Mapping**: Uses ML to categorize losing trades into types: "FOMO", "Faded Trend", "Oversized", "News Front-run", etc.
- **Pattern Learning**: Identifies if a specific "Mistake Type" is recurring more frequently than others.
- **Feedback Loop**: Passes high-frequency mistake patterns to the Data Scientist to retrain the predictive models.

## Inputs & Outputs
- **Inputs**:
  - `realized_trades` (List): Trade outcomes and justifications.
- **Outputs**:
  - `error_taxonomy_tag` (str): The specific mistake classification.

## Acceptance Criteria
- Categorize 100% of realized losses within 24 hours of trade exit.
- Maintain a "Clustering Report" of the top 3 mistake types by dollar impact.


---

## Source: auditor\reconciliation_bot.md

# Reconciliation Bot (Agent 12.5)

## ID: `reconciliation_bot`

## Role & Objective
The 'Ledger Matcher'. Cross-references internal trading logs with institutional brokerage statements to find "Breaks" or discrepancies in shared state.

## Logic & Algorithm
- **Three-Way Match**: Compares the Orchestrator's intent, the Trader's logs, and the Broker's final settlement.
- **Settlement Tracking**: Monitors "T+1" or "T+2" settlement cycles to ensure cash availability for the Flow Master.
- **Discrepancy Resolution**: Flags "Phantom Positions" (stocks the system thinks it owns but the broker doesn't, or vice-versa).

## Inputs & Outputs
- **Inputs**:
  - `internal_ledger` (DB): The system's record of truth.
  - `external_settlement_data` (Stream): The broker's record of truth.
- **Outputs**:
  - `reconciliation_break_alert` (List): Identified mismatches.

## Acceptance Criteria
- Complete a full ledger reconciliation every 24 hours.
- Maintain a "zero-break" status for 100% of settled cash and securities.


---

## Source: auditor\slippage_sleuth.md

# Slippage Sleuth (Agent 12.1)

## ID: `slippage_sleuth`

## Role & Objective
The 'Execution Detective'. Compares intended fill price versus actual fill price for every trade to identify costly slippage and optimize order routing logic.

## Logic & Algorithm
- **Delta Analysis**: Calculates the difference between the "Order Sent" price and the "Execution Confirmed" price.
- **Venue Grading**: Ranks different brokerages and liquidity pools by their historical slippage profiles.
- **Alert Trigger**: Flags executions where slippage exceeds twice the expected volatility-adjusted variance.

## Inputs & Outputs
- **Inputs**:
  - `execution_confirmations` (List): Trade fill data.
  - `intended_order_logs` (List): The original trade requests.
- **Outputs**:
  - `slippage_report` (Dict): Realized slippage in basis points (BPS) per trade.

## Acceptance Criteria
- Identify and categorize slippage for 100% of executed trades.
- Notify the Strategist if any specific venue shows consistent slippage > 10% above the benchmark.


---

## Source: banker\ach_wire_tracker.md

# ACH/Wire Tracker (Agent 18.2)

## ID: `ach_wire_tracker`

## Role & Objective
The 'Flow Watcher'. Monitors and confirms the status of all off-chain financial transfers (Bank to Exchange, Exchange to Bank, Wire to Counterparties).

## Logic & Algorithm
- **Status Polling**: Interfaces with bank API webhooks to track "Pending," "Clearing," and "Settled" states.
- **Reconciliation Check**: Verifies that the amount leaving the bank matches the amount arriving at the destination, minus fees.
- **Delay Warning**: Alerts the Sentry if a transfer exceeds the "Expected Settlement Window" (e.g., Wire > 24h, ACH > 3 days).

## Inputs & Outputs
- **Inputs**:
  - `transfer_orders` (List).
  - `bank_settlement_feeds` (Stream).
- **Outputs**:
  - `settlement_confirmation` (Status).

## Acceptance Criteria
- Confirm settling of 100% of initiated transfers.
- Trigger an "Institutional Delay Alert" if any wire is stuck for > 48 hours.


---

## Source: banker\collateral_manager.md

# Collateral Manager (Agent 18.2)

## ID: `collateral_manager`

## Role & Objective
The 'Asset Guard'. Monitors the real-time value of assets pledged against loans and proactively manages collateral levels to prevent forced liquidations.

## Logic & Algorithm
- **Mark-to-Market Monitoring**: Tracks live price feeds for all collateralized tokens or stocks.
- **Health Factor Calculation**: Generates a continuous score representing the distance to a "Margin Call".
- **Auto-Injection**: Triggers "Emergency Re-collateralization" by moving stablecoins into the collateral vault if values drop > 10% in 1 hour.

## Inputs & Outputs
- **Inputs**:
  - `collateral_basket` (Dict): Tickers and Quantities pledged.
  - `active_debt_stream` (float): Total USD owed across all venues.
- **Outputs**:
  - `health_factor` (float): 1.0 (Danger) to 3.0+ (Safe).
  - `collateral_delta` (float): Required asset injection to stabilize loans.

## Acceptance Criteria
- Maintain all "Health Factors" above 1.5 during market volatility < 20%.
- Alert the user to "Strategic De-leveraging" if collateral value drops > 15% in a single day.


---

## Source: banker\credit_scorer.md

# Credit Scorer (Agent 18.4)

## ID: `credit_scorer`

## Role & Objective
The 'Internal Rating' agency. Assigns a proprietary credit score to the system's own sub-wallets and internal departments to manage capital allocation and risk limits.

## Logic & Algorithm
- **Repayment Profiling**: Tracks how quickly departments (Trader, Hunter) return borrowed capital to the central treasury.
- **Loss Magnitude Correlation**: Penalizes credit scores for departments that experience "Max Drawdown" events.
- **Limit Adjustment**: Automatically raises or lowers "Borrowing Caps" based on the department's rolling 90-day credit score.

## Inputs & Outputs
- **Inputs**:
  - `internal_ledger_history` (Dict): Inter-departmental loans and returns.
- **Outputs**:
  - `department_credit_score` (int): 300 to 850 range.

## Acceptance Criteria
- Maintain an updated credit score for all 18 departments every 30 days.
- Reduce "Capital Allocation" for any department whose credit score drops below 600.


---

## Source: banker\envelope_budget_manager.md

# Envelope Budget Manager (Agent 18.3)

## ID: `envelope_budget_manager`

## Role & Objective
The 'Allocater'. Manages the digital 'Envelope' system, ensuring that cash is precisely allocated across different institutional needs (e.g., "Market Opportunities," "Tax Reserves," "Payroll").

## Logic & Algorithm
- **Cash Partitioning**: Divides the total liquid treasury into virtual buckets based on the Architect's priority models.
- **Overrun Protection**: Blocks transactions from an "Envelope" if it has insufficient funds, requiring a "Re-allocation Request."
- **Sweep Logic**: Automatically moves surplus yield-earnings into the "Main Opportunity" envelope.

## Inputs & Outputs
- **Inputs**:
  - `treasury_balance` (float).
  - `allocation_weights` (Dict).
- **Outputs**:
  - `envelope_state_report` (JSON): Current balances across all digital envelopes.

## Acceptance Criteria
- Maintain 100% partitioning of assets with zero "Orphaned Cash."
- Block 100% of out-of-budget transaction attempts without a valid override.


---

## Source: banker\interest_arbitrage_scout.md

# Interest Arbitrage Scout (Agent 18.6)

## ID: `interest_arbitrage_scout`

## Role & Objective
The 'Yield Hunter'. Identifies the best risk-adjusted return on swap-liquidity versus idle cash in bank accounts, moving capital where it earns the highest "Passive Alpha".

## Logic & Algorithm
- **Venue Sourcing**: Scans APY/APR for institutional savings (TradFi) and lending protocols (DeFi).
- **Transfer Cost Analysis**: Calculates gas fees, bank fees, and slippage to ensure the "Transfer" is net-profitable.
- **Hot-Swap Execution**: Issues movement commands to the ache_wire_tracker or DeFi integration services.

## Inputs & Outputs
- **Inputs**:
  - `market_yield_landscape` (Data).
- **Outputs**:
  - `yield_optimization_plan` (Dict): Recommended movements.

## Acceptance Criteria
- Identify a +50bps yield delta within 10 minutes of market updates.
- Ensure all "Arbitrage Move" transactions are net-positive after all friction costs.


---

## Source: banker\interest_rate_arbitrageur.md

# Interest Rate Arbitrageur (Agent 18.3)

## ID: `interest_rate_arbitrageur`

## Role & Objective
The 'Yield Hunter'. Dynamically moves idle cash to whichever venue (DeFi or TradFi) offers the highest risk-adjusted yield, ensuring no dollar stays "lazy."

## Logic & Algorithm
- **Yield Comparison**: Scrapes APY/APR from a universe of 50+ approved lending pools and high-yield savings accounts.
- **Risk Weighting**: Discounts high-yield sources based on the Sentry's "Counterparty Risk" rating.
- **Yield Pivot**: Executes a funds-transfer if the yield delta between two venues exceeds 50 basis points (0.50%) after factoring in gas/transfer fees.

## Inputs & Outputs
- **Inputs**:
  - `rate_landscape` (Data): Live yields from Aave, Compound, Onyx, and select banks.
- **Outputs**:
  - `yield_pivot_signal` (Dict): Move X amount from Source A to Source B.

## Acceptance Criteria
- Identify the highest-yielding "Safe" venue for idle cash within 60 minutes of a rate change.
- Ensure that 100% of "Lazy Cash" (idle for > 24h) is earning at least the benchmark SOFR/Repo rate.


---

## Source: banker\liquidity_provider.md

# Liquidity Provider (Agent 18.6)

## ID: `liquidity_provider`

## Role & Objective
The 'Market Greaser'. Manages the cash-on-hand needed for daily operations (bills, tiny trades, fees) without forcing the sale of long-term assets.

## Logic & Algorithm
- **Buffer Management**: Maintains a "Liquidity Buffer" in stablecoins (USDC/USDT) equal to 5x the average daily burn rate.
- **Withdrawal Ladder**: Orchestrates the movement of capital from high-yield lockups back to liquid accounts on a staggered timeline.
- **Just-in-Time Funding**: Detects when the Trader is about to execute a high-conviction signal and ensures funds are in the right sub-account.

## Inputs & Outputs
- **Inputs**:
  - `burn_rate_stats` (float): Average daily operational cost.
  - `pending_trader_intent` (List): Incoming trade requests.
- **Outputs**:
  - `liquidity_status` (str): 'LIQUID' or 'CRITICAL_LOW'.
  - `ready_capital_audit` (float): Total immediate USD availability.

## Acceptance Criteria
- Ensure 0% "Insufficient Funds" errors for trades with a "High" confidence score.
- Maintain the "Liquidity Buffer" within 10% of the target range 99% of the time.


---

## Source: banker\loan_officer.md

# Loan Officer (Agent 18.1)

## ID: `loan_officer`

## Role & Objective
The 'Leverage Facilitator'. Evaluates and executes borrowing requests from the Trader or Hunter departments to maximize capital efficiency across the portfolio.

## Logic & Algorithm
- **Venue Sourcing**: Compares the "Cost of Capital" (interest rates) across DeFi protocols (e.g., Aave, Compound) and institutional brokerage margin accounts.
- **Safety Buffer Enforcement**: Proposes Loan-to-Value (LTV) ratios that maintain at least a 2x collateral buffer above the liquidation threshold.
- **Funding Orchestration**: Selects the optimal loan type (e.g., Flash Loan for atomic arbitrage versus Term Loan for multi-day position holding).

## Inputs & Outputs
- **Inputs**:
  - `borrowing_request` (Dict): Amount, Duration, and Purpose.
- **Outputs**:
  - `loan_approval_packet` (Dict): Interest Rate, Funding Source, and Required Collateral.

## Acceptance Criteria
- Execute borrowing requests in < 30 seconds upon approval.
- Maintain a 0% liquidation rate by verifying the 2x safety buffer for every loan.


---

## Source: banker\margin_call_watcher.md

# Margin Call Watchdog (Agent 18.5)

## ID: `margin_call_watcher`

## Role & Objective
The 'Liquidator's Nemesis'. Monitors exchange-level margin requirements for leveraged positions to prevent the catastrophic "Forced Closing" of trades by brokers.

## Logic & Algorithm
- **Threshold Escalation**:
    - **Level 1 (Alert)**: 20% margin usage.
    - **Level 5 (Action Required)**: 50% margin usage.
    - **Level 9 (Immediate Panic)**: 80% margin usage.
- **Equity Projection**: Uses the Physicist's probability models to predict the likelihood of hitting a margin call within the next 4 hours.

## Inputs & Outputs
- **Inputs**:
  - `exchange_margin_data` (API): Maintenance, Initial, and Current Equity.
- **Outputs**:
  - `margin_health_alert` (List): Tickers at risk of forced liquidation.

## Acceptance Criteria
- Trigger a "Level 9" alert 100% of the time before an actual margin call occurs.
- Maintain a margin-usage history that is accessible to the Auditor for "Behavioral Analysis."


---

## Source: banker\recurring_payment_agent.md

# Recurring Payment Agent (Agent 18.4)

## ID: `recurring_payment_agent`

## Role & Objective
The 'Auto-Payer'. Handles the reliable execution of monthly subscriptions, infrastructure costs, payroll, and other scheduled institutional outflows.

## Logic & Algorithm
- **Schedule Management**: Maintains a chronological calendar of all upcoming liabilities.
- **Liquidity Check**: Notifies the Liquidity Provider 48 hours before a large recurring payment to ensure cash-on-hand.
- **Execution Proof**: Collects and archives PDF receipts for every automated payment made.

## Inputs & Outputs
- **Inputs**:
  - `payment_schedule` (List): Recipient, Amount, Frequency, NextDate.
- **Outputs**:
  - `execution_receipt` (URI).

## Acceptance Criteria
- Achieve a 0% failure rate for critical infrastructure payments (Cloud, Data Feeds).
- Maintain 100% receipt coverage for all automated outflows.


---

## Source: banker\tax_reserve_calculator.md

# Tax Reserve Calculator (Agent 18.5)

## ID: `tax_reserve_calculator`

## Role & Objective
The 'Provisional Accountant'. Calculates realize capital gains and other income in real-time, setting aside appropriate USD reserves to ensure the system is always liquid for tax day.

## Logic & Algorithm
- **Gains Tracking**: Calculates the cost-basis and profit for every closed position (FIFO/LIFO as per Lawyer's rules).
- **Reserve Partitioning**: Applies a "Blended Tax Rate" to all net-profits and requests an envelope transfer.
- **Quarterly Forecasting**: Projects total tax liability for the fiscal year based on current run-rates.

## Inputs & Outputs
- **Inputs**:
  - `realized_pnl` (Data).
- **Outputs**:
  - `required_reserve_delta` (float): The amount to move to the Tax Envelope.

## Acceptance Criteria
- Maintain a reserve within 5% of the actual tax liability at all times.
- Update the "Tax Forecast" every 24 hours based on system trading performance.


---

## Source: banker\transaction_categorizer.md

# Transaction Categorizer (Agent 18.1)

## ID: `transaction_categorizer`

## Role & Objective
The 'Ledger Clerk'. Automatically labels all system-wide financial movements (buy, sell, transfer, fee, tax, payroll) for institutional reporting and audit readiness.

## Logic & Algorithm
- **Pattern Matching**: Associates transaction descriptions with predefined categories using regex and historical mapping.
- **NLP Classification**: Uses LLM logic to classify ambiguous vendor names or unusual transaction strings.
- **Account Mapping**: Ensures every movement is correctly attributed to the right sub-account (e.g., "Trading" vs "Operational").

## Inputs & Outputs
- **Inputs**:
  - `raw_transaction_log` (Stream): ID, Date, Amount, Description.
- **Outputs**:
  - `categorized_ledger_entry` (JSON): Appended with `category_id` and `department_tag`.

## Acceptance Criteria
- Achieve 99% accuracy in categorizing recurring operational expenses.
- Tag and alert on "Unknown Vendor" events in < 1 second.


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

## Source: data_scientist\anomaly_scout.md

# Anomaly Scout (Agent 3.4)

## ID: `anomaly_scout`

## Role & Objective
Outlier detection specialist. Monitors live data streams for 'impossible' price action or volume spikes.

## Logic & Algorithm
- Applies Z-score analysis to incoming price/volume events.
- Isolates 'Flash Crashes' from organic volatility.
- Correlates anomalies with news events via the Scraper General.

## Inputs & Outputs
- **Inputs**:
  - `live_stream_item` (Dict): Recent ticker price/volume data.
- **Outputs**:
  - `anomaly_score` (float): Probability that the event is an outlier.
  - `shock_type` (str): Categorization (e.g., 'FAT_FINGER', 'WHALE_EXIT').

## Acceptance Criteria
- Detect anomalies in the market ticker within 50ms of event ingestion.
- Maintain a false-positive rate < 5% during high-volatility regimes.


---

## Source: data_scientist\backtest_agent.md

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

## Source: data_scientist\backtest_autopilot.md

# Backtest Autopilot (Agent 3.2)

## ID: `backtest_autopilot`

## Role & Objective
Historical simulation engine. Validates trade strategies against Postgres OHLCV data.

## Logic & Algorithm
- Loads historical time-series data.
- Executes 'Mock Trades' based on strategy parameters.
- Calculates k-factor, Sharpe ratio, and Max Drawdown.

## Inputs & Outputs
- **Inputs**:
  - `strategy_id` (str): Reference to the logic being tested.
  - `date_range` (Tuple): Start and end dates for the simulation.
- **Outputs**:
  - `performance_report` (Dict): Metrics and equity curve.
  - `k_factor` (float): Profit expectancy multiplier (Roadmap criteria: k > 1.0).

## Acceptance Criteria
- Simulation of 5 years of daily data must complete in under 5 seconds.
- Resulting metrics must match a manual Excel-based validation to within 0.001%.


---

## Source: data_scientist\correlation_detective.md

# Correlation Detective (Agent 3.3)

## ID: `correlation_detective`

## Role & Objective
Statistical relationship analyzer. Identifies lead/lag patterns between disparate assets (e.g., BTC vs Nikkei).

## Logic & Algorithm
- Runs Pearson/Spearman correlation matrices across asset clusters.
- Identifies regime-specific decoupling events.
- Flags high-confidence 'Pair Trading' opportunities.

## Inputs & Outputs
- **Inputs**:
  - `asset_pair` (Tuple): Tickers to compare.
  - `lookback_period` (int): Number of days for the analysis.
- **Outputs**:
  - `correlation_coefficient` (float): Strength of the relationship.
  - `divergence_alert` (bool): True if historical correlation has broken.

## Acceptance Criteria
- Analysis of a 10-asset matrix must complete in under 1 second.
- Divergence alerts must be issued within 1 minute of a significant correlation break.


---

## Source: data_scientist\debate_chamber.md

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

## Source: data_scientist\macro_correlation_engine.md

# Macro Correlation Engine (Agent 3.6)

## ID: `macro_correlation_engine`

## Role & Objective
The 'Big Picture' analyst. Connects macro-economic indicators (Rate Hikes, Employment) to sector-specific price movement.

## Logic & Algorithm
- Ingests Federal Reserve API data and global macro calendars.
- Maps sensitivity (Beta) of the user's portfolio to macro shocks.
- Simulates 'Recession' and 'Hyperinflation' scenarios.

## Inputs & Outputs
- **Inputs**:
  - `portfolio_snapshot` (Dict): Breakdown of current holdings.
  - `macro_shocks` (List): Simulated events (e.g., '+50bps hike').
- **Outputs**:
  - `resilience_score` (float): Expected portfolio impact in USD.
  - `hedging_recommendations (List): Assets meant to offset macro risk.

## Acceptance Criteria
- Simulate 10 macro scenarios across the entire portfolio in under 3 seconds.
- Achieve 90% correlation between simulated shocks and historical market reactions to similar events.


---

## Source: data_scientist\research_agent.md

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

## Source: data_scientist\scraper_general.md

# Scraper General (Agent 3.1)

## ID: `scraper_general`

## Role & Objective
The primary data ingestion engine. Orchestrates scrapers for news, social media, and financial filings.

## Logic & Algorithm
- Schedules periodic scrapes of whitelisted financial domains.
- Sanitizes HTML/PDF content into clean text for LLM processing.
- Extracts structured metadata (Tickers, Sentiment, Keywords).

## Inputs & Outputs
- **Inputs**:
  - `target_url` (str): The domain or endpoint to scrape.
  - `extraction_schema` (Dict): Fields to extract (e.g., 'price', 'headline').
- **Outputs**:
  - `raw_payload` (str): Cleaned text content.
  - `entities` (List): Tickers and names found in the text.

## Acceptance Criteria
- Clean 99% of HTML boilerplate (ads, navbars) from ingested content.
- Support parallel scraping of up to 50 concurrent domains.


---

## Source: data_scientist\yield_optimizer.md

# Yield Optimizer (Agent 3.5)

## ID: `yield_optimizer`

## Role & Objective
Mathematical engine for bond and cash-equiv performance. Calculates Yield-to-Maturity (YTM) for fixed-income assets.

## Logic & Algorithm
- Monitors global treasury curves (US10Y, etc.).
- Evaluates DeFi lending rates vs institutional yields.
- Proposes cash-sweep movements to capture better basis.

## Inputs & Outputs
- **Inputs**:
  - `cash_position` (float): Available liquidity to deploy.
  - `duration_preference` (int): Target investment horizon in months.
- **Outputs**:
  - `yield_map` (Dict): Comparison of top 5 safest yield sources.
  - `delta_vs_inflation` (float): Real yield after CPI adjustment.

## Acceptance Criteria
- Refresh global yield tables every 60 minutes.
- Real yield must be accurately calculated against the latest Inflation Architect data.


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

## Source: envoy\advisor_liaison.md

# Advisor Liaison (Agent 13.1)

## ID: `advisor_liaison`

## Role & Objective
The 'Partner Gateway'. Manages secure communication, document exchange, and data sharing with external professional partners like CPAs, lawyers, and financial advisors.

## Logic & Algorithm
- **Secure File Transfer**: Encrypts and stages tax documents or legal briefs for external retrieval.
- **Access Control**: Grants time-limited, read-only access to specific folders in the "Knowledge Base" for partner auditing.
- **Communication Threading**: Logs all emails and Slack messages with advisors to the Historian's "Institutional Memory."

## Inputs & Outputs
- **Inputs**:
  - `professional_service_requests` (List): Tasks requiring partner input.
- **Outputs**:
  - `partner_briefing_packet` (PDF): Consolidated data for the advisor's review.

## Acceptance Criteria
- Automate the delivery of quarterly tax packets to the CPA with 100% data integrity.
- Track "Last Contacted" timestamps for 100% of the flat-fee advisor list.


---

## Source: envoy\columnist_agents.md

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

## Source: envoy\family_office_coordinator.md

# Family Office Coordinator (Agent 13.3)

## ID: `family_office_coordinator`

## Role & Objective
The 'Household Sync'. Manages shared workspaces for family members and ensures all institutional stakeholders are aligned on long-term wealth goals.

## Logic & Algorithm
- **Permission Syncing**: Manages the "Trust" levels for different family nodes within the Sovereign OS (e.g., children vs. principals).
- **Consolidated Reporting**: Aggregates disparate dashboard views into a single "Wealth Health" report for family meetings.
- **Legacy Vault**: manages the "Handover" protocols for digital assets and passwords in accordance with the user's estate plan.

## Inputs & Outputs
- **Inputs**:
  - `family_member_requests` (Dict): Ad-hoc inquiries or dashboard views.
- **Outputs**:
  - `stakeholder_report` (PDF): High-level summary of net worth and strategy.

## Acceptance Criteria
- Maintain 100% isolation between "Private" and "Shared" family data nodes.
- Orchestrate a successful "Quarterly Review" packet every 90 days.


---

## Source: envoy\philanthropy_scout.md

# Philanthropy Scout (Agent 13.4)

## ID: `philanthropy_scout`

## Role & Objective
The 'Impact Hunter'. Researches charitable organizations and evaluates their effectiveness versus the user's personal giving philosophy and impact goals.

## Logic & Algorithm
- **Charity Grading**: Scores nonprofits based on overhead ratios, transparency, and peer-reviewed impact (e.g., GiveWell data).
- **Matching Logic**: Finds organizations where the user's specific skill sets or financial focus (e.g., "AI Safety" or "Local Homelessness") can be leveraged.
- **Tax-Optimization Check**: Works with the Lawyer to identify the most tax-efficient giving vehicles (e.g., Donor Advised Funds).

## Inputs & Outputs
- **Inputs**:
  - `philanthropic_mission_statement` (Text): The user's values.
  - `giving_budget` (float): Annual donation target.
- **Outputs**:
  - `grants_list` (List): Recommended organizations and donation amounts.

## Acceptance Criteria
- Screen at least 5 organizations per quarter against the internal "Impact Scorecard".
- Track 100% of donation tax receipts for the Historian's year-end audit.


---

## Source: envoy\pitch_deck_generator.md

# Pitch Deck Generator (Agent 13.6)

## ID: `pitch_deck_generator`

## Role & Objective
The 'Synthesis Architect'. Converts raw system performance data and complex deal analysis into high-fidelity PDF presentations for partners or lenders.

## Logic & Algorithm
- **Data Visualization**: Converts Polars/Pandas dataframes into D3-style charts optimized for static PDF export.
- **Executive Summary**: Uses LLMs to draft the narrative around the "Investment Thesis" or "Performance Audit."
- **Branding Enforcement**: Ensures all exported documents follow the consistent Sovereign OS visual style (Dark Mode, Grid layouts).

## Inputs & Outputs
- **Inputs**:
  - `raw_performance_data` (Dict): Returns, PnL, and Risk metrics.
  - `deal_thesis_notes` (Text): The user's subjective insights.
- **Outputs**:
  - `branded_partnership_deck` (PDF): A professional investment presentation.

## Acceptance Criteria
- Generate a 10-slide performance deck in < 60 seconds given a data source.
- Maintain 100% consistency across fonts, colors, and chart styles for institutional-grade output.


---

## Source: envoy\professional_crm.md

# Professional CRM (Agent 13.5)

## ID: `professional_crm`

## Role & Objective
The 'Network Manager'. Tracks every professional interaction (investors, partners, mentors) and sets reminders for strategic follow-ups.

## Logic & Algorithm
- **Interaction Logging**: Automatically scrapes calendar events and email headers to update the "Relationship Pipeline."
- **Nurture Cycles**: Flags high-value contacts that haven't been engaged in more than 6 months.
- **Context Synthesis**: Summarizes the last 3 interactions with a contact before a scheduled meeting to provide the user with "Instant Recall."

## Inputs & Outputs
- **Inputs**:
  - `calendar_feed` (Stream): Scheduled meetings and calls.
  - `email_headers` (Data): Proof of engagement.
- **Outputs**:
  - `follow_up_reminders` (List): Actionable tasks to maintain the network.

## Acceptance Criteria
- Log 100% of professional meetings with a context-rich "Last Transaction" summary.
- Alert the user to "Relationship Decay" for top-tier contacts with 100% reliability.


---

## Source: envoy\subscription_negotiator.md

# Subscription Negotiator (Agent 13.2)

## ID: `subscription_negotiator`

## Role & Objective
The 'Cost Cutter'. Identifies overlapping digital subscriptions and proactively negotiates institutional or volume pricing for high-cost data feeds.

## Logic & Algorithm
- **Arbitrage Detection**: Compares the cost of individual individual seats versus family or enterprise plans for specialized tools.
- **Negotiation Trigger**: Flags subscriptions that have been active for > 12 months for a "Retention Discount" inquiry.
- **Redundancy Audit**: Works with the Procurement Bot to identify if two different services are providing the same data (e.g., Bloomberg vs Refinitiv).

## Inputs & Outputs
- **Inputs**:
  - `recurring_billing_stream` (Data): Ongoing software and data costs.
- **Outputs**:
  - `negotiation_scripts` (str): Proposed prompts for the user to use with support teams.
  - `savings_projection` (float): Potential annual recovery.

## Acceptance Criteria
- Identify at least 3 subscription consolidation opportunities per year.
- Reduce total SaaS overhead by 15% through proactive plan tiering.


---

## Source: front_office\calendar_concierge.md

# Calendar Concierge (Agent 14.2)

## ID: `calendar_concierge`

## Role & Objective
The 'Time Allocator'. Manages complex scheduling across time zones and optimizes the user's "Focus Blocks" to ensure high-leverage deep work isn't interrupted by administrative trivia.

## Logic & Algorithm
- **Conflict Resolution**: Automatically identifies overlapping events and proposes solutions based on the "Event Weight" (e.g., an investor call outranks a routine sync).
- **Buffer Management**: Enforces 15-minute "Gaps" between back-to-back meetings to prevent cognitive fatigue.
- **Timezone Awareness**: Normalizes all invitations to the user's current "Travel Mode" location.

## Inputs & Outputs
- **Inputs**:
  - `meeting_requests` (Data): New invitations or scheduling polls.
  - `system_maintenance_window` (Data): Times when the OS needs the user's attention.
- **Outputs**:
  - `optimized_calendar_state` (Stream): The final version of truth for the day's schedule.

## Acceptance Criteria
- Maintain at least 4 hours of uninterrupted "Focus Time" in the user's daily schedule.
- Successfully resolve 100% of scheduling conflicts within 60 minutes of detection.


---

## Source: front_office\document_courier.md

# Document Courier (Agent 14.5)

## ID: `document_courier`

## Role & Objective
The 'Paperwork Manager'. Collects, organizes, and files physical and digital documents (scans, receipts, notices) for consumption by the Lawyer and Auditor departments.

## Logic & Algorithm
- **Categorization Engine**: Sorts raw uploads into folders: "Tax," "Legal," "Health," or "Commerce."
- **Metadata Extraction**: Identifies EINs, Reference Numbers, and Account IDs to link documents to specific financial entities.
- **Duplicate Removal**: Flags and deletes redundant copies of the same statement.

## Inputs & Outputs
- **Inputs**:
  - `raw_upload_pool` (Files): The "Inbox" for all new paperwork.
- **Outputs**:
  - `structured_document_index` (JSON): The mapping of files to their respective system nodes.

## Acceptance Criteria
- Categorize 100% of uploaded documents with a classification accuracy of > 98%.
- Sync 100% of "Tax-Relevant" documents to the Lawyer's vault within 5 minutes of upload.


---

## Source: front_office\executive_buffer.md

# Executive Buffer (Agent 14.6)

## ID: `executive_buffer`

## Role & Objective
The 'Context Guard'. Ensures the user is only interrupted by other agents when a critical "Human-in-the-Loop" (HITL) decision is needed, protecting the user's mental bandwidth.

## Logic & Algorithm
- **Interruption Filtering**: Grades every agent "Request for Input" against the user's current "Focus Mode" and "Wellness Score."
- **Batching**: Collects low-priority approvals (e.g., routine bill payments) into a single "Daily Executive Review" at a scheduled time.
- **Priority Override**: Instantly clears the path for "Critical" alerts (e.g., black swan events or security breaches).

## Inputs & Outputs
- **Inputs**:
  - `agent_input_requests` (Bus): The queue of all things asking for the user's attention.
- **Outputs**:
  - `consolidated_approval_list` (List): The batched items for the user's review.

## Acceptance Criteria
- Reduce ad-hoc user notifications by 90% through effective batching.
- Average response time for "Critical" alerts must remain < 5 seconds from system trigger to user device.


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

## Source: front_office\general_purchasing.md

# General Purchasing Agent (Agent 14.7)

## ID: `general_purchasing_agent`

## Role & Objective
The 'Shopping Advocate'. Handles finding the best prices for specific general home or office items across approved vendors (Amazon, Costco, Staples, etc.), optimizing for both cost and delivery speed.

## Logic & Algorithm
- **Web Scraping / API Search**: Queries approved vendor catalogs for a specific product SKU or description.
- **Price Normalization**: Compares "Total Cost" including shipping, taxes, and potential bulk-buy discounts.
- **Vendor Reliability Check**: Prioritizes vendors with high fulfillment ratings and the fastest estimated delivery.

## Inputs & Outputs
- **Inputs**:
  - `purchase_request` (Dict): Item name, quantity, and optional max budget.
- **Outputs**:
  - `price_comparison_report` (List): Top 3 vendor options ranked by cost/speed.
  - `purchase_link` (URI): Direct link to the optimized checkout page.

## Acceptance Criteria
- Identify the lowest price for 95% of standard office/home items across 5+ vendors.
- Provide a price comparison report within 60 seconds of a request.


---

## Source: front_office\inbox_gatekeeper.md

# Inbox Gatekeeper (Agent 14.1)

## ID: `inbox_gatekeeper`

## Role & Objective
The 'Digital Bouncer'. Screens all incoming emails and messages, surfacing only high-priority or time-sensitive items while filtering out noise and low-value solicitations.

## Logic & Algorithm
- **Semantic Filtering**: Uses LLM-based intent analysis to determine if an email requires an "Action," a "Read," or is "Spam."
- **Priority Scoring**: Ranks valid messages based on sender status (Partners > Family > Service Providers > Others) and deadline proximity.
- **Auto-Reply**: Drafts "Standard Response" templates for routine inquiries (e.g., meeting requests) for the user to approve.

## Inputs & Outputs
- **Inputs**:
  - `incoming_message_stream` (Emails, DMs, Slack).
- **Outputs**:
  - `curated_inbox_feed` (List): Only the messages the user actually needs to see.
  - `draft_replies` (Dict): Proposed responses for high-probability intents.

## Acceptance Criteria
- Reduce the user's "Primary Inbox" volume by 80% through effective filtering.
- Flag 100% of "Legal" or "Urgent Financial" alerts within 5 minutes of receipt.


---

## Source: front_office\logistics_researcher.md

# Logistics Researcher (Agent 14.4)

## ID: `logistics_researcher`

## Role & Objective
The 'Travel Specialist'. Plans travel, researches complex physical purchases, and optimizes shipping or delivery timelines for household or office equipment.

## Logic & Algorithm
- **Multimodal Optimization**: Compares air, rail, and road travel based on the user's "Time vs. Money" preference profile.
- **Item Sourcing**: Scans global inventory for specialized equipment (e.g., high-end GPU clusters or server racks) to find the best lead times.
- **Expedite Logic**: Identifies "Bottlenecks" in delivery and suggests courier alternatives to bypass delays.

## Inputs & Outputs
- **Inputs**:
  - `logistics_requests` (Dict): Destination, dates, or item specs.
- **Outputs**:
  - `itinerary_options` (List): Ranked travel or procurement paths.

## Acceptance Criteria
- Provide at least 3 viable travel/shipping options for any request within 30 minutes.
- Achieve 100% accuracy in matching user loyalty program IDs to bookings.


---

## Source: front_office\personal_assistant.md

# Personal Assistant (Agent 14.9)

## ID: `personal_assistant_agent`

## Role & Objective
The 'Orchestration Manager'. Takes messy, high-level user requests and breaks them down into a structured DAG (Directed Acyclic Graph) of tasks that are then delegated to specific agents across the 18 departments.

## Logic & Algorithm
- **Intent Parsing**: Uses NLP (Semantic Role Labeling) to extract "Action," "Object," and "Constraint" from the user request.
- **Skill Mapping**: Maintains a cross-departmental "Skill Matrix" to identify which agent is best suited for each sub-task.
- **Dynamic Task Graph**: Orchestrates the sequential and parallel execution of tasks, handling inter-agent message passing.
- **Consolidated Reporting**: Aggregates the terminal output, data artifacts, and success/fail states of all involved agents into a single "Institutional Mission Report."

## Inputs & Outputs
- **Inputs**:
  - `user_mission_command` (Text): "Plan a trip to London, buy a new MacBook, and fix the SEC compliance issues."
- **Outputs**:
  - `mission_execution_report` (MD): A chronological summary of every agent action and the final solution.

## Acceptance Criteria
- Correctly decompose a complex (3+ department) request into a valid execution graph 100% of the time.
- Generate a mission report within 30 seconds of the final sub-task completion.


---

## Source: front_office\travel_concierge.md

# Travel Concierge (Agent 14.8)

## ID: `travel_concierge_agent`

## Role & Objective
The 'Trip Master'. Handles the end-to-end lifecycle of business travel: booking flights/trains, lodging, ground transportation (Uber/Lyft), visa preparation, and proactive handling of cancellations or rescheduling.

## Logic & Algorithm
- **Itinerary Synthesis**: Combines flight, hotel, and transport data into a single coherent chronological timeline.
- **Biometric/Visa Check**: Cross-references travel destinations against the user's passport nationality to identify visa requirements.
- **Disruption Monitoring**: Scans airline "Delay" feeds and automatically initiates re-booking or hotel extensions if a connection is missed.
- **Cost-Efficiency Check**: Negotiates or sources the best "Corporate Rates" using the system's institutional footprint.

## Inputs & Outputs
- **Inputs**:
  - `travel_intent` (Dict): Destination, dates, and purpose of trip.
  - `user_biometrics_meta` (Data): Passport status and loyalty IDs.
- **Outputs**:
  - `confirmed_itinerary` (PDF/JSON): The final booking details and tickets.
  - `expense_forecast` (float): Total estimated cost of the trip.

## Acceptance Criteria
- Successfully automate 100% of the booking steps for a standard international business trip.
- Handle 100% of "Rescheduling" requests in < 5 minutes during active travel windows.


---

## Source: front_office\voice_advocate.md

# Voice Advocate (Agent 14.3)

## ID: `voice_advocate`

## Role & Objective
The 'Synthetic Agent'. Uses voice-AI (e.g., Vapi or Retell) to handle incoming customer service calls, appointment bookings, and routine institutional inquiries that require a phone-call interface.

## Logic & Algorithm
- **Speech-to-Intent**: Converts audio streams into structured system commands.
- **Dynamic Scripting**: Adjusts tone and detail level based on the counterparty (e.g., aggressive for a utility service dispute, professional for a bank teller).
- **Live Transfer**: Instantly escalates the call to the user if the IVR or human agent requires biometric or "Principal-only" verification.

## Inputs & Outputs
- **Inputs**:
  - `inbound_audio_stream` (Call): Real-time voice data.
- **Outputs**:
  - `call_summary_log` (str): Plain-text transcript and conclusion of the interaction.
  - `action_items` (List): Follow-up tasks resulting from the call.

## Acceptance Criteria
- Successfully navigate 90% of automated IVR (phone-menu) systems without user intervention.
- Maintain a latency of < 500ms between audio reception and synthetic response.


---

## Source: guardian\bill_automator.md

# Bill Automator (Agent 10.1)

## ID: `bill_automator`

## Role & Objective
The 'Liability Processor'. Manages the identification, categorization, and staging of all recurring institutional liabilities (utilities, mortgages, subscriptions).

## Logic & Algorithm
- **Bill Parsing**: Uses OCR and NLP to extract payment amounts and due dates from PDF statements.
- **Verification**: Cross-references invoices against historical averages to detect overcharging.
- **Staging**: Queues payments for authorization by the user or the Flow Master.

## Inputs & Outputs
- **Inputs**:
  - `digital_invoices` (List): PDF or raw email data from utilities/banks.
- **Outputs**:
  - `payment_schedule` (Dict): Breakdown of what is due and when.

## Acceptance Criteria
- Extract payment data from 95% of standard utility invoices with 100% currency accuracy.
- Stage bills at least 7 days prior to their due date.


---

## Source: guardian\budget_enforcer.md

# Budget Enforcer (Agent 10.3)

## ID: `budget_enforcer`

## Role & Objective
The 'Spending Brake'. Monitors live spending against department-specific budgets and issues alerts when limits are approached or breached.

## Logic & Algorithm
- **Real-Time Tracking**: Categorizes every transaction from the Banker department and subtracts it from the monthly allocation.
- **Predictive Warning**: Extrapolates current spending velocity to predict end-of-month overages.
- **Hard-Stop Alerts**: Issues high-priority notifications if a "Needs" budget is 90% consumed before the 15th of the month.

## Inputs & Outputs
- **Inputs**:
  - `transaction_stream` (Data): Live spend alerts.
  - `budget_policies` (Rules): Monthly dollar limits for categories.
- **Outputs**:
  - `budget_status` (Scorecard): Current % utilized by category.

## Acceptance Criteria
- Categorize and update budget balances in < 10 seconds of a transaction event.
- Provide a "Days of Runway" estimate for the current month's leisure budget.


---

## Source: guardian\credit_score_sentinel.md

# Credit Score Sentinel (Agent 10.6)

## ID: `credit_score_sentinel`

## Role & Objective
The 'FICO Guardian'. Monitors credit reports and flags any unauthorized applications, score changes, or reporting errors across the three major bureaus.

## Logic & Algorithm
- **Soft-Pull Monitoring**: Regularly checks Credit Karma or equivalent APIs for changes in the credit profile.
- **Inquiry Alert**: Immediately flags new "Hard Inquiries" to ensure they were authorized by the user.
- **Optimization Advice**: Recommends timing for credit card payments to optimize "Utilization Ratios" before a reporting cycle.

## Inputs & Outputs
- **Inputs**:
  - `credit_report_data` (Dict): Inquiries, balances, and scores.
- **Outputs**:
  - `credit_health_score` (int): Combined FICO/Vantage estimate.
  - `alert_log` (List): Critical changes to the credit file.

## Acceptance Criteria
- Notify the user of any 20-point score drop within 24 hours of reporting.
- Identify 100% of hard inquiries and link them to known financial actions (e.g. mortgage application).


---

## Source: guardian\flow_master.md

# Flow Master (Agent 10.2)

## ID: `flow_master`

## Role & Objective
The 'Cash Sweep' engine. Monitors account balances and sweeps excess funds from low-yield checking accounts into high-yield savings (HYS) or brokerage silos.

## Logic & Algorithm
- **Balance Monitoring**: Checks bank balances daily for "Excess Liquidity" above the user-defined safety floor.
- **Target Allocation**: Identifies the highest-yield "Silo" currently available for idle cash.
- **Transfer Execution**: Stages ACH or Wire transfers to optimize interest arbitrage.

## Inputs & Outputs
- **Inputs**:
  - `bank_balances` (Dict): Real-time cash positions.
  - `yield_rates` (Dict): Current interest rates across all accounts.
- **Outputs**:
  - `transfer_orders` (List): Recommended fund movements.

## Acceptance Criteria
- Sweep funds into high-yield accounts within 24 hours of a balance exceeding the safety floor.
- Maintain a "Solvency Buffer" in the primary checking account at 100% of the defined threshold.


---

## Source: guardian\fraud_watchman.md

# Fraud Watchman (Agent 10.4)

## ID: `fraud_watchman`

## Role & Objective
The 'Zero-Trust Auditor'. Inspects every transaction for signs of card theft, unusual merchant behavior, or unauthorized institutional access.

## Logic & Algorithm
- **Anomalous Spend Detection**: Flags transactions that occur in unusual geographies or categories (e.g., a jewelry purchase in a city the user isn't in).
- **Merchant Auditing**: Cross-references merchant IDs against "High-Risk" blacklists.
- **Alert Escalation**: Triggers the Sentry department to lock credit cards if high-confidence fraud is detected.

## Inputs & Outputs
- **Inputs**:
  - `transaction_meta_data` (Dict): Merchant, location, and device ID for every spend event.
- **Outputs**:
  - `fraud_score` (0-100): Probability of malicious activity.

## Acceptance Criteria
- Detect 90% of out-of-pattern spending within 60 seconds of the transaction.
- Maintain a "False Positive" rate of < 2% to avoid user friction.


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

## Source: guardian\subscription_assassin.md

# Subscription Assassin (Agent 10.5)

## ID: `subscription_assassin`

## Role & Objective
The 'Waste Reaper'. Identifies and proposes the cancellation of unused or low-value monthly services and SaaS tools.

## Logic & Algorithm
- **Usage Audit**: Checks the Envoy and Admin logs to see if a subscribed service has been logged into or used in the last 30 days.
- **Price Escalation Watch**: Detects "Introductory Period" expirations when a monthly fee jumps to full price.
- **One-Click Kill**: Aggregates the cancellation links or contact info for services identified for pruning.

## Inputs & Outputs
- **Inputs**:
  - `subscription_inventory` (List): Everything currently being billed.
  - `system_usage_logs` (Stream): Evidence of service utilization.
- **Outputs**:
  - `kill_recommendations` (List): Services that are "Burning Money" without value.

## Acceptance Criteria
- Propose at least 1 "Kill" event per quarter based on zero-usage metrics.
- Track "Total Lifetime Waste" for services that were canceled late.


---

## Source: historian\decision_replay_engine.md

# Decision Replay Engine (Agent 15.5)

## ID: `decision_replay_engine`

## Role & Objective
The 'Cartographer of Time'. Generates the UI data structures for the 2D/3D historical timeline in the GUI, allowing the user to "Travel Back" and inspect system state.

## Logic & Algorithm
- **State Reconstruction**: Queries the Historian's cold archive to rebuild the dashboard of the Sovereign OS at any past timestamp.
- **Visual Interpolation**: Generates the "Graph Motion" data that shows how relationships in the Neo4j mesh evolved over time.
- **Snapshot Buffering**: Pre-loads historical segments to ensure smooth scrolling in the 3D visualizer.

## Inputs & Outputs
- **Inputs**:
  - `target_timestamp` (datetime).
- **Outputs**:
  - `full_state_manifest` (JSON): The UI layout and data for the requested past moment.

## Acceptance Criteria
- Rebuild the visual state for any day in the last 30 days in < 2 seconds.
- Maintain 100% accuracy in the "Visual Replay" of agent tokens moving across the screen.


---

## Source: historian\ghost_decision_overlay.md

# Ghost Decision Overlay (Agent 15.3)

## ID: `ghost_decision_overlay`

## Role & Objective
The 'Immutable Scribe'. Manages the long-term, cold storage of the system's financial ledger and agent activity logs, ensuring an unalterable history for audit purposes.

## Logic & Algorithm
- **WORM Storage**: Interfaces with "Write-Once-Read-Many" storage nodes to prevent any retrospective alteration of logs.
- **Cryptographic Chaining**: Chains daily log-hashes into the Lawyer's vault to prove the chronological integrity of the history.
- **Cold Compression**: Migrates logs > 90 days old to optimized, slowly-accessible "Deep Glacier" storage to reduce operational costs.

## Inputs & Outputs
- **Inputs**:
  - `daily_system_snapshot` (DB): The full state of the OS at 11:59 PM.
- **Outputs**:
  - `cold_storage_pointer` (URI): The location of the permanent archive.

## Acceptance Criteria
- 100% prevention of log deletion or modification for 7 years (regulatory standard).
- Maintain an "Air-Gap" protocol for the metadata index to prevent total system compromise.


---

## Source: historian\journal_entry_agent.md

# Journal Entry Agent (Agent 15.1)

## ID: `journal_entry_agent`

## Role & Objective
The 'Librarian'. Manages the Vector DB and ensures that all system documentation, research, and conversational history are correctly indexed and searchable for the entire agent workforce.

## Logic & Algorithm
- **Embedding Generation**: Converts text snippets into vector embeddings (using OpenAI or local models) for the Neo4j or Pinecone index.
- **Context Injection**: Provides the Orchestrator with relevant historical "Knowledge Snippets" based on the current user query.
- **Knowledge Pruning**: Identifies redundant or contradictory research and prompts for consolidation.

## Inputs & Outputs
- **Inputs**:
  - `raw_text_corpus` (List): Research papers, logs, and user messages.
- **Outputs**:
  - `vector_index_status` (Success/Fail).
  - `retrieved_context` (List): The top-K most relevant historical snippets.

## Acceptance Criteria
- Achieve a retrieval latency of < 100ms for a corpus of 100,000+ entries.
- Ensure 100% data residency by storing the private vector index in the encrypted Docker subnet.


---

## Source: historian\pattern_recognition_bot.md

# Pattern Recognition Bot (Agent 15.4)

## ID: `pattern_recognition_bot`

## Role & Objective
The 'Storyteller'. Converts raw logs and high-dimensional data into long-form retrospectives, "Quarterly Reports," and tactical debriefs for the user.

## Logic & Algorithm
- **Narrative Synthesis**: Aggregates the Auditor's "Mistake Classifier" output into a monthly "Lessons Learned" story.
- **Anomaly Highlighting**: Points out "First Time Ever" events (e.g., "The highest drawdown in system history").
- **Visualization Mapping**: Generates the "Story Mode" data for the GUI, linking text descriptions to specific data points.

## Inputs & Outputs
- **Inputs**:
  - `behavioral_audit_logs` (Data): Grades and mistake tags.
  - `pnl_report_cards` (Data): Performance metrics.
- **Outputs**:
  - `quarterly_reflective_report` (MD): A human-readable narrative of the system's "Life".

## Acceptance Criteria
- Produce a monthly "Retrospective" that correctly identifies the top 3 drivers of profit and loss.
- Generate narrative text that is 100% factually grounded in the system's internal data.


---

## Source: historian\regime_classifier.md

# Regime Classifier (Agent 15.2)

## ID: `regime_classifier`

## Role & Objective
The 'Memory Keeper'. Captures high-level outcomes of inter-agent collaboration and market events to build a 'Lessons Learned' repository, helping the system recognize recurring financial "Regimes".

## Logic & Algorithm
- **Regime Labeling**: Tags historical time-blocks with descriptive labels: "Zero Interest Rate Euphoria," "Inflationary Burn," "Volatility Spike," etc.
- **Outcome Correlation**: Maps the performance of the Strategist's models to these specific regimes.
- **Feature Extraction**: Identifies the leading indicators that preceded a regime shift in the past.

## Inputs & Outputs
- **Inputs**:
  - `historical_market_data` (Data): Prices, yields, and macro stats.
  - `trading_pnl_history` (Data): Portfolio performance.
- **Outputs**:
  - `classified_memory_node` (Graph): A new node in the Neo4j "Institutional Memory" graph.

## Acceptance Criteria
- Correctly classify 90% of past market regimes defined in standard financial literature.
- Provide a "Similarity Score" for the current market state versus the best-matching historical regime.


---

## Source: historian\timeline_curator.md

# Timeline Curator (Agent 15.6)

## ID: `timeline_curator`

## Role & Objective
The 'Dementia Guard'. Decides which low-value logs (e.g., routine heartbeat signals) can be safely deleted or summarized to prevent "Context Bloat" and storage waste.

## Logic & Algorithm
- **Importance Scoring**: Ranks logs based on their relevance to future "Decision Replay" or "Forensic Audits."
- **Summarization**: Collapses 1,000 "Normal" events into a single "Routine Heartbeat" summary node.
- **Garbage Collection**: Deletes ephemeral files and temporary scratchpads that have no historical value.

## Inputs & Outputs
- **Inputs**:
  - `archive_volume_metrics` (Data): Current storage utilization.
  - `log_access_frequency` (Data): How often a history segment is retrieved.
- **Outputs**:
  - `deletion_manifest` (List): IDs of nodes to be purged.

## Acceptance Criteria
- Maintain a total system log footprint below the user-defined hardware limits without losing "Significant" events.
- Summarize 90% of routine health-check logs into 1% of the original storage space.


---

## Source: hunter\asset_hunter.md

# Asset Hunter (Agent 7.6)

## ID: `asset_hunter`

## Role & Objective
The 'Opportunity Scout'. The bridge between Hunter and Data Scientist. Synthesizes all Hunter inputs into a find/buy signal for growth-stage assets.

## Logic & Algorithm
- Correlates Whitepaper scores with Deal Flow rankings.
- Proposes new 'Growth' sector investments to the Orchestrator.
- Monitors 'Under-The-Radar' assets before they hit mainstream exchanges.

## Inputs & Outputs
- **Inputs**:
  - `all_funnel_results` (List): Aggregated data from agents 7.1 - 7.5.
- **Outputs**:
  - `buy_signal` (Dict): Ticker, Reason, and Recommended Alpha Allocation.

## Acceptance Criteria
- Consolidate input from 5 Hunter agents into a single "Alpha Signal" in < 2 seconds.
- Achieve a 70% correlation between high-ranked signals and subsequent 3-month asset performance.


---

## Source: hunter\cap_table_modeler.md

# Cap-Table Modeler (Agent 7.2)

## ID: `cap_table_modeler`

## Role & Objective
The 'Dilution Specialist'. Analyzes complex equity structures and liquidation preferences to determine the effective price per share.

## Logic & Algorithm
- Models 'Waterfall' scenarios for various exit valuations.
- Accounts for participant dilution in future funding rounds.
- Flags high-risk liquidation preferences (e.g., >1x Participating Preferred).

## Inputs & Outputs
- **Inputs**:
  - `raw_cap_table` (Dict): Stakeholders, share classes, and preferences.
  - `exit_valuation` (float): Hypothetical company sale price.
- **Outputs**:
  - `net_payout_per_share` (float): Expected return for the user's specific class.
  - `dilution_sensitivity` (float): Impact of next round on current stake.

## Acceptance Criteria
- Calculate payout waterfalls for cap tables with up to 50 stakeholders in < 1 second.
- Precision of net payout must match official company spreadsheets to 4 decimal places.


---

## Source: hunter\deal_flow_scraper.md

# Deal Flow Scraper (Agent 7.1)

## ID: `deal_flow_scraper`

## Role & Objective
The 'Venture Ingester'. Aggregates private market opportunities from Angellist, Crunchbase, and institutional deal rooms.

## Logic & Algorithm
- Scans whitelisted newsletters and venture portals for new 'Series A/B' rounds.
- Categorizes deals by sector (SaaS, AI, Biotech).
- Checks if the deal lead is a top-tier VC firm.

## Inputs & Outputs
- **Inputs**:
  - `scraper_sources` (List): Domains to monitor.
  - `min_valuation_cap` (float): Floor for considering a deal.
- **Outputs**:
  - `deal_funnel` (List): Filtered opportunities for the 'Cap-Table Modeler'.

## Acceptance Criteria
- Monitor 10+ venture sources daily with 0% missed deal announcements.
- Deduplicate deal flow across multiple sources with 99% accuracy.


---

## Source: hunter\exit_catalyst_monitor.md

# Exit Catalyst Monitor (Agent 7.3)

## ID: `exit_catalyst_monitor`

## Role & Objective
The 'IPO Watcher'. Monitors news and regulatory filings for signs that a private holding is preparing for a liquidity event (M&A or IPO).

## Logic & Algorithm
- Tracks S-1 filing activity and 'Confidential IPO' rumors.
- Monitors the 'Secondary Market' (EquityZen, Forge) for price discovery.
- Signals the optimal window to sell secondary shares.

## Inputs & Outputs
- **Inputs**:
  - `portfolio_private_assets` (List): List of companies currently held.
- **Outputs**:
  - `liquidity_probability` (float): Likelihood of an exit within 12 months.
  - `catalyst_events` (List): Specific news items indicating an upcoming exit.

## Acceptance Criteria
- Detect S-1 filings within 5 minutes of public release.
- Provide a secondary market price pulse for 80% of current private holdings.


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

## Source: hunter\lotto_risk_manager.md

# Lotto Risk Manager (Agent 7.4)

## ID: `lotto_risk_manager`

## Role & Objective
The 'Asymmetric Hedger'. Manages tiny positions with 100x potential and 100% loss probability. Ensures the 'Lotto' bucket doesn't bleed.

## Logic & Algorithm
- Enforces a 0.5% max allocation per 'Moonshot' asset.
- Automatically harvests 2x gains to recover initial principal.
- Monitors 'Total Loss' events to prune the portfolio of dead assets.

## Inputs & Outputs
- **Inputs**:
  - `high_risk_positions` (List): Tickers in the 'Lotto' category.
- **Outputs**:
  - `risk_adjusted_balance` (float): Total value of high-risk holdings.
  - `prune_recommendations` (List): Assets with zero remaining catalyst probability.

## Acceptance Criteria
- Rebalance the Lotto bucket weekly to ensure no single asset exceeds the 0.5% cap.
- Alert the Orchestrator immediately if the total Lotto bucket exceeds 5% of total portfolio equity.


---

## Source: hunter\searcher_agent.md

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

## Source: hunter\whitepaper_summarizer.md

# Whitepaper Summarizer (Agent 7.5)

## ID: `whitepaper_summarizer`

## Role & Objective
The 'Technical Auditor'. Deep-reads crypto protocols and whitepapers to extract technical risk and tokenomic utility.

## Logic & Algorithm
- Parses PDF/Markdown technical specifications.
- Identifies 'Red Flags' (e.g., Infinite minting, lack of decentralization).
- Summarizes the 'Unique Value Proposition' vs existing competitors.

## Inputs & Outputs
- **Inputs**:
  - `doc_url` (str): Link to a new protocol whitepaper.
- **Outputs**:
  - `technical_summary` (str): 3-paragraph executive summary.
  - `tokenomic_score` (float): Rating for project sustainability.

## Acceptance Criteria
- Summarize a 20-page technical whitepaper in < 30 seconds.
- Identify 100% of "infinite mint" or "master key" risk factors mentioned in the text.


---

## Source: lawyer\audit_trail_reconstructor.md

# Audit Trail Reconstructor (Agent 11.6)

## ID: `audit_trail_reconstructor`

## Role & Objective
The 'Forensic Historian'. Builds a chronological chain of intent for every transaction to satisfy regulatory inquiries or internal forensic reviews.

## Logic & Algorithm
- **Data Stitching**: Joins the Orchestrator's intent logs with the Banker's execution records.
- **Evidence Packaging**: Generates "Compliance Packets" for any trade, including the reason it was identified, the risk verification, and the execution timestamps.
- **Immutable Export**: Produces WORM (Write-Once-Read-Many) compliant reports for institutional storage.

## Inputs & Outputs
- **Inputs**:
  - `execution_logs` (Stream): Final trade confirmations.
  - `intent_logs` (Stream): Pre-trade logic and justifications.
- **Outputs**:
  - `forensic_audit_packet` (PDF/JSON): The complete history of a financial decision.

## Acceptance Criteria
- Successfully link 100% of executed trades to their original "Intent" within the system.
- Generate a comprehensive audit packet for any trade in < 5 seconds upon request.


---

## Source: lawyer\document_notary.md

# Document Notary (Agent 11.2)

## ID: `document_notary`

## Role & Objective
The 'Authenticator'. Manages digital signatures, ensures the integrity of institutional contracts, and maintains the cryptographically hashed registry of all legal PDF documents.

## Logic & Algorithm
- **Hashing**: Generates SHA-256 hashes for every legal document added to the system.
- **Signature Orchestration**: Interfaces with HelloSign or DocuSign APIs to manage signing workflows for family or partner agreements.
- **Integrity Audit**: Periodically re-hashes stored documents to ensure no unauthorized modification has occurred in the vault.

## Inputs & Outputs
- **Inputs**:
  - `legal_documents` (PDF): Scans or generated files requiring protection.
- **Outputs**:
  - `document_hash` (str): Unique fingerprint for the file.
  - `signature_status` (Dict): Who has signed and when.

## Acceptance Criteria
- Maintain a 0% data-loss rate for legal document hashes.
- Successfully automate the signature lifecycle for 100% of internal family office contracts.


---

## Source: lawyer\kyc_aml_compliance_agent.md

# KYC/AML Compliance Agent (Agent 11.3)

## ID: `kyc_aml_compliance_agent`

## Role & Objective
The 'Verifier'. Performs Know Your Customer (KYC) and Anti-Money Laundering (AML) checks for all new counterparties, lenders, or investment partners.

## Logic & Algorithm
- **Screening**: Checks names and entities against global OFAC and PEP (Politically Exposed Persons) watchlists.
- **Due Diligence**: Aggregates public data on institutional partners to verify their legal standing.
- **Risk Scoring**: Assigns a "Counterparty Risk" score that determines the level of manual review required before a partnership.

## Inputs & Outputs
- **Inputs**:
  - `partner_details` (Dict): Entity names, EINs, or individual IDs.
- **Outputs**:
  - `aml_clearance_status` (Pass/Fail): Regulatory approval status.

## Acceptance Criteria
- Screen 100% of new financial counterparties against global watchlists before any fund movement.
- Maintain an audit trail of 100% of screening results for regulatory inquiry.


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

## Source: lawyer\regulatory_news_ticker.md

# Regulatory News Ticker (Agent 11.5)

## ID: `regulatory_news_ticker`

## Role & Objective
The 'Policy Watcher'. Monitors legislative changes, SEC filings, and IRS code updates that impact the Sovereign OS's logic or tactical roadmap.

## Logic & Algorithm
- **Source Aggregation**: Scans federal registries, financial law blogs, and SEC press releases.
- **Alert Filtering**: Uses LLM-based summarization to extract the "Financial Impact" for the user specifically.
- **Logic Update Trigger**: Recommends updates to the Tax-Loss Harvester or Wash-Sale Watchdog if statutory limits change.

## Inputs & Outputs
- **Inputs**:
  - `legislative_rss_feeds` (Stream): Raw legal news updates.
- **Outputs**:
  - `regulatory_impact_summary` (str): Plain-English explanation of rule changes.

## Acceptance Criteria
- Alert the user of any relevant tax-code changes within 24 hours of their announcement.
- Categorize 100% of news items by "Impact Level" (Low, Medium, High).


---

## Source: lawyer\tax_loss_harvester.md

# Tax Loss Harvester (Agent 11.4)

## ID: `tax_loss_harvester`

## Role & Objective
The 'Deduction Finder'. Identifies unrealized losses in the portfolio that can be strategically harvested to offset capital gains and reduce total tax liability.

## Logic & Algorithm
- **Loss Scanning**: Monitors every open position for unrealized losses exceeding a user-defined threshold (e.g., $1,000).
- **Gain Offsetting**: Matches identified losses against realized capital gains from the current tax year.
- **Efficiency Scoring**: Prioritizes harvests that provide the most significant immediate tax benefit (Short-term vs. Long-term).

## Inputs & Outputs
- **Inputs**:
  - `open_positions_pnl` (Dict): Real-time unrealized profit/loss.
  - `realized_gains_ytd` (float): Current tax liability baseline.
- **Outputs**:
  - `harvest_recommendations` (List): Specific tickers and lot numbers to sell for a tax offset.

## Acceptance Criteria
- Identify 100% of harvestable losses that meet the defined "Efficiency Threshold".
- Coordinate with the Wash-Sale Watchdog to ensure no harvested losses are accidentally negated.


---

## Source: lawyer\wash_sale_watchdog.md

# Wash-Sale Watchdog (Agent 11.1)

## ID: `wash_sale_watchdog`

## Role & Objective
The 'Tax Guard'. Blocks trades that would trigger wash-sale tax violations (selling at a loss and rebuying within 30 days), protecting the portfolio's after-tax returns.

## Logic & Algorithm
- **Rebuy Monitoring**: Scans all realized losses from the last 30 days for any asset.
- **Trade Blocking**: Issues a "DENY" signal to the Trader department if a buy order is attempted for a recently sold losing position.
- **Replacement Sourcing**: Suggests similar but non-identical assets (e.g., a different ETF in the same sector) to maintain exposure without triggering the rule.

## Inputs & Outputs
- **Inputs**:
  - `realized_loss_history` (Dict): Tickers and dates of recent losses.
  - `pending_buy_orders` (List): Orders queued for execution.
- **Outputs**:
  - `compliance_decision` (Allow/Block): Permission status for each trade.

## Acceptance Criteria
- Block 100% of wash-sale violations across all connected brokerage accounts.
- Provide a "Replacement Asset" recommendation for 90% of blocked trades.


---

## Source: media_team\article_synthesizer.md

# Article Synthesizer (Agent 19.1)

## ID: `article_synthesizer`

## Role & Objective
The 'Ghostwriter'. Generates high-quality blog posts, articles, and long-form content based on institutional data, market research, and system events.

## Logic & Algorithm
- **Data Distillation**: Extracts key performance metrics and market signals to serve as the "ground truth" for content.
- **Narrative Framing**: Adapts the tone (e.g., Professional, Visionary, Urgent) based on the target audience and platform.
- **Fact-Checking Loop**: Queries the Data Scientist to verify any numerical claims made within the draft.

## Inputs & Outputs
- **Inputs**:
  - `content_prompt` (Text): "Write a quarterly review of our portfolio performance."
  - `system_data_feed` (JSON).
- **Outputs**:
  - `draft_article` (MD): Markdown-formatted content with charts and citations.

## Acceptance Criteria
- Produce a 500-word draft in < 45 seconds.
- Maintain 100% accuracy for all cited percentages and price points.


---

## Source: media_team\document_drafter.md

# Document Drafter (Agent 19.4)

## ID: `document_drafter`

## Role & Objective
The 'Technical Writer'. Creates professional PDFs, governance reports, whitepapers, and legal-adjacent documentation from system raw data.

## Logic & Algorithm
- **Template Application**: Maps data into standard institutional templates (e.g., "Monthly Audit," "New Strategy Proposal").
- **Citation Management**: Automatically generates bibliographies and links to on-chain transaction hashes or data sources.
- **WORM Storage Integration**: Ensures the final document is signed and stored in Immutable storage if marked as "Critical."

## Inputs & Outputs
- **Inputs**:
  - `report_data` (JSON).
  - `document_type` (Enum): Whitepaper, Audit, Proposal.
- **Outputs**:
  - `final_pdf` (URI): Path to the rendered PDF document.

## Acceptance Criteria
- Generate a 10-page report with 0 layout orphans or overflows.
- Ensure all PDF metadata (Author, Date, Version) is correctly populated.


---

## Source: media_team\mesh_architect.md

# Mesh Architect (Agent 19.5)

## ID: `mesh_architect`

## Role & Objective
The '3D Modeler'. Handles the generation, optimization, and conversion of 3D meshes (GLB/OBJ) for use in the system's "3D Graph Visualizer" or virtual reality environments.

## Logic & Algorithm
- **Geometry Generation**: Converts nodal data (e.g., the 19-department hierarchy) into a spatial 3D structure.
- **LOD Optimization**: Manages "Level of Detail" to ensure 3D visualizations remain performant on low-end hardware.
- **Texture Mapping**: Applies dynamic "Heatmap" textures to meshes based on real-time activity levels.

## Inputs & Outputs
- **Inputs**:
  - `graph_topology` (JSON).
  - `activity_metrics` (Data).
- **Outputs**:
  - `spatial_asset` (GLB): Optimized 3D model for Three.js.

## Acceptance Criteria
- Optimize 3D meshes to < 5MB file size for web rendering.
- Correctly map 100% of "Activity Heat" to vertex colors.


---

## Source: media_team\presentation_designer.md

# Presentation Designer (Agent 19.6)

## ID: `presentation_designer`

## Role & Objective
The 'Slide Deck Expert'. Creates professional-grade institutional presentations and slide decks from system-generated content and insights.

## Logic & Algorithm
- **Slideware Orchestration**: Breaks high-level narratives into "Slide Units" (Title, Bullet, Chart, Image).
- **Visual Hierarchy**: Ensures that key data points are emphasized through scale and color contrast.
- **Export Management**: Generates decks in multiple formats (PPTX, PDF, Interactive HTML).

## Inputs & Outputs
- **Inputs**:
  - `deck_narrative` (Text).
  - `chart_data` (List).
- **Outputs**:
  - `presentation_file` (PPTX): Professional slide deck.

## Acceptance Criteria
- Maintain a consistent "Institutional Theme" across 100% of slides.
- Support 3+ export formats for every created deck.


---

## Source: media_team\video_director.md

# Video Director (Agent 19.3)

## ID: `video_director`

## Role & Objective
The 'Showrunner'. Orchestrates the creation of video clips, animation sequences, and data visualizations for institutional presentations and social updates.

## Logic & Algorithm
- **Storyboard Generation**: Breaks down a video request into individual "Scenes" with specific visual and auditory requirements.
- **Asset Sequencing**: Coordinates with the Visual Aesthetics agent to generate backgrounds and overlays.
- **Timeline Assembly**: Uses FFmpeg or similar libraries to stitch assets into a coherent 10-60 second video clip.

## Inputs & Outputs
- **Inputs**:
  - `video_brief` (Text): "Create a 30-second wrap-up for the week's trading."
- **Outputs**:
  - `video_clip` (MP4): Fully rendered and encoded output.

## Acceptance Criteria
- Correctly sequence 100% of defined scenes from the brief.
- Output video in standard 1080p/60fps format.


---

## Source: media_team\visual_aesthetics_agent.md

# Visual Aesthetics Agent (Agent 19.2)

## ID: `visual_aesthetics_agent`

## Role & Objective
The 'Art Director'. Generates and refines high-fidelity images, UI mockups, and visual branding assets for the system's external and internal interfaces.

## Logic & Algorithm
- **Prompt Engineering**: Converts high-level visual descriptions into optimized diffusion model prompts.
- **Style Consistency**: Ensures all generated assets adhere to the current "Institutional Design Tokens" (Dark mode, glassmorphism, accent colors).
- **Asset Upscaling**: Manages the resolution and file-type conversion for different deployment targets (Web, Mobile, Print).

## Inputs & Outputs
- **Inputs**:
  - `image_request` (Text): "Generate a professional banner for the Banker department."
- **Outputs**:
  - `visual_asset` (URI): Path to the generated and optimized image.

## Acceptance Criteria
- Generate a preview mockup in < 20 seconds.
- 100% adherence to the defined color palette (HEX/HSL).


---

## Source: orchestrator\command_interpreter.md

# Command Interpreter (Agent 1.2)

## ID: `command_interpreter`

## Role & Objective
The linguistic gateway of the system. It translates natural language (voice or text) into structured, executable system calls that other agents can understand.

## Logic & Algorithm
1. **Verb Extraction**: Identifies primary actions (BUY, REBALANCE, AUDIT) using a high-precision whitelist.
2. **Entity Recognition**: Extracted Tickers, Amounts, and Dates using optimized Regex and NLP models.
3. **Context Sensitivity**: Resolves ambiguous terms (e.g., "Apple" to AAPL) based on portfolio context.
4. **Validation**: Scores output confidence to determine if a follow-up clarification is needed.

## Inputs & Outputs
- **Inputs**:
  - Raw User Text/Voice Transcripts
- **Outputs**:
  - Structured System Call (JSON)
  - Confidence Score

## Acceptance Criteria
- 99% accuracy on entity extraction for Tickers, Accounts, and Dates.
- Interpretation latency must be < 100ms for standard commands.


---

## Source: orchestrator\consensus\consensus_agents.md

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

## Source: orchestrator\context_weaver.md

# Context Weaver (Agent 1.6)

## ID: `context_weaver`

## Role & Objective
The system's short-term memory manager. It ensures that when a user or agent switches contexts (e.g., from Portfolio view to Tax view), the relevant history is injected so no information is lost.

## Logic & Algorithm
1. **Session Buffering**: Maintains a sliding window of the last 5 critical actions.
2. **Redis Coordination**: Persists context across Docker container restarts for zero-loss state.
3. **Knowledge Injection**: Dynamically builds prompt prefixes for LLM-based agents based on recent activity.

## Inputs & Outputs
- **Inputs**:
  - Agent Action Completion Events
  - Role-Switch Signals
- **Outputs**:
  - Formatted Context Strings
  - Redis State Updates

## Acceptance Criteria
- Injects 100% of the last 5 relevant actions into departmental role-switches.
- Context lookup latency must be < 10ms.


---

## Source: orchestrator\layout_morphologist.md

# Layout Morphologist (Agent 1.4)

## ID: `layout_morphologist`

## Role & Objective
The predictive UI engine. It ensures the user interface is always showing the most relevant information by anticipating the user's needs based on market conditions or system events.

## Logic & Algorithm
1. **Vol Trigger**: Monitors market volatility and automatically switches the GUI to the "Trader HUD" if a > 2% move occurs.
2. **Contextual Layout**: Adjusts widget positioning based on the active department the user is interacting with.
3. **Transition Management**: Coordinates smooth, sub-500ms transitions between complex D3/Three.js views.

## Inputs & Outputs
- **Inputs**:
  - Real-time Volatility Data
  - User Navigation Events
- **Outputs**:
  - UI State Transitions (JSON)
  - Widget Visibility Toggles

## Acceptance Criteria
- Auto-transition to Trader HUD within 500ms of high-volatility detection.
- Zero UI jank during layout morphing (maintain 60fps).


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

## Source: orchestrator\personas\persona_agents.md

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

## Source: orchestrator\red_team_sentry.md

# Red-Team Sentry (Agent 1.5)

## ID: `red_team_sentry`

## Role & Objective
The inner-kernel security enforcer. It audits every system call and code execution attempt within the agent workforce to prevent privilege escalation or malicious code injection.

## Logic & Algorithm
1. **Syscall Inspection**: Intercepts and validates all calls to sensitive modules (os, subprocess).
2. **Blacklist Enforcement**: Blocks any attempt to use dangerous patterns (eval, exec) from non-whitelisted agents.
3. **Emergency Isolation**: Issues an immediate SIGKILL to any agent container that violates the zero-trust protocols.

## Inputs & Outputs
- **Inputs**:
  - System Audit Logs
  - Code Execution Requests
- **Outputs**:
  - Safety Verdict (ALLOW/KILL)
  - Security Violation Reports

## Acceptance Criteria
- Immediate termination (SIGKILL) on any unauthorized attempt to use `os.system` or `eval`.
- Audit overhead must not exceed 2% of total CPU utilization.


---

## Source: orchestrator\synthesizer.md

# Synthesizer (Agent 1.1)

## ID: `synthesizer`

## Role & Objective
The central intelligence aggregator of the Sovereign OS. The Synthesizer is responsible for distilling thousands of granular agent logs and system events into a high-fidelity executive summary for the user.

## Logic & Algorithm
1. **Log Aggregation**: Ingests `agent.log` events from all 108 agents.
2. **Ledger Validation**: Compares internal briefing totals with the absolute truth stored in the Postgres ledger.
3. **Conflict Mapping**: Identifies divergent signals between departments (e.g., Strategist vs Trader) and queues them for resolution.
4. **Briefing Generation**: Synthesizes a daily Markdown report with cryptographic integrity checks.

## Inputs & Outputs
- **Inputs**: 
  - Kafka Activity Streams
  - Postgres Ledger Snapshots
  - Neo4j Relationship Data
- **Outputs**:
  - Daily Strategic Briefing (Markdown)
  - Conflict Resolution Queue (JSON)

## Acceptance Criteria
- Daily briefing totals must match the Postgres ledger to within 0.01% variance.
- Briefing generation must complete in under 5 seconds for a 24-hour log window.


---

## Source: orchestrator\traffic_controller.md

# Traffic Controller (Agent 1.3)

## ID: `traffic_controller`

## Role & Objective
The systemic safeguard for the message bus. It monitors the health of the Kafka infrastructure and manages backpressure to prevent "event-flooding" during market high-volatility events.

## Logic & Algorithm
1. **Lag Monitoring**: Tracks real-time consumer lag on critical topics (e.g., `market.live`).
2. **Backpressure Trigger**: Automatically activates message throttling if lag cross the 200ms safety threshold.
3. **Routing Optimization**: Dynamically re-prioritizes high-importance signals (e.g., Flash-Crash alerts) over routine logging.

## Inputs & Outputs
- **Inputs**:
  - Kafka Consumer Metrics
  - System Throughput Stats
- **Outputs**:
  - Backpressure Status (BOOLEAN)
  - Route Optimization Signals

## Acceptance Criteria
- Maintain consumer lag < 200ms during message spikes of up to 5,000 msg/sec.
- Backpressure state must propagate to all 18 departments within 50ms of activation.


---

## Source: physicist\black_swan_insurance_agent.md

# Black Swan Insurance Agent (Agent 6.6)

## ID: `black_swan_insurance_agent`

## Role & Objective
The "Tail-Risk Specialist". This agent manages the defensive layer of the portfolio, ensuring protection against rare, catastrophic market events.

## Logic & Algorithm
1. **Protection Sourcing**: Allocates a fixed monthly budget to deep Out-of-the-Money (OTM) protective options.
2. **Rolling Coverage**: Ensures there are no gaps in insurance coverage as options approach expiration.
3. **Budget Optimization**: Aggressively buys tail-protection when Implied Volatility (IV) is at historical lows (Cheap Insurance).

## Inputs & Outputs
- **Inputs**:
  - `portfolio_value` (float): Total AUM for sizing.
  - `insurance_budget` (float): Max allowed monthly premium spend.
- **Outputs**:
  - `insurance_status` (COVERED/UNINSURED).
  - `payout_at_minus_25pct` (float): Projected USD gain in a crash scenario.

## Acceptance Criteria
- 100% portfolio coverage against any single-day market drop exceeding 15%.
- Maintain an "insurance premium" spend of < 1.5% of total portfolio equity per annum.


---

## Source: physicist\delta_hedger.md

# Delta Hedger (Agent 6.4)

## ID: `delta_hedger`

## Role & Objective
The "Risk Neutralizer". The Delta Hedger ensures the portfolio's directional risk is mathematically neutralized according to the specific safety tolerances of the Sovereign OS.

## Logic & Algorithm
1. **Exposure Summation**: Aggregates net delta (directional bias) from all assets (Stocks, Options, Futures).
2. **Neutralization Math**: Calculates the exact number of shares or futures needed to offset the current bias.
3. **Drift Enforcement**: Automatically triggers hedge adjustments whenever the net portfolio delta drifts more than 5% from its neutral target.

## Inputs & Outputs
- **Inputs**:
  - `position_deltas` (Dict): Delta breakdown by asset class.
  - `risk_policy` (Dict): Safety thresholds.
- **Outputs**:
  - `hedge_adjustment_qty` (int): Units required for re-neutralization.

## Acceptance Criteria
- Maintain a net portfolio delta within the ±5% safety band at all times.
- Hedge adjustments must be executed with a preference for liquidity-rich instruments (e.g., SPY or ES Futures).


---

## Source: physicist\gamma_warning_system.md

# Gamma Warning System (Agent 6.3)

## ID: `gamma_warning_system`

## Role & Objective
The "Market Acceleration Monitor". Detects when large price swings are being forced by the institutional need to hedge large option positions (Dealer Gamma).

## Logic & Algorithm
1. **Net Gamma Calculation**: Aggregates open interest to estimate the combined hedging requirement of market makers.
2. **Pin Detection**: Identifies specific "Magnetic" strikes (Pins) where price is likely to settle during monthly opex.
3. **Acceleration Alerts**: Warns when the market enters "Short Gamma" regimes, where volatility is likely to become convex and explosive.

## Inputs & Outputs
- **Inputs**:
  - `open_interest_data` (Dict): Exchange-wide OI snapshots.
  - `current_market_price` (float): Underlying spot price.
- **Outputs**:
  - `gamma_exposure_score` (float): Predicted volatility multiplier.
  - `volatility_forecast` (STABLE/ACCELERATING).

## Acceptance Criteria
- Successfully predict Gamma-induced "Flip Zones" (where market character changes) with 75% accuracy.
- Alert the Trader department within 10 seconds of price breaching a major Gamma support level.


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

## Source: physicist\probability_modeler.md

# Probability Modeler (Agent 6.5)

## ID: `probability_modeler`

## Role & Objective
The "System Odds-Maker". This agent uses advanced statistical distributions to calculate the exact probability of specific financial outcomes.

## Logic & Algorithm
1. **Distribution Selection**: Utilizes Log-Normal and Cauchy distributions to model asset returns, accounting for "Fat Tails".
2. **EV Assessment**: Calculates the Expected Value (EV) for every open trade idea produced by the Strategist department.
3. **Profit Visibility**: Generates Probability of Profit (POP) and Probability of Touch (POT) metrics for the front-end dashboard.

## Inputs & Outputs
- **Inputs**:
  - `ticker_history` (List): Returns data for distributional fit.
  - `option_ivs` (float): The market's forward-looking volatility.
- **Outputs**:
  - `p_hit_target` (float): Probability of price reaching X by date Y.
  - `expected_move_1sd` (float): Statistically anticipated price range.

## Acceptance Criteria
- Calculate 1,000+ Monte Carlo price paths for an asset in under 1 second.
- Probability projections must align with historical realized outcomes within a 5% margin of error.


---

## Source: physicist\theta_collector.md

# Theta Collector (Agent 6.1)

## ID: `theta_collector`

## Role & Objective
The "Time-Decay Harvester". The Theta Collector ensures the portfolio generates consistent income through the mathematical erosion of option value over time.

## Logic & Algorithm
1. **Decay Tracking**: Calculates dailyUSD impact of time-decay across all option holdings.
2. **Acceleration Detection**: Identifies positions entering the "Gamma/Theta Ramp" (last 30-45 days of life) where decay is most aggressive.
3. **Strategic Ingestion**: Recommends high-probability short-dated option sales (Covered Calls, Puts) to maintain target daily yields.

## Inputs & Outputs
- **Inputs**:
  - `option_positions` (List): Tickers, strikes, and expiries.
  - `target_daily_yield` (float): Minimum desired USD daily decay.
- **Outputs**:
  - `theta_snapshot` (float): Total portfolio theta.
  - `yield_projections` (Dict): Projected income for 7/30 day windows.

## Acceptance Criteria
- Maintain a portfolio-wide positive theta balance as defined by the risk policy.
- Provide yield projections accurate to within 2% of actual decay, assuming constant price.


---

## Source: physicist\volatility_surface_mapper.md

# Volatility Surface Mapper (Agent 6.2)

## ID: `volatility_surface_mapper`

## Role & Objective
The "Surface Architect". This agent maps Implied Volatility (IV) across all available strikes and expiries to identify statistical mispricing in the options market.

## Logic & Algorithm
1. **Mesh Construction**: Builds a 3D visualization of IV (the 'Smile' or 'Smirk') for major underlying assets.
2. **Skew Analysis**: Compares the pricing of downside protection (Puts) vs upside speculation (Calls).
3. **Mean Reversion Scoring**: Flags strikes where IV is significantly stretched compared to its 20-day moving average.

## Inputs & Outputs
- **Inputs**:
  - `option_chain_data` (Dict): Comprehensive pricing/IV data.
- **Outputs**:
  - `v_surface_3d` (List): Data points for 3D UI render.
  - `skew_alert` (Dict): Deep-dive into skew deviations.

## Acceptance Criteria
- Reconstruct the global volatility surface every 5 minutes during market hours.
- Identify "cheap" vs "expensive" volatility with 90% confidence based on historical standard deviation.


---

## Source: refiner\agent_performance_reviewer.md

# Agent Performance Reviewer (Agent 17.3)

## ID: `agent_performance_reviewer`

## Role & Objective
The 'Quality Judge'. Ranks multiple LLM outputs (e.g., comparing Claude 3.5 vs. Gemini 1.5 Pro) to select the most logically sound and safe response for a given task.

## Logic & Algorithm
- **Multi-Model Consensus**: Runs critical prompts through multiple models simultaneously.
- **Voting Mechanism**: Uses a weighted "Reviewer" logic to select the best output based on adherence to instructions.
- **Dynamic Routing**: Recommends which model is "Winning" for specific categories (e.g., "Physicist tasks are better handled by Gemini").

## Inputs & Outputs
- **Inputs**:
  - `multi_model_outputs` (Dict): Responses from different AI engines.
- **Outputs**:
  - `selected_best_response` (str).
  - `leaderboard_update` (Dict): Updated performance stats for each model provider.

## Acceptance Criteria
- Achieve a "Selection Accuracy" of > 95% when compared against human expert preference.
- Maintain a latency overhead of < 500ms for the review process.


---

## Source: refiner\autocoder_agent.md

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

## Source: refiner\context_window_manager.md

# Context Window Manager (Agent 17.6)

## ID: `context_window_manager`

## Role & Objective
The 'System Optimizer'. Dynamically adjusts temperature, top-p, frequency penalties, and "Context Window" depth for all agents based on the urgency and nature of the task.

## Logic & Algorithm
- **Hyperparameter Tuning**: Lowers "Temperature" for financial calculations and increases it for "Creative Strategy brainstorming."
- **Focus Narrowing**: Automatically trims long conversation histories to fit within the "Sweet Spot" of a model's context window.
- **Self-Correction Trigger**: If a model produces a "Garbage" or recursive output, this agent resets the parameters and tries a different configuration.

## Inputs & Outputs
- **Inputs**:
  - `active_task_metadata` (Dict): Urgency, type, and source.
- **Outputs**:
  - `llm_parameter_set` (Dict): Temp, TopP, MaxTokens, ContextDepth.

## Acceptance Criteria
- Ensure 0% "Context Overflow" errors across the entire workforce.
- Achieve a 10% improvement in "Task Precision" through task-specific hyperparameter tuning.


---

## Source: refiner\hallucination_sentinel.md

# Hallucination Sentinel (Agent 17.1)

## ID: `hallucination_sentinel`

## Role & Objective
The 'LLM Refiner'. Iteratively tests and improves the system prompts across all departments to reduce hallucination and ensure that LLM outputs adhere strictly to institutional logic and verified facts.

## Logic & Algorithm
- **Fact-Check Loop**: Cross-references LLM assertions against the Historian's "Verified Truth" database.
- **Reference Validation**: Ensures that every claim made by an agent (e.g., "The S&P is up 2%") is backed by an actual data point from a trusted source.
- **Syntactic Audit**: Rejects responses that fail to adhere to the required JSON or Markdown structure.

## Inputs & Outputs
- **Inputs**:
  - `agent_raw_responses` (Stream): The output from any agent in the workforce.
- **Outputs**:
  - `audit_pass_fail` (Bool).
  - `hallucination_report` (Dict): Specific areas of logic failure.

## Acceptance Criteria
- Achieve a hallucination rate of < 0.1% for high-stakes financial decisions.
- Successfully block 100% of responses containing "Confidently Wrong" numerical data.


---

## Source: refiner\model_router.md

# Model Router (Agent 17.5)

## ID: `model_router`

## Role & Objective
The 'Token Saver'. Compresses long conversational histories and identifies which tasks can be handled by "Cheap" models versus "Premium" models to optimize costs.

## Logic & Algorithm
- **Complexity Estimation**: Predicts the difficulty of a task before it's sent to an LLM.
- **Cost-Weighted Routing**: Sends easy tasks (e.g., "Summarize this email") to Haiku/Flash and hard tasks (e.g., "Math-heavy Options Greek analysis") to Opus/Ultra.
- **Availability Switching**: Automatically routes traffic to secondary providers if a primary API experiences downtime.

## Inputs & Outputs
- **Inputs**:
  - `pending_task_queue` (List).
- **Outputs**:
  - `routed_model_selection` (str): e.g., "gemini-1.5-flash".

## Acceptance Criteria
- Reduce average cost per task by 40% through intelligent routing.
- Maintain 99.9% uptime by successfully failing over between model providers.


---

## Source: refiner\performance_reviewer_agent.md

# Performance Reviewer (Agent 17.3)

## ID: `performance_reviewer_agent`

## Role & Objective
The 'Quality Judge'. Ranks multiple LLM outputs to select the most logically sound, safe, and efficient response. Acts as the final filter before a response is sent to the Orchestrator.

## Logic & Algorithm
- **Candidate Evaluation**: Scores multiple responses based on "Factuality," "Coherence," and "Safety."
- **Model Consensus**: Compares the output of a primary model (e.g., Gemini) with a secondary validator (e.g., Claude or GPT) if the task complexity is high.
- **Safety Shield**: Filters out any response that violates institutional privacy or security protocols.

## Inputs & Outputs
- **Inputs**:
  - `candidate_responses` (List): Multiple versions of the same answer.
- **Outputs**:
  - `winning_response` (String): The optimal content to return.

## Acceptance Criteria
- Select the objectively better answer 95% of the time in A/B testing.
- Block 100% of responses containing sensitive system configuration details.


---

## Source: refiner\prompt_optimizer.md

# Prompt Optimizer (Agent 17.4)

## ID: `prompt_optimizer`

## Role & Objective
The 'Signal Extractor'. Sanitizes raw data feeds and complex user requests into "Prompt-Ready" structures that maximize the reasoning capabilities of the agent workforce.

## Logic & Algorithm
- **Information Density Maximization**: Rephrases clunky user requests into structured systemic instructions.
- **Context Prioritization**: Moves the most critical data points to the "Start" or "End" of the prompt to avoid "Lost in the Middle" errors.
- **Instruction Injection**: Automatically adds mandatory safety and formatting constraints to every outgoing prompt.

## Inputs & Outputs
- **Inputs**:
  - `raw_interactive_input` (Text).
- **Outputs**:
  - `optimized_prompt_structure` (Text): The refined instruction set.

## Acceptance Criteria
- Increase "First-Shot Success Rate" for complex tasks by 15% through prompt refinement.
- Ensure 100% of optimized prompts include the "Zero-Trust" safety headers.


---

## Source: refiner\token_efficiency_reaper.md

# Token Efficiency Reaper (Agent 17.2)

## ID: `token_efficiency_reaper`

## Role & Objective
The 'Custom Brain' manager. Prepares training data for local or private LLM fine-tuning and monitors the token consumption vs logic-quality ratio of the system.

## Logic & Algorithm
- **Training Set Curation**: Selects high-quality interactions where the Orchestrator successfully solved a complex task.
- **Synthetic Data Generation**: Uses GPT-4o to generate diversified training examples for smaller, faster local models (e.g., Llama 3).
- **Redundancy Pruning**: Removes repetitive tokens or low-value filler words from agent prompts to reduce API costs.

## Inputs & Outputs
- **Inputs**:
  - `historical_interaction_logs` (Stream).
- **Outputs**:
  - `fine_tuning_dataset` (JSONL): Valid formatting for model training.

## Acceptance Criteria
- Reduce total token consumption by 20% without decreasing the "Logic Score" of the system.
- Produce 1,000+ high-fidelity training pairs per month for local model refinement.


---

## Source: sentry\api_key_rotator.md

# API Key Rotator (Agent 8.2)

## ID: `api_key_rotator`

## Role & Objective
The 'Internal Auditor'. Periodically attempts to 'hack' the system's own logic to find vulnerabilities and manages the lifecycle of all external API credentials.

## Logic & Algorithm
- **Automated Rotation**: Enforces 30-day rotation cycles for all brokerage and data provider API keys.
- **Secrets Management**: Interfaces with the encrypted vault to update environment variables across the container fleet.
- **Vulnerability Scanning**: Simulates unauthorized access attempts to verify the integrity of the Permission Auditor's gates.

## Inputs & Outputs
- **Inputs**:
  - `active_secrets_inventory` (Dict): List of service keys and their expiration dates.
- **Outputs**:
  - `rotation_status` (Success/Fail): Confirmation of key updates.
  - `vulnerability_report` (List): Identified weak points in the internal logic.

## Acceptance Criteria
- 100% of external API keys must be rotated without service downtime.
- New credentials must be propagated to all microservices within 10 seconds of creation.


---

## Source: sentry\breach_sentinel.md

# Breach Sentinel (Agent 8.1)

## ID: `breach_sentinel`

## Role & Objective
The 'Traffic Gatekeeper'. Monitors all incoming API requests and WebSocket connections for malicious patterns, ensuring the digital perimeter remains uncompromised.

## Logic & Algorithm
- **Anomaly Detection**: Analyzes request frequency and payload size to detect DDoS or injection attempts.
- **Pattern Matching**: Checks incoming traffic against known exploit signatures.
- **Auto-Throttle**: Implementation of circuit breakers that temporarily block IPs showing aggressive behavior.

## Inputs & Outputs
- **Inputs**:
  - `incoming_traffic_stream` (Stream): Raw network logs and API headers.
- **Outputs**:
  - `threat_level` (Score): 0-100 rating of active malicious activity.
  - `block_list` (List): IPs to be banned at the load balancer level.

## Acceptance Criteria
- Identify and throttle 99% of brute-force attempts within 3 failed login cycles.
- Maintain a latency overhead of < 5ms for all pass-through traffic.


---

## Source: sentry\cold_storage_auditor.md

# Cold Storage Auditor (Agent 8.4)

## ID: `cold_storage_auditor`

## Role & Objective
The 'Governance Auditor'. Ensures all code changes and trade activities follow pre-defined SEC and departmental rules, specifically focusing on the integrity of air-gapped or restricted assets.

## Logic & Algorithm
- **Integrity Checking**: Verifies checksums of offline data backups and cold wallet transaction history.
- **Compliance Mapping**: Checks every outbound trade against a "Restricted List" of assets.
- **Air-Gap Verification**: Monitors the "Hardware Bridge" to ensure cold wallets are only connected during authorized signing sessions.

## Inputs & Outputs
- **Inputs**:
  - `checksum_registry` (List): Hashes of critical data assets.
  - `compliance_policy` (Rules): SEC and internal trading constraints.
- **Outputs**:
  - `integrity_score` (float): Confirmation that historical data hasn't been tampered with.

## Acceptance Criteria
- Detect any unauthorized modification to historical audit logs within 1 second.
- Block 100% of trades that violate the internal "Cold Storage Only" asset list.


---

## Source: sentry\permission_auditor.md

# Permission Auditor (Agent 8.5)

## ID: `permission_auditor`

## Role & Objective
The 'Grand Keymaster'. Manages and audits the distribution of encryption keys and user/agent permissions across the entire Docker subnet.

## Logic & Algorithm
- **RBAC Enforcement**: Validates that every agent request is authorized for the specific data node (Postgres, Neo4j, Redis).
- **Encryption Handshake**: Orchestrates the TLS/SSL cert distribution to internal microservices.
- **Privilege Reaper**: Automatically revokes "Admin" or "Write" access from agents that have been inactive for more than 24 hours.

## Inputs & Outputs
- **Inputs**:
  - `agent_request_token` (JWT): Identity and scope of the requesting agent.
- **Outputs**:
  - `auth_decision` (Allow/Deny): Perimeter clearance status.

## Acceptance Criteria
- Grant or deny access requests in < 2ms to ensure zero impact on system throughput.
- Audit 100% of "Elevated Privilege" sessions and store them in the Historian's immutable ledger.


---

## Source: sentry\protector_agent.md

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

## Source: sentry\recovery_path_builder.md

# Recovery Path Builder (Agent 8.6)

## ID: `recovery_path_builder`

## Role & Objective
The 'Eternal Scribe'. Categorizes and stores every event in the system for historical review, creating a "Black Box" recorder for institutional recovery.

## Logic & Algorithm
- **Event Serialization**: Converts complex Kafka message streams into structured, searchable JSON archives.
- **Failure Simulation**: Works with the Stress-Tester to build "Restore Points" after simulated system crashes.
- **Trace Reconstruction**: Maps chronological events to specific user intents for forensic debugging.

## Inputs & Outputs
- **Inputs**:
  - `all_system_events` (Bus): The master Kafka stream for the department.
- **Outputs**:
  - `recovery_snapshot` (DB): Optimized partitions for fast historical state reconstruction.

## Acceptance Criteria
- Reconstruct the full state of the Sovereign OS to any point in the last 72 hours in < 5 minutes.
- Ensure zero loss of event data even during peak traffic (10k+ events/sec).


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

## Source: sentry\travel_mode_guard.md

# Travel Mode Guard (Agent 8.3)

## ID: `travel_mode_guard`

## Role & Objective
The 'Anomaly Watcher'. Monitors internal system logs and device telemetry for 'unusual' agent or user behavior that might indicate a physical or digital compromise (e.g., travel-based login shifts).

## Logic & Algorithm
- **Geofencing**: Tracks the Euclidean distance between the primary workstation and secondary mobile devices.
- **Behavioral Profiling**: Flags transactions that occur outside of defined "Safe Zones" or at unusual hours.
- **Travel Protocol**: When "Travel Mode" is active, restricts the Banker department's ability to move high-value funds without secondary biometric confirmation.

## Inputs & Outputs
- **Inputs**:
  - `device_coordinates` (Lat/Lon): Real-time telemetry from authorized devices.
  - `activity_logs` (Stream): User interaction timestamps and locations.
- **Outputs**:
  - `divergence_alert` (Bool): Trigger for system-wide lockout if proximity thresholds are breached.

## Acceptance Criteria
- Detect device divergence of > 100 miles within 60 seconds of a sync event.
- Trigger "Travel Mode" restrictions with 100% reliability when geofence boundaries are exited.


---

## Source: steward\inventory_agent.md

# Inventory Agent (Agent 9.3)

## ID: `inventory_agent`

## Role & Objective
The 'Physical Stockman'. Tracks high-value physical assets (watches, jewelry, electronics, art) for insurance and net-worth purposes.

## Logic & Algorithm
- **Asset Registry**: Maintains a cryptographically signed list of luxury assets and their purchase receipts (stored in the Lawyer's vault).
- **Index Tracking**: For assets like luxury watches or fine art, tracks secondary market indices (e.g., Subdial, Chrono24) to adjust valuations.
- **Insurance Audit**: Compares the sum of the inventory value against the current "Personal Articles Floater" coverage.

## Inputs & Outputs
- **Inputs**:
  - `asset_ledger` (List): Item descriptions, serial numbers, and purchase prices.
  - `market_index_feeds` (Data): Pricing trends for luxury collectables.
- **Outputs**:
  - `inventory_valuation` (float): Total USD value of inventoried luxury goods.

## Acceptance Criteria
- Re-index luxury asset valuations quarterly based on global secondary market trends.
- Notify the user if inventory value exceeds insurance coverage by more than 10%.


---

## Source: steward\maintenance_scheduler.md

# Maintenance Scheduler (Agent 9.6)

## ID: `maintenance_scheduler`

## Role & Objective
The 'Preventative Guard'. Tracks service schedules for home, car, and major equipment to prevent costly emergency repairs and maintain asset longevity.

## Logic & Algorithm
- **Schedule Management**: Maintains a chronological log of HVAC service, oil changes, roof inspections, and water filtration cycles.
- **Sinking Fund Interaction**: Informs the Guardian department of upcoming "Maintenance Events" so capital is reserved in advance.
- **Manual Log**: Allows the user to photo-document repairs and store them in the Historian's asset timeline.

## Inputs & Outputs
- **Inputs**:
  - `asset_life_cycles` (Dict): Industry-standard service intervals for property and vehicles.
- **Outputs**:
  - `upcoming_maintenance_calendar` (List): 12-month schedule of required service actions.

## Acceptance Criteria
- Alert the user 14 days prior to any required PM (Preventative Maintenance) event.
- Maintain a digital "Service History" with 100% uptime for insurance and resale purposes.


---

## Source: steward\procurement_bot.md

# Procurement Bot (Agent 9.4)

## ID: `procurement_bot`

## Role & Objective
The 'Smart Shopper'. Analyzes household recurring purchases and identifies bulk-buying or subscription optimization opportunities.

## Logic & Algorithm
- **Consumption Analysis**: Identifies patterns in spending on essentials (groceries, utilities, supplies) using the Banker's transaction data.
- **Price Comparison**: Scans Amazon, Costco, and specialized retailers to find lower unit prices for frequently purchased items.
- **Subscription Reaper**: Flags duplicate or under-utilized digital subscriptions (e.g., multiple streaming services) for the user to "Kill".

## Inputs & Outputs
- **Inputs**:
  - `household_transaction_history` (Data): Stream of commerce alerts.
- **Outputs**:
  - `bulk_buy_recommendations` (List): Items that should be bought in volume for X% savings.
  - `subscription_kill_list` (List): Proposed cancellations.

## Acceptance Criteria
- Identify at least $100/mo in recurring savings within the first 30 days of operation.
- Achieve 95% accuracy in matching transaction strings to specific household product categories.


---

## Source: steward\property_manager.md

# Property Manager (Agent 9.1)

## ID: `property_manager`

## Role & Objective
The 'Real Estate Scribe'. Tracks property valuations, taxes, and mortgage health for physical real estate assets, ensuring real-world equity is accurately reflected in the digital net worth.

## Logic & Algorithm
- **Valuation Tracking**: Interfaces with real estate APIs (Zillow, Redfin) to obtain monthly "Zestimates" or equivalent data.
- **Equity Calculation**: Subtracts outstanding mortgage balances from current market value to determine net real estate equity.
- **Tax Monitor**: Tracks property tax cycles and deadlines to ensure escrow or manual payments are planned for by the Guardian department.

## Inputs & Outputs
- **Inputs**:
  - `property_addresses` (List): Locations of physical holdings.
  - `mortgage_statements` (Dict): Outstanding balances and interest rates.
- **Outputs**:
  - `net_property_equity` (float): Aggregate USD value of real estate equity.

## Acceptance Criteria
- Update physical asset valuations within 1% of market-standard API data monthly.
- Alert the Orchestrator 30 days before property tax deadlines.


---

## Source: steward\vehicle_fleet_ledger.md

# Vehicle Fleet Ledger (Agent 9.2)

## ID: `vehicle_fleet_ledger`

## Role & Objective
The 'Mobility Auditor'. Tracks car valuations, fuel efficiency, and depreciation schedules for the user's vehicle fleet.

## Logic & Algorithm
- **Depreciation Modeling**: Uses standard mileage-based and age-based depreciation curves to estimate private vehicle value.
- **Operating Cost Analysis**: Aggregates gas, insurance, and charging costs to calculate "Cost Per Mile" (CPM).
- **Secondary Market Pulse**: Monitors private sale listings for similar models to refine the valuation mesh.

## Inputs & Outputs
- **Inputs**:
  - `vehicle_vin_list` (List): Vehicle identification numbers.
  - `fuel_receipt_stream` (Data): Log of operating expenses.
- **Outputs**:
  - `fleet_liquidation_value` (float): Estimated USD if all vehicles were sold today.
  - `cpm_metrics` (float): Cost-per-mile efficiency score.

## Acceptance Criteria
- Maintain vehicle valuations within 5% of Kelly Blue Book or equivalent trade-in values.
- Categorize 100% of vehicle-related expenses from the Banker's transaction stream.


---

## Source: steward\wellness_sync.md

# Wellness Sync (Agent 9.5)

## ID: `wellness_sync`

## Role & Objective
The 'Human Capital Monitor'. Tracks lifestyle metrics (sleep, focus, activity) that impact financial decision-making quality and long-term health benchmarks.

## Logic & Algorithm
- **Data Ingestion**: Syncs with Apple Health/Google Fit to monitor biometric stability (RHR, HRV, Sleep Duration).
- **Decision Correlation**: Cross-references "Poor Sleep" nights with "Impulsive" trades or budget breaches identified by the Auditor.
- **Lifestyle Scoring**: Provides a "Readiness" score to the Orchestrator, influencing the priority of high-stress tasks.

## Inputs & Outputs
- **Inputs**:
  - `biometric_data` (Stream): Health metrics from authorized wearables.
- **Outputs**:
  - `readiness_score` (0-100): Daily metric of cognitive and physical performance potential.

## Acceptance Criteria
- Maintain biometric data privacy by storing raw health feeds in a local, encrypted node.
- Provide a daily readiness score within 30 minutes of the user's wake event.


---

## Source: strategist\conviction_analyzer.md

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

## Source: strategist\edge_decay_monitor.md

# Edge Decay Monitor (Agent 4.5)

## ID: `edge_decay_monitor`

## Role & Objective
The "Strategy Auditor". Monitors live performance vs historical expectations to detect "Alpha Decay"—the statistical vanishing of a trading edge.

## Logic & Algorithm
1. **Benchmarking**: Compares current Sharpe/Sortino ratios against the strategy's historical backtest performance.
2. **Regime Detection**: Identifies if the current market environment (e.g., high volatility) has shifted away from the strategy's profitable regime.
3. **Retirement Sentinel**: Issues automated warnings to de-risk or retire strategies that are failing to meet statistical benchmarks.

## Inputs & Outputs
- **Inputs**:
  - `live_performance` (Dict): Recent P&L and reward stats.
  - `historical_expectations` (Dict): Backtest baseline.
- **Outputs**:
  - `decay_status` (STABLE/DEGRADING/FAILED).
  - `retirement_alert` (bool): Flag to halt the strategy.

## Acceptance Criteria
- Issue a 'DEGRADING' warning if a strategy underperforms its backtest mean by 1 standard deviation for 30 consecutive days.
- Detect regime shifts within 5 trading days of a fundamental market character change.


---

## Source: strategist\logic_architect.md

# Logic Architect (Agent 4.1)

## ID: `logic_architect`

## Role & Objective
The "Strategy Designer" of the Sovereign OS. The Logic Architect converts qualitative investment theses into structured, executable code blocks for the backtesting engine.

## Logic & Algorithm
1. **Thesis Parsing**: Analyzes natural language strategy descriptions (e.g., 'Buy when RSI < 30 and volume spikes').
2. **Blueprint Generation**: Outputs JSON objects defining entry/exit rules and risk parameters.
3. **Circular Dependency Check**: Validates that strategies do not rely on future data or circular logic.

## Inputs & Outputs
- **Inputs**:
  - `strategy_thesis` (str): Qualitative description of a trading signal.
- **Outputs**:
  - `code_blueprint` (Dict): Structured entry/exit rules and risk parameters.

## Acceptance Criteria
- Successfully parse and convert 95% of standard technical analysis patterns into executable JSON.
- Blueprint generation must complete in under 500ms.


---

## Source: strategist\opportunity_screener.md

# Opportunity Screener (Agent 4.4)

## ID: `opportunity_screener`

## Role & Objective
The "Watchlist Filter". Scans the entire asset universe (Top 500+) for specific technical or fundamental setups that match the current strategy playbook.

## Logic & Algorithm
1. **Parallel Screening**: Applies Logic Architect filters across thousands of ticker data points.
2. **Alpha Ranking**: Ranks matching assets by their expected risk-adjusted return (Sharpe expectancy).
3. **Signal Guarding**: Flags high-conviction signals to the Orchestrator for human-in-the-loop approval.

## Inputs & Outputs
- **Inputs**:
  - `universe_data` (List): Price and volume snapshots for symbols.
  - `screen_criteria` (Dict): Multi-factor filters (PE, RSI, Momentum).
- **Outputs**:
  - `filtered_watchlist` (List): Tickers meeting criteria, ranked by score.

## Acceptance Criteria
- Screen 500+ symbols against 5+ technical criteria in under 1 second.
- False positive rate for signal detection must be < 5% when compared to backtest logic.


---

## Source: strategist\playbook_evolutionist.md

# Playbook Evolutionist (Agent 4.6)

## ID: `playbook_evolutionist`

## Role & Objective
The "Meta-Learner". Improving strategy parameters based on actual outcomes. It ensures the Sovereign OS learns from its mistakes and successes.

## Logic & Algorithm
1. **Outcome Feedback**: Feeds successful and failed trade results back into the parameter optimizer.
2. **Mistake Classification**: Analyzes trade slippage and execution errors to tighten future strategy constraints.
3. **Incremental Improvement**: Proposes weekly parameter tweaks to the Logic Architect based on cross-sectional performance data.

## Inputs & Outputs
- **Inputs**:
  - `trade_history` (List): Full ledger of past outcomes.
  - `optimization_goals` (e.g., 'Minimize Drawdown').
- **Outputs**:
  - `proposed_tweaks` (Dict): Suggested changes to strategy constants.

## Acceptance Criteria
- Proposed tweaks must demonstrate a backtested improvement of at least 1% in the Sharpe ratio before being submitted for approval.
- The evolutionist must document the "Reasoning Path" for every proposed change.


---

## Source: strategist\rebalance_bot.md

# Rebalance Bot (Agent 4.3)

## ID: `rebalance_bot`

## Role & Objective
The "Portfolio Gardener". The Rebalance Bot ensures the portfolio stays within its target strategic allocation bands, managing drift and maintaining the intended risk profile.

## Logic & Algorithm
1. **Drift Assessment**: Compares current asset weights in the ledger against the target model.
2. **Trade Generation**: Calculates the exact buy/sell orders needed to return to the target allocation.
3. **Tax Optimization**: Prioritizes tax-loss harvesting during the exit of overweight positions.

## Inputs & Outputs
- **Inputs**:
  - `target_weights` (Dict): Ideal asset percentage breakdown.
  - `live_positions` (Dict): Current portfolio held in the ledger.
- **Outputs**:
  - `rebalance_orders` (List): specific trade requests.
  - `drift_delta` (float): Total percentage variance from the model.

## Acceptance Criteria
- Trigger rebalance notifications within 60 seconds of any asset drifting more than 2.5% from its target.
- Trade generation must minimize transaction costs by aggregation across accounts.


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

## Source: strategist\stress_tester.md

# Stress Tester (Agent 4.2)

## ID: `stress_tester`

## Role & Objective
The "Adversarial Agent". The Stress Tester subjects strategies to artificial market shocks and liquidity droughts to identify their "Burst Point".

## Logic & Algorithm
1. **Monte Carlo Attack**: Runs historical simulations with 'fat tail' risk parameters (rare but extreme events).
2. **Shocks Injection**: Simulates specific trauma (Credit Crunch, Flash Crash, Hyperinflation).
3. **Fragility Analysis**: Calculates the drawdown levels and likelihood of portfolio wipeout.

## Inputs & Outputs
- **Inputs**:
  - `baseline_strategy` (Dict): The strategy blueprint to attack.
  - `shock_vectors` (List): Types of market trauma to simulate.
- **Outputs**:
  - `fragility_report` (Dict): failure modes and max drawdown projections.
  - `survival_probability` (float): Likelihood of surviving a decade of volatility.

## Acceptance Criteria
- Fragility reports must identify the exact asset price move that results in a 50%+ drawdown.
- Survival probability calculations must be accurate to within 1% based on historical fat-tail distributions.


---

## Source: stress_tester\black_swan_randomizer.md

# Black Swan Randomizer (Agent 16.2)

## ID: `black_swan_randomizer`

## Role & Objective
The 'Network Slower'. Injects artificial latency into the inter-agent message bus (Kafka/Redis) to test the system's resilience to "Jitter" and slow execution environments.

## Logic & Algorithm
- **Latency Spiking**: Randomly delays a percentage of messages by 10ms to 5,000ms.
- **Race Condition Finder**: Specifically targets sequential dependencies to see if asynchronous out-of-order delivery breaks the state machine.
- **Threshold Testing**: Identifies the "Breaking Point" where increased latency causes the circuit breakers to trip.

## Inputs & Outputs
- **Inputs**:
  - `inter_agent_traffic` (Bus): The stream of data between departments.
- **Outputs**:
  - `latency_tolerance_score` (float): The maximum delay the system can handle before logic failure.

## Acceptance Criteria
- Identify the exact latency threshold where trading logic becomes unreliable.
- Ensure 100% adherence to "Time-to-Live" (TTL) constraints for all financial commands.


---

## Source: stress_tester\cascade_failure_detector.md

# Cascade Failure Detector (Agent 16.4)

## ID: `cascade_failure_detector`

## Role & Objective
The 'Flash Crowd' simulator. Floods individual components (API Gateway, DB, Workers) with 1,000x normal request volume to find the breaking point and test horizontal autoscaling.

## Logic & Algorithm
- **Load Generation**: Uses distributed stress-testing tools (e.g., Locust or JMeter) to hammer the system with concurrent requests.
- **Resource Profiling**: Monitors CPU, Memory, and Disk I/O to identify which process fails first under pressure.
- **Circuit Breaker Audit**: Verifies that the system "Fails Gracefully" by shutting down non-critical UI features while preserving the core trade-engine.

## Inputs & Outputs
- **Inputs**:
  - `target_service_endpoints` (List).
- **Outputs**:
  - `load_test_report` (Dict): Throughput (RPS), Error Rate, and Scaling latency.

## Acceptance Criteria
- Identify the "Maximum Capacity" of the API gateway within a 5% error margin.
- Successfully scale from 1 to 10 worker nodes in < 60 seconds under 80% CPU load.


---

## Source: stress_tester\liquidation_optimizer.md

# Liquidation Optimizer (Agent 16.3)

## ID: `liquidation_optimizer`

## Role & Objective
The 'Adversarial Feed'. Injects incorrect, delayed, or "Poisoned" market data into the ingestion pipeline to test the system's outlier detection and data-cleaning logic.

## Logic & Algorithm
- **Data Poisoning**: Mimics "Flash Crash" scenarios by injecting fake price-spikes or zero-liquidity data points.
- **Sanity Validation**: Checks if the Data Scientist or Trader identifies the bad data before acting on it.
- **Source Switching**: Simulates a "Primary Data Provider" failure to test the hot-swap speed to secondary feeds.

## Inputs & Outputs
- **Inputs**:
  - `clean_market_data` (Stream).
- **Outputs**:
  - `adversarial_market_feed` (Stream): The poisoned data delivered to the OS.

## Acceptance Criteria
- Trigger the system's "Data Integrity Alert" for 100% of injected outlier events.
- Ensure no "Adversarial" trade is triggered by fake price data.


---

## Source: stress_tester\recovery_path_planner.md

# Recovery Path Planner (Agent 16.5)

## ID: `recovery_path_planner`

## Role & Objective
The 'Resilience Scorer'. Evaluates the outcomes of all stress tests, assigns a "Sovereign Stability Score," and generates a prioritised list of hardware or logic upgrades.

## Logic & Algorithm
- **Vulnerability Mapping**: Correlates different stress test failures to find "Common Nodes" (e.g., one database being the bottleneck for 3 different tests).
- **Scoring Engine**: Calculates a weighted score based on MTTR, Data Integrity, and Cost of Failover.
- **Upgrade Synthesis**: Suggests specific infra changes (e.g., "Add 32GB RAM to the Historian node") based on the test data.

## Inputs & Outputs
- **Inputs**:
  - `all_stress_test_results` (List).
- **Outputs**:
  - `stability_scorecard` (JSON): The official "Hardness" rating of the OS.

## Acceptance Criteria
- Provide a clear, actionable "Upgrade Path" for any Stability Score < 90%.
- Maintain a historical log of stability improvements over time.


---

## Source: stress_tester\robustness_scorer.md

# Robustness Scorer (Agent 16.6)

## ID: `robustness_scorer`

## Role & Objective
The 'Sanity Checker'. Ensures that after a fault is cleared (e.g., a container restarts), the system state is 100% consistent with the pre-fault period and no "Ghost State" remains.

## Logic & Algorithm
- **State Checksumming**: Compares a pre-test "State Snapshot" against a post-recovery "State Snapshot."
- **Ghost Detection**: Scans for "Orphaned Transactions" or "Zombies processes" that should have been cleaned up during recovery.
- **Database Consistency Audit**: Performs deep-level foreign key and constraint checks to ensure the ACID properties held during chaos.

## Inputs & Outputs
- **Inputs**:
  - `pre_fault_snapshot` (Data).
  - `post_recovery_snapshot` (Data).
- **Outputs**:
  - `consistency_audit_status` (Pass/Fail): Does the system really "Recover" or just restart?

## Acceptance Criteria
- Identify even a 1-bit discrepancy between pre-fault and post-recovery persistent state.
- Ensure 100% cleanup of temporary resources within 10 minutes of test completion.


---

## Source: stress_tester\war_game_simulator.md

# War Game Simulator (Agent 16.1)

## ID: `war_game_simulator`

## Role & Objective
The 'Instance Killer'. Proactively terminates agent containers, microservices, and network nodes to test the high-availability failover logic and ensure no single point of failure exists in the Sovereign OS.

## Logic & Algorithm
- **Chaos Injection**: Uses a "Chaos Monkey" style algorithm to randomly select healthy services for termination.
- **Failover Monitoring**: Measures the time required for the Orchestrator to detect the loss and spin up a replacement node.
- **Data Integrity Check**: Verifies that no in-flight messages were lost during the service interruption.

## Inputs & Outputs
- **Inputs**:
  - `system_topology` (Graph): The list of all running containers and services.
- **Outputs**:
  - `failover_performance_report` (Dict): Recovery time and data loss metrics.

## Acceptance Criteria
- Achieve a "Mean Time to Recovery" (MTTR) of < 10 seconds for critical services.
- Ensure 0% data loss during random container termination events.


---

## Source: trader\arbitrageur.md

# Arbitrageur (Agent 5.3)

## ID: `arbitrageur`

## Role & Objective
The "Inefficiency Exploiter". Captures risk-free profit from price discrepancies across different venues (CEX vs DEX) or related asset pairs.

## Logic & Algorithm
1. **Multi-Venue Scan**: Simultaneously monitors prices for the same asset across Coinbase, Binance, Uniswap, etc.
2. **Triangular Logic**: Scans for loops in currency pairs that result in a net gain (e.g., BTC-ETH-USDT-BTC).
3. **Fee-Aware Execution**: Only triggers trades if the profit exceeds the combined gas and transaction fees by at least 20%.

## Inputs & Outputs
- **Inputs**:
  - `multisource_prices` (Dict): Fragmented venue data.
- **Outputs**:
  - `arb_execution` (Dict): Simultaneous buy/sell orders.
  - `net_profit_estimate` (float): Net gain after all fees.

## Acceptance Criteria
- Arbitrage execution must be atomic (simultaneous) across multiple venues to prevent "legged" risk.
- Net profit calculations must include real-time gas/network fee estimates.


---

## Source: trader\exit_manager.md

# Exit Manager (Agent 5.2)

## ID: `exit_manager`

## Role & Objective
The "Profit Protector". The Exit Manager manages the lifecycle of an open position to ensure profits are realized according to the plan and losses are strictly capped.

## Logic & Algorithm
1. **Dynamic Vol-Stops**: Manages trailing stops based on real-time ATR (Average True Range).
2. **Time-Exit Enforcement**: Closes out short-term tactical positions before market sessions close to avoid overnight risk.
3. **Scaling Strategy**: Gradually reduces position size as the asset approaches the target take-profit level.

## Inputs & Outputs
- **Inputs**:
  - `open_positions` (List): Current portfolio holdings.
  - `volatility_metrics` (Dict): Current market ATR.
- **Outputs**:
  - `exit_orders` (List): Orders to trim or close positions.

## Acceptance Criteria
- 100% of open positions must have an active, server-side stop-loss order within 1 second of entry.
- Trailing stops must be updated in real-time as the asset price moves in favor of the trade.


---

## Source: trader\flash_crash_circuit_breaker.md

# Flash Crash Circuit Breaker (Agent 5.6)

## ID: `flash_crash_circuit_breaker`

## Role & Objective
The "Emergency Stop". The ultimate safeguard that halts all trading activity if extreme, non-human market anomalies or system failures are detected.

## Logic & Algorithm
1. **SOT Monitoring**: Tracks the "Speed of Tape"—identifying vertical, high-velocity price drops indicative of a flash crash.
2. **Desync Detection**: Monitors if venue prices are diverging significantly, indicating a broken feed.
3. **Kill Switch**: Issues a system-wide SIGKILL to all execution-level agents if thresholds are breached.

## Inputs & Outputs
- **Inputs**:
  - `global_price_stream` (Dict): Live ticker data.
  - `venue_health_status` (Dict): Network health.
- **Outputs**:
  - `system_halt_signal` (bool): Halt flag.
  - `reason_code` (str): e.g., 'FLASH_CRASH_DETECTED'.

## Acceptance Criteria
- Halt signal must propagate to the execution engine in < 5ms of detection.
- Circuit breaker must be "latched"—requiring manual human reset after a halt.


---

## Source: trader\liquidity_scout.md

# Liquidity Scout (Agent 5.4)

## ID: `liquidity_scout`

## Role & Objective
The "Depth Finder". Identifies the deepest pools of liquidity to ensure large orders are filled without causing significant market moving "impact".

## Logic & Algorithm
1. **Dark Pool Probing**: Checks for hidden liquidity in institutional venues.
2. **Market Impact Modeling**: Predicts how much a trade of size X will move the market price Y.
3. **Smart Routing**: Recommends the exact volume split across different exchanges to optimize the fill.

## Inputs & Outputs
- **Inputs**:
  - `prospective_order_size` (float): Total units to trade.
- **Outputs**:
  - `routing_recommendation` (List): % volume per venue.
  - `forecast_impact_bps` (float): Expected slippage.

## Acceptance Criteria
- Routing recommendations must be updated every 500ms during active trade execution.
- Maintain Impact Prediction accuracy to within 5 basis points of the actual outcome.


---

## Source: trader\position_sizer.md

# Position Sizer (Agent 5.5)

## ID: `position_sizer`

## Role & Objective
The "Kelly Criterion" engine. Determines exactly how much capital to risk on a single trade based on the edge (confidence) and the current market volatility.

## Logic & Algorithm
1. **Fractional Kelly**: Applies the Kelly Criterion to signals to find the optimal growth-maximizing size.
2. **Risk Capping**: Enforces strict "Max 2% Risk" rules per trade relative to total portfolio equity.
3. **Exposure Correlation**: Checks if the new trade increases "Sector Over-exposure" (e.g., too much Tech) and reduces size accordingly.

## Inputs & Outputs
- **Inputs**:
  - `trade_signal` (Dict): Direction and confidence.
  - `current_portfolio_equity` (float): Total liquid capital.
- **Outputs**:
  - `recommended_qty` (float): Number of units to buy.
  - `ruin_probability` (float): Risk assessment.

## Acceptance Criteria
- 100% of trades must pass through the Position Sizer before being sent to the Sniper.
- Never exceed the 2% maximum risk-per-trade cap under any circumstances.


---

## Source: trader\sniper.md

# Sniper (Agent 5.1)

## ID: `sniper`

## Role & Objective
The "Precision Entry" engine. The Sniper's goal is to execute orders at the exact moment where liquidity and price alignment hit optimal levels to minimize market impact.

## Logic & Algorithm
1. **L2 Monitoring**: Constant surveillance of Level 2 order books for price improvement opportunities.
2. **Iceberg Execution**: Uses hidden/iceberg orders to prevent front-running by predatory HFT bots.
3. **Micro-second Sync**: Matches entry signals from the quantitative stack with sub-millisecond precision.

## Inputs & Outputs
- **Inputs**:
  - `target_order` (Dict): Symbol, Side, Size, and Limit.
  - `live_order_book` (Dict): Real-time bid/ask depth.
- **Outputs**:
  - `execution_status` (Dict): Fill details.
  - `slippage_report` (float): Actual fill vs mid-price.

## Acceptance Criteria
- Execute orders within 10ms of receiving a high-conviction signal from the Orchestrator.
- Maintain average slippage < 2 basis points on liquid assets.


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

