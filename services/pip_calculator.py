"""
Service for calculating pip and pipette differences for currency pairs.
"""
from decimal import Decimal
from typing import Optional

from config.currency_pairs import get_pair_config
from utils.decimal_handler import to_decimal, decimal_sub, decimal_div

class PipCalculatorService:
    """
    High-precision engine for measuring market movement in pips and pipettes.
    Singleton pattern compliant.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PipCalculatorService, cls).__new__(cls)
        return cls._instance

    def calculate_pips(self, price1: float | str | Decimal, price2: float | str | Decimal, pair: str) -> float:
        """
        Calculate the difference in pips between two prices.
        
        Args:
            price1: Starting price
            price2: Ending price
            pair: Currency pair symbol (e.g., "EUR/USD")
            
        Returns:
            Float representing the difference in pips. 
            Positive means price2 > price1.
            
        Example:
            EUR/USD: 1.09500 -> 1.09520 = 2.0 pips
        """
        p1 = to_decimal(price1)
        p2 = to_decimal(price2)
        
        config = get_pair_config(pair)
        pip_value = to_decimal(config["pip_value"])
        
        diff = decimal_sub(p2, p1)
        pips = decimal_div(diff, pip_value)
        
        return float(pips)

    def calculate_pipettes(self, price1: float | str | Decimal, price2: float | str | Decimal, pair: str) -> float:
        """
        Calculate the difference in pipettes between two prices.
        1 pipette = 0.1 pip.
        
        Args:
            price1: Starting price
            price2: Ending price
            pair: Currency pair symbol
            
        Returns:
            Float representing the difference in pipettes.
        """
        p1 = to_decimal(price1)
        p2 = to_decimal(price2)
        
        config = get_pair_config(pair)
        pipette_value = to_decimal(config["pipette_value"])
        
        diff = decimal_sub(p2, p1)
        pipettes = decimal_div(diff, pipette_value)
        
        return float(pipettes)
