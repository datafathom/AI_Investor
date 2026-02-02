import logging
import random
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UplinkManagerService:
    """
    Phase 213.1: Orbital Uplink Manager.
    Manages connection failover between terrestrial ISP and Starlink Satellite constellation.
    """

    def __init__(self):
        self.active_interface = "FIBER_OPTIC"
        self.starlink_dish_status = "STANDBY"

    def check_connection(self) -> Dict[str, Any]:
        """
        Pings internet to check health. Auto-switches if down.
        """
        logger.info(f"Checking connectivity on {self.active_interface}...")
        
        # Mock connection failure on Fiber
        fiber_healthy = random.choice([True, True, True, False]) # Mostly active
        
        if not fiber_healthy and self.active_interface == "FIBER_OPTIC":
            logger.warning("Fiber connection LOST. Switching to ORBITAL UPLINK...")
            self._switch_to_satellite()
            
        return {
            "status": "ONLINE" if (fiber_healthy or self.active_interface == "STARLINK") else "OFFLINE",
            "interface": self.active_interface,
            "latency_ms": 15 if self.active_interface == "FIBER_OPTIC" else 45
        }

    def _switch_to_satellite(self):
        self.active_interface = "STARLINK"
        self.starlink_dish_status = "TRACKING_SATELLITE"
        logger.info("Starlink Uplink Established. Privacy Mode: HIGH.")
