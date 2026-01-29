"""
Fed Balance Sheet Ingest.
Parses weekly H.4.1 data.
"""
import logging

logger = logging.getLogger(__name__)

class FedBalanceIngest:
    """Ingests Fed total assets."""
    def get_latest_assets(self) -> float:
        # MOCK
        return 7.5e12 # $7.5 Trillion
