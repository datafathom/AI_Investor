# departmentRegistry.js — The Navigation & Routing Source of Truth

> **Last Updated**: 2026-02-14
> **File**: `Frontend/src/config/departmentRegistry.js`
> **Consumers**: `MenuBar.jsx`, `DynamicWorkstation`, route test files, CLI verification tools

## Overview

The `departmentRegistry.js` is the **single source of truth** for department configuration across the Sovereign OS frontend. It defines every department's identity, routing, navigation structure, and sub-module inventory. Any change to how departments appear in navigation, what pages they expose, or how URLs are structured starts here.

## Data Structure

```javascript
export const DEPT_REGISTRY = {
  [departmentId]: {
    id: Number,           // Unique department identifier (1-19)
    name: String,         // Human-readable name ("Data Scientist", "Stress Tester")
    slug: String,         // URL slug ("data-scientist", "stress-tester")
    basePath: String,     // Root URL path ("/data-scientist", "/stress-tester")
    icon: String,         // Lucide icon name ("Brain", "Zap")
    description: String,  // Short department description
    subModules: [
      {
        path: String,     // Full URL path ("/auditor/attribution-analysis")
        label: String,    // Navigation display text ("Attribution Analysis")
        icon: String,     // Lucide icon name for this sub-module
      },
      // ... more sub-modules
    ],
  },
};
```

## Department Inventory (as of 2026-02-14)

| ID | Name | Slug | SubModules Count |
|----|------|------|------------------|
| 1 | Orchestrator | `orchestrator` | ~15 |
| 2 | Data Scientist | `data-scientist` | ~18 |
| 3 | Strategist | `strategist` | ~12 |
| 4 | Trader | `trader` | ~16 |
| 5 | Physicist | `physicist` | ~10 |
| 6 | Hunter | `hunter` | ~14 |
| 7 | Sentry | `sentry` | ~11 |
| 8 | Steward | `steward` | ~9 |
| 9 | Guardian | `guardian` | ~8 |
| 10 | Architect | `architect` | ~12 |
| 11 | Lawyer | `lawyer` | ~10 |
| 12 | Auditor | `auditor` | ~21 |
| 13 | Envoy | `envoy` | ~10 |
| 14 | Front Office | `front-office` | ~5 |
| 15 | Historian | `historian` | ~4 |
| 16 | Stress Tester | `stress-tester` | ~10 |
| 17 | Refiner | `refiner` | ~10 |
| 18 | Banker | `banker` | ~14 |
| 19 | System Administration | `admin` | ~40 |

## How the Registry Connects to the Rest of the System

### MenuBar.jsx (Navigation)

The `MenuBar` component reads `DEPT_REGISTRY` to dynamically construct department dropdown menus:

1. Iterates over all department entries (excluding ID 19 / admin from the main list)
2. For each department, renders a dropdown with the department name and icon
3. Each `subModule` becomes a clickable `<Link>` in the dropdown
4. Admin department (ID 19) is handled separately with role-based visibility

### DynamicWorkstation (Route Resolution)

When a user clicks a subModule link (e.g., `/auditor/attribution-analysis`):

1. React Router matches `/:deptSlug/:subSlug`
2. `DynamicWorkstation` extracts `deptSlug = "auditor"` and `subSlug = "attribution-analysis"`
3. Converts to PascalCase: `Auditor` + `AttributionAnalysis`
4. Searches `pages/workstations/auditor/` for matching files
5. Lazy-loads and renders the matched component

### Route Test Files (Verification)

The route test files in `DEBUGGING/FrontEndAudit/Routes2Test/depts/` reference the same URL paths from the registry's `subModules`. The verification framework navigates to each URL and checks the page status.

### CLI Verification (Proposed)

A proposed `frontend validate-registry` CLI command would cross-reference every `subModule.path` in the registry against actual files in `pages/workstations/` to identify gaps.

## Registry Integrity Rules

### Every subModule MUST have:

1. **A workstation file** in `pages/workstations/<dept-slug>/` following the `DeptPascalSubPascal.jsx` naming convention
2. **A route test entry** in the corresponding department's route test file
3. **A valid Lucide icon** name in the `icon` field

### Known Gaps (Backlog)

28 subModule paths do not currently have workstation files. These are pre-existing entries that were in the registry before the admin route migration and need separate implementation work:

- `special/terminal`, `special/mission-control`, `special/homeostasis`, `special/command`, `special/venn`, `special/search`
- `architect/blueprints`
- `data-scientist/debate`, `data-scientist/debate-history`, `data-scientist/forced-sellers`, `data-scientist/whale-flow`, `data-scientist/indicators`, `data-scientist/social-sentiment-radar`, `data-scientist/factor-analysis`, `data-scientist/fundamental-scanner`, `data-scientist/quant-backtest`
- `trader/execution`
- `hunter/pulse`, `hunter/unusual-options`, `hunter/news-aggregator`, `hunter/social-trading-feed`, `hunter/rumor-mill`
- `sentry/firewall`
- `lawyer/library`
- `legal/144a-compliance` (note: uses `legal` slug but department slug is `lawyer`)
- `auditor/equity-curve` (duplicate entry)
- `envoy/inbox`

## Modifying the Registry

### Adding a New SubModule

```javascript
// In the target department's subModules array:
subModules: [
  // ... existing entries ...
  { path: "/dept-slug/new-feature", label: "New Feature", icon: "Star" },
],
```

Then create the corresponding file: `pages/workstations/<dept-slug>/<DeptPascal>NewFeature.jsx`

### Adding a New Department

Add a new entry to `DEPT_REGISTRY` with the next available ID:

```javascript
20: {
  id: 20,
  name: "New Department",
  slug: "new-dept",
  basePath: "/new-dept",
  icon: "Sparkles",
  description: "Description of what this department does",
  subModules: [],
},
```

Then create the directory: `pages/workstations/new-dept/`

### Removing a SubModule

1. Remove the entry from `subModules` in the registry
2. Optionally delete the workstation file (or keep it for the admin path)
3. Remove the corresponding URL from the route test file
