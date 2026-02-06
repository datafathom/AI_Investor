# PHASE 2 IMPLEMENTATION PLAN: THE INTELLIGENCE MATRIX (DATA SCIENCE)
## FOCUS: NEWS INGESTION, SENTIMENT ANALYSIS, AND QUANT DATA

---

## 1. PROJECT OVERVIEW: PHASE 2
With the "Bunker" built in Phase 1, Phase 2 focuses on filling it with intelligence. This is the **Data Forge**. We build the specialized pipelines for news ingestion, sentiment analysis, and the quantitative backtesting engines. This phase empowers the Data Scientist and Strategist departments.

---

## 2. GOALS & ACCEPTANCE CRITERIA `[STATUS: 🟡 STARTED]`
- **G1**: Automated ingestion of 50+ financial news sources with real-time sentiment scoring.
- **G2**: Deployment of a vectorized backtesting engine using `Polars` for sub-second trade simulations.
- **G3**: Implementation of the "Correlation Web" in Neo4j, linking tickers based on Pearson r-values.
- **G4**: Interactive "Logic Lab" UI for the Strategist department to build drag-and-drop strategy blueprints.

---

## 3. FULL STACK SPECIFICATIONS

### 3.1 FRONTEND (The Quant Hub)
- **Description**: Implementation of the Data Scientist workstation with D3.js Correlation Chord diagrams.
- **Acceptance Criteria**:
    - **C1**: Chord diagram supports 500+ nodes with fluid 60fps interaction during hover/zoom.
    - **C2**: Sentiment Heatmap: Visual colors link instantly ( < 100ms) to filtered ticker selections.
    - **C3**: Deep-Search: Omnibox permits filtering news by Sentiment Magnitude (e.g., "Find all -0.9 news for Semiconductor sector").

### 3.2 BACKEND (Ingestion & Vectorization)
- **Description**: Building the Scraper-General and the Polars-driven backtest core.
- **Acceptance Criteria**:
    - **C1**: Ingestion throughput: System can process and score 50 articles/minute without CPU throttling.
    - **C2**: Sentiment Accuracy: `DistilBERT` results match human-labeled "Trade Sentiment" on 90% of a 100-sample test set.
    - **C3**: Memory Management: Vectorized Polars frames for 1M+ rows are discarded instantly after backtest to prevent memory leaks.

### 3.3 INFRASTRUCTURE (Data Lake & Scraping)
- **Description**: Managing the Playwright grid and the Postgres TimescaleDB extension.
- **Acceptance Criteria**:
    - **C1**: Playwright instances are ephemeral (spawn -> scrape -> die) to prevent session hanging.
    - **C2**: TimescaleDB Hypertables: Automated partitioning for `market_data` based on 30-day time chunks.
    - **C3**: Proxy Management: 100% success rate on whitelisted scraping sites via randomized residential proxy rotation.

### 3.4 TESTING & VERIFICATION
- **Description**: Data integrity and mathematical validation.
- **Acceptance Criteria**:
    - **T1: Parity Test**: Backtest engine results (Sharpe/Drawdown) match `VectorBT` or `Backtrader` reference results within a 0.01% margin.
    - **T2: Stress Test**: Ingestion worker maintains 100% uptime during "Flash News" events (10x normal volume).
    - **T3: Graph Audit**: A nightly script verifies that NO ticker node is "Orphaned" from the sentiment web.

---

## 4. AGENT CONTRACTS

##### 👤 AGENT 2.1: The Scraper-General
- **Acceptance Criteria**: Ingests 100% of whitelisted RSS feeds with < 30s latency between post and Neo4j node creation.

##### 👤 AGENT 2.2: The Backtest Autopilot
- **Acceptance Criteria**: `Polars` execution of a 10-year SMA cross strategy on 1-min data in < 2 seconds.

##### 👤 AGENT 2.4: The Anomaly Scout
- **Acceptance Criteria**: Triggers a "Lethal Anomaly" Kafka alert within 500ms of identifying price variance > 4 standard deviations from the 30-min Mean.

---

## 5. MILESTONES & TIMELINE
- **Week 1**: Scraper-General + Sentiment Ingestion Pipeline. `[STATUS: ✅ COMPLETED]`
- **Week 2**: Backtest Engine (Polars) + Historical Data Ingestion (PG). `[STATUS: ✅ COMPLETED]`
- **Week 3**: Strategist Logic Lab UI + Blueprint Schema.
- **Week 4**: Correlation Detective + Anomaly Scout Integration.

---
**END OF PHASE 2 IMPLEMENTATION PLAN**
