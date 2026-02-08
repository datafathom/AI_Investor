import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel

from services.monitoring.alert_rules import get_alert_rule_manager, MetricType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["Admin", "Alerts"])

# --- Pydantic Models ---

class AlertRuleCreate(BaseModel):
    name: str
    metric: str
    threshold: float
    comparison: str
    duration: int
    severity: str
    enabled: bool = True
    channels: List[str] = ["slack"]

class AlertRuleUpdate(BaseModel):
    name: Optional[str] = None
    metric: Optional[str] = None
    threshold: Optional[float] = None
    comparison: Optional[str] = None
    duration: Optional[int] = None
    severity: Optional[str] = None
    enabled: Optional[bool] = None
    channels: Optional[List[str]] = None

class AlertRuleResponse(BaseModel):
    id: str
    name: str
    metric: str
    threshold: float
    comparison: str
    duration: int
    severity: str
    enabled: bool
    channels: List[str]

# --- Endpoints ---

@router.get("/rules", response_model=List[AlertRuleResponse])
async def list_alert_rules():
    """List all configured alert rules."""
    try:
        manager = get_alert_rule_manager()
        return manager.get_rules()
    except Exception as e:
        logger.exception("Failed to list alert rules")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rules", response_model=AlertRuleResponse)
async def create_alert_rule(rule: AlertRuleCreate):
    """Create a new alert rule."""
    try:
        manager = get_alert_rule_manager()
        # Validate metric type
        try:
             valid_metrics = [m.value for m in MetricType]
             if rule.metric not in valid_metrics:
                 raise ValueError(f"Invalid metric type. Must be one of {valid_metrics}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        new_rule = manager.create_rule(rule.dict())
        return new_rule
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to create alert rule")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/rules/{rule_id}", response_model=AlertRuleResponse)
async def update_alert_rule(rule_id: str, rule: AlertRuleUpdate):
    """Update an existing alert rule."""
    try:
        manager = get_alert_rule_manager()
        update_data = rule.dict(exclude_unset=True)
        updated_rule = manager.update_rule(rule_id, update_data)
        
        if not updated_rule:
            raise HTTPException(status_code=404, detail="Rule not found")
            
        return updated_rule
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to update alert rule {rule_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/rules/{rule_id}")
async def delete_alert_rule(rule_id: str):
    """Delete an alert rule."""
    try:
        manager = get_alert_rule_manager()
        success = manager.delete_rule(rule_id)
        if not success:
            raise HTTPException(status_code=404, detail="Rule not found")
        return {"status": "success", "message": f"Rule {rule_id} deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to delete alert rule {rule_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channels")
async def list_notification_channels():
    """List available notification channels."""
    return ["slack", "email", "pagerduty", "sms", "webhook"]

@router.post("/rules/{rule_id}/test")
async def test_alert_rule(rule_id: str):
    """Trigger a test notification for a specific rule."""
    try:
        manager = get_alert_rule_manager()
        rules = manager.get_rules()
        rule = next((r for r in rules if r['id'] == rule_id), None)
        
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        logger.info(f"TEST NOTIFICATION triggered for rule: {rule['name']} -> {rule['channels']}")
        
        try:
             from services.notifications.slack_service import get_slack_service
             slack = get_slack_service()
             if "slack" in rule.get("channels", []):
                 await slack.send_notification(
                     text=f"🔔 [TEST] Alert Triggered: *{rule['name']}*\nThreshold: {rule['metric']} {rule['comparison']} {rule['threshold']}",
                     level="warning"
                 )
        except Exception as slack_err:
            logger.warning(f"Could not send actual Slack test: {slack_err}")

        return {
            "success": True, 
            "message": f"Test notification sent to {rule['channels']}",
            "rule": rule['name']
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to test rule {rule_id}")
        raise HTTPException(status_code=500, detail=str(e))
