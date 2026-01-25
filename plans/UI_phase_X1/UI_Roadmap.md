# AI Investor UI Roadmap

> **Source of Truth** for UI Development Cycle  
> Last Updated: 2026-01-18  
> Status Legend: `[ ]` Not Started | `[/]` In Progress | `[x]` Completed | `[!]` Blocked/Paused

---

## Strategic Vision

Transform the AI Investor GUI from a trading terminal into a **Total Financial Homeostasis Engine** using the **Yellowstone Wolf Principle**. The interface serves as a warden's console for a complex adaptive financial ecosystem where autonomous agents hunt for alpha while maintaining ecosystem balance.

### Architecture Principles

- **Widget-Based Architecture**: All page content organized into reusable, customizable widgets
- **Macro Task Routes**: Routes organized by specialization (e.g., "The Analyst", "The Executor", "The Guardian")
- **Terminal/Dashboard Customization**: Main view assembled from widgets across the entire application

---

## Route Organization by Macro Task

| Macro Task | Route Prefix | Purpose | Widgets Available |
|------------|--------------|---------|-------------------|
| **The Analyst** | `/analytics/*` | Deep research, options modeling, backtesting | Options Chain, Greeks, Fear/Greed, Attribution |
| **The Executor** | `/terminal/*` | Trade execution, order management | DOM, Quick Actions, Risk Modal, Symbol Linking |
| **The Guardian** | `/risk/*` | Risk monitoring, margin, kill switches | Margin Danger, Kill Switch, Compliance Logs |
| **The Strategist** | `/portfolio/*` | Portfolio management, tax optimization | Tax Harvesting, Attribution, Allocation |
| **The Observer** | `/scanner/*` | Market scanning, sentiment tracking | Global Scanner, HypeMeter, Social NLP |
| **The Architect** | `/system/*` | System health, infrastructure | Kafka Monitor, DB Health, Agent Load Balancer |

---

## Phase 1: Foundation & Window Management (Phases 43-44)

**Implementation Plan**: [Phase_1_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_1_ImplementationPlan.md)

> Each phase has its own dedicated implementation plan with verbose acceptance criteria, Jest test requirements, and backend specifications.

### 43: Institutional OS-Style Window Management
- [ ] **43.1** Window Wrapper Pattern with React 19 hooks + Zustand
- [ ] **43.2** 8-direction resize handles (N, S, E, W, NE, NW, SE, SW)
- [ ] **43.3** Z-Index Stacking Engine for active window focus
- [ ] **43.4** Postgres-backed workspace layout persistence (<200ms restore)
- [ ] **43.5** Framer Motion dragging physics with zero-latency feedback

### 43.1: Glassmorphism UI Chrome
- [ ] **43.1.1** CSS backdrop-filter 20px blur + 70% opacity
- [ ] **43.1.2** High-contrast professional shadows
- [ ] **43.1.3** Active window neon border (Green/Yellow/Red risk state)
- [ ] **43.1.4** Window chrome buttons (Close/Minimize/Maximize)

### 44: Taskbar Logic & Agent Heartbeat
- [ ] **44.1** Dynamic bottom dock with agent icons
- [ ] **44.2** Kafka-driven heartbeat indicators (Green/Red)
- [ ] **44.3** Window restoration to exact coordinates (<100ms)
- [ ] **44.4** Hover tooltip with D3.js mini-sparklines

---

## Phase 2: Navigation & Core Widgets (Phases 45, 12, 6.2)

**Implementation Plan**: [Phase_2_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_2_ImplementationPlan.md)

### 45: Advanced Logical Workspace Routing
- [ ] **45.1** Breadcrumb Navigation (Workspace > Terminal > AI Agent)
- [ ] **45.2** `/analytics/options` route with Fama-French + GEX metrics
- [ ] **45.3** Zustand state persistence across route transitions
- [ ] **45.4** Deep-linking to specific agent-ID configurations

### 12: D3.js Fear & Greed Composite Gauge
- [ ] **12.1** SVG needle with real-time Kafka SignalEvents
- [ ] **12.2** Color zones: Red (0-20), Yellow (21-79), Green (80-100)
- [ ] **12.3** Hover tooltips with VIX, Google Trends, Social Sentiment weights
- [ ] **12.4** Framer Motion smooth needle transitions

### 6.2: Kafka Nervous System Stream Monitor
- [ ] **6.2.1** Scrolling activity log (Market Data, Sentiment, Risk)
- [ ] **6.2.2** D3.js latency graph (Target <200ms)
- [ ] **6.2.3** Color-coded events: Blue/Purple/Orange/Green
- [ ] **6.2.4** User-defined Kafka topic filtering

---

## Phase 3: Social & Sentiment Intelligence (Phase 8.1)

**Implementation Plan**: [Phase_3_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_3_ImplementationPlan.md)

### 8.1: Social NLP Pipeline & HypeMeter Tape
- [ ] **8.1.1** Real-time scrolling tape with sentiment scores (-1 to +1)
- [ ] **8.1.2** Viral Alert badge (>5 std dev mention velocity)
- [ ] **8.1.3** NLP keyword extraction (Gamma Squeeze, Short Interest)
- [ ] **8.1.4** HypeMeter Engine integration for platform-weighted Hype Score

---

## Phase 4: Options & Market Depth (Phases 46, 46.2, 47)

**Implementation Plan**: [Phase_4_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_4_ImplementationPlan.md)

### 46: Institutional Options Chain Widget
- [ ] **46.1** Vertical strike ladder with <100ms Bid/Ask updates
- [ ] **46.2** D3.js volatility smile + Greeks (Δ, Γ, Θ, Vega)
- [ ] **46.3** One-click order entry to Pre-Trade Risk Modal
- [ ] **46.4** IV Rank and IV Percentile calculation

### 46.2: Level 2 Market Depth (DOM)
- [ ] **46.2.1** Vertical Price Ladder with histogram volume
- [ ] **46.2.2** "The Gap" visualization (<50ms updates)
- [ ] **46.2.3** Institutional Whale order filter
- [ ] **46.2.4** Drag-and-drop limit order placement

### 47: Multi-Sense Symbol Linking
- [ ] **47.1** Color-group linking (Red/Blue/Green) with <50ms propagation
- [ ] **47.2** Visual group badges in window corners
- [ ] **47.3** Global hotkeys: Shift+B (Buy), Shift+S (Sell), ESC (Kill)
- [ ] **47.4** Persistent group assignments across sessions

---

## Phase 5: Risk Management & Safety (Phases 48, 48.1, 48.2)

**Implementation Plan**: [Phase_5_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_5_ImplementationPlan.md)

### 48: Execution Shield - AI Risk Modal
- [x] **48.1** Mandatory Position Size, Margin Impact, Sector Concentration display
- [x] **48.2** AI Risk Rating badge (SAFE/CAUTION/DANGER) with justification
- [x] **48.3** Nancy Pelosi Index contextual display
- [x] **48.4** Focus-trap with background blur

### 48.1: Global Kill Switch
- [x] **48.1.1** Floating Kill Switch button with <1s Socket.io/SignalR broadcast
- [x] **48.1.2** Priority Kafka message bypass
- [x] **48.1.3** "System Frozen" overlay with passcode unlock
- [x] **48.1.4** Broker API freeze confirmation (<1.5s)

### 48.2: Notification Engine
- [x] **48.2.1** Toast notifications with severity colors (Blue/Orange/Red)
- [ ] **48.2.2** Deep-linking from Whale Flow to Options Chain
- [ ] **48.2.3** Heuristic-based Delta/OI CRITICAL alerts
- [x] **48.2.4** Configurable alert mute toggles

---

## Phase 6: Portfolio Analytics (Phase 49)

**Implementation Plan**: [Phase_6_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_6_ImplementationPlan.md)

### 49: Brinson-Fachler Performance Attribution
- [x] **49.1** Sector Allocation Attribution Widget (D3.js diverging bars)
- [x] **49.2** Interaction Effect Heatmap (60 FPS zoom/pan)
- [x] **49.3** Benchmark Relative-Strength Overlay (10k+ data points Canvas)

---

## Phase 7: Fixed Income & Yield (Phase 50)

**Implementation Plan**: [Phase_7_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_7_ImplementationPlan.md)

### 50: Fixed Income & Yield Curve
- [x] **50.1** Bond Ladder Construction (drag-and-drop D3 bars)
- [x] **50.2** FRED API Yield Curve Plotter with inversion detection
- [x] **50.3** Duration & Convexity Risk Gauges

---

## Phase 8: Crypto & Web3 (Phase 51)

**Implementation Plan**: [Phase_8_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_8_ImplementationPlan.md)

### 51: Multi-Asset Cryptographic Vaulting
- [ ] **51.1** Hardware Wallet Dashboard (Ledger/Trezor)
- [ ] **51.2** LP Position Tracker with impermanent loss visualization
- [ ] **51.3** Gas Fee Optimization & Gwei Pulse widget

---

## Phase 9: Tax Strategy (Phase 52)

**Implementation Plan**: [Phase_9_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_9_ImplementationPlan.md)

### 52: Tax-Advantaged Strategy UI
- [ ] **52.1** Unrealized Loss Grid (Wash-Sale Protected)
- [ ] **52.2** Automated Tax-Loss Harvesting Toggle
- [ ] **52.3** Long-term vs Short-term Capital Gains Forecaster

---

## Phase 10: Global Macro (Phase 53)

**Implementation Plan**: [Phase_10_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_10_ImplementationPlan.md)

### 53: Global Macro & Commodities
- [ ] **53.1** D3 World Map (Shipping + Nancy Pelosi Index)
- [ ] **53.2** Futures Contango/Backwardation Visualizer
- [ ] **53.3** Neo4j Inflation-Sensitive Correlation Matrix

---

## Phase 11: Security & Compliance (Phases 54, 59)

**Implementation Plan**: [Phase_11_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_11_ImplementationPlan.md)

### 54: Institutional KYC & Document Vault
- [ ] **54.1** Encrypted Identity Verification Portal (AES-256)
- [ ] **54.2** Audit-Trail Document Management
- [ ] **54.3** 13F Regulatory Filing Tracker

### 59: Regulatory Compliance & Audit
- [ ] **59.1** Anti-Market Abuse Monitoring Feed
- [ ] **59.2** Immutable Activity Audit Log (SHA-256 chain)
- [ ] **59.3** SAR Automated Flagging UI

---

## Phase 12: AI Debate Chamber (Phase 55)

**Implementation Plan**: [Phase_12_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_12_ImplementationPlan.md)

### 55: Debate Chamber 2.0
- [ ] **55.1** Multi-Agent Chat Interface (Bull vs Bear)
- [ ] **55.2** Voting/Consensus Progress Bar (70% threshold)
- [ ] **55.3** Neo4j Argument Mapping Tree

---

## Phase 13: Multi-Currency & FX (Phase 56)

**Implementation Plan**: [Phase_13_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_13_ImplementationPlan.md)

### 56: Multi-Currency Cash Management
- [ ] **56.1** Global Cash Balance Pulse Widget
- [ ] **56.2** Limit-Order FX Conversion Interface
- [ ] **56.3** Interest-Bearing Cash Optimization Dashboard

---

## Phase 14: Backtesting V2 (Phase 57)

**Implementation Plan**: [Phase_14_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_14_ImplementationPlan.md)

### 57: Advanced Backtest Explorer
- [ ] **57.1** Monte Carlo 10k Path Visualizer (60 FPS Canvas)
- [ ] **57.2** Maximum Drawdown Stress Point Timeline
- [ ] **57.3** Out-of-Sample Overfit Warning Matrix

---

## Phase 15: Estate Planning (Phase 58)

**Implementation Plan**: [Phase_15_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_15_ImplementationPlan.md)

### 58: Estate & Inheritance Protocol
- [ ] **58.1** Dead Man's Switch Configuration
- [ ] **58.2** Beneficiary Asset Allocation Mapping
- [ ] **58.3** Neo4j Trust/Entity Legal Structure Visualizer

---

## Phase 16: Scenario Modeling (Phase 60)

**Implementation Plan**: [Phase_16_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_16_ImplementationPlan.md)

### 60: What-If Impact Simulator
- [ ] **60.1** Drag-and-Drop Macro Event Trigger
- [ ] **60.2** Portfolio Revaluation Forecast Chart
- [ ] **60.3** Liquidity Stress Test "Bank Run" Simulator

---

## Phase 17: Philanthropy & ESG (Phase 61)

**Implementation Plan**: [Phase_17_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_17_ImplementationPlan.md)

### 61: Philanthropy & Impact Investing
- [ ] **61.1** Excess Alpha Donation Routing
- [ ] **61.2** ESG Score Aggregator
- [ ] **61.3** Carbon Footprint vs Return Scatterplot

---

## Phase 18: System Health (Phase 62)

**Implementation Plan**: [Phase_18_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_18_ImplementationPlan.md)

### 62: System Health Telemetry
- [ ] **62.1** Kafka Cluster Health & Topic Latency Dashboard
- [ ] **62.2** Database I/O & Memory Pressure Gauges
- [ ] **62.3** Agent Brain Load Balancer UI

---

## Phase 19: Corporate Actions (Phase 63)

**Implementation Plan**: [Phase_19_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_19_ImplementationPlan.md)

### 63: Corporate Actions & Earnings
- [ ] **63.1** Earnings Calendar with Whisper Numbers
- [ ] **63.2** DRIP Management Console
- [ ] **63.3** Stock Split & Spin-off Visualizer

---

## Phase 20: Margin Management (Phase 64)

**Implementation Plan**: [Phase_20_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_20_ImplementationPlan.md)

### 64: Advanced Margin & Collateral
- [ ] **64.1** Maintenance Margin Danger Zone Visualizer
- [ ] **64.2** Cross-Collateralization Priority Toggle
- [ ] **64.3** Automated Margin Call Liquidation Editor

---

## Phase 21: Mobile V2 (Phase 65)

**Implementation Plan**: [Phase_21_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_21_ImplementationPlan.md)

### 65: Mobile Portfolio Quick-Actions
- [ ] **65.1** Biometric Kill Switch (FaceID/Fingerprint)
- [ ] **65.2** Push-Notification Trade Authorization
- [ ] **65.3** Haptic-Feedback Alert Vibrations

---

## Phase 22: API Marketplace (Phase 66)

**Implementation Plan**: [Phase_22_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_22_ImplementationPlan.md)

### 66: API Marketplace & Integration
- [x] **66.1** Third-party Data Connector UI
- [x] **66.2** API Key Encryption/Vaulting UI
- [x] **66.3** Custom Webhook Trigger Configuration

---

## Phase 23: Real Estate & Illiquid (Phase 67)

**Implementation Plan**: [Phase_23_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_23_ImplementationPlan.md)

### 67: Real-Estate & Illiquid Asset Tracking
- [x] **67.1** Manual Asset Entry (Property, Art, PE)
- [x] **67.2** Depreciation/Appreciation Slider
- [x] **67.3** Unified Net Worth Circular Gauges

---

## Phase 24: Homeostasis Zen Mode (Phase 68)

**Implementation Plan**: [Phase_24_ImplementationPlan.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/Phase_24_ImplementationPlan.md)

### 68: The Homeostasis "Zen" Mode
- [x] **68.1** Minimalist Goal Tracking ("Enough" Metric)
- [x] **68.2** Time-to-Retirement Countdown Gauge
- [x] **68.3** System Autopilot Master Override

---

## Widget Registry

All widgets must be registered in the Widget Catalog for Terminal/Dashboard customization:

| Widget ID | Category | Description |
|-----------|----------|-------------|
| `fear-greed-gauge` | Sentiment | Fear & Greed Composite Index |
| `kafka-monitor` | System | Nervous System Stream Monitor |
| `hype-meter` | Social | Social NLP HypeMeter Tape |
| `options-chain` | Trading | Institutional Options Chain |
| `dom-ladder` | Trading | Level 2 Market Depth |
| `risk-modal` | Risk | AI-Assisted Pre-Trade Check |
| `kill-switch` | Risk | Global Safety Pin |
| `attribution` | Portfolio | Brinson-Fachler Attribution |
| `yield-curve` | Fixed Income | FRED Yield Curve Plotter |
| `debate-chamber` | AI | Multi-Agent Debate Interface |

---

## Change Log

| Date | Phase | Item | Status | Notes |
|------|-------|------|--------|-------|
| 2026-01-18 | - | Initial Roadmap Creation | Completed | Created from trello_0003.txt |

