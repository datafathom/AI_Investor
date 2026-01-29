import pytest
import uuid
from services.evolution.gene_logic import get_gene_splicer

def test_crossover():
    splicer = get_gene_splicer()
    p1 = {"a": 1, "b": 2, "c": 3}
    p2 = {"a": 10, "b": 20, "c": 30}
    
    child = splicer.crossover(p1, p2)
    
    assert "a" in child
    assert "b" in child
    assert "c" in child
    assert child["a"] in [1, 10]
    assert child["b"] in [2, 20]
    assert child["c"] in [3, 30]

def test_mutate():
    splicer = get_gene_splicer()
    genes = {"rsi": 14, "leverage": 1.5}
    bounds = {"rsi": (7, 21), "leverage": (1.0, 3.0)}
    
    # Force mutation by rate 1.0
    mutated = splicer.mutate(genes, bounds, mutation_rate=1.0)
    
    assert mutated["rsi"] != 14 or mutated["leverage"] != 1.5
    assert 7 <= mutated["rsi"] <= 21
    assert 1.0 <= mutated["leverage"] <= 3.0

def test_splice_agents():
    splicer = get_gene_splicer()
    p1_genes = {"rsi": 14}
    p2_genes = {"rsi": 21}
    bounds = {"rsi": (7, 30)}
    
    result = splicer.splice_agents("P1", "P2", p1_genes, p2_genes, bounds)
    
    assert result["id"].startswith("AGENT-")
    assert result["parents"] == ["P1", "P2"]
    assert "rsi" in result["genes"]
    assert result["status"] == "born"
