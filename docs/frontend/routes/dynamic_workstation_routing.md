# Dynamic Workstation Routing — How Department Pages Load

> **Last Updated**: 2026-02-14
> **Key Files**: `App.jsx` (lines 317–405, 1790–1798), `departmentRegistry.js`
> **Pattern**: URL slug → file glob match → lazy-loaded React component

## Overview

The Sovereign OS frontend uses a **dynamic component loading system** called `DynamicWorkstation` to serve department-specific pages. Instead of declaring hundreds of explicit `<Route>` entries in `App.jsx`, a single catch-all route dynamically resolves URL slugs to JSX files on disk using Vite's `import.meta.glob`.

This architecture enables the team to add new department pages simply by creating a file in the correct directory — no route registration required in `App.jsx`.

## Architecture Flow

```
User navigates to /auditor/attribution-analysis
          │
          ▼
    React Router matches /:deptSlug/:subSlug
          │
          ▼
    DynamicWorkstation component mounts
          │ deptSlug = "auditor"
          │ subSlug  = "attribution-analysis"
          ▼
    import.meta.glob("./pages/workstations/**/*.jsx")
          │ returns map of all 125+ .jsx file paths
          ▼
    3-Strategy file matching:
          │
          ├─ Strategy 1: Exact SubPascal match
          │  "auditor/AttributionAnalysis.jsx"
          │
          ├─ Strategy 2: DeptPascal+SubPascal combined
          │  "auditor/AuditorAttributionAnalysis.jsx"  ← MATCH
          │
          └─ Strategy 3: Case-insensitive fallback
             "auditor/auditorattributionanalysis.jsx"
          │
          ▼
    Lazy import() the matched module
          │
          ▼
    Render module.default as <Component />
```

## File Discovery — `import.meta.glob`

At the top of `App.jsx` (line 317), all workstation files are registered:

```javascript
const workstationModules = import.meta.glob("./pages/workstations/**/*.jsx");
```

This Vite-specific API creates a **lazy-import map** at build time. The keys are relative file paths, the values are `() => import(...)` functions. Example:

```javascript
{
  "./pages/workstations/auditor/AuditorAttribution.jsx": () => import("./pages/workstations/auditor/AuditorAttribution.jsx"),
  "./pages/workstations/auditor/AuditorAttributionAnalysis.jsx": () => import("./pages/workstations/auditor/AuditorAttributionAnalysis.jsx"),
  // ... 123 more entries
}
```

### Why This Matters

- **No manual route registration** — adding a new `.jsx` file to `pages/workstations/<dept>/` automatically makes it routable
- **Code splitting** — each workstation is a separate dynamic import, so browser only downloads what's needed
- **Build-time validation** — Vite resolves all globs during build, so missing files surface immediately

## URL-to-File Resolution — The 3 Strategies

The `DynamicWorkstation` component (lines 319–405) uses three strategies to match a URL slug pair to a file path:

### Strategy 1: Exact SubPascal Match
Converts the `subSlug` to PascalCase and searches for an exact match in the department folder.

```
URL: /data-scientist/backtest-engine
→ subPascal = "BacktestEngine"
→ Searches for: pages/workstations/data-scientist/BacktestEngine.jsx
```

### Strategy 2: DeptPascal + SubPascal Combined (Case-Insensitive)
Concatenates the department and sub-slug PascalCase names and does a case-insensitive match.

```
URL: /auditor/attribution-analysis
→ deptPascal = "Auditor"
→ subPascal = "AttributionAnalysis"
→ Searches for: pages/workstations/auditor/AuditorAttributionAnalysis.jsx (case-insensitive)
```

**This is the primary match strategy for migrated admin routes**, which follow the `DeptPascal + SubPascal` naming convention.

### Strategy 3: Loose Case-Insensitive Fallback
Does a case-insensitive match on just the `subPascal` portion.

```
URL: /hunter/pulse
→ subPascal = "Pulse"
→ Searches for any file ending in /pulse.jsx in the hunter/ folder (case-insensitive)
```

## Route Definitions in `App.jsx`

Two catch-all routes handle the dynamic loading (lines 1790–1798):

```jsx
{/* Primary: /:deptSlug/:subSlug */}
<Route path="/:deptSlug/:subSlug" element={<DynamicWorkstation />} />

{/* Legacy: /dept/:deptSlug/:subSlug */}
<Route path="/dept/:deptSlug/:subSlug" element={<DynamicWorkstation />} />
```

Both patterns trigger the same `DynamicWorkstation` component. The `/dept/` prefix version exists for backward compatibility with older URL formats.

### Route Priority

These catch-all routes are placed **after** all explicit routes in `App.jsx`. React Router evaluates routes top-down, so explicit routes (like `/admin/*`, `/architect/*`, `/account/*`) take priority. The `DynamicWorkstation` catch-all only fires for paths that don't match any explicit route.

## File Naming Convention

All workstation files must follow this naming pattern for the resolution to work:

```
Frontend/src/pages/workstations/<dept-slug>/<DeptPascal><SubPascal>.jsx
```

### Examples

| URL Path | File Path |
|----------|-----------|
| `/auditor/attribution-analysis` | `workstations/auditor/AuditorAttributionAnalysis.jsx` |
| `/data-scientist/backtest-engine` | `workstations/data-scientist/DataScientistBacktestEngine.jsx` |
| `/stress-tester/wargame-arena` | `workstations/stress-tester/StresstesterWargame.jsx` |
| `/refiner/autocoder-sandbox` | `workstations/refiner/RefinerAutocoderSandbox.jsx` |

### Important Notes

- The **directory name** must exactly match the department slug from `departmentRegistry.js` (e.g., `data-scientist`, not `datascientist`)
- The **file name** can use either `SubPascal.jsx` or `DeptPascalSubPascal.jsx` format
- Multi-word slugs like `stress-tester` become `Stresstester` (single word) in the DeptPascal portion — this is by design from the migration script
- The component inside the file **must use `export default`** — the loader accesses `module.default`

## departmentRegistry.js — The Navigation Source of Truth

The `departmentRegistry.js` file at `Frontend/src/config/departmentRegistry.js` is the central configuration for department navigation. It maps department IDs to their metadata, routes, and sub-modules.

### Structure

```javascript
export const DEPT_REGISTRY = {
  1: {
    id: 1,
    name: "Orchestrator",
    slug: "orchestrator",
    basePath: "/orchestrator",
    subModules: [
      { path: "/orchestrator/fleet", label: "Fleet Manager", icon: "Cpu" },
      { path: "/orchestrator/singularity", label: "Singularity Panel", icon: "Zap" },
      // ... more sub-modules
    ],
  },
  // ... departments 2-19
};
```

### How It Connects

1. **`MenuBar.jsx`** reads `DEPT_REGISTRY` to build department navigation dropdowns
2. Each `subModule.path` becomes a clickable navigation link
3. When clicked, React Router matches the path to the `DynamicWorkstation` catch-all
4. `DynamicWorkstation` resolves the slug pair to a file in `pages/workstations/`

### Registry → File Resolution Map

For any `subModule` path like `/auditor/attribution-analysis`:

```
subModule.path = "/auditor/attribution-analysis"
           │
           ├── dept slug: "auditor"
           │   → directory: pages/workstations/auditor/
           │
           └── sub slug: "attribution-analysis"
               → file: AuditorAttributionAnalysis.jsx
```

## Admin Routes — Dual-Path Architecture

The `/admin/*` routes in `App.jsx` (lines 1410–1615) are **separate** from the `DynamicWorkstation` system. Admin pages:

- Live in `Frontend/src/pages/admin/`
- Have explicit `<Route>` entries in `App.jsx`
- Are guarded by `AuthGuard` with admin role enforcement
- Belong to Department ID 19 ("System Administration") in the registry

After the admin route migration, many admin pages now also have department-specific versions:

```
/admin/attribution-analysis  → pages/admin/AttributionAnalysis.jsx   (admin-only, explicit route)
/auditor/attribution-analysis → pages/workstations/auditor/AuditorAttributionAnalysis.jsx (dept route, DynamicWorkstation)
```

Both paths are intentionally kept — the admin version serves the System Administration dashboard, while the dept version serves the department's own dashboard.

## Troubleshooting

### "WORKSTATION_NOT_FOUND" Error
The `DynamicWorkstation` shows this when none of the 3 strategies find a matching file. Common causes:

1. **File naming mismatch** — verify the file follows `DeptPascalSubPascal.jsx` convention
2. **Wrong directory** — file must be in `pages/workstations/<exact-dept-slug>/`
3. **Missing export default** — the file must have `export default ComponentName`
4. **Vite cache stale** — restart the dev server (`npm run dev`) to re-glob files

### Build Fails on Missing Component
If `vite build` fails with `Could not load ... (imported by ...)`, it means a component is explicitly imported somewhere instead of going through the dynamic loader. Check for hardcoded `import` statements.

## Current State (as of 2026-02-14)

| Metric | Count |
|--------|-------|
| Total workstation files | 125 |
| Departments with workstation files | 18 |
| SubModules in registry | ~259 |
| SubModules resolving to files | ~213 |
| SubModules without files (pre-existing gaps) | ~28 |
| Admin pages in `pages/admin/` | ~50+ |
