import pytest
from services.estate.snt_filter import SNTDistributionFilter
from services.estate.resource_monitor import ResourceMonitor

@pytest.fixture
def snt_filter():
    return SNTDistributionFilter()

@pytest.fixture
def monitor():
    return ResourceMonitor()

def test_snt_filter_allowed_vendor(snt_filter):
    # Medical to vendor is allowed
    result = snt_filter.validate_payout("VENDOR", "MEDICAL")
    assert result['is_allowed'] is True
    assert result['impact_on_ssi'] == "NONE"

def test_snt_filter_blocked_food(snt_filter):
    # Food is prohibited
    result = snt_filter.validate_payout("VENDOR", "FOOD")
    assert result['is_allowed'] is False
    assert result['impact_on_ssi'] == "BENEFIT_REDUCTION"

def test_resource_monitor_risk(monitor):
    # $1900 is risky (near $2k limit)
    result = monitor.check_eligibility_risk(1900.0)
    assert result['is_eligible'] is True
    assert result['risk_level'] == "HIGH"
