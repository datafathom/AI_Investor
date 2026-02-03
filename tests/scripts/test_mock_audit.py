"""Unit tests for mock audit script."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

class TestMockAudit:
    def test_auditor_instantiation(self):
        """Test that MockAuditor can be instantiated."""
        from scripts.runners.mock_audit import MockAuditor
        auditor = MockAuditor()
        assert auditor.entries == []
        assert auditor.stats["total"] == 0

    def test_keyword_detection(self):
        """Test that mock keywords are properly detected."""
        from scripts.runners.mock_audit import MOCK_KEYWORDS
        assert "mock" in MOCK_KEYWORDS
        assert "TODO" in MOCK_KEYWORDS
        assert "FIXME" in MOCK_KEYWORDS

    def test_add_entry(self):
        """Test entry addition updates stats correctly."""
        from scripts.runners.mock_audit import MockAuditor
        auditor = MockAuditor()
        auditor._add_entry("test.py", 1, "keyword_match", "snippet", "action", "critical")
        
        assert len(auditor.entries) == 1
        assert auditor.stats["total"] == 1
        assert auditor.stats["critical"] == 1
