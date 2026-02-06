import pytest
from services.attribution_service import get_attribution_service

def test_attribution_math():
    service = get_attribution_service()
    
    # Scene: 
    # Total PnL: $1000
    # Gas Cost: $100
    # Net Profit: $900
    # Intel Depts: [1] (Strategist)
    # Exec Depts: [5] (Trader)
    
    mission_result = {
        "total_pnl": 1000.0,
        "gas_cost": 100.0,
        "intelligence_depts": [1],
        "execution_depts": [5]
    }
    
    attribution = service.calculate_attribution(mission_result)
    
    # Expected:
    # Net = 900
    # Intel (40%) = 360 -> Dept 1
    # Exec (60%) = 540 -> Dept 5
    
    assert attribution["1"] == 360.0
    assert attribution["5"] == 540.0

def test_multi_agent_attribution():
    service = get_attribution_service()
    
    # Scene:
    # Net Profit: $1000 (Gas=0 for simplicity)
    # Intel: [1, 2] (Two strategists)
    # Exec: [5] (One trader)
    
    mission_result = {
        "total_pnl": 1000.0,
        "gas_cost": 0.0,
        "intelligence_depts": [1, 2],
        "execution_depts": [5]
    }
    
    attribution = service.calculate_attribution(mission_result)
    
    # Intel Pool (400) split 2 ways -> 200 each
    # Exec Pool (600) split 1 way -> 600
    
    assert attribution["1"] == 200.0
    assert attribution["2"] == 200.0
    assert attribution["5"] == 600.0

def test_loss_attribution():
    service = get_attribution_service()
    
    # Scene: Loss
    # Net: -100
    
    mission_result = {
        "total_pnl": -90.0,
        "gas_cost": 10.0,
        "intelligence_depts": [1],
        "execution_depts": [5]
    }
    
    attribution = service.calculate_attribution(mission_result)
    
    # Net = -100
    # Intel = -40
    # Exec = -60
    
    assert attribution["1"] == -40.0
    assert attribution["5"] == -60.0
