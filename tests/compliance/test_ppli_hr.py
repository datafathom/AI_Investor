import pytest
from decimal import Decimal
from services.compliance.mec_tester import MECTester
from services.hr.heir_governance_svc import HeirGovernanceService

@pytest.fixture
def mec_tester():
    return MECTester()

@pytest.fixture
def heir_svc():
    return HeirGovernanceService()

def test_mec_compliance_pass(mec_tester):
    # Limit $1M, Paid $500k -> PASS
    result = mec_tester.run_7pay_test(Decimal('1000000'), Decimal('500000'))
    assert result['is_mec_compliant'] is True
    assert result['status'] == "TAX_FREE_WRAPPER"

def test_mec_compliance_fail(mec_tester):
    # Paid $1.1M -> FAIL
    result = mec_tester.run_7pay_test(Decimal('1000000'), Decimal('1100000'))
    assert result['is_mec_compliant'] is False
    assert result['status'] == "TAXABLE_MEC"

def test_heir_role_audit_nepotism(heir_svc):
    # 200k salary, 100k market -> 2.0x ratio -> Nepotism
    result = heir_svc.evaluate_role_productivity(None, "VP", 200000, 100000)
    assert result['status'] == "CUSHY_JOB"
    assert result['pay_premium_pct'] == 100.0
