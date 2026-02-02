import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResourceLogService:
    """
    Phase 204.4: Critical Resource Inventory (Water/Food).
    IoT interface for water tank levels and freeze-dried food inventory.
    """

    def __init__(self):
        self.water_tank_level = 4500 # Gallons
        self.food_supply_days = 365 # Person-Days

    def check_water_levels(self) -> Dict[str, Any]:
        """
        Reads from ultrasonic tank sensor.
        """
        percent = (self.water_tank_level / 5000) * 100
        logger.info(f"Water Tank Level: {self.water_tank_level} gal ({percent}%%)")
        return {
            "level_gallons": self.water_tank_level,
            "capacity": 5000,
            "days_at_current_usage": self.water_tank_level / 50 # 50 gal/day usage
        }

    def update_food_inventory(self, consumed_calories: int):
        # 2000 cal/day per person
        day_equivalent = consumed_calories / 2000
        self.food_supply_days -= day_equivalent
        logger.info(f"Food Supply Updated: {self.food_supply_days} days remaining.")
