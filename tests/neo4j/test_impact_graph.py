import pytest
from services.neo4j.impact_graph import ImpactGraph

@pytest.fixture
def i_graph():
    return ImpactGraph()

def test_map_impact_event(i_graph):
    res = i_graph.map_impact_event("u_99", "GREENPEACE", 0.85)
    assert res["user_id"] == "u_99"
    assert res["charity"] == "GREENPEACE"
    assert res["score"] == 0.85
    assert res["status"] == "MAPPED"

def test_map_heir_legacy(i_graph):
    res = i_graph.map_heir_legacy("u_99", "u_100", "ESTATE_DISTRIBUTION")
    assert res["parent"] == "u_99"
    assert res["heir"] == "u_100"
    assert res["legacy"] == "ESTATE_DISTRIBUTION"
    assert res["status"] == "MAPPED"
