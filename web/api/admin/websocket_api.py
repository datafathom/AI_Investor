import logging
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from web.websocket.department_gateway import get_websocket_stats, list_active_connections, force_disconnect

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/websocket", tags=["Admin", "Infrastructure"])

@router.get("/stats")
async def get_ws_stats():
    """Get global WebSocket connection and message statistics."""
    try:
        return get_websocket_stats()
    except Exception as e:
        logger.exception("Error fetching WS stats")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/connections")
async def get_active_connections():
    """List all currently active WebSocket connections."""
    try:
        return list_active_connections()
    except Exception as e:
        logger.exception("Error listing WS connections")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/connections/{conn_id}/disconnect")
async def disconnect_client(conn_id: str):
    """Forcefully terminate a WebSocket connection."""
    try:
        await force_disconnect(conn_id)
        return {"status": "success", "message": f"Connection {conn_id} terminated"}
    except Exception as e:
        logger.exception(f"Error disconnecting client {conn_id}")
        raise HTTPException(status_code=500, detail=str(e))
