import pytest
from datetime import date, timedelta
from services.market.anomaly_detector_svc import AnomalyDetectorService
from services.social.bot_monitor_svc import BotMonitorService
from services.compliance.legend_verifier_svc import LegendVerifierService

@pytest.fixture
def anomaly_detector():
    return AnomalyDetectorService()

@pytest.fixture
def bot_monitor():
    return BotMonitorService()

@pytest.fixture
def legend_verifier():
    return LegendVerifierService()

def test_anomaly_pump_detection(anomaly_detector):
    # Price rises 20%, Volume drops (classic divergence)
    # Price: 100 -> 120 (+20%)
    # Vol: 1000 -> 500 (average drops)
    price_series = [100.0, 105.0, 110.0, 115.0, 120.0]
    # Early vol high, late vol low
    volume_series = [1000.0, 1000.0, 800.0, 500.0, 500.0] 
    
    result = anomaly_detector.detect_price_volume_divergence(price_series, volume_series, "PUMP")
    
    assert result['divergence_score'] > 80
    assert result['anomaly_type'] == "PRICE_VOL_DIVERGENCE_PUMP"

def test_bot_monitor_attack(bot_monitor):
    # 1000 mentions, 50 authors -> 0.05 ratio (Suspicious)
    # 90% duplicates
    result = bot_monitor.analyze_social_stream("SCAM", 1000, 50, 0.90)
    
    assert result['is_promo_attack'] is True
    assert result['bot_suspicion_score'] > 80

def test_legend_removal_dates(legend_verifier):
    # Acquired 7 months ago
    acquisition_date = date.today() - timedelta(days=210)
    
    # Reporting Company -> 6 month hold -> Should be Eligible
    result = legend_verifier.check_legend_removal_eligibility(acquisition_date, is_reporting_company=True)
    assert result['is_eligible_for_removal'] is True
    assert result['status'] == "LEGEND_REMOVABLE"
    
    # Non-Reporting -> 1 year hold -> Not Eligible
    result2 = legend_verifier.check_legend_removal_eligibility(acquisition_date, is_reporting_company=False)
    assert result2['is_eligible_for_removal'] is False
    assert result2['status'] == "RESTRICTED"
