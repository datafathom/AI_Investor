import pytest
from services.compliance.sma_risk_verifier import SMARiskVerifier

def test_sma_verified_reduction():
    svc = SMARiskVerifier()
    # SMA 0.5% std, Bench 1.0% std
    sma_r = [0.005, -0.005] * 10
    bench_r = [0.01, -0.01] * 10
    res = svc.verify_vol_reduction(sma_r, bench_r)
    assert res["is_lower_risk"] == True
    assert res["vol_reduction"] > 0

def test_sma_failed_reduction():
    svc = SMARiskVerifier()
    # SMA more volatile than bench
    sma_r = [0.02, -0.02] * 10
    bench_r = [0.01, -0.01] * 10
    res = svc.verify_vol_reduction(sma_r, bench_r)
    assert res["is_lower_risk"] == False
