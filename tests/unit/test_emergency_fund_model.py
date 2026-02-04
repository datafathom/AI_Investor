import pytest
from schemas.emergency_fund import EmergencyFund
from uuid import uuid4

def test_emergency_fund_model():
    data = {
        "user_id": uuid4(),
        "total_liquid_cash": 15000.0,
        "monthly_expenses": 3000.0,
        "coverage_tier": "LOW"
    }
    fund = EmergencyFund(**data)
    assert fund.total_liquid_cash == 15000.0
    assert fund.monthly_expenses == 3000.0
    assert fund.coverage_tier == "LOW"
