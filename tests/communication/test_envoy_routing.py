import pytest
from services.communication.envoy_service import get_envoy_service

def test_envoy_classification():
    envoy = get_envoy_service()
    
    # 1. Security Alert
    res1 = envoy.ingest_signal("system@monitor.com", "Urgent: Login detected in Russia")
    assert res1['classification'] == "SECURITY_ALERT"
    assert res1['routed_to'] == "Dept 8 (Sentry)"
    
    # 2. Investor Update
    res2 = envoy.ingest_signal("ir@nvidia.com", "NVIDIA Q1 Results Update")
    assert res2['classification'] == "INVESTOR_UPDATE"
    
    # 3. Spam
    res3 = envoy.ingest_signal("spammer@ads.com", "Unsubscribe from free toast newsletter")
    assert res3['classification'] == "SPAM"
