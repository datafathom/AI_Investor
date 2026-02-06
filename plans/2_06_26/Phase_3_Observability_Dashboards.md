# Phase 3: Observability Dashboards

## Overview
This phase focuses on the spatial and analytical visualization of the Sovereign OS. We are moving beyond simple tables into high-fidelity interaction maps. The goal is to provide the human operator with a "Battle Map" of the agent's experiences, resource consumption, and financial efficiency.

## Deliverables

### 1. 3D Semantic Memory Map (D3/Three.js)
**Description**: A visual cluster of agent experiences projected into 3D space using dimensionality reduction.
- **Acceptance Criteria**:
  - Nodes represent individual memories, color-coded by Department (e.g., Green for Trade, Red for Alert).
  - Clicking a node opens a slide-out panel with the raw, redacted content and its metadata.
  - Relationships (Links) are rendered between nodes with a cosine similarity > 0.85.

### 2. Department ROI Performance Radar
**Description**: A scatter chart visualizing the Efficiency Frontier (Gas/API Cost vs. Alpha Generated).
- **Acceptance Criteria**:
  - X-Axis represents total resource cost (credits/gas); Y-Axis represents total profit in USD.
  - "Leech" missions (High cost, Low profit) are automatically highlighted in Red.
  - Data updates in real-time as missions report their P&L via Socket.io.

### 3. Global Sector Heatmap (Grid View)
**Description**: A condensed 100-cell grid for monitoring the health of a high-density mission fleet.
- **Acceptance Criteria**:
  - Each cell represents a registered mission; color indicates status (Idle, Running, Successful, Breached).
  - "Hover" state reveals sub-agent invocation count and current TTL.
  - Clicking a cell navigates directly to that mission's "Deep Trace" view.

### 4. Alpha Attribution Engine (Visualized)
**Description**: A stacked bar chart showing which departments contributed most to a mission's profit.
- **Acceptance Criteria**:
  - Attribution logic correctly splits profit between "Intelligence" (signals) and "Execution" (trades).
  - Chart supports "Drill-down" into specific sub-agent contributions.
  - Total Alpha matches the value in the `sovereign_bank` ledger.

### 5. Multi-Source Telemetry Feed
**Description**: A unified dashboard component that aggregates logs from Kafka, Postgres, and Neo4j.
- **Acceptance Criteria**:
  - Feed allows filtering by `DEPT_ID` or `MISSION_ID` across all storage sources simultaneously.
  - Latency between a Kafka event and its appearance in the HUD is < 200ms.
  - High-priority alerts stay "Pinned" to the top of the feed until acknowledged.

### 6. Interactive "Time-Travel" Slider
**Description**: A UI control to filter visual maps based on historical timestamps.
- **Acceptance Criteria**:
  - Adjusting the slider updates the 3D Map and Heatmap to show the system state at that specific moment.
  - Slider supports "Replay" mode with 1x, 5x, and 10x speeds for post-mortem analysis.
  - State rehydration logic is optimized to load historical snapshots in < 1s.

## Proposed Changes

### [Frontend] [Visualizations]
- [NEW] [MemoryMap.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/MemoryMap.jsx): 3D graph implementation.
- [NEW] [PerformanceRadar.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/PerformanceRadar.jsx): Recharts scatter plot.
- [NEW] [GlobalHeatmap.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/GlobalHeatmap.jsx): High-density status grid.

### [Backend] [Analytics]
- [NEW] [attribution_service.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/attribution_service.py): The math behind the ROI splits.

## Verification Plan

### Automated Tests
- `pytest tests/frontend/test_data_transformers.py`
- `pytest tests/services/test_attribution_math.py`

### Manual Verification
- Pan and zoom through the 3D Memory Map and verify node interactivity.
- Simulate a high-cost mission and verify its move into the "Red" quadrant of the Radar.
