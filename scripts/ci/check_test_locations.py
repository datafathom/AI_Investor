"""
CI Script: Check Test Locations

This script enforces that all Python test files (starting with test_ or ending with _test.py)
are located exclusively within the tests/ directory.

Usage:
    python scripts/ci/check_test_locations.py

Exit Codes:
    0 - All tests correctly located (pass)
    1 - Found misplaced tests (fail)
"""
import sys
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).parent.parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"

# Patterns defining a test file
TEST_PATTERNS = ["test_*.py", "*_test.py"]

# Directories to exclude from scanning (e.g., venv, node_modules)
EXCLUDE_DIRS = [
    "venv",
    "node_modules",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache"
]

def is_excluded(path: Path) -> bool:
    """Check if path is in an excluded directory."""
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False

def main() -> int:
    """Main function. Returns exit code."""
    print("=" * 60)
    print("CI Check: Test Location Enforcer")
    print("=" * 60)

    misplaced_tests: List[Path] = []
    
    # helper to check if a file is inside tests/
    # using strict string check on resolved paths to avoid symlink confusion
    tests_dir_abs = TESTS_DIR.resolve()

    # Scan the entire project root
    for pattern in TEST_PATTERNS:
        for file_path in PROJECT_ROOT.rglob(pattern):
            if is_excluded(file_path):
                continue
            
            try:
                # Check if the file is strictly relative to tests_dir
                file_path.resolve().relative_to(tests_dir_abs)
            except ValueError:
                # relative_to raises ValueError if not relative, meaning it's outside tests/
                # Exception: check if it is explicitly skipped/allowed (none for now)
                misplaced_tests.append(file_path)

    if misplaced_tests:
        print(f"\n❌ FAIL: Found {len(misplaced_tests)} test file(s) outside of tests/ directory:\n")
        for test_file in misplaced_tests:
            print(f"  {test_file.relative_to(PROJECT_ROOT)}")
        print("\n→ Action: Move these files into the appropriate subdirectory in tests/")
        return 1
    else:
        print(f"\n✅ PASS: All test files are correctly located in tests/")
        return 0

if __name__ == "__main__":
    sys.exit(main())
