"""
Forensics Logger Service.
Persists agent debate metadata and dissent records for post-trade analysis.
"""
import logging
import json
from typing import Dict, Any, List
from datetime import timezone, datetime
from utils.database_manager import get_database_manager

logger = logging.getLogger(__name__)

class ForensicsLogger:
    """
    Service to record detailed multi-agent decision trails.
    """
    def __init__(self):
        self.db = get_database_manager()

    def log_debate(
        self, 
        proposal_id: str, 
        symbol: str, 
        decision: str, 
        votes: List[Dict[str, Any]], 
        metadata: Dict[str, Any] = None
    ):
        """
        Record a full debate record to Postgres.
        """
        try:
            with self.db.pg_cursor() as cur:
                cur.execute("""
                    INSERT INTO debate_logs (
                        proposal_id, symbol, decision, votes_json, metadata, timestamp
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    proposal_id, 
                    symbol, 
                    decision, 
                    json.dumps(votes), 
                    json.dumps(metadata or {}), 
                    datetime.now(timezone.utc)
                ))
                logger.info(f"Debate Logged: {proposal_id} ({decision})")
        except Exception as e:
            logger.error(f"Failed to log debate forensics: {e}")

# Global Instance
forensics_logger = ForensicsLogger()
