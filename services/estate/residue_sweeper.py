
import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ResidueSweeper:
    """
    Sweeps remaining estate assets (The Residue) into the Testamentary Trust.
    Occurs after all specific bequest (e.g., 'Avenue House to John') are satisfied.
    """
    
    def sweep_residue(self, total_estate_value: Decimal, specific_bequests_total: Decimal) -> Dict[str, Any]:
        """
        Calculates and 'transfers' the residue.
        """
        residue = total_estate_value - specific_bequests_total
        logger.info(f"Estate Residue Sweep: Estate=${total_estate_value}, Bequests=${specific_bequests_total}, Residue=${residue}")
        
        return {
            "total_estate": total_estate_value,
            "bequests_satisfied": specific_bequests_total,
            "residue_funded": residue,
            "recipient_trust": "TESTAMENTARY_RESIDUE_TRUST"
        }
