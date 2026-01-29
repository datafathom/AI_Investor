import pytest
from services.retirement.vesting_engine import VestingEngine
from datetime import date

def test_vesting_cliff():
    engine = VestingEngine()
    hire = date(2020, 1, 1)
    
    config = {"vesting_type": "CLIFF", "vesting_cliff_months": 36}
    
    # 2 years service -> 0%
    assert engine.calculate_vested_pct(hire, date(2022, 1, 1), config) == 0.0
    # 3 years service -> 100%
    assert engine.calculate_vested_pct(hire, date(2023, 1, 1), config) == 1.0

def test_vesting_graded():
    engine = VestingEngine()
    hire = date(2020, 1, 1)
    config = {
        "vesting_type": "GRADED",
        "vesting_schedule": {"12": 0.25, "24": 0.50, "36": 0.75, "48": 1.0}
    }
    
    # 18 months -> 25%
    assert engine.calculate_vested_pct(hire, date(2021, 7, 1), config) == 0.25
    # 25 months -> 50%
    assert engine.calculate_vested_pct(hire, date(2022, 2, 1), config) == 0.50
