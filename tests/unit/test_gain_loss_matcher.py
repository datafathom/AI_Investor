import pytest
from services.tax.gain_loss_matcher import GainLossMatcher

def test_matching_short_term():
    svc = GainLossMatcher()
    gains = [{"term": "SHORT", "amount": 5000}]
    losses = [{"term": "SHORT", "amount": 3000}]
    res = svc.match_losses(gains, losses)
    assert res["short_term_net"] == 2000.0

def test_full_harvest_offset():
    svc = GainLossMatcher()
    gains = [{"term": "LONG", "amount": 10000}]
    losses = [{"term": "LONG", "amount": 15000}]
    res = svc.match_losses(gains, losses)
    assert res["long_term_net"] == -5000.0
    assert res["total_harvested_offset"] == 15000.0
