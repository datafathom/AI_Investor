import pytest
from datetime import datetime
from decimal import Decimal
from services.trusts.crt_service import CRTService, CRTConfig

def test_create_crt_crat():
    service = CRTService()
    config = CRTConfig(
        trust_id="CRT_001",
        trust_type="CRAT",
        initial_value=Decimal("1000000"),
        payout_rate=Decimal("0.05"),
        charity_name="Red Cross"
    )
    service.create_crt(config)
    
    # Distribution should be fixed
    dist = service.calculate_distribution("CRT_001", Decimal("1200000"))
    assert dist == Decimal("50000")

def test_create_crt_crut():
    service = CRTService()
    config = CRTConfig(
        trust_id="CRT_002",
        trust_type="CRUT",
        initial_value=Decimal("1000000"),
        payout_rate=Decimal("0.06"),
        charity_name="UNICEF"
    )
    service.create_crt(config)
    
    # Distribution should vary with current value
    dist = service.calculate_distribution("CRT_002", Decimal("1500000"))
    assert dist == Decimal("90000")

def test_invalid_payout_rate():
    with pytest.raises(ValueError):
        CRTConfig(
            trust_id="CRT_FAIL",
            trust_type="CRAT",
            initial_value=Decimal("1000000"),
            payout_rate=Decimal("0.04"), # Too low
            charity_name="Charity"
        )

def test_remainder_rule_failure():
    service = CRTService()
    config = CRTConfig(
        trust_id="CRT_FAIL_ACTUARIAL",
        trust_type="CRAT",
        initial_value=Decimal("1000000"),
        payout_rate=Decimal("0.10"),
        term_years=20, # 10% * 20 = 2.0 (fails our placeholder check > 0.8)
        charity_name="Charity"
    )
    with pytest.raises(ValueError, match="fails the 10% remainder rule"):
        service.create_crt(config)
