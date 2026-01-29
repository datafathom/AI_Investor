"""
Major currency pair configurations and pip definitions.
"""
from typing import Dict, TypedDict

class PipConfig(TypedDict):
    pip_decimal_place: int
    pip_value: float
    pipette_value: float

# Standard pip configuration (most pairs)
STANDARD_PIP_CONFIG: PipConfig = {
    "pip_decimal_place": 4,
    "pip_value": 0.0001,
    "pipette_value": 0.00001
}

# JPY pip configuration
JPY_PIP_CONFIG: PipConfig = {
    "pip_decimal_place": 2,
    "pip_value": 0.01,
    "pipette_value": 0.001
}

MAJOR_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CHF", "USD/CAD", "NZD/USD"
]

def get_pair_config(pair: str) -> PipConfig:
    """
    Get pip configuration for a given currency pair.
    
    Args:
        pair: Currency pair string (e.g., "EUR/USD", "USD/JPY")
        
    Returns:
        PipConfig dictionary containing decimal place and values
    """
    if "JPY" in pair.upper():
        return JPY_PIP_CONFIG
    return STANDARD_PIP_CONFIG
