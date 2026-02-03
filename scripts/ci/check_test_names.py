"""
CI Script: Check Test Naming Conventions

This script enforces that test files do not contain "phase", "sprint", or similar
temporal project management terms in their filenames. Tests must be named semantically.

Usage:
    python scripts/ci/check_test_names.py

Exit Codes:
    0 - All test names compliant (pass)
    1 - Found non-compliant test names (fail)
"""
import sys
import re
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).parent.parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"

# Patterns that are forbidden in test filenames
FORBIDDEN_PATTERNS = [
    r"phase[-_]?\d+",  # Matches phase-1, phase_1, phase1
    r"sprint[-_]?\d+", # Matches sprint-1, sprint_1, sprint1
    r"p\d{2,}",        # Matches p01, p45 (legacy shorthand for phase)
]

def main() -> int:
    """Main function. Returns exit code."""
    print("=" * 60)
    print("CI Check: Test Naming Convention Enforcer")
    print("=" * 60)
    
    violations: List[Path] = []
    
    # compiled regular expressions
    regexes = [re.compile(p, re.IGNORECASE) for p in FORBIDDEN_PATTERNS]

    # Scan only the tests directory
    for test_file in TESTS_DIR.rglob("*.py"):
        filename = test_file.name
        
        for regex in regexes:
            if regex.search(filename):
                violations.append(test_file)
                break

    if violations:
        print(f"\n❌ FAIL: Found {len(violations)} test file(s) with forbidden naming patterns:\n")
        for test_file in violations:
            print(f"  {test_file.relative_to(PROJECT_ROOT)}")
        print("\n→ Action: Rename these files to reflect the FEATURE being tested (e.g., test_billing.py), not the phase.")
        return 1
    else:
        print(f"\n✅ PASS: All test filenames are semantically named")
        return 0

if __name__ == "__main__":
    sys.exit(main())
