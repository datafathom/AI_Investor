import pytest
from services.retirement.match_calculator import MatchCalculator
from models.employer_match import EmployerMatchConfig
from uuid import uuid4

def test_match_dollar_for_dollar():
    calc = MatchCalculator()
    config = EmployerMatchConfig(
        user_id=uuid4(),
        employer_name="TestCorp",
        match_type="DOLLAR_FOR_DOLLAR",
        match_percentage=1.0,
        max_match_percentage=4.0
    )
    # Salary 100k, 6% contribution. Should match 4% (max_match_percentage)
    match = calc.calculate_match(100000, 6.0, config)
    assert match == 4000.0

def test_match_tiered():
    calc = MatchCalculator()
    config = EmployerMatchConfig(
        user_id=uuid4(),
        employer_name="TieredInc",
        match_type="TIERED",
        match_percentage=0, # not used in tiered
        tier_1_employee_pct=3.0,
        tier_1_employer_pct=1.0, # 100% of first 3%
        tier_2_employee_pct=2.0,
        tier_2_employer_pct=0.5 # 50% of next 2%
    )
    # Salary 100k, 5% contribution.
    # Tier 1: 3% * 100k * 1.0 = 3000
    # Tier 2: 2% * 100k * 0.5 = 1000
    # Total: 4000
    match = calc.calculate_match(100000, 5.0, config)
    assert match == 4000.0
