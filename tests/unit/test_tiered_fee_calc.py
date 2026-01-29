import pytest
from services.billing.tiered_fee_calc import TieredFeeCalculator
from models.fee_billing import FeeSchedule
from uuid import uuid4
from datetime import date

def test_tiered_billing_high_worth():
    calc = TieredFeeCalculator()
    schedule = FeeSchedule(
        client_id=uuid4(),
        advisor_id=uuid4(),
        fee_type="AUM",
        tier_1_max=1000000.0, tier_1_rate=0.0100, # 1% on first 1M
        tier_2_max=5000000.0, tier_2_rate=0.0075, # 0.75% on next 4M
        tier_3_rate=0.005,                        # 0.5% on remainder
        effective_date=date.today()
    )
    # $10M AUM
    # 1M @ 1.0% = 10,000
    # 4M @ 0.75% = 30,000
    # 5M @ 0.50% = 25,000
    # Total = 65,000
    annual_fee = calc.calculate_annual_fee(10000000, schedule)
    assert annual_fee == 65000.0

def test_tiered_billing_simple():
    calc = TieredFeeCalculator()
    schedule = FeeSchedule(
        client_id=uuid4(), advisor_id=uuid4(), fee_type="AUM",
        tier_1_max=1000000, tier_1_rate=0.01,
        effective_date=date.today()
    )
    # 500k @ 1% = 5000
    assert calc.calculate_annual_fee(500000, schedule) == 5000.0
