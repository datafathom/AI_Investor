
import logging
from datetime import datetime
from utils.database_manager import get_database_manager

logger = logging.getLogger(__name__)

class LegalComplianceService:
    """
    Manages versioned legal agreements and user consents.
    """
    _instance = None

    # Hardcoded current versions for simplicity in this phase
    REQUIRED_TOS_VERSION = "1.0"
    REQUIRED_RISK_DISCLAIMER_VERSION = "2.1"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LegalComplianceService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.db = get_database_manager()

    def get_user_consent_status(self, user_id: str) -> dict:
        """
        Returns the versions of agreements the user has accepted.
        """
        try:
            with self.db.pg_cursor() as cur:
                cur.execute("""
                    SELECT agreement_type, version, accepted_at 
                    FROM user_consents 
                    WHERE user_id = %s
                """, (user_id,))
                
                consents = {}
                for row in cur.fetchall():
                    consents[row[0]] = {"version": row[1], "accepted_at": row[2]}
                    
                return {
                    "tos": consents.get("TOS", {}),
                    "risk_disclaimer": consents.get("RISK_DISCLAIMER", {}),
                    "is_tos_current": consents.get("TOS", {}).get("version") == self.REQUIRED_TOS_VERSION,
                    "is_risk_current": consents.get("RISK_DISCLAIMER", {}).get("version") == self.REQUIRED_RISK_DISCLAIMER_VERSION
                }
        except Exception as e:
            logger.error(f"Failed to get consent status: {e}")
            return {}

    def accept_agreement(self, user_id: str, agreement_type: str, version: str) -> bool:
        """
        Records a user's acceptance of a specific agreement version.
        """
        try:
            with self.db.pg_cursor() as cur:
                # Upsert consent
                cur.execute("""
                    INSERT INTO user_consents (user_id, agreement_type, version, accepted_at)
                    VALUES (%s, %s, %s, NOW())
                    ON CONFLICT (user_id, agreement_type) 
                    DO UPDATE SET version = EXCLUDED.version, accepted_at = NOW()
                """, (user_id, agreement_type, version))
                
                logger.info(f"User {user_id} accepted {agreement_type} v{version}")
                return True
        except Exception as e:
            logger.error(f"Failed to record consent: {e}")
            return False

def get_legal_compliance_service() -> LegalComplianceService:
    return LegalComplianceService()
