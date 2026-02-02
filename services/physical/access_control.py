import logging
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AccessControlService:
    """
    Phase 202.3: Biometric Access Control Logger.
    Tracks entry/exit logs from secure zones (Server Room, Safe Room).
    """

    def __init__(self):
        self.access_logs = []
        self.secure_zones = ["Server Room", "Vault", "Command Center"]

    def log_access_attempt(self, user_id: str, zone: str, method: str, success: bool) -> Dict[str, Any]:
        """
        Logs an access event.
        """
        if zone not in self.secure_zones:
            logger.warning(f"Access attempt on unknown zone: {zone}")
            return {"status": "ERROR", "message": "UNKNOWN_ZONE"}
            
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "zone": zone,
            "method": method, # Retina, Fingerprint, NFC
            "success": success
        }
        self.access_logs.append(entry)
        
        if not success:
            logger.warning(f"FAILED ACCESS: {user_id} -> {zone} via {method}")
        else:
            logger.info(f"ACCESS GRANTED: {user_id} -> {zone}")
            
        return {"status": "LOGGED", "entry": entry}

    def get_recent_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.access_logs[-limit:]
