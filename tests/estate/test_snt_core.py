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
    result = snt_filter.validate_distribution("VENDOR", "MEDICAL_REHABILITATION", 100.0)
    assert result['status'] == "ALLOWED"
    assert result['risk_level'] == "LOW"

def test_snt_filter_blocked_food(snt_filter):
    # Food is restricted (ISM reduction)
    result = snt_filter.validate_distribution("VENDOR", "FOOD_GROCERIES", 100.0)
    assert result['status'] == "WARNING"
    assert result['risk_level'] == "HIGH"

def test_resource_monitor_risk(monitor):
    # $1900 is risky (near $2k limit)
    from decimal import Decimal
    result = monitor.check_eligibility_buffer(Decimal('1900.00'))
    assert result['is_within_limit'] is True
    # Buffer is 100 < 500 -> WARNING
    assert result['recommend_action'] == "WARNING"
