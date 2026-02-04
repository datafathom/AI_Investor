# Phase 5: Frontend Performance Optimization
## Implementation Plan - Source of Truth

**Parent Roadmap**: [ROADMAP_2_03_26.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/2_03_26/ROADMAP_2_03_26.md)

---

## 📋 Phase Overview

| Attribute | Value |
|-----------|-------|
| **Phase Number** | 5 |
| **Focus Area** | Frontend Performance |
| **Deliverables** | 4 (Storage, Concurrent Rendering, Web Workers, Resource Optimization) |
| **Estimated Effort** | 5-7 days |
| **Dependencies** | None |

> [!IMPORTANT]
> This phase transforms the frontend from "React App" to "High-Performance Financial Terminal".

---

## 5.1 Advanced Storage Implementation (App-Wide)

### Goal
Replace 100% of direct `localStorage.getItem/setItem` calls with a tiered `StorageService`.

### Target Files (Refactor List)
The following files likely use `localStorage` and MUST be updated to use `src/utils/storageService.js`:
- `src/stores/*.js` (Zustand persistance middleware)
- `src/hooks/useLocalStorage.js` (Update implementation)
- `src/auth.js` (Token storage -> Shift to Secure/IndexedDB if possible, or keep Local but wrapped)
- `src/Settings/Settings.jsx` (User preferences)

### Implementation Detail
1.  **Create** `src/utils/storageService.js` (Tiered: Memory -> IDB -> Local).
2.  **Create** `src/utils/indexedDBProvider.js` (Wrapper for `idb`).
3.  **Refactor**: Search project for `localStorage`. Replace with `await StorageService.get(...)`.

## 5.2 React Concurrent Features (Targeted & App-Wide)

### Goal
Eliminate UI freezing during heavy renders using React 18+ features.

### Target Components (Verified "Heavy" Files)
We have identified the largest components in `frontend2/src/pages/` and `components/`. These are the **primary targets**:

| Component | Size | Optimization Strategy |
|-----------|------|-----------------------|
| `PoliticalAlpha.jsx` | **40KB** | **Lazy Load** sections using `Suspense`. Use `useTransition` for tabs. |
| `Dashboard.jsx` | **32KB** | **Lazy Load** widgets. Use `useDeferredValue` for layout shifts. |
| `DebateRoom.jsx` | **15KB** | **useTransition** for incoming chat messages/updates. |
| `GlobalScanner.jsx` | **12KB** | **useDeferredValue** for search input to prevent typing lag. |
| `AdvancedRiskDashboard.jsx` | **12KB** | **Offload** calculations to Worker (see 5.3). |
| `AutoCoderDashboard.jsx` | **10KB** | **Memoize** syntax highlighting or editor views. |

### Implementation Detail
- **Suspense**: Wrap all top-level Route components in `App.jsx` with `Suspense`.
- **Transitions**: Wrap state updates that cause heavy re-renders (like filtering a table) in `startTransition(() => { setSearch(value) })`.

## 5.3 Web Worker Offloading (App-Wide Calculation)

### Goal
Move all financial math off the main thread.

### Implementation
1.  **Create** `src/workers/calculationWorker.js`.
2.  **Create** `src/services/workerManager.js` (Singleton).
3.  **Refactor Targets**:
    - `AdvancedRiskDashboard.jsx`: Move VaR/Drawdown math to worker.
    - `PortfolioOptimizationDashboard.jsx`: Move Optimizer logic to worker.
    - `AdvancedChartingDashboard.jsx`: Move data normalization/parsing to worker.

## 5.4 Resource Optimization (App-Wide)

### Goal
Lighthouse Score > 90.

### Implementation
1.  **Fonts**: Add `<link rel="preload" ...>` for Inter font in `index.html`.
2.  **Images**: Add `loading="lazy"` to all `<img>` tags in `src/components/`.
3.  **Virtualization**: Use `react-window` for any list > 50 items (e.g. `DebateRoom` chat, `GlobalScanner` results).

## 📊 Verification Plan
### Automated Tests (Jest)
- `tests/utils/storageService.test.js`: Verify IDB fallback and tiers.
- `tests/workers/calculationWorker.test.js`: Verify complex math returns correct results off-thread.

### Manual Verification (Lighthouse)
- Run Chrome DevTools > Lighthouse on `http://localhost:5173/dashboard`.
- **Pass Criteria**:
    - **LCP**: < 2.5s
    - **TBT**: < 200ms
    - **CLS**: < 0.1
    - **Score**: > 90 (Performance) on Desktop.
