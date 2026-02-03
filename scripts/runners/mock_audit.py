"""
Mock Audit Script - Phase 2.1
Scans the codebase for hardcoded/mock data that needs real implementation.
"""
import os
import re
import json
import ast
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_PATH = PROJECT_ROOT / "notes" / "MockResponses_needImplemenetation.json"

# Directories to scan
SCAN_DIRECTORIES = [
    "services",
    "agents", 
    "web/routes",
    "apis"
]

# Keywords indicating mock/placeholder code
MOCK_KEYWORDS = [
    "mock", "dummy", "fake", "sample_data", "placeholder",
    "TODO", "FIXME", "hardcoded", "stub", "test_data"
]

# Known hotspot files to specifically verify
KNOWN_HOTSPOTS = [
    "services/trading/fx_service.py",
    "services/trading/simulation_service.py",
    "services/payments/plaid_service.py",
    "services/social/youtube_client.py",
    "services/reputation/deepfake_detect.py"
]


class MockAuditor:
    """Scans Python files for mock/hardcoded data patterns."""
    
    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []
        self.stats = {"total": 0, "critical": 0, "warning": 0}
    
    def scan_all(self) -> Dict[str, Any]:
        """Main entry point - scan all configured directories."""
        for directory in SCAN_DIRECTORIES:
            dir_path = PROJECT_ROOT / directory
            if dir_path.exists():
                self._scan_directory(dir_path)
        
        # Also verify known hotspots
        for hotspot in KNOWN_HOTSPOTS:
            hotspot_path = PROJECT_ROOT / hotspot
            if hotspot_path.exists() and not any(e["file"] == hotspot for e in self.entries):
                self._scan_file(hotspot_path)
        
        return {
            "summary": self.stats,
            "entries": self.entries
        }
    
    def _scan_directory(self, directory: Path) -> None:
        """Recursively scan a directory for Python files."""
        for file_path in directory.rglob("*.py"):
            # Skip test files
            if "test" in file_path.name.lower() or "/tests/" in str(file_path):
                continue
            self._scan_file(file_path)
    
    def _scan_file(self, file_path: Path) -> None:
        """Scan a single Python file for mock patterns."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            relative_path = str(file_path.relative_to(PROJECT_ROOT))
            
            # Check for keyword matches
            self._check_keywords(content, relative_path)
            
            # Check for large literal returns
            self._check_literal_returns(content, relative_path)
            
            # Check for test imports in non-test files
            self._check_test_imports(content, relative_path)
            
            # Check for pass statements in methods
            self._check_pass_statements(content, relative_path)
            
        except Exception as e:
            logger.warning(f"Error scanning {file_path}: {e}")
    
    def _check_keywords(self, content: str, file_path: str) -> None:
        """Check for mock-related keywords in comments and code."""
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            for keyword in MOCK_KEYWORDS:
                if keyword.lower() in line_lower:
                    # Skip if it's in a docstring describing the function purpose
                    if line.strip().startswith('#') or '"""' in line or "'''" in line:
                        priority = "warning"
                    else:
                        priority = "critical" if keyword.lower() in ["mock", "fake", "dummy"] else "warning"
                    
                    self._add_entry(
                        file_path, line_num, "keyword_match",
                        line.strip()[:100], 
                        f"Found '{keyword}' - verify if real implementation needed",
                        priority
                    )
                    break  # Only one entry per line
    
    def _check_literal_returns(self, content: str, file_path: str) -> None:
        """Check for functions returning large literal dictionaries/lists."""
        # Simple regex pattern for hardcoded returns
        pattern = r'return\s+\{[^}]{100,}\}'
        for match in re.finditer(pattern, content, re.DOTALL):
            line_num = content[:match.start()].count('\n') + 1
            snippet = match.group(0)[:100] + "..."
            self._add_entry(
                file_path, line_num, "hardcoded_return",
                snippet, "Large hardcoded return - likely needs API integration",
                "critical"
            )
    
    def _check_test_imports(self, content: str, file_path: str) -> None:
        """Check for test module imports in production code."""
        if "from tests" in content or "import tests" in content:
            self._add_entry(
                file_path, 1, "test_import",
                "from tests / import tests",
                "Test module imported in production code",
                "critical"
            )
    
    def _check_pass_statements(self, content: str, file_path: str) -> None:
        """Check for pass statements that might indicate unimplemented methods."""
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped == "pass":
                # Check if previous line is a def statement (unimplemented method)
                if line_num > 1:
                    prev_line = lines[line_num - 2].strip()
                    if prev_line.startswith("def ") and not prev_line.startswith("def __"):
                        self._add_entry(
                            file_path, line_num, "unimplemented_method",
                            prev_line[:80],
                            "Method has only 'pass' - needs implementation",
                            "warning"
                        )
    
    def _add_entry(self, file_path: str, line: int, entry_type: str, 
                   snippet: str, action_item: str, priority: str) -> None:
        """Add an entry to the audit log."""
        self.entries.append({
            "file": file_path,
            "line": line,
            "type": entry_type,
            "snippet": snippet,
            "action_item": action_item,
            "priority": priority
        })
        self.stats["total"] += 1
        if priority == "critical":
            self.stats["critical"] += 1
        else:
            self.stats["warning"] += 1


def run_mock_audit(**kwargs) -> None:
    """CLI handler for running the mock audit."""
    print("Running Mock Audit...")
    
    auditor = MockAuditor()
    results = auditor.scan_all()
    
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nMock Audit Complete!")
    print(f"  Total issues found: {results['summary']['total']}")
    print(f"  Critical: {results['summary']['critical']}")
    print(f"  Warnings: {results['summary']['warning']}")
    print(f"\nOutput saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_mock_audit()
