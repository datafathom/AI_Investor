import pytest
from unittest.mock import MagicMock
from services.neo4j.master_graph import MasterGraphService

def test_reflexivity_shock_logic():
    # Mock Neo4jService
    mock_neo4j = MagicMock()
    # Mock record data for execute_query
    mock_neo4j.execute_query.return_value = [
        {
            'affected': MagicMock(id='Node_B', labels=['Trust'], get=lambda x: 'Node_B'),
            'path': MagicMock(nodes=[
                MagicMock(get=lambda x: 'Asset_A'),
                MagicMock(get=lambda x: 'Node_B')
            ])
        }
    ]
    
    service = MasterGraphService()
    service.neo4j = mock_neo4j
    
    result = service.trigger_reflexivity_shock("Asset_A", -0.2)
    
    assert result['asset_id'] == "Asset_A"
    assert result['magnitude'] == -0.2
    assert len(result['affected_nodes']) >= 1
    assert result['contagion_velocity'] > 0
    assert len(result['propagation_paths']) >= 1

def test_spatial_projection():
    from services.neo4j.spatial_service import spatial_service
    # Test NYC coordinates
    lat, lon = 40.7128, -74.0060
    x, y, z = spatial_service.project_to_sphere(lat, lon)
    
    assert isinstance(x, float)
    assert isinstance(y, float)
    assert isinstance(z, float)
    # Check if NYC is roughly in the +X, +Y, -Z octant (depending on coordinate system choice)
    # But mainly check they aren't all zero
    assert abs(x) + abs(y) + abs(z) > 0
