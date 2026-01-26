# Phase 61: Philanthropy & Impact Investing Dashboard

> **Phase ID**: 61 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Completes the homeostasis loop by routing 'Excess Alpha' back to the external environment.

---

## Overview

Manages automated charitable routing and ESG impact tracking. This phase ensures that once the portfolio achieves "Enough," the excess capital is systematically directed toward positive impact, creating a sustainable equilibrium between wealth accumulation and societal benefit.

---

## Sub-Deliverable 61.1: Excess Alpha Donation Routing Interface

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Impact/DonationRouter.jsx` | Automated giving interface |
| `[NEW]` | `frontend2/src/widgets/Impact/DonationRouter.css` | Glassmorphism styling |
| `[NEW]` | `frontend2/src/stores/impactStore.js` | Impact state management |
| `[NEW]` | `services/philanthropy/donation_service.py` | Donation routing engine |
| `[NEW]` | `web/api/philanthropy_api.py` | REST endpoints |

### UI/UX Design Specifications

#### Visual Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  🌱 Excess Alpha Donation Router                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Your "Enough" Threshold: $3,000,000                                     │
│  Current Net Worth:       $3,247,500                                     │
│  ────────────────────────────────────────────────────────────────────   │
│  EXCESS ALPHA:            $247,500  [✨ Ready for Impact]               │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Allocation Pipeline                                             │    │
│  │                                                                   │    │
│  │  ┌───────────┐    ┌───────────┐    ┌───────────┐                │    │
│  │  │ 🌍 Climate│───▶│ 📚 Education│──▶│ 🏥 Health│                │    │
│  │  │   40%     │    │    35%     │    │   25%    │                │    │
│  │  │ $99,000   │    │ $86,625    │    │ $61,875  │                │    │
│  │  └───────────┘    └───────────┘    └───────────┘                │    │
│  │                                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  [Configure Allocations] [Trigger Donation] [View Impact History]       │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns
- **Threshold Slider**: Drag to adjust "Enough" number (Framer Motion spring)
- **Allocation Adjustment**: Drag-and-drop percentage distribution
- **Pipeline Animation**: Flow particles move between cause categories
- **Trigger Button**: 3-second hold with progress ring to prevent accidents
- **Confirmation Modal**: Tax implication summary before execution

#### Celebration Animation
```javascript
// On successful donation
confetti({
  particleCount: 150,
  spread: 80,
  origin: { y: 0.6 },
  colors: ['#22c55e', '#3b82f6', '#f59e0b']
});
```

### Verbose Acceptance Criteria

1. **Giving API Integration**
   - [ ] GivingBlock API for crypto donations
   - [ ] CharityNavigator API for charity verification
   - [ ] Secure webhook for donation confirmation
   - [ ] Real-time status tracking

2. **Tax Deduction Alpha**
   - [ ] Calculate tax savings from charitable deductions
   - [ ] Display "Effective Cost" of donation
   - [ ] Year-end tax projection impact
   - [ ] Export for CPA documentation

3. **Impact Pulse Feed**
   - [ ] Real-time fund impact visualization
   - [ ] Projects funded by your donations
   - [ ] Beneficiary stories (where available)
   - [ ] Social sharing option (optional)

4. **Automation Rules**
   - [ ] Auto-donate when excess exceeds threshold for N days
   - [ ] Monthly/quarterly scheduled donations
   - [ ] Tax-loss harvesting coordination
   - [ ] Override controls for manual intervention

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DonationRouter.test.jsx` | Threshold slider, allocation drag, trigger hold, confirmation |
| `impactStore.test.js` | Allocation persistence, automation rules |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/philanthropy/test_donation_service.py` | `test_api_integration`, `test_tax_calculation`, `test_automation_trigger` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 61.2: ESG (Environmental, Social, Governance) Score Aggregator

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Impact/ESGScores.jsx` | Triple-gauge display |
| `[NEW]` | `frontend2/src/widgets/Impact/ESGScores.css` | Styling |
| `[NEW]` | `services/analysis/esg_service.py` | ESG data aggregation |

### UI/UX Design Specifications

#### Triple Circular Gauge Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  🌿 Portfolio ESG Composite Score                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│       🌎 Environmental      👥 Social          🏛️ Governance           │
│        ┌─────────┐         ┌─────────┐         ┌─────────┐              │
│        │         │         │         │         │         │              │
│        │   78    │         │   65    │         │   82    │              │
│        │   /100  │         │   /100  │         │   /100  │              │
│        └─────────┘         └─────────┘         └─────────┘              │
│           A-                   B                   A                     │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Portfolio Karma Score: 74 / 100  ⭐⭐⭐⭐                         │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  Sin Stock Alert: 2 positions violate your filters                      │
│  [View Details] [Configure Filters]                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Gauge Animation
- **Fill Animation**: Arc fills from 0 to score value (1.5s, ease-out-cubic)
- **Color Gradient**: Red (0-30) → Yellow (31-60) → Green (61-100)
- **Hover Effect**: Gauge expands 10%, shows breakdown tooltip
- **Data Update**: Smooth transition when Kafka feeds new data

### Verbose Acceptance Criteria

1. **Real-time ESG Updates**
   - [ ] Kafka macro feeds for ESG data
   - [ ] Multiple data provider aggregation (MSCI, Sustainalytics)
   - [ ] Weighted average by position size
   - [ ] Historical trend sparklines

2. **Sin Stock Filtering**
   - [ ] User-defined "Sin Stock" categories (tobacco, arms, gambling, fossil fuels)
   - [ ] Automatic alert on exposure
   - [ ] Suggested divestment actions
   - [ ] "Ethical Exception" override with reason logging

3. **Portfolio Karma Score**
   - [ ] Aggregated ESG metric displayed in main header
   - [ ] Contribution breakdown by holding
   - [ ] Peer comparison (vs. S&P 500 ESG average)
   - [ ] Improvement recommendations

4. **Component Deep Dives**
   - [ ] Click gauge to see detailed component breakdown
   - [ ] Environmental: Carbon, Water, Waste metrics
   - [ ] Social: Labor, Diversity, Community metrics
   - [ ] Governance: Board, Ethics, Transparency metrics

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ESGScores.test.jsx` | Gauges render, animations play, sin stock alert, karma updates |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_esg_service.py` | `test_score_aggregation`, `test_sin_filter`, `test_karma_calculation` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 61.3: Carbon Footprint vs. Portfolio Return Scatterplot

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Impact/CarbonScatter.jsx` | D3.js scatterplot |
| `[NEW]` | `frontend2/src/widgets/Impact/CarbonScatter.css` | Styling |

### UI/UX Design Specifications

#### Scatterplot Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  🌡️ Alpha Efficiency vs. Carbon Intensity                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Return ▲                                                                │
│    +40% │                           ◉ NVDA                              │
│    +30% │                    ◉ MSFT      ◉ AAPL                        │
│    +20% │        ◉ NEE                                                  │
│    +10% │  ◉ AES                    ─────────── Regression Line        │
│     0%  ├──────────────────────────────────────────────────────▶       │
│   -10% │              ◉ XOM         ◉ CVX                              │
│   -20% │                        ◉ BP                                    │
│         │    Low Carbon ◀────────────────▶ High Carbon                 │
│                                                                          │
│  Correlation: -0.34 (Weak negative - ethics doesn't hurt returns)       │
│                                                                          │
│  [🌱 Offset Portfolio Carbon: $4,200]  [View Emission Details]          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns
- **Dot Sizing**: By position size (larger = bigger dot)
- **Hover Tooltip**: Company name, return, tCO2e, Scope 1/2/3 breakdown
- **Zoom/Pan**: D3 zoom behavior for exploring dense regions
- **Selection**: Click dot to highlight in portfolio grid
- **Regression Line**: Animated draw with correlation coefficient

### Verbose Acceptance Criteria

1. **Return-Efficiency Visualization**
   - [ ] Regression line showing correlation
   - [ ] Statistical significance indicator
   - [ ] Historical correlation trend
   - [ ] Sector coloring option

2. **Carbon Offset Integration**
   - [ ] One-click buy carbon credits
   - [ ] Proportional to portfolio emissions
   - [ ] Verified offset providers only
   - [ ] Certificate storage in vault

3. **Emissions Data**
   - [ ] Scope 1: Direct emissions
   - [ ] Scope 2: Electricity/energy
   - [ ] Scope 3: Value chain emissions
   - [ ] Data source attribution

4. **Portfolio Optimization**
   - [ ] "Greener Alternative" suggestions
   - [ ] Impact on expected return
   - [ ] Sector balance considerations
   - [ ] One-click swap execution

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `CarbonScatter.test.jsx` | Plot renders, hover tooltip, offset button, regression line |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_esg_service.py` | `test_emissions_calculation`, `test_offset_pricing`, `test_correlation_analysis` |

### Test Coverage Target: **85%**

---

## Route Integration

**Route:** `/strategist/impact`

**Macro Task:** Excess Alpha Recycling

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Impact

# Backend
.\venv\Scripts\python.exe -m pytest tests/philanthropy/ tests/analysis/test_esg_service.py -v --cov=services
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/strategist/impact
# Verify: Donation router works, ESG gauges animate, carbon scatter interactive
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 61 with enhanced UI/UX and interaction patterns |
