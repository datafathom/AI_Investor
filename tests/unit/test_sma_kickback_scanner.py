import pytest
from services.compliance.sma_kickback_scanner import SMAKickbackScanner
from uuid import uuid4

def test_kickback_detection():
    scanner = SMAKickbackScanner()
    smas = [
        {"name": "Growth SMA", "has_revenue_share": True},
        {"name": "Value SMA", "has_revenue_share": False}
    ]
    conflicts = scanner.scan_for_kickbacks(uuid4(), smas)
    assert len(conflicts) == 1
    assert conflicts[0]["sma_name"] == "Growth SMA"

def test_kickback_impact():
    scanner = SMAKickbackScanner()
    # 1M AUM, 0.25% share
    impact = scanner.calculate_kickback_impact(1000000, 0.25)
    assert impact == 2500.0
