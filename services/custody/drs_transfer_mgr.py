import logging
from uuid import UUID
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DRSTransferManager:
    """
    Automates the transfer of securities from 'Street Name' to Direct Registration (DRS).
    Mitigates 'Great Taking' risks by placing shares directly in the client's name.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DRSTransferManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("DRSTransferManager initialized")

    def initiate_drs_transfer(self, asset_id: UUID, broker_id: UUID, share_quantity: int) -> Dict[str, Any]:
        """
        Policy: MOVE assets from Street Name -> Transfer Agent.
        """
        logger.warning(f"DRS_LOG: INITIATING DRS TRANSFER: {share_quantity} shares of {asset_id} from Broker {broker_id}.")
        
        return {
            "transfer_ticket_id": "DRS-8771A",
            "source": "BROKER_STREET_NAME",
            "destination": "TRANSFER_AGENT_DRS",
            "shares": share_quantity,
            "estimated_settlement_days": 5,
            "status": "INITIATED"
        }

    def verify_legal_title(self, registration_status: str) -> bool:
        """
        Returns True if the client holds direct legal title (DRS/Physical).
        """
        is_direct = registration_status.upper() in {'DRS', 'PHYSICAL', 'ISSUER_DIRECT'}
        return is_direct
