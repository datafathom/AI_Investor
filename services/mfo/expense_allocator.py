import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MFOExpenseAllocator:
    """
    Allocates Multi-Family Office (MFO) operating costs among participating families.
    Supports PRO_RATA_AUM and FIXED_SPLIT methods.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MFOExpenseAllocator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("MFOExpenseAllocator initialized")

    def split_monthly_overhead(self, total_overhead: Decimal, family_aums: Dict[str, Decimal], method: str = 'PRO_RATA') -> List[Dict[str, Any]]:
        """
        Splits fixed costs (Rent, Tech, Staff) across families.
        """
        allocations = []
        
        if method == 'FIXED':
            count = len(family_aums)
            per_family = total_overhead / Decimal(str(count))
            for f_id in family_aums.keys():
                allocations.append({"family_id": f_id, "amount": round(per_family, 2), "method": "FIXED"})
        else:
            total_aum = sum(family_aums.values())
            for f_id, aum in family_aums.items():
                share = (aum / total_aum) * total_overhead
                allocations.append({"family_id": f_id, "amount": round(share, 2), "method": "PRO_RATA_AUM"})
                
        logger.info(f"MFO_LOG: Allocated ${total_overhead:,.2f} via {method} to {len(allocations)} families.")
        return allocations
