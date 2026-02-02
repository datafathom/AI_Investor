import logging
import random
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SolarMonitorService:
    """
    Phase 204.1: Solar Array Production Monitor.
    Interfaces with SolarEdge/Enphase inverters to track kW production.
    """

    def __init__(self):
        self.capacity_kw = 25.0 # 25kW Array
        self.current_output = 0.0

    def fetch_production(self) -> Dict[str, Any]:
        """
        Simulates fetching live production metrics.
        """
        # Mocking values based on "Time of Day" (Random for now)
        efficiency = random.uniform(0.1, 0.95)
        output = self.capacity_kw * efficiency
        self.current_output = round(output, 2)
        
        logger.info(f"Solar Array Output: {self.current_output} kW ({int(efficiency*100)}%% Eff.)")
        
        return {
            "status": "ONLINE",
            "capacity_kw": self.capacity_kw,
            "current_output_kw": self.current_output,
            "daily_total_kwh": 120.5, # Mock
            "net_metering": "EXPORTING" if self.current_output > 10 else "IMPORTING"
        }
