import pytest
from services.alerts.emergency_fund_alerts import EmergencyFundAlertService

def test_alert_evaluation_critical():
    service = EmergencyFundAlertService()
    result = service.evaluate_coverage(2.0)
    assert result["tier"] == "CRITICAL"
    assert result["action_required"] == True

def test_alert_evaluation_healthy():
    service = EmergencyFundAlertService()
    result = service.evaluate_coverage(18.0)
    assert result["tier"] == "STRONG"
    assert result["action_required"] == False
