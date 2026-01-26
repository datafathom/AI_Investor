# Phase 17: Scenario Modeling & 'What-If' Impact Simulator

> **Phase 60** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Anticipates 'Black Swan' shocks by stress-testing the Yellowstone equilibrium.

---

## Overview

Interactive 'Torture Chamber' for simulating extreme macro shifts and testing portfolio resilience.

---

## Sub-Deliverable 60.1: Drag-and-Drop Macro Event Trigger

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Scenario/EventTrigger.jsx` | Trigger widget |
| `[NEW]` | `frontend2/src/widgets/Scenario/EventTrigger.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Scenario/EventCard.jsx` | Draggable event |
| `[NEW]` | `frontend2/src/stores/scenarioStore.js` | Scenario state |

### Verbose Acceptance Criteria

1. **Neo4j Correlation Graph Propagation**
   - [ ] Macro-shock events propagate through Neo4j correlation graph
   - [ ] Affect related sectors automatically
   - [ ] Oil spike → Energy sector → Airlines → Consumer
   - [ ] Visualize cascade effect

2. **Instant Net Worth Revaluation**
   - [ ] Recalculate total Net Worth under shock conditions
   - [ ] Show delta from current value
   - [ ] Breakdown by asset class
   - [ ] Time-series projection

3. **Shield Hedge Indicator**
   - [ ] Visual "Shield" icon shows hedge sufficiency
   - [ ] Green: Fully hedged against this shock
   - [ ] Yellow: Partially hedged
   - [ ] Red: Exposed, recommend action

4. **Pre-Built Event Library**
   - [ ] "Oil spikes to $150"
   - [ ] "Fed hikes +200bps"
   - [ ] "China invades Taiwan"
   - [ ] "Major tech company bankruptcy"
   - [ ] Custom event builder

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/scenario/simulate` | POST | Run scenario simulation |
| `/api/v1/scenario/events` | GET | Pre-built event library |
| `/api/v1/scenario/correlations` | GET | Neo4j correlation graph |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `EventTrigger.test.jsx` | Events draggable, simulation runs |
| `EventCard.test.jsx` | Card display, drag behavior |
| `scenarioStore.test.js` | Active scenarios, results storage |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 60.2: Portfolio Revaluation Forecast Chart

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Scenario/ForecastChart.jsx` | Chart widget |
| `[NEW]` | `frontend2/src/widgets/Scenario/ForecastChart.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Scenario/ScenarioComparison.jsx` | Side-by-side |

### Verbose Acceptance Criteria

1. **Framer Motion Animated Area Chart**
   - [ ] Show shock trajectory over time
   - [ ] Recovery path projection
   - [ ] Smooth animation on scenario change
   - [ ] Confidence bands

2. **Correlation Breakdown**
   - [ ] Consider "correlation breakdown" scenarios
   - [ ] When all assets fall together (crisis correlations)
   - [ ] Visual indicator of correlation assumptions
   - [ ] Toggle: Normal vs Crisis correlations

3. **Time to Break-even**
   - [ ] Calculate recovery time per scenario
   - [ ] Best/worst/expected cases
   - [ ] Compare to historical recoveries
   - [ ] Alert if recovery >5 years

4. **Scenario Saving**
   - [ ] Zustand state allows saving scenarios
   - [ ] Compare saved scenarios side-by-side
   - [ ] Share scenarios with team
   - [ ] Delete/archive old scenarios

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ForecastChart.test.jsx` | Chart renders, animation triggers |
| `ScenarioComparison.test.jsx` | Side-by-side display, delta calculation |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 60.3: Liquidity Stress Test 'Bank Run' Simulator

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Scenario/BankRunSim.jsx` | Simulator widget |
| `[NEW]` | `frontend2/src/widgets/Scenario/BankRunSim.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Scenario/ExitPlaybook.jsx` | Playbook generator |

### Verbose Acceptance Criteria

1. **Depth of Market Drying Visualization**
   - [ ] Animated visualization of order book during liquidation
   - [ ] Show spreading bid-ask as volume increases
   - [ ] Time progression slider
   - [ ] Impact cost accumulation

2. **Toxic Position Identification**
   - [ ] Identify illiquid positions that could trap capital
   - [ ] "Toxicity Score" per position
   - [ ] Warning for positions >10% of daily volume to exit
   - [ ] Suggested exit timeline

3. **Emergency Exit Playbook**
   - [ ] Auto-generate liquidation priority order
   - [ ] Consider tax implications
   - [ ] Estimate total slippage cost
   - [ ] Export as PDF action plan

4. **Simulation Parameters**
   - [ ] Configure market stress level (1x-5x normal selling)
   - [ ] Time horizon (1 day, 1 week, 1 month)
   - [ ] Assume market circuit breakers
   - [ ] Include after-hours liquidity

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `BankRunSim.test.jsx` | Simulation runs, visualization works |
| `ExitPlaybook.test.jsx` | Playbook generates, PDF export |

### Test Coverage Target: **85%**

---

## Route Integration

**Route:** `/guardian/scenarios`

**Macro Task:** The Guardian

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

