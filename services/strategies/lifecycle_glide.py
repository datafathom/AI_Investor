"""
Lifecycle Leverage Glide Path.
Structural deleveraging based on investor age.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LifecycleGlide:
    """Calculates age-appropriate leverage ratio."""
    
    def get_target_leverage(self, age: int) -> float:
        if age < 30: return 2.0
        elif age >= 65: return 1.0
        
        # Linear glide from 2.0 to 1.0
        glide = 2.0 - (age - 30) * (1.0 / 35)
        return round(glide, 2)
