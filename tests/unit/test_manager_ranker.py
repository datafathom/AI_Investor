import pytest
from services.analysis.manager_ranker import ManagerRanker

def test_rank_by_sortino():
    svc = ManagerRanker()
    managers = [
        {"name": "Alpha", "sortino": 1.2},
        {"name": "Beta", "sortino": 2.5},
        {"name": "Gamma", "sortino": 0.8}
    ]
    res = svc.rank_by_sortino(managers)
    assert res[0]["name"] == "Beta"
    assert res[1]["name"] == "Alpha"
    assert res[2]["name"] == "Gamma"

def test_detect_underperformers():
    svc = ManagerRanker()
    managers = [
        {"name": "A", "sortino": 2.0},
        {"name": "B", "sortino": 1.0}
    ]
    # Benchmark is 1.5. B should be flagged.
    under = svc.detect_underperformers(managers, 1.5)
    assert "B" in under
    assert "A" not in under
