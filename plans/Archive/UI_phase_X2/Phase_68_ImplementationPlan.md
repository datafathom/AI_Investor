# Phase 68: The Homeostasis 'Zen' Mode

> **Phase ID**: 68 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: The ultimate goal: the absence of unnecessary oscillation and the focus on 'Enough'.

---

## Overview

A minimalist interface focused on long-term peace of mind and goal achievement. This is the terminal phase of the AI_Investor expansion, representing the pinnacle of the homeostasis philosophy.

---

## Sub-Deliverable 68.1: Minimalist Goal Tracking UI (The 'Enough' Metric)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/pages/ZenMode.jsx` | Zen page |
| `[NEW]` | `frontend2/src/widgets/Zen/ZenMode.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Zen/GoalProgress.jsx` | Progress bar |
| `[NEW]` | `services/portfolio/homeostasis_service.py` | Zen logic |

### Verbose Acceptance Criteria

1. **Noise Reduction**
   - [ ] Hide all price charts
   - [ ] No red/green flash indicators
   - [ ] Calm, muted color palette
   - [ ] Slow, deliberate animations only

2. **Freedom Number Progress**
   - [ ] Simple progress bar to user-defined "Freedom Number"
   - [ ] Tailwind neon "Glow" effect when goal reached
   - [ ] Percentage complete display
   - [ ] "You're X% to Enough" message

3. **Income vs Expenses Focus**
   - [ ] "Projected Annual Income" from dividends/interest
   - [ ] vs "Annual Expenses" (user-defined)
   - [ ] "Covered: X years of expenses" calculation
   - [ ] "The Gap" metric for homeostasis

### Test Coverage Target: **80%**

---

## Sub-Deliverable 68.2: Time-to-Retirement Countdown & Probability Gauge

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Zen/RetirementGauge.jsx` | D3.js gauge |
| `[NEW]` | `frontend2/src/widgets/Zen/RetirementGauge.css` | Styling |

### Verbose Acceptance Criteria

1. **Monte Carlo Survival**
   - [ ] 10k path simulation
   - [ ] Target > 99% success probability
   - [ ] Red warning if < 90%
   - [ ] Animated probability display

2. **Safety Buffer**
   - [ ] "X years of expenses covered" display
   - [ ] Adjust for inflation
   - [ ] Best/Expected/Worst scenarios
   - [ ] Visual confidence band

3. **Lifestyle Toggle**
   - [ ] Zustand-based "Frugal vs Lux" switch
   - [ ] Immediate recalculation
   - [ ] Side-by-side comparison option

### Test Coverage Target: **80%**

---

## Sub-Deliverable 68.3: System Autopilot Master Override (The 'Peace of Mind' Toggle)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Zen/AutopilotToggle.jsx` | Master switch |
| `[NEW]` | `frontend2/src/widgets/Zen/AutopilotToggle.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Zen/HomeostasisOverlay.jsx` | Zen overlay |

### Verbose Acceptance Criteria

1. **High-Frequency Disable**
   - [ ] Disable all high-frequency Kafka consumers
   - [ ] Agents shift to dividend-seeking logic
   - [ ] No active trading mode
   - [ ] Capital preservation focus

2. **Manual Trading Lock**
   - [ ] Lock out all manual trading buttons
   - [ ] Prevent emotional intervention
   - [ ] Re-authentication required to unlock
   - [ ] Cool-down period enforcement

3. **Homeostatic Display**
   - [ ] "System Homeostatic" status message
   - [ ] 20px backdrop-blur overlay
   - [ ] Slow-moving particle animation
   - [ ] Optional calming ambient sounds

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/zen`

**Macro Task:** Ultimate Equilibrium

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Zen

# Backend
.\venv\Scripts\python.exe -m pytest tests/portfolio/test_homeostasis_service.py -v --cov=services/portfolio
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/zen
# Verify: Goal progress shown, no flashy charts, autopilot toggles correctly
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 68 - Final Phase |
