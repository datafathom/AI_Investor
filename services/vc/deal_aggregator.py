import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VCDealAggregator:
    """
    Phase 165.1: Accredited Investor Deal Flow List Service.
    Aggregates active venture deals from syndicates and direct networks.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VCDealAggregator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("VCDealAggregator initialized")

    def get_active_deals(self, min_ticket_k: int = 50) -> List[Dict[str, Any]]:
        """
        Mock active deals.
        """
        deals = [
            {"id": "VC-001", "name": "NeuralLink_Proxy", "sector": "BioTech", "min_ticket_k": 100, "stage": "Series C"},
            {"id": "VC-002", "name": "Mars_Colony_Infra", "sector": "Space", "min_ticket_k": 250, "stage": "Seed"},
            {"id": "VC-003", "name": "Fusion_Core_V2", "sector": "Energy", "min_ticket_k": 50, "stage": "Series A"}
        ]
        
        filtered = [d for d in deals if d["min_ticket_k"] >= min_ticket_k]
        logger.info(f"VC_LOG: Found {len(filtered)} active deals for accredited investors.")
        return filtered
