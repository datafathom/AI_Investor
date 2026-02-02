# Backend-Frontend Connection Roadmap: Major Build Cycle

## Overview
This roadmap defines the deep logical integration for the AI Investor platform. It moves beyond simple "wiring" to implement practical workflows, advanced UI/UX widgets, and systemic connectivity for a production-ready institutional experience.

---

## 1. Institutional Orchestrator (Phase 33)
**Goal**: Transition from a static dashboard to a functional Hierarchical Management Engine.

### Advanced Logical Implementation
- **Hierarchical RBAC (Role-Based Access Control)**: 
    - Implement logic for "Advisor-Level" vs "Manager-Level" views.
    - Logic to inherit branding permissions from parent organizations.
- **Client Onboarding Workflow**:
    - `AdvisorOnboardingWizard.jsx`: A 5-step flow (Identity -> KYC -> Funding -> Allocation -> Approval).
- **Practicality Widgets**:
    - `RevenuePulse`: Real-time projected fee calculator based on individual client AUM and tiered structures.
    - `ClientHealthCompass`: AI-driven scoring of client risk based on portfolio volatility vs. documented risk tolerance.

### Wiring & API
- Wire `useInstitutionalStore` to `PresenceService.js` for live advisor collaboration events.
- Endpoint Mapping: `POST /api/institutional/client/onboard`, `GET /api/institutional/analytics/fees`.

---

## 2. Evolution Suite (Phase 39+)
**Goal**: A "Genomic Lab" for AI trading agents, moving from status to active intervention.

### Advanced Logical Implementation
- **Genomic Time-Travel (Playback Logic)**:
    - Ability to select a "Fitness Spike" and replay the specific market conditions/agent decisions at that moment.
- **Gene Splicing Lab**:
    - UI to drag "conviction logic" from one agent and "risk parameters" from another to create a hybrid agent (Splice Job).
- **Practicality Widgets**:
    - `AncestryTree`: Interactive D3.js map showing successful gene propagation across 100+ generations.
    - `AgentHallOfFame`: Persistence view for agents that survived rare "Black Swan" scenarios.

### Wiring & API
- Multi-threaded progress via `PresenceService` (`on('evolution:step', ...)`).
- Endpoint Mapping: `POST /api/v1/evolution/splice`, `GET /api/v1/evolution/playback/<agent_id>`.

---

## 3. Master Orchestrator (Phase 200)
**Goal**: The "Spatial Brain" - Visualizing systemic reflexivity across Neo4j and TimescaleDB.

### Advanced Logical Implementation
- **Reflexivity Propagation (Impact Logic)**:
    - "Select a Node -> Inject Shock (% drop) -> Visualize Propagation". Logic to show which trusts/entities are liquidated first.
- **Node-to-Doc Deep Link**:
    - Click a "Property Trust" node in the graph and immediately open the associated Legal PDF using the `Documents` API.
- **Practicality Widgets**:
    - `SpatialPortfolioCockpit`: A 3D/VR Ready view of the whole portfolio using the `Spatial` API coordinates.
    - `GraphEventTimeline`: A horizontal scrubber to see how the graph connections evolved over time.

### Wiring & API
- Direct Neo4j Bolt protocol proxying for sub-20ms graph updates.
- Endpoint Mapping: `GET /api/v1/master/reflexivity/simulate`, `GET /api/v1/master/spatial/coordinates`.

---

## 4. Universal Navigation & Command Center
**Goal**: High-UX "Command & Control" for the entire platform.

### Advanced Logical Implementation
- **Universal Data Spotlight (Deep Search)**:
    - Expand `CommandPalette.jsx` (Ctrl+K) to index all Entities, Clients, Agents, and Symbols.
- **Global Event Scrubber (Systemic Timeline)**:
    - A horizontal timeline widget at the base of the UI that syncs:
        - **News Sentiment Spikes**
        - **Trade Execution Events**
        - **Graph Reflexivity Changes**
- **Practicality Widgets**:
    - `ShadowStrategyEngine`: A "Mirror Widget" that runs a hypothetical version of a live strategy with alternative parameters (e.g., higher leverage) to compare performance in real-time.
    - `SentimentFlowRadar`: A sector-by-sector heatmap showing the velocity of news sentiment shifting from Bullish to Bearish in real-time.
    - `HarvestHunter`: A tax-optimization tool that constantly scans for "Loss Harvesting" opportunities across integrated Brokerage and Crypto accounts.
    - `DriftMonitor`: Visualizes "Model Drift" for algorithmic strategies, alerting when real-world performance deviates statistically from backtest expectations.
    - `LiquidityLattice`: For Web3/Crypto, a real-time visualization of pool depth and potential slippage impact for the user's current positions.
    - `MacroRegimeMatrix`: A 2x2 matrix showing the current economic regime (Growth vs. Inflation) and the directional vector of the system's shift.
    - `AuditStreamLENS`: A transparent, live-streaming audit log of all system administrative actions (API Key access, MFA confirmations, etc.).
    - `GenePulseVisualizer`: A micro-view of an AI Agent's specific gene mutations occurring during the current evolution cycle.
    - `OrderImpactSimulator`: A pre-trade widget that shows the projected impact of a pending order on the user's Margin, Delta, and Gamma profile.

### Wiring & API
- Shared `useTimelineStore` that aggregates events from `PresenceService`.
- Endpoint Mapping: `GET /api/v1/system/timeline/aggregate`, `POST /api/v1/simulation/shadow-run`.

---

## 5. OS Style Taskbar Logic (The System Anchor)
**Goal**: Transform the bottom taskbar into a functional OS command center for window management and live system telemetry.

### Practical Implementation
- **Window & Workspace Management**:
    - **Active App Previews**: Hovering over a taskbar icon (e.g., Estate, Scenario) shows a live thumbnail preview of that window's current state.
    - **Workspace Switcher**: Group icons by logical context (Research, Strategy, Admin). Clicking a group expands the related windows.
- **Live Agent Status Indicators**:
    - **Agent Mood Icons**: Miniature avatars of active Evolution agents. Color/Expression changes based on real-time P&L or "Risk Stress".
    - **Action Badges**: Numbers on icons showing pending alerts (e.g., 3 new KYC verifications on the Institutional icon).
- **System Telemetry & Control**:
    - **The "Start" Menu (Orchestrator Launcher)**: Categorized access to all system modules, searchable via the Spotlight logic.
    - **System Health Mini-Meters**: 1-pixel high progress bars at the very top of the taskbar showing global CPU, Memory, and Network throughput.
    - **Global Kill Switch**: A persistent, red-glowing "Force Stop" button (requiring long-press + MFA) to immediately halt all active trading and evolution processes.

### Wiring & API
- **Taskbar Service**: Aggregates `windowManager` state and `presenceService` agent status.
- **State Synchronization**: Unified `taskbarStore.js` that persists pinned apps and custom icon layouts to `/api/v1/workspace/taskbar/config`.

### Acceptance Criteria
- [ ] Taskbar icons update in real-time as windows are opened, minimized, or closed.
- [ ] Hovering over the "Evolution" icon shows the current generation count.
- [ ] Kill Switch triggers the backend `guardian:kill_all` event across all services.

---

## 6. Security & Hardware Bridging (Phase 51)
**Goal**: Secure, physical-tethered identity and asset management.

### Advanced Logical Implementation
- **Hardware-Locked Multi-Sig**:
    - Logic to require physical hardware wallet signature (Ledger/Trezor) for high-value organizational transfers (> $100k).
- **Physical Identity Bridge**:
    - Wiring the `Identity` service to NFC/Biometric hardware for "Architect-Level" system access.

### Acceptance Criteria
- [ ] System prompts for hardware signature on specific transaction thresholds.
- [ ] Successful pairing of YubiKey/NFC verified via backend `/api/v1/identity/hardware-verify`.

---

## 6. Standardization: The "Golden Path" Refactor
**Goal**: Clean up existing Phase 18-31 debt using a unified pattern.

### Patterns to Enforce
- **The "Service-Store-Page" Triad**:
    - Every page *must* use a Service (pure API) and a Store (Zustand) for state.
- **Versioned API Client**:
    - Centralize all requests through an `apiClient.js` wrapper that handles global 401/429 logic and auto-retries.

---

## 6. Implementation Cycle Priority

### Sprint 1: The Foundation (Core Navigation & Connectivity)
**Widgets to Implement**:
1. `QuotaHealthMeter`: Real-time visual tracking of API rate limits (Polygon, FRED, etc.).
2. `LatencyGlobalMap`: Interactive map showing latency to various market data providers.
3. `SearchHistorySpotlight`: High-speed access to recently queried entities and clients.
4. `SystemLoadRibbon`: Minimalist 1px visualizer for CPU/RAM/Kafka stress.
5. `CliHistoryWizard`: Interactive command memory for the Integrated Terminal.
6. `AuthSessionTimer`: Visual countdown to JWT expiry with proactive "Refresh" notification.

---

### Sprint 2: Institutional Logic (Advisor/Client Workflows)
**Widgets to Implement**:
1. `FeeRevenueForecast`: Tiered fee simulator for AUM-based revenue projections.
2. `ClientRetentionAI`: Predictive scoring for client churn based on engagement patterns.
3. `DocSignaturePulse`: Real-time status tracking for legal document signatures.
4. `AssetAllocationWheel`: Drag-and-drop rebalancing UI for client portfolios.
5. `AdvisorCommissionTracker`: Live earnings tracking for the advisor managing the client pool.
6. `KycRiskGauge`: Instant AML/KYC risk flags during the onboarding process.

---

### Sprint 3: The Brain (Master Orchestrator & Spatial Graph)
**Widgets to Implement**:
1. `NodeConnectionHeatmap`: Visualizes relationship density within the Neo4j super-graph.
2. `SpatialAssetBubble`: 3D volumetric representation of asset size within coordinates.
3. `ReflexivityEcho`: Visual "ripple" propagation showing secondary/tertiary shock impacts.
4. `Neo4jHealthVitals`: Direct monitoring of graph memory usage and lock latency.
5. `EntityOwnershipMatrix`: Traditional matrix view for complex, multi-layered entities.
6. `GraphTimeScrubber`: Vertical timeline to view graph state at any historical point.

---

### Sprint 4: Evolution Lab (Genomics & AI Training)
**Widgets to Implement**:
1. `FitnessSurface3D`: Interactive 3D terrain mapping the agent fitness "Search Space".
2. `GeneFrequencyPlot`: Distribution chart of the most profitable genes across generations.
3. `MutationRateSlider`: Real-time control to adjust training randomness and evolution speed.
4. `SurvivalProbabilityMeter`: Live calculation of an agent's likelihood to survive the cycle.
5. `AncestorLineageMap`: Tree view tracing agents back to "Generation Zero" (Genesis).
6. `SplicingConflictResolver`: Visual Diff-tool for gene clashes during hybrid agent creation.

---

## Acceptance Criteria for Build Cycle
- [ ] **No Mock Data**: Every dashboard rendered in the "Walkthrough" must be backed by a live database or the simulation engine.
- [ ] **Latency Targets**: All graph interactions must resolve in < 50ms (Store-first, Sync-later).
- [ ] **Audit Readiness**: Every action (Trade, Onboarding, Splice) must generate a log in the System Audit pool.
