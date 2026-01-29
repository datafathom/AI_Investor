"""
SL Removal Blocker Service.
Prevents the removal of stop-loss levels from existing positions.
Only allows SL to be TIGHTENED (moved in favor of the trade).
"""
import logging
from decimal import Decimal
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class SLRemovalBlocker:
    """
    Compliance logic for stop-loss management.
    """

    @staticmethod
    def validate_modification(
        current_sl: Decimal, 
        new_sl: Decimal, 
        side: str, 
        entry_price: Decimal
    ) -> Tuple[bool, str]:
        """
        Validate changes to a stop-loss level.
        Only allows tightening or maintaining SL.
        """
        if new_sl is None or new_sl == 0:
             return False, "FORBIDDEN: Attempted to remove SL protection."

        if side.upper() == "LONG":
            # New SL must be > Current SL (cannot move SL further away)
            if new_sl < current_sl:
                return False, f"ILLEGAL_MOVE: Moved SL from {current_sl} to {new_sl} (Increasing risk)."
        else:
            # New SL must be < Current SL
            if new_sl > current_sl:
                return False, f"ILLEGAL_MOVE: Moved SL from {current_sl} to {new_sl} (Increasing risk)."

        return True, "VALIDATED"
