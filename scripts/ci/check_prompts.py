"""
CI Script: Check for Hardcoded Prompts

This script scans agent files for hardcoded LLM prompts that should be
externalized to agents/prompts/prompts.json.

Usage:
    python scripts/ci/check_prompts.py

Exit Codes:
    0 - All prompts externalized (pass)
    1 - Found hardcoded prompts (fail)
"""
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).parent.parent.parent
AGENTS_DIR = PROJECT_ROOT / "agents"

# Patterns that indicate hardcoded LLM prompts
PROMPT_PATTERNS = [
    r'(?:self\.)?system_prompt\s*=\s*["\'](?:[^"\']{150,})',  # Long string assignment
    r'"""You are\s',  # Triple-quoted prompts starting with "You are"
    r"'''You are\s",  # Single triple-quoted prompts
    r'"Act as\s(?:[^"]{100,})"',  # "Act as" prompts
]

# Files to skip (known good)
SKIP_FILES = [
    "prompt_loader.py",
    "__init__.py",
    "base_agent.py"
]


def scan_file(file_path: Path) -> List[Tuple[int, str]]:
    """Scan a file for hardcoded prompts. Returns list of (line_num, snippet)."""
    violations = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern in PROMPT_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append((i, line.strip()[:80]))
                    break
    except Exception as e:
        print(f"Warning: Could not scan {file_path}: {e}")
    
    return violations


def main() -> int:
    """Main function. Returns exit code."""
    print("=" * 60)
    print("CI Check: Hardcoded Prompts Scanner")
    print("=" * 60)
    
    total_violations = 0
    files_with_issues = []
    
    # Scan all Python files in agents/
    for py_file in AGENTS_DIR.rglob("*.py"):
        if py_file.name in SKIP_FILES:
            continue
        
        violations = scan_file(py_file)
        
        if violations:
            relative_path = py_file.relative_to(PROJECT_ROOT)
            files_with_issues.append((relative_path, violations))
            total_violations += len(violations)
    
    # Report results
    if files_with_issues:
        print(f"\n❌ FAIL: Found {total_violations} hardcoded prompt(s)\n")
        for file_path, violations in files_with_issues:
            print(f"  {file_path}:")
            for line_num, snippet in violations:
                print(f"    Line {line_num}: {snippet}...")
        print("\n→ Action: Externalize these prompts to agents/prompts/prompts.json")
        return 1
    else:
        print(f"\n✅ PASS: No hardcoded prompts detected")
        print(f"  Scanned {sum(1 for _ in AGENTS_DIR.rglob('*.py'))} files")
        return 0


if __name__ == "__main__":
    sys.exit(main())
