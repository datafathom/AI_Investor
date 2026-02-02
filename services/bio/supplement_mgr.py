import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SupplementManager:
    """
    Phase 203.4: Supplement Stack & Inventory Manager.
    Track automated re-ordering and compliance with the 'Longevity Stack'.
    """

    def __init__(self):
        self.inventory = {
            "NMN": {"dose": "1g", "on_hand": 30, "threshold": 10},
            "Resveratrol": {"dose": "500mg", "on_hand": 25, "threshold": 10},
            "Magnesium": {"dose": "400mg", "on_hand": 5, "threshold": 15}, # Low stock
            "Omega-3": {"dose": "2g", "on_hand": 60, "threshold": 20}
        }

    def check_inventory(self) -> List[str]:
        """
        Checks for low stock items.
        """
        to_order = []
        for item, details in self.inventory.items():
            if details["on_hand"] <= details["threshold"]:
                logger.warning(f"Low Stock Alert: {item} ({details['on_hand']} remaining)")
                to_order.append(item)
        
        return to_order

    def consume_daily_stack(self):
        """
        Simulates daily consumption.
        """
        logger.info("Logging daily supplement consumption...")
        for item in self.inventory:
            self.inventory[item]["on_hand"] -= 1

    def generate_order_list(self) -> Dict[str, Any]:
        needed = self.check_inventory()
        if needed:
            logger.info(f"Generating Auto-Reorder for: {needed}")
            return {"status": "ORDER_PLACED", "items": needed, "vendor": "LifeExtension/Thorne"}
        return {"status": "STOCKED", "items": []}
