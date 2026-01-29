import pytest
from services.quantitative.outlier_detector import VolatilityOutlierFilter

def test_outlier_detection_3_sigma():
    svc = VolatilityOutlierFilter()
    # 10 similar returns + 1 massive spike (e.g. flash crash)
    rets = [0.01] * 10 + [-0.15]
    res = svc.detect_outliers(rets, sigma_threshold=3.0)
    assert len(res) == 1
    assert res[0]["index"] == 10
    assert res[0]["return"] == -0.15

def test_no_outliers():
    svc = VolatilityOutlierFilter()
    rets = [0.01, 0.012, 0.009, 0.011] * 3
    assert len(svc.detect_outliers(rets)) == 0
