"""
Velocity Calculator.
Calculates market velocity (pips per second).
"""
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class VelocityCalculator:
    """Calculates price velocity."""
    
    def __init__(self):
        self.ticks: List[Dict[str, Any]] = []
        
    def add_tick(self, price: float):
        now = datetime.now()
        self.ticks.append({"price": price, "time": now})
        # Keep last 60 seconds
        self.ticks = [t for t in self.ticks if (now - t["time"]).total_seconds() < 60]
        
    def get_velocity(self) -> float:
        if len(self.ticks) < 2:
            return 0.0
        
        start_price = self.ticks[0]["price"]
        end_price = self.ticks[-1]["price"]
        duration = (self.ticks[-1]["time"] - self.ticks[0]["time"]).total_seconds()
        
        if duration == 0:
            return 0.0
            
        return (end_price - start_price) / duration
