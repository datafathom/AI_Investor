import pytest
from services.venture.cap_table_service import get_cap_table_service

def test_waterfall_logic():
    svc = get_cap_table_service()
    
    # Setup: 2 Investors (Pref) and 1 Founder (Common)
    cap_table = [
        {"name": "VC Fund A", "type": "Preferred", "investment_amount": 100_000, "shares": 1000},
        {"name": "Founder", "type": "Common", "investment_amount": 0, "shares": 4000} # 20% / 80% split
    ]
    
    # Scenario 1: Low Exit (Down Side Protection)
    # Exit at $80k. VC should take it all (Pref). Founder gets 0.
    payouts_low = svc.run_waterfall(80_000, cap_table)
    assert payouts_low["VC Fund A"] == 80_000
    # Founder might get 0 or close to 0 depending on implementation details, 
    # but strictly Pref logic says VC gets first dibs.
    
    # Scenario 2: High Exit ($10M)
    # 1. VC gets $100k back. (Remaining: $9.9M)
    # 2. Pro-Rata Split of %9.9M. 
    # Total Shares = 5000. VC owns 20%. Founder 80%.
    payouts_high = svc.run_waterfall(10_100_000, cap_table)
    
    # VC gets 100k (Pref) + 20% of 10M (2M) = 2.1M
    # Founder gets 80% of 10M = 8M
    assert payouts_high["VC Fund A"] == 2_100_000
    assert payouts_high["Founder"] == 8_000_000
