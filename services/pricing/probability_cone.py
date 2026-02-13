import logging
import math
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

class ProbabilityConeService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProbabilityConeService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

    async def get_probability_cone(self, ticker: str, current_price: float, iv: float, days: int = 30) -> Dict:
        """
        Calculate 1 and 2 standard deviation cones for specific ticker.
        IV is decimal (e.g., 0.20 for 20%).
        """
        cone_data = []
        now = datetime.now()
        
        # Daily steps
        for i in range(days + 1):
            date = now + timedelta(days=i)
            t = i / 365.0 # Time in years
            
            # Sigma = Price * IV * sqrt(t)
            sigma = current_price * iv * math.sqrt(t) if t > 0 else 0
            
            upper_1sd = current_price + sigma
            lower_1sd = current_price - sigma
            upper_2sd = current_price + (2 * sigma)
            lower_2sd = current_price - (2 * sigma)
            
            cone_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "upper_1sd": round(upper_1sd, 2),
                "lower_1sd": round(lower_1sd, 2),
                "upper_2sd": round(upper_2sd, 2),
                "lower_2sd": round(lower_2sd, 2),
                "price": current_price # Center line
            })
            
        return {
            "ticker": ticker,
            "current_price": current_price,
            "iv": iv,
            "data": cone_data
        }

    async def get_expected_move(self, ticker: str, price: float, iv: float, dte: int) -> Dict:
        """Calculate expected move for a specific expiration."""
        t = dte / 365.0
        move = price * iv * math.sqrt(t)
        
        return {
            "ticker": ticker,
            "price": price,
            "iv": iv,
            "dte": dte,
            "expected_move": round(move, 2),
            "upper_bound": round(price + move, 2),
            "lower_bound": round(price - move, 2)
        }
