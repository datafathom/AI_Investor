import pytest
from uuid import UUID
from services.estate.funding_monitor import FundingMonitor

@pytest.fixture
def monitor():
    return FundingMonitor()

def test_funding_monitor_singleton():
    s1 = FundingMonitor()
    s2 = FundingMonitor()
    assert s1 is s2

def test_check_funding_status(monitor):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    result = monitor.check_funding_status(trust_id)
    assert len(result) > 0
    assert result[0]['status'] == "TITLED"
    assert result[1]['status'] == "UNFUNDED"
