import pytest
from services.market_data.volume_monitor import VolumeMonitor

@pytest.fixture
def monitor():
    return VolumeMonitor()

def test_calculate_avg_weekly_volume(monitor):
    # 5 days of 1000 units = 1000 avg daily -> 5000 weekly
    daily_vols = [1000] * 5
    avg_weekly = monitor.calculate_avg_weekly_volume(daily_vols)
    assert avg_weekly == 5000

    # Empty list
    assert monitor.calculate_avg_weekly_volume([]) == 0

def test_detect_promo_spike(monitor):
    # Normal volume, low sentiment
    res = monitor.detect_promo_spike("PLTR", 100000, 80000, 0.5)
    assert res["is_promo_spike"] is False
    assert res["action"] == "NONE"

    # Spike: 3x volume, 0.9 sentiment
    res2 = monitor.detect_promo_spike("GME", 300000, 100000, 0.9)
    assert res2["is_promo_spike"] is True
    assert res2["action"] == "FLAG_FOR_144_AUDIT"
    assert res2["volume_ratio"] == 3.0

    # High volume but low sentiment (organic move?)
    res3 = monitor.detect_promo_spike("TSLA", 500000, 100000, 0.2)
    assert res3["is_promo_spike"] is False
