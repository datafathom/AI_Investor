import pytest
from services.tax.estate_exclusion import EstateExclusionAnalyzer

def test_irrevocable_funded_exclusion():
    svc = EstateExclusionAnalyzer()
    # 5M Irrevocable, titled -> 5M excluded
    res = svc.analyze_exclusion(5000000, "IRREVOCABLE", True)
    assert res["is_excluded"] == True
    assert res["excluded_amount"] == 5000000.0
    assert res["probate_status"] == "AVOIDED"

def test_irrevocable_unfunded_exposure():
    svc = EstateExclusionAnalyzer()
    # 5M Irrevocable but NOT titled -> 0 excluded, exposed to probate
    res = svc.analyze_exclusion(5000000, "IRREVOCABLE", False)
    assert res["is_excluded"] == False
    assert res["probate_status"] == "EXPOSED_TO_PROBATE"

def test_revocable_taxable_inclusion():
    svc = EstateExclusionAnalyzer()
    # Revocable is always taxable
    res = svc.analyze_exclusion(5000000, "REVOCABLE", True)
    assert res["is_excluded"] == False
    assert res["taxable_amount"] == 5000000.0
