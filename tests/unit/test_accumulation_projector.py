import pytest
from services.retirement.accumulation_projector import AccumulationProjector

def test_accumulation_growth():
    projector = AccumulationProjector()
    # Start: 100k, Contrib: 10k, Rate: 10%
    # Year 1: (100k * 1.1) + 10k = 120k
    res = projector.project_growth(100000, 10000, 0.10, 1)
    assert res[0]["ending_balance"] == 120000.0

def test_multi_year_accumulation():
    projector = AccumulationProjector()
    res = projector.project_growth(0, 1000, 0.10, 2)
    # Yr 1: (0 * 1.1) + 1000 = 1000
    # Yr 2: (1000 * 1.1) + 1000 = 2100
    assert res[1]["ending_balance"] == 2100.0
