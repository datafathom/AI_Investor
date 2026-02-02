import pytest
from services.neo4j.mobility_graph import MobilityGraph

@pytest.fixture
def m_graph():
    return MobilityGraph()

def test_map_citizenship(m_graph):
    res = m_graph.map_citizenship("u_101", "IT", "HERITAGE")
    assert res["user_id"] == "u_101"
    assert res["country"] == "IT"
    assert res["type"] == "HERITAGE"
    assert res["status"] == "MAPPED"

def test_find_heritage_path(m_graph):
    paths = m_graph.find_heritage_path("u_101", "IE")
    assert isinstance(paths, list)
    assert len(paths) > 0
    assert "ELIGIBILITY_CONFIRMED" in paths
