import pytest
from services.neo4j.policy_graph import PolicyGraph

@pytest.fixture
def p_graph():
    return PolicyGraph()

def test_map_policy_impact(p_graph):
    res = p_graph.map_policy_impact("NO", "WEALTH_TAX", 0.9)
    assert res["country"] == "NO"
    assert res["policy"] == "WEALTH_TAX"
    assert res["severity"] == 0.9
    assert res["status"] == "MAPPED"

def test_get_impacted_investments(p_graph):
    investments = p_graph.get_impacted_investments("NATIONALIZATION")
    assert isinstance(investments, list)
    assert len(investments) > 0
