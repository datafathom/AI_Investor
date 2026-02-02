import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BatteryManagerService:
    """
    Phase 204.2: Battery Storage & Grid Arbitrage.
    Manages charge/discharge cycles for Tesla Powerwall bank.
    """

    def __init__(self):
        self.capacity_kwh = 40.5 # 3x Powerwalls
        self.charge_level = 95.0
        self.mode = "SELF_POWERED" # BACKUP, TOU (Time of Use), SELF_POWERED

    def optimize_cycle(self, grid_price: float) -> str:
        """
        Decides whether to Charge, Discharge, or Idel based on grid price.
        """
        if self.charge_level < 20:
             logger.warning("Battery Low! Forcing Charge.")
             return "FORCE_CHARGE"
             
        if grid_price > 0.40: # Peak Rate
            logger.info("Peak Rate Detected. Discharging Battery.")
            return "DISCHARGE"
            
        if grid_price < 0.10: # Off-Peak
            logger.info("Cheap Energy. Charging Battery.")
            return "CHARGE"
            
        return "IDLE"

    def get_status(self) -> Dict[str, Any]:
        return {
            "charge_level": f"{self.charge_level}%%",
            "capacity_kwh": self.capacity_kwh,
            "runtime_remaining": "14h 30m" if self.charge_level > 50 else "2h 15m",
            "grid_status": "CONNECTED"
        }
