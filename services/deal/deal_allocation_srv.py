import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DealAllocationService:
    """
    Allocates scarce deal capacity among UHNW and SFO clients.
    Prioritizes based on Client Tier (SFO > UHNW > HNW) and pro-rata AUM.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DealAllocationService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("DealAllocationService initialized")

    def allocate_oversubscribed_deal(self, total_capacity: Decimal, commitments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Policy: 
        1. Fully fill SFOs first (if possible).
        2. Pro-rata remaining to UHNW.
        3. Exclude/Waitlist HNW if capacity hit.
        """
        total_demand = sum(c['amount'] for c in commitments)
        
        if total_demand <= total_capacity:
            logger.info(f"ALLOC_LOG: Full fill for all {len(commitments)} commitments (${total_demand:,.2f}).")
            return [{**c, "allocated": c['amount'], "status": "CONFIRMED"} for c in commitments]
            
        # Oversubscribed logic
        allocations = []
        remaining = total_capacity
        
        # Sort by tier priority
        tier_weights = {"SFO": 1, "UHNW": 2, "HNW": 3}
        sorted_commitments = sorted(commitments, key=lambda x: tier_weights.get(x.get('tier', 'HNW'), 99))
        
        for comm in sorted_commitments:
            if remaining <= 0:
                allocations.append({**comm, "allocated": Decimal('0'), "status": "WAITLISTED"})
                continue
                
            fill = min(comm['amount'], remaining)
            allocations.append({**comm, "allocated": round(fill, 2), "status": "CONFIRMED" if fill > 0 else "WAITLISTED"})
            remaining -= fill
            
        logger.info(f"ALLOC_LOG: Allocated ${total_capacity:,.2f} among {len(commitments)} requests.")
        return allocations
