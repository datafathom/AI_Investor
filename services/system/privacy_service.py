
import logging
import json
from datetime import datetime
from typing import Dict, Any, List
from utils.database_manager import get_database_manager
from services.system.logging_service import get_logging_service

logger = logging.getLogger(__name__)

class PrivacyService:
    """
    Service for handling GDPR/CCPA compliance requests: Data Export and Account Deletion.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrivacyService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.db = get_database_manager()

    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Aggregates all data related to a user for GDPR export.
        """
        logger.info(f"Privacy: Processing data export request for user {user_id}")
        
        export_data = {
            "metadata": {
                "exported_at": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "platform": "AI Investor"
            },
            "user_profile": {},
            "activity_logs": [],
            "portfolio_data": [],
            "financial_data": []
        }

        try:
            with self.db.pg_cursor() as cur:
                # 1. User Profile
                cur.execute("SELECT email, username, created_at, role FROM users WHERE id = %s", (user_id,))
                user = cur.fetchone()
                if user:
                    export_data["user_profile"] = {
                        "email": user[0],
                        "username": user[1],
                        "created_at": user[2].isoformat() if user[2] else None,
                        "role": user[3]
                    }

                # 2. Activity Logs (from UnifiedActivityService if applicable)
                cur.execute("SELECT activity_type, details, created_at FROM activity_logs WHERE user_id = %s LIMIT 100", (user_id,))
                export_data["activity_logs"] = [
                    {"type": r[0], "details": r[1], "at": r[2].isoformat()} for r in cur.fetchall()
                ]

                # 3. Portfolio
                cur.execute("SELECT symbol, amount, price FROM portfolio WHERE user_id = %s", (user_id,))
                export_data["portfolio_data"] = [
                    {"symbol": r[0], "amount": float(r[1]), "avg_price": float(r[2])} for r in cur.fetchall()
                ]

            return export_data
        except Exception as e:
            logger.error(f"Failed to export user data: {e}")
            raise

    def delete_user_account(self, user_id: str) -> bool:
        """
        Performs a full wipe of user data ('Right to be Forgotten').
        """
        logger.warning(f"Privacy: PERMANENT DELETION request for user {user_id}")
        
        try:
            with self.db.pg_cursor() as cur:
                # Delete from related tables (in order of foreign key dependency if not CASCADE)
                cur.execute("DELETE FROM activity_logs WHERE user_id = %s", (user_id,))
                cur.execute("DELETE FROM portfolio WHERE user_id = %s", (user_id,))
                cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            
            # Neo4j Cleanup
            self.db.run_neo4j_query("MATCH (u:User {id: $uid}) DETACH DELETE u", {"uid": user_id})
            
            logger.info(f"Privacy: Account {user_id} successfully purged.")
            return True
        except Exception as e:
            logger.error(f"Failed to delete user account: {e}")
            return False

def get_privacy_service() -> PrivacyService:
    return PrivacyService()
