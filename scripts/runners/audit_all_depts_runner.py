"""
==============================================================================
FILE: scripts/runners/audit_all_depts_runner.py
ROLE: Concurrent department-level frontend audit runner
PURPOSE: Scans all *_routes.py files in the depts folder and runs
         verify_urls for each department concurrently using a thread pool.
USAGE: python cli.py frontend verify all-depts [--workers 3] [--retries 1]
==============================================================================
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

from scripts.runners.frontend_verify_runner import verify_urls

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEPTS_DIR = PROJECT_ROOT / "DEBUGGING" / "FrontEndAudit" / "Routes2Test" / "depts"


def run_all_depts(workers: int = 3, retries: int = 1, skip: Optional[str] = None) -> None:
    """
    Discover all *_routes.py files in the depts folder and run
    verify_urls for each one concurrently with a thread pool.

    Args:
        workers: Number of concurrent audit workers (default 3).
        retries: Max retries per route within each department audit.
        skip: Comma-separated list of dept names to skip (e.g. "admin,architect").
    """
    if not DEPTS_DIR.exists():
        print(f"[ERROR] Depts directory not found: {DEPTS_DIR}", flush=True)
        return

    # Discover all department route files
    route_files = sorted(DEPTS_DIR.glob("*_routes.py"))
    if not route_files:
        print(f"[ERROR] No *_routes.py files found in {DEPTS_DIR}", flush=True)
        return

    # Parse skip list
    skip_set: set[str] = set()
    if skip:
        skip_set = {s.strip().lower() for s in skip.split(",")}

    # Filter out skipped departments
    dept_queue: list[Path] = []
    for f in route_files:
        dept_name = f.stem.replace("_routes", "")
        if dept_name in skip_set:
            print(f"  [SKIP] {dept_name} (user-excluded)", flush=True)
        else:
            dept_queue.append(f)

    total = len(dept_queue)
    print(f"\n{'='*60}", flush=True)
    print(f"  CONCURRENT FRONTEND AUDIT", flush=True)
    print(f"  Departments: {total} | Workers: {workers} | Retries: {retries}", flush=True)
    print(f"{'='*60}\n", flush=True)

    for i, f in enumerate(dept_queue, 1):
        dept_name = f.stem.replace("_routes", "")
        print(f"  [{i:02d}] {dept_name:20s} ({f.name})", flush=True)
    print(flush=True)

    completed_count = 0
    failed_depts: list[str] = []
    results_summary: dict[str, str] = {}
    start_time = time.time()

    def _run_single_dept(route_file: Path) -> tuple[str, bool]:
        """Run a single department audit. Returns (dept_name, success)."""
        dept_name = route_file.stem.replace("_routes", "")
        try:
            print(f"\n>>> [START] {dept_name.upper()} ({route_file.name})", flush=True)
            verify_urls(
                file_path=str(route_file.relative_to(PROJECT_ROOT)),
                retries=retries
            )
            print(f"<<< [DONE]  {dept_name.upper()} ✓", flush=True)
            return dept_name, True
        except Exception as e:
            logger.exception(f"Department audit failed for {dept_name}: {e}")
            print(f"<<< [FAIL]  {dept_name.upper()} ✗ — {e}", flush=True)
            return dept_name, False

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_run_single_dept, route_file): route_file
            for route_file in dept_queue
        }

        for future in as_completed(futures):
            dept_name, success = future.result()
            completed_count += 1
            status = "SUCCESS" if success else "FAILED"
            results_summary[dept_name] = status
            if not success:
                failed_depts.append(dept_name)
            print(f"    Progress: {completed_count}/{total} departments completed", flush=True)

    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    print(f"\n{'='*60}", flush=True)
    print(f"  AUDIT COMPLETE — {minutes}m {seconds}s", flush=True)
    print(f"  Total: {total} | Passed: {total - len(failed_depts)} | Failed: {len(failed_depts)}", flush=True)
    if failed_depts:
        print(f"  Failed: {', '.join(failed_depts)}", flush=True)
    print(f"{'='*60}\n", flush=True)

    # Print per-department summary table
    print(f"  {'Department':<25s} {'Result'}", flush=True)
    print(f"  {'-'*25} {'-'*10}", flush=True)
    for dept_name in sorted(results_summary.keys()):
        marker = "✓" if results_summary[dept_name] == "SUCCESS" else "✗"
        print(f"  {dept_name:<25s} {marker} {results_summary[dept_name]}", flush=True)
    print(flush=True)
