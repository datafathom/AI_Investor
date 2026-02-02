import pytest
import datetime
from decimal import Decimal
from services.compliance.insider_trading_svc import InsiderTradingService

@pytest.fixture
def svc():
    return InsiderTradingService()

def test_calculate_sellable_volume(svc):
    # Case: 1% of shares is greater than avg volume
    # 10M shares outstanding -> 100k limit
    # 50k avg weekly volume
    res = svc.calculate_sellable_volume("TICKER1", 10000000, 50000)
    assert res["max_sellable_volume"] == 100000
    assert res["one_percent_limit"] == 100000

    # Case: Avg weekly volume is greater than 1% of shares
    # 10M shares outstanding -> 100k limit
    # 150k avg weekly volume -> 150k limit
    res2 = svc.calculate_sellable_volume("TICKER2", 10000000, 150000)
    assert res2["max_sellable_volume"] == 150000

def test_check_lockup_status(svc):
    # Case: Locked (expiry in future)
    future_date = datetime.date.today() + datetime.timedelta(days=30)
    res = svc.check_lockup_status("TICKER3", future_date)
    assert res["is_locked"] is True
    assert res["can_sell"] is False
    assert res["days_remaining"] > 0

    # Case: Extinguished (expiry in past)
    past_date = datetime.date.today() - datetime.timedelta(days=1)
    res2 = svc.check_lockup_status("TICKER4", past_date)
    assert res2["is_locked"] is False
    assert res2["can_sell"] is True
    assert res2["days_remaining"] == 0

def test_validate_sale_compliance(svc):
    outstanding = 10000000 # 100k limit
    avg_vol = 50000
    locked_date = datetime.date.today() + datetime.timedelta(days=30)
    open_date = datetime.date.today() - datetime.timedelta(days=1)

    # Compliant sale
    res = svc.validate_sale_compliance("ABC", 50000, outstanding, avg_vol, open_date)
    assert res["compliant"] is True

    # Fail: Locked
    res2 = svc.validate_sale_compliance("DEF", 50000, outstanding, avg_vol, locked_date)
    assert res2["compliant"] is False
    assert "Lock-up" in res2["reason"]

    # Fail: Volume exceeds limit (150k > 100k)
    res3 = svc.validate_sale_compliance("GHI", 150000, outstanding, avg_vol, open_date)
    assert res3["compliant"] is False
    assert "volume" in res3["reason"].lower()
