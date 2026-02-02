import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GeneratorTrackerService:
    """
    Phase 204.3: Backup Generator Fuel & Maintenance.
    Tracks diesel/propane levels and maintenance schedules.
    """

    def __init__(self):
        self.fuel_level = 78.5 # Percent
        self.runtime_hours = 142
        self.last_maintenance = "2025-11-15"

    def check_readiness(self) -> Dict[str, Any]:
        """
        Checks if the generator is ready for emergency start.
        """
        if self.fuel_level < 25:
             logger.warning(f"Generator Fuel Low: {self.fuel_level}%%")
             return {"status": "WARNING", "message": "LOW_FUEL"}
             
        return {"status": "READY", "fuel_level": self.fuel_level}

    def log_run(self, hours: float):
        self.runtime_hours += hours
        self.fuel_level -= (hours * 1.5) # Mock consumption
        logger.info(f"Generator ran for {hours} hrs. Fuel now: {self.fuel_level}%%")
