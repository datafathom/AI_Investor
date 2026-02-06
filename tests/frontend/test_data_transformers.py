import pytest
import math

# Simulating Frontend Logic in Python for Verification
# In a real app, this would be Jest tests. Here we verify the TRANSFORM logic conceptual integrity.

def transform_to_graph(nodes, links, similarity_threshold=0.85):
    """
    Transforms raw API data into GraphData structure.
    Simulates: MemoryService -> Frontend
    """
    valid_links = [
        l for l in links 
        if l['similarity'] >= similarity_threshold
    ]
    return {
        "nodes": nodes,
        "links": valid_links
    }

def transform_to_heatmap(missions):
    """
    Transforms mission list to 100-cell grid.
    """
    grid = [{"id": i, "status": "idle"} for i in range(100)]
    for m in missions:
        if m['slot_id'] < 100:
            grid[m['slot_id']] = {
                "id": m['slot_id'],
                "status": m['status'],
                "mission_id": m['id']
            }
    return grid

def test_graph_filtering():
    nodes = [{"id": 1}, {"id": 2}, {"id": 3}]
    links = [
        {"source": 1, "target": 2, "similarity": 0.90},
        {"source": 2, "target": 3, "similarity": 0.50}, # Should be filtered
        {"source": 1, "target": 3, "similarity": 0.86}
    ]
    
    graph = transform_to_graph(nodes, links, 0.85)
    
    assert len(graph["nodes"]) == 3
    assert len(graph["links"]) == 2
    assert graph["links"][0]["source"] == 1
    assert graph["links"][1]["source"] == 1
    
def test_heatmap_population():
    missions = [
        {"id": "m1", "slot_id": 5, "status": "running"},
        {"id": "m2", "slot_id": 99, "status": "failed"}
    ]
    
    grid = transform_to_heatmap(missions)
    
    assert len(grid) == 100
    assert grid[5]["status"] == "running"
    assert grid[5]["mission_id"] == "m1"
    assert grid[99]["status"] == "failed"
    assert grid[0]["status"] == "idle"

def test_radar_point_generation():
    # Verify that a high cost low profit point is identified correctly 
    # This logic usually resides in standard code or backend, testing math here.
    
    cost = 500
    profit = 100
    
    is_leech = profit < cost
    roi = (profit - cost) / cost
    
    assert is_leech is True
    assert math.isclose(roi, -0.8)
