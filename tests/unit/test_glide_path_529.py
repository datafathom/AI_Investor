import pytest
from services.education.glide_path_529 import GlidePathRecommender529

def test_glide_path_aggressive():
    rec = GlidePathRecommender529()
    # 18 years out -> high equity
    res = rec.recommend_allocation(18)
    assert res["equity"] == 0.90

def test_glide_path_capital_preservation():
    rec = GlidePathRecommender529()
    # 1 year out -> high cash
    res = rec.recommend_allocation(1)
    assert res["cash"] == 0.50
    assert res["equity"] == 0.10
