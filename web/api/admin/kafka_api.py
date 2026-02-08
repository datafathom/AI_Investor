import logging
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from services.kafka.admin_client import get_kafka_admin

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/kafka", tags=["Admin", "Infrastructure"])

@router.get("/groups")
async def list_consumer_groups():
    """List all consumer groups."""
    try:
        admin = get_kafka_admin()
        groups = admin.list_groups()
        return {"groups": groups, "count": len(groups)}
    except Exception as e:
        logger.exception("Error listing Kafka groups")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/groups/{group_id}")
async def get_group_details(group_id: str):
    """Get health and lag for a group."""
    try:
        admin = get_kafka_admin()
        return admin.get_group_health(group_id)
    except Exception as e:
        logger.exception(f"Error fetching details for group {group_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_kafka_metrics():
    """Aggregate health metrics across all groups."""
    try:
        admin = get_kafka_admin()
        groups = admin.list_groups()
        metrics = []
        for gid in groups:
            metrics.append(admin.get_group_health(gid))
        return {
            "groups": metrics,
            "broker_status": "Connected",
            "total_lag": sum(m.get('total_lag', 0) for m in metrics if 'total_lag' in m)
        }
    except Exception as e:
        logger.exception("Error fetching Kafka metrics")
        raise HTTPException(status_code=500, detail=str(e))
