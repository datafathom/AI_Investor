import pytest
from services.retirement.db_dc_bridge import DBDCBridge

def test_bridge_normalization():
    bridge = DBDCBridge()
    pension = {"monthly_benefit": 2000.0}
    dc_balance = 600000.0 # 600k
    
    # dc_monthly = (600k * 0.04) / 12 = 2000
    # total = 2000 + 2000 = 4000
    res = bridge.normalize_to_income_stream(pension, dc_balance, 30)
    assert res["total_estimated_monthly"] == 4000.0
    assert res["pension_portion_pct"] == 50.0
