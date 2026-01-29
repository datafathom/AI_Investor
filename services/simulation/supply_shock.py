"""
Supply Shock Simulator.
Estimates revenue impact of supplier halts.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SupplyShockSim:
    """Stress-tests supply chain dependency."""
    
    def simulate_halt(self, critical_supplier: str, duration_days: int) -> Dict[str, float]:
        # MOCK Hit to major customers
        logger.warning(f"SHOCK_SIM: Simulating {duration_days} day halt for {critical_supplier}")
        return {
            "AAPL_REVENUE_HIT": -0.15,
            "NVDA_REVENUE_HIT": -0.08,
            "TOTAL_SECTOR_LOSS": -45000000.0
        }
