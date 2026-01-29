"""
Crop Yield Forecast Model.
Predicts agricultural output based on weather inputs.
"""
import logging
from typing import str, float

logger = logging.getLogger(__name__)

class CropYieldModel:
    """Predicts commodity yield."""
    
    def predict_yield(self, commodity: str, moisture: float, temp: float) -> str:
        if moisture < 0.3:
             return "LOW_YIELD_DROUGHT"
        elif temp > 35:
             return "STRESS_WARNING"
        return "OPTIMAL"
