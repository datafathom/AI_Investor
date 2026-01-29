import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from config.database import SessionLocal, Base
from sqlalchemy import Column, Integer, String, DateTime, JSON

logger = logging.getLogger(__name__)

# Define Model here for simplicity in this re-implementation phase
class ActivityLog(Base):
    __tablename__ = "unified_activity_log"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    agent_id = Column(String, index=True)
    action_type = Column(String, index=True)
    action_payload = Column(JSON)
    metadata_json = Column(JSON, nullable=True)

class UnifiedActivityService:
    """
    Immutable log for all system and agent decisions.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UnifiedActivityService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("UnifiedActivityService initialized")

    def log_activity(
        self, 
        agent_id: str, 
        action_type: str, 
        payload: Dict[str, Any], 
        meta: Optional[Dict[str, Any]] = None
    ):
        """
        Persists an action to the audit log.
        """
        logger.info(f"AUDIT LOG [{agent_id}]: {action_type}")
        
        if SessionLocal:
            try:
                db = SessionLocal()
                log_entry = ActivityLog(
                    agent_id=agent_id,
                    action_type=action_type,
                    action_payload=payload,
                    metadata_json=meta,
                    timestamp=datetime.utcnow()
                )
                db.add(log_entry)
                db.commit()
            except Exception as e:
                logger.error(f"Failed to write to DB audit log: {e}")
        else:
            logger.warning("DB Session not available. Activity logged to stdout only.")
