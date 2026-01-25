# Phase 60: Scenario Modeling & 'What-If' Impact Simulator

> **Phase ID**: 60 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Anticipates 'Black Swan' shocks by stress-testing the Yellowstone equilibrium.

---

## Overview

Interactive 'Torture Chamber' for simulating extreme macro shifts. This phase provides the warden with the ability to stress-test portfolio resilience against catastrophic scenarios before they occur, enabling proactive hedging decisions.

---

## Sub-Deliverable 60.1: Drag-and-Drop Macro Event Trigger

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Scenario/EventTrigger.jsx` | Macro shock interface |
| `[NEW]` | `frontend2/src/widgets/Scenario/EventTrigger.css` | Glassmorphism styling |
| `[NEW]` | `frontend2/src/stores/scenarioStore.js` | Scenario state management |
| `[NEW]` | `services/analysis/scenario_service.py` | Shock propagation engine |
| `[NEW]` | `web/api/scenario_api.py` | REST endpoints |

### UI/UX Design Specifications

#### Visual Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  🌪️ Scenario Torture Chamber                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Available Shocks (Drag onto Portfolio)                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 🛢️ Oil   │ │ 📈 Fed   │ │ 🦠 Pandemic│ │ 💣 Geo-  │ │ 🏦 Bank  │       │
│  │ $150/bbl │ │ +200bps  │ │ Lockdown │ │ political│ │ Failure │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│        ↓ Drag Here ↓                                                     │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                                                                    │  │
│  │   📊 PORTFOLIO IMPACT ZONE                                        │  │
│  │                                                                    │  │
│  │   Net Worth: $2,450,000  →  $1,892,000 (-22.8%)                   │  │
│  │                                                                    │  │
│  │   🛡️ Hedge Coverage: 68% (Insufficient for this shock)            │  │
│  │                                                                    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  [Reset] [Save Scenario] [Apply Hedge Recommendations]                   │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns
- **Drag Initiation**: Touch/click-hold on shock card (0.2s delay to prevent accidental)
- **Drop Zone Feedback**: Glow effect on portfolio zone when dragging over (box-shadow pulse)
- **Impact Animation**: Numbers animate from current → shocked value (CountUp.js, 1.5s)
- **Shake Effect**: Portfolio container shakes briefly on large shocks (> 15% impact)
- **Undo Gesture**: Swipe right on applied shock to remove, or shake device (mobile)

#### Shock Card Design
```css
.shock-card {
  width: 100px;
  height: 80px;
  background: linear-gradient(135deg, rgba(239,68,68,0.3), rgba(239,68,68,0.1));
  border: 1px solid rgba(239,68,68,0.5);
  border-radius: 8px;
  cursor: grab;
  transition: transform 0.2s, box-shadow 0.2s;
}
.shock-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(239,68,68,0.3);
}
.shock-card.dragging {
  cursor: grabbing;
  opacity: 0.8;
  transform: scale(1.05) rotate(-2deg);
}
```

### Verbose Acceptance Criteria

1. **Neo4j Correlation Propagation**
   - [ ] Shock propagates through correlation graph (Oil → Airlines, Energy, Transport)
   - [ ] Visual highlighting of affected sectors on graph
   - [ ] Cascade intensity based on edge weights
   - [ ] Second-order effects visualization (Airlines → Tourism → Hotels)

2. **Real-time Net Worth Impact**
   - [ ] Header displays shocked Net Worth instantly
   - [ ] Delta shown as both absolute and percentage
   - [ ] Color coding: Red (>10% loss), Yellow (5-10%), Green (<5%)
   - [ ] Historical comparison: "Worse than 2008?" indicator

3. **Hedge Sufficiency Indicator**
   - [ ] Visual 'Shield' icon with fill level (0-100%)
   - [ ] Green glow if hedges absorb shock
   - [ ] Red pulse if hedges insufficient
   - [ ] One-click hedge recommendations

4. **Custom Shock Builder**
   - [ ] Create custom shocks with multiple parameters
   - [ ] Save custom shocks to library
   - [ ] Share scenarios with team members
   - [ ] Import historical black swan templates

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `EventTrigger.test.jsx` | Drag works, drop calculates impact, animation plays, reset clears |
| `scenarioStore.test.js` | Shock propagation, hedge calculation, custom shock saving |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_scenario_service.py` | `test_correlation_propagation`, `test_impact_calculation`, `test_hedge_sufficiency`, `test_custom_shock_persistence` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 60.2: Portfolio Revaluation Forecast Chart (Framer Motion)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Scenario/ForecastChart.jsx` | Animated forecast |
| `[NEW]` | `frontend2/src/widgets/Scenario/ForecastChart.css` | Styling |

### UI/UX Design Specifications

#### Visual Layout
```
┌───────────────────────────────────────────────────────────────────────┐
│  📉 Shock Trajectory & Recovery Forecast                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   $2.5M ┤                                    ╭──────────────          │
│         │     Current                       ╱    Recovery              │
│   $2.0M ┤─────────────╮                   ╱                           │
│         │              ╲                 ╱                             │
│   $1.5M ┤               ╲───────────────╯                             │
│         │                 ↑ Shock Point                                │
│   $1.0M ┤                                                              │
│         │                                                              │
│   $0.5M ┤                                                              │
│         └────┬────┬────┬────┬────┬────┬────┬────┬────┬───→            │
│             Now  +1m  +3m  +6m  +1y  +2y  +3y  +4y  +5y               │
│                                                                        │
│  Time to Break-even: 18 months │ Recovery Probability: 87%            │
└───────────────────────────────────────────────────────────────────────┘
```

#### Animation Specifications
- **Path Draw**: SVG path animates from left to right (Framer Motion, 2s duration)
- **Shock Point**: Pulsing red dot with expanding ring animation
- **Recovery Zone**: Gradient fill from red (shock) to green (recovery)
- **Tooltip Follow**: Crosshair follows cursor with value/date display
- **Confidence Band**: Shaded area showing 10th-90th percentile paths

### Verbose Acceptance Criteria

1. **Correlation Breakdown Modeling**
   - [ ] Model when all assets fall in unison (correlation → 1.0)
   - [ ] Visual indicator of "contagion risk"
   - [ ] Historical correlation during past crises
   - [ ] Dynamic correlation slider for sensitivity analysis

2. **Time-to-Break-even Calculation**
   - [ ] Based on historical recovery averages
   - [ ] Adjusts for current market conditions
   - [ ] Best/Expected/Worst case scenarios
   - [ ] Countdown display in months

3. **Multi-Scenario Comparison**
   - [ ] Zustand state saves multiple scenarios
   - [ ] Side-by-side view of up to 4 scenarios
   - [ ] Color-coded path lines per scenario
   - [ ] Export comparison report

4. **Interactive Time Scrubbing**
   - [ ] Drag slider to see portfolio value at any future point
   - [ ] Real-time probability update as time moves
   - [ ] Marker for "point of no return" if applicable

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ForecastChart.test.jsx` | Chart animates, tooltip works, scenarios compare, time scrub |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_scenario_service.py` | `test_recovery_projection`, `test_correlation_breakdown`, `test_breakeven_calculation` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 60.3: Liquidity Stress Test 'Bank Run' Simulator

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Scenario/BankRunSim.jsx` | Liquidity simulator |
| `[NEW]` | `frontend2/src/widgets/Scenario/BankRunSim.css` | Styling |

### UI/UX Design Specifications

#### Visual Layout - DOM Depletion Animation
```
┌───────────────────────────────────────────────────────────────────────┐
│  💸 Liquidity Stress Test: "Can You Exit?"                            │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Depth of Market Simulation (Your sell orders vs. available bids)     │
│                                                                        │
│  ████████████████████████████  Bid Depth                              │
│  ████████████████             Your Orders                              │
│  ██████████                   Remaining Bids After Impact             │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ Position      │ Size      │ Est. Slippage │ Time to Exit │ Risk │  │
│  ├───────────────┼───────────┼───────────────┼──────────────┼──────┤  │
│  │ AAPL          │ $450,000  │ 0.12%         │ 2 min        │ 🟢   │  │
│  │ Crypto Fund LP│ $280,000  │ 3.45%         │ 72 hours     │ 🔴   │  │
│  │ Private Equity│ $150,000  │ N/A           │ 90+ days     │ ⚫   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                        │
│  Total Portfolio: $2,450,000 │ Liquid in 1 hour: $890,000 (36%)       │
│                                                                        │
│  [📋 Generate Emergency Exit Playbook]                                 │
└───────────────────────────────────────────────────────────────────────┘
```

#### Animation - DOM Depletion
- **Histogram Bars**: Animate depletion as orders consume bids (60 FPS)
- **Color Transition**: Green → Yellow → Red as depth depletes
- **Sound Effect**: Optional "cash register" sounds per lot sold
- **Completion State**: "All Clear" green banner or "Trapped" red warning

### Verbose Acceptance Criteria

1. **Depth of Market Visualization**
   - [ ] 60 FPS histogram of bid depth consumption
   - [ ] Real-time slippage calculation per position
   - [ ] Market impact preview before execution
   - [ ] Compare normal vs. crisis liquidity

2. **Toxic Position Identification**
   - [ ] Flag illiquid positions that could trap capital
   - [ ] Calculate "days to exit" for each position
   - [ ] Risk rating: 🟢 Liquid, 🟡 Moderate, 🔴 Illiquid, ⚫ Trapped
   - [ ] Suggest liquidity improvement actions

3. **Emergency Exit Playbook**
   - [ ] Auto-generate prioritized liquidation order
   - [ ] Consider tax implications in sequence
   - [ ] Broker-specific constraints (settlement, limits)
   - [ ] PDF export with SHA-256 integrity hash

4. **Scenario Parameters**
   - [ ] Adjustable market-wide liquidity factor (0.1x to 1.0x normal)
   - [ ] Time-of-day consideration (market hours vs. after-hours)
   - [ ] Concurrent seller assumptions (% of float trying to exit)

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `BankRunSim.test.jsx` | DOM animates, positions rated, playbook generates |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_scenario_service.py` | `test_slippage_calculation`, `test_liquidity_rating`, `test_exit_sequence_optimization` |

### Test Coverage Target: **85%**

---

## Route Integration

**Route:** `/analyst/scenarios`

**Macro Task:** Black Swan Preparedness

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Scenario

# Backend
.\venv\Scripts\python.exe -m pytest tests/analysis/test_scenario_service.py -v --cov=services/analysis
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/analyst/scenarios
# Verify: Drag shock works, forecast animates, bank run simulates
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 60 with detailed UI/UX specifications |
