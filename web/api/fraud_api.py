from fastapi import APIRouter
import uuid

router = APIRouter(prefix="/api/v1/fraud", tags=["Fraud Detection"])

@router.get('/alerts')
async def get_fraud_alerts():
    """Get suspicious activty alerts."""
    return {"success": True, "data": [
        {"id": "fr_01", "type": "LOGIN_ANOMALY", "severity": "HIGH", "details": "Login from new device in Russia", "timestamp": "2025-02-09T01:00:00"},
        {"id": "fr_02", "type": "ORDER_VELOCITY", "severity": "MEDIUM", "details": "50 orders in 1 second", "timestamp": "2025-02-09T02:30:00"}
    ]}

@router.get('/settings')
async def get_detection_settings():
    """Get fraud detection sensitivity."""
    return {"success": True, "data": {
        "ip_whitelist_enabled": True,
        "max_order_velocity": 20,
        "withdrawal_hold_hours": 24,
        "anomaly_threshold": 0.85
    }}
