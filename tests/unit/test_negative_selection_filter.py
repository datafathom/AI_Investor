import pytest
from services.analysis.negative_selection_filter import NegativeSelectionFilter

def test_negative_selection_detection():
    filter_svc = NegativeSelectionFilter()
    listings = [
        {"ticker": "ABC", "prev_rank": 800, "curr_rank": 1500, "perf_12m": -0.60},
        {"ticker": "XYZ", "prev_rank": 1500, "curr_rank": 1400, "perf_12m": 0.10}
    ]
    laggards = filter_svc.filter_laggards(listings)
    assert len(laggards) == 1
    assert laggards[0]["ticker"] == "ABC"

def test_no_laggards():
    filter_svc = NegativeSelectionFilter()
    listings = [{"ticker": "GOOG", "prev_rank": 5, "curr_rank": 5}]
    assert len(filter_svc.filter_laggards(listings)) == 0
