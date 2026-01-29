"""
Term Structure Monitor.
Monitors VIX Futures Contango/Backwardation.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TermStructureMonitor:
    """Monitors futures curve shape."""
    
    def check_curve(self, m1: float, m2: float) -> str:
        """m1/m2 are first/second month futures."""
        if m1 > m2:
            return "BACKWARDATION (Panic)"
        return "CONTANGO (Normal)"
