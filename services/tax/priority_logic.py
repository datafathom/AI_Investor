
import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TaxPriorityLogic:
    """
    Prioritizes offsetting Short-Term gains (high tax) over Long-Term gains.
    """
    
    def determine_harvest_priority(self, st_gains: float, lt_gains: float) -> str:
        """
        Determines whether to focus on Short-Term or Long-Term realization.
        """
        if st_gains > 0:
            return "ST_REALIZATION"
        return "LT_REALIZATION"

    def prioritize_lots(self, lot_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sorts lots by tax efficiency (Short-Term losses first).
        """
        # Logic: Short-term losses offset Short-term gains first.
        # Then Long-term losses offset Long-term gains.
        
        def tax_score(lot):
            # Short-term is more valuable to harvest
            return 2 if lot.get("holding_period", "LONG") == "SHORT" else 1
            
        sorted_lots = sorted(lot_candidates, key=tax_score, reverse=True)
        return sorted_lots
