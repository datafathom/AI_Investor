import pytest
from services.neo4j.affiliate_graph import AffiliateGraph

@pytest.fixture
def graph():
    return AffiliateGraph()

def test_map_affiliate(graph):
    # Test mapping structure
    res = graph.map_affiliate("u_77", "NVDA", "DIRECTOR")
    assert res["user_id"] == "u_77"
    assert res["ticker"] == "NVDA"
    assert res["role"] == "DIRECTOR"
    assert res["status"] == "MAPPED"

def test_get_insider_exposure(graph):
    # Test exposure retrieval (mock)
    exposure = graph.get_insider_exposure("u_77")
    assert isinstance(exposure, list)
    assert len(exposure) > 0
    assert "ticker" in exposure[0]
    assert "role" in exposure[0]
