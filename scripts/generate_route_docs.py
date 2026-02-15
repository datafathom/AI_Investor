"""
Generate per-route .md documentation files for every subModule
in departmentRegistry.js.

Creates:
  docs/frontend/routes/depts/<dept_slug>_routes/<subpage_slug>.md

Each file documents current state and has a planning roadmap section.
"""
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


# ── paths ───────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "Frontend" / "src" / "config" / "departmentRegistry.js"
DOCS_ROOT = PROJECT_ROOT / "docs" / "frontend" / "routes" / "depts"
SPECIAL_DOCS = PROJECT_ROOT / "docs" / "frontend" / "routes" / "depts" / "special_routes"


import subprocess

def parse_registry() -> dict[str, Any]:
    """
    Extract department data by running a node script to dump the registry to JSON.
    Returns dict keyed by dept id (as string in JSON).
    """
    try:
        result = subprocess.run(
            ["node", "scripts/dump_registry.mjs"],
            capture_output=True,
            text=True,
            check=True,
            cwd=PROJECT_ROOT
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running node script: {e.stderr}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}

# ... (rest of file)

def main() -> None:
    """Generate all route documentation files."""
    print("Reading departmentRegistry.js via Node...")
    departments = parse_registry()

    print(f"Found {len(departments)} departments")



def path_to_slug(route_path: str) -> str:
    """Convert a route path like /orchestrator/fleet to a filename slug."""
    # Take the last segment(s) after the dept slug
    parts = route_path.strip("/").split("/")
    if len(parts) >= 2:
        return parts[-1]
    return parts[0]


def generate_doc(
    dept_name: str,
    dept_slug: str,
    dept_description: str,
    quadrant: str,
    sub_label: str,
    sub_path: str,
    sub_description: str,
) -> str:
    """Generate the markdown content for a single route doc."""
    return f"""# {sub_label}

> **Department**: {dept_name}
> **Quadrant**: {quadrant}
> **Route**: `{sub_path}`

## Overview

{sub_description}

---

## Current State

<!-- Document the current implementation status of this page -->

| Aspect | Status |
|--------|--------|
| Component File | <!-- e.g. `Frontend/src/pages/workstations/{dept_slug}/SubPage.jsx` --> |
| Backend Service | <!-- e.g. `services/service_name/` --> |
| API Endpoints | <!-- e.g. `GET /api/v1/{dept_slug}/...` --> |
| Data Store | <!-- Zustand store or Context used --> |
| Implementation | 🔴 Not Started / 🟡 Stub / 🟢 Complete |

### UI Components Used

<!-- List the key UI components rendered on this page -->

- 

### Data Flow

<!-- Describe how data flows from backend to this page -->

1. 

---

## Planning & Roadmap

<!-- Define the target GUI and functionality for this page -->

### MVP Requirements

- [ ] 

### Enhanced Features

- [ ] 

### Design Notes

<!-- Link to mockups, wireframes, or design references -->

---

## Dependencies

| Dependency | Type | Status |
|-----------|------|--------|
| <!-- e.g. Market Data API --> | Backend | <!-- Ready / Needed --> |

---

## Notes

<!-- Any additional context, known issues, or technical debt -->

"""


def main() -> None:
    """Generate all route documentation files."""
    print("Reading departmentRegistry.js via Node...")
    departments = parse_registry()

    print(f"Found {len(departments)} departments")

    total_files = 0
    skipped_files = 0

    # Track special routes separately
    special_routes: list[dict[str, str]] = []

    # Filter out non-numeric keys if any (e.g. comments or metadata)
    dept_ids = [k for k in departments.keys() if k.isdigit()]
    
    # Sort numerically
    dept_ids.sort(key=int)

    for dept_id_str in dept_ids:
        dept = departments[dept_id_str]
        dept_id = int(dept_id_str)
        
        dept_slug = dept["slug"]
        dept_name = dept["name"]
        dept_description = dept["description"]
        quadrant = dept["quadrant"]

        # Create dept folder
        dept_folder = DOCS_ROOT / f"{dept_slug}_routes"
        dept_folder.mkdir(parents=True, exist_ok=True)

        # 1. Generate _Dashboard_<DeptName>.md
        dashboard_filename = f"_Dashboard_{dept_name.replace(' ', '')}.md"
        dashboard_filepath = dept_folder / dashboard_filename
        
        if not dashboard_filepath.exists():
            dashboard_content = generate_doc(
                dept_name, dept_slug, dept_description,
                quadrant, "Department Dashboard", f"/dept/{dept_slug}", 
                f"Main dashboard for {dept_name}. {dept_description}"
            )
            dashboard_filepath.write_text(dashboard_content, encoding="utf-8")
            total_files += 1

        # De-duplicate subModules by path
        seen_paths: set[str] = set()
        unique_subs = []
        for sub in dept.get("subModules", []):
            if sub["path"] not in seen_paths:
                seen_paths.add(sub["path"])
                unique_subs.append(sub)

        for sub in unique_subs:
            sub_path = sub["path"]
            sub_label = sub["label"]
            sub_description = sub["description"]

            # Determine if this is a special route (cross-department)
            is_special = sub_path.startswith("/special/")
            # Also check if it's already covered by another dept (unlikely with this iteration)
            
            if is_special:
                # Special routes go to special_routes folder
                page_slug = path_to_slug(sub_path)
                target_folder = SPECIAL_DOCS
                target_folder.mkdir(parents=True, exist_ok=True)
                filepath = target_folder / f"{page_slug}.md"

                if filepath.exists():
                    skipped_files += 1
                    continue

                content = generate_doc(
                    dept_name, dept_slug, dept_description,
                    quadrant, sub_label, sub_path, sub_description,
                )
                filepath.write_text(content, encoding="utf-8")
                total_files += 1
                special_routes.append({"path": sub_path, "label": sub_label})
                continue

            # Normal dept route
            page_slug = path_to_slug(sub_path)
            filepath = dept_folder / f"{page_slug}.md"

            if filepath.exists():
                skipped_files += 1
                continue

            content = generate_doc(
                dept_name, dept_slug, dept_description,
                quadrant, sub_label, sub_path, sub_description,
            )
            filepath.write_text(content, encoding="utf-8")
            total_files += 1

        print(f"  [{dept_id:2d}] {dept_name:<25s} → {len(unique_subs)} routes ({dept_slug}_routes/)")

    print(f"\nCreated {total_files} new files ({skipped_files} already existed)")
    print(f"Special routes: {len(special_routes)} files in special_routes/")
    print("Done!")


if __name__ == "__main__":
    main()
