
import logging
import hashlib
import json
from datetime import datetime
from utils.database_manager import get_database_manager

logger = logging.getLogger(__name__)

class AuditIntegrityService:
    """
    Service to ensure the immutability and integrity of audit logs using hash chaining.
    """
    
    @staticmethod
    def calculate_hash(current_data: dict, previous_hash: str) -> str:
        """
        Computes SHA-256 hash of (current_record + previous_hash).
        """
        # Canonicalize input data to ensure consistent hashing
        data_str = json.dumps(current_data, sort_keys=True, default=str)
        payload = f"{previous_hash}|{data_str}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def verify_chain(self, limit: int = 100) -> bool:
        """
        Verifies the integrity of the last N records in the audit log.
        """
        db = get_database_manager()
        try:
            with db.pg_cursor() as cur:
                cur.execute("""
                    SELECT id, user_id, activity_type, details, created_at, previous_hash, verification_hash
                    FROM activity_logs
                    ORDER BY created_at DESC
                    LIMIT %s
                """, (limit,))
                records = cur.fetchall()
                
                # Check consistency from oldest retrieved to newest
                # Note: This is a simplified check. A full check would walk the entire chain.
                for i in range(len(records) - 1, 0, -1):
                    prev = records[i]
                    curr = records[i-1]
                    
                    # Columns: 0:id, 1:uid, 2:type, 3:details, 4:created_at, 5:prev_hash, 6:hash
                    
                    # Verify current record's 'previous_hash' matches prev record's 'verification_hash'
                    if curr[5] != prev[6]:
                        logger.error(f"Audit Chain Broken! Record {curr[0]} prev_hash mismatch.")
                        return False
                    
                    # Verify current record's hash matches calculated hash
                    data_to_hash = {
                        "id": str(curr[0]),
                        "user_id": curr[1],
                        "activity_type": curr[2],
                        "details": curr[3],
                        "created_at": curr[4]
                    }
                    calculated = self.calculate_hash(data_to_hash, curr[5])
                    if calculated != curr[6]:
                        logger.error(f"Audit Integrity Failure! Record {curr[0]} hash mismatch.")
                        return False
                        
                return True
        except Exception as e:
            logger.error(f"Audit Verification Failed: {e}")
            return False

def get_audit_integrity_service() -> AuditIntegrityService:
    return AuditIntegrityService()
