import pytest
from services.neo4j.flow_graph import FlowGraph

@pytest.fixture
def f_graph():
    return FlowGraph()

def test_map_passive_inflow(f_graph):
    res = f_graph.map_passive_inflow("VANGUARD_VOO", "NVDA", 1000000.0)
    assert res["fund"] == "VANGUARD_VOO"
    assert res["ticker"] == "NVDA"
    assert res["status"] == "MAPPED"

def test_query_structural_risk(f_graph):
    risks = f_graph.query_structural_risk("AAPL")
    assert isinstance(risks, list)
    assert len(risks) > 0
    assert "exposure" in risks[0]
