"""Unit tests for vendor audit script."""
import pytest
from pathlib import Path

class TestVendorAudit:
    def test_auditor_instantiation(self):
        """Test that VendorAuditor can be instantiated."""
        from scripts.runners.vendor_audit import VendorAuditor
        auditor = VendorAuditor()
        assert auditor.vendors == []

    def test_vendor_mappings_exist(self):
        """Test that vendor mappings are properly defined."""
        from scripts.runners.vendor_audit import VENDOR_MAPPINGS
        assert "stripe" in VENDOR_MAPPINGS
        assert "plaid" in VENDOR_MAPPINGS
        assert "twilio" in VENDOR_MAPPINGS
        assert "openai" in VENDOR_MAPPINGS

    def test_vendor_mapping_structure(self):
        """Test that each vendor mapping has required fields."""
        from scripts.runners.vendor_audit import VENDOR_MAPPINGS
        required_keys = ["vendor_name", "purpose", "env_vars", "documentation_url", "cost_tier"]
        
        for sdk_name, config in VENDOR_MAPPINGS.items():
            for key in required_keys:
                assert key in config, f"Missing '{key}' in {sdk_name} mapping"
