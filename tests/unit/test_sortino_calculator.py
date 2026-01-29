import pytest
from services.quantitative.sortino_calculator import SortinoCalculator

def test_sortino_asymmetric():
    svc = SortinoCalculator()
    # Case: High upside vol, low downside vol
    # rets: [5%, -1%, 5%, -1%]
    rets = [0.05, -0.01, 0.05, -0.01]
    # Sharpe would include the 5% spikes as "risk"
    # Sortino should only penalize the -1% drops
    res = svc.calculate_sortino(rets, 0.05)
    assert res > 0

def test_sortino_no_losses():
    svc = SortinoCalculator()
    # Pure gains -> 0 downside dev -> high sortino
    rets = [0.01, 0.02, 0.01]
    res = svc.calculate_sortino(rets, 0.0)
    assert res == 99.9

def test_downside_deviation_accuracy():
    svc = SortinoCalculator()
    # 0% target. returns: [-5%, 5%].
    # downside: [-5%]. 
    rets = [-0.05, 0.05]
    # Annualized dev of 5% hit
    dev = svc.calculate_downside_deviation(rets, 0.0)
    assert dev > 0
