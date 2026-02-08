import logging
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from services.infrastructure.event_bus import EventBusService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/event-bus", tags=["Admin", "Infrastructure"])

@router.get("/topics")
async def get_all_topics():
    """List all registered topics with metadata."""
    try:
        eb = EventBusService()
        return eb.get_all_topics_metadata()
    except Exception as e:
        logger.exception("Error fetching topics")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topics/{topic}/messages")
async def get_topic_messages(topic: str, limit: int = Query(50, le=100), offset: int = 0):
    """Recent messages for a topic (paginated)."""
    try:
        eb = EventBusService()
        messages = eb.get_recent_messages(topic, limit, offset)
        return {
            "topic": topic,
            "messages": messages,
            "count": len(messages),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.exception(f"Error fetching messages for topic {topic}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_event_bus_stats():
    """Throughput metrics per topic."""
    try:
        eb = EventBusService()
        return eb.get_stats()
    except Exception as e:
        logger.exception("Error fetching event bus stats")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topics/{topic}/replay")
async def replay_message(topic: str, message: Dict[str, Any]):
    """Replay a specific message."""
    try:
        eb = EventBusService()
        eb.publish(topic, message)
        return {"status": "success", "message": f"Message replayed to topic {topic}"}
    except Exception as e:
        logger.exception(f"Error replaying message to topic {topic}")
        raise HTTPException(status_code=500, detail=str(e))
