# Proposed CLI Command: `frontend validate-registry`

> **Last Updated**: 2026-02-14
> **Status**: PROPOSED (not yet implemented)
> **Priority**: Medium — would catch registry-file mismatches before they become runtime errors
> **Category**: Frontend Verification / Quality Assurance

## Problem Statement

The `departmentRegistry.js` file defines `subModules` entries with URL paths that are expected to resolve to workstation files in `Frontend/src/pages/workstations/`. Currently, there is no automated way to verify that every registry entry has a corresponding file on disk. Gaps between the registry and the filesystem can lead to:

1. **Navigation broken links** — users click a menu item and see `WORKSTATION_NOT_FOUND`
2. **Silent failures** — no build error, no test failure, just broken navigation at runtime
3. **Audit blind spots** — the route verification framework tests URLs but doesn't validate file existence

A `frontend validate-registry` CLI command would close this gap.

## Proposed Behavior

### Command Syntax

```bash
python cli.py frontend validate-registry
```

### What It Would Do

1. **Parse** `Frontend/src/config/departmentRegistry.js` to extract all `subModule` entries with their `path` and `label` fields
2. **Scan** `Frontend/src/pages/workstations/` recursively for all `.jsx` files
3. **Simulate** the same 3-strategy matching that `DynamicWorkstation` uses in `App.jsx`:
   - Strategy 1: Exact `SubPascal.jsx` in the department folder
   - Strategy 2: `DeptPascalSubPascal.jsx` (case-insensitive)
   - Strategy 3: Loose case-insensitive `SubPascal.jsx` match
4. **Report** results in a structured format:
   - ✅ Resolved entries (registry → file match found)
   - ❌ Missing entries (registry path has no matching file)
   - ⚠️ Orphaned files (workstation files with no registry entry)

### Expected Output

```
=== Frontend Registry Validation ===

Scanning departmentRegistry.js ... 259 subModule entries found
Scanning pages/workstations/ ... 125 .jsx files found

--- Resolution Results ---

[AUDITOR] 21/21 subModules resolved ✅
  ✅ /auditor/attribution → AuditorAttribution.jsx
  ✅ /auditor/attribution-analysis → AuditorAttributionAnalysis.jsx
  ... (all green)

[DATA-SCIENTIST] 9/18 subModules resolved ⚠️
  ✅ /data-scientist/backtest-engine → DataScientistBacktestEngine.jsx
  ✅ /data-scientist/correlation-risk → DataScientistCorrelationRisk.jsx
  ❌ /data-scientist/debate → NO MATCHING FILE
  ❌ /data-scientist/debate-history → NO MATCHING FILE
  ❌ /data-scientist/forced-sellers → NO MATCHING FILE
  ... 

[SPECIAL] 0/6 subModules resolved ❌
  ❌ /special/terminal → NO MATCHING FILE
  ... 

--- Orphaned Files (No Registry Entry) ---
  ⚠️ workstations/architect/ArchitectCapex.jsx → No subModule path found
  ...

--- Summary ---
  Total subModules: 259
  Resolved: 213 (82.2%)
  Missing files: 28 (10.8%)
  Skipped (admin/special): 18 (6.9%)
  Orphaned files: 5

  EXIT CODE: 1 (failures detected)
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All non-admin subModules resolve to files |
| 1 | One or more subModules have no matching file |

### CLI Flags (Optional)

| Flag | Purpose |
|------|---------|
| `--include-admin` | Also validate admin department subModules |
| `--include-orphans` | Report workstation files without registry entries |
| `--json` | Output results as JSON for CI/CD pipelines |
| `--fix-missing` | Auto-generate placeholder workstation files for missing entries |
| `--dept <slug>` | Validate only a specific department |

## Implementation Notes

### File Location

```
scripts/runners/frontend_validate_registry_runner.py
```

### CLI Configuration Entry

Add to `config/cli_configuration.json`:

```json
{
  "command": "frontend validate-registry",
  "description": "Validate that all departmentRegistry.js subModules have matching workstation files",
  "runner": "scripts/runners/frontend_validate_registry_runner.py",
  "function": "run"
}
```

### Key Implementation Logic

The core matching logic must replicate the `DynamicWorkstation` component's 3-strategy approach. Here's the pseudocode:

```python
def to_pascal(slug: str) -> str:
    """Convert kebab-case to PascalCase: 'attribution-analysis' -> 'AttributionAnalysis'"""
    return ''.join(word.capitalize() for word in slug.split('-'))

def find_workstation_file(dept_slug: str, sub_slug: str, all_files: list[str]) -> str | None:
    dept_pascal = to_pascal(dept_slug)
    sub_pascal = to_pascal(sub_slug)
    combined = dept_pascal + sub_pascal
    
    # Strategy 1: Exact SubPascal match
    for f in all_files:
        if f"/{dept_slug}/" in f and f.endswith(f"/{sub_pascal}.jsx"):
            return f
    
    # Strategy 2: DeptPascal+SubPascal (case-insensitive)
    for f in all_files:
        if f"/{dept_slug}/" in f and f.lower().endswith(f"/{combined.lower()}.jsx"):
            return f
    
    # Strategy 3: Loose case-insensitive
    for f in all_files:
        if f"/{dept_slug}/" in f and f.lower().endswith(f"/{sub_pascal.lower()}.jsx"):
            return f
    
    return None
```

### Integration with Existing Verification

This command complements the existing `frontend verify all-depts` command:

- `validate-registry` = **Static check** — file existence, no server needed
- `verify all-depts` = **Runtime check** — browser navigation, page content verification

Both should be part of a comprehensive frontend CI pipeline.

## Relationship to Other CLI Commands

| Command | What It Checks |
|---------|---------------|
| `frontend verify <dept>` | Navigates URLs in browser, checks page content |
| `frontend verify all-depts` | Runs verify for all departments |
| `frontend validate-registry` (proposed) | Static cross-reference of registry vs files |
| `frontend build` | Production build with Vite |

## Priority Justification

This command is medium priority because:

1. **Build doesn't catch it** — Vite only validates imported files, not the registry-to-file mapping
2. **Runtime errors are silent** — a missing file just shows "WORKSTATION_NOT_FOUND" with no build failure
3. **Fast to run** — pure filesystem operations, no browser or server needed (<1 second)
4. **Useful for CI** — would catch missing files in PR reviews before they reach production
