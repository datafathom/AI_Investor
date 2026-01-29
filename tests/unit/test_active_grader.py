import pytest
from services.quantitative.active_share_grader import ActiveShareGrader

def test_alpha_master_grade():
    svc = ActiveShareGrader()
    # 3% alpha, positive in bear market
    assert svc.grade_manager(0.03, 0.01) == "ALPHA_MASTER"

def test_benchmark_hugger():
    svc = ActiveShareGrader()
    # 0.1% alpha
    assert svc.grade_manager(0.001, 0.0) == "BENCHMARK_HUGGER"

def test_laggard():
    svc = ActiveShareGrader()
    # -2% alpha
    assert svc.grade_manager(-0.02, -0.05) == "LAGGARD"
