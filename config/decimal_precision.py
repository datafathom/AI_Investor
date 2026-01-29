"""
Decimal Precision Configuration.
Defines pricing standards for FX Major, Minor, and Cross pairs.
"""
from typing import Dict, Any

# Precision Mapping: (Total Decimals, Pip Position)
# EUR/USD: 1.08505 -> 5 decimals, Pip is 0.0001 (4th)
# USD/JPY: 149.505 -> 3 decimals, Pip is 0.01 (2nd)

PRECISION_STANDARDS: Dict[str, Dict[str, int]] = {
    'DEFAULT': {
        'decimals': 5,
        'pip_position': 4
    },
    'JPY_PAIRS': {
        'decimals': 3,
        'pip_position': 2
    },
    'EQUITIES': {
        'decimals': 2,
        'pip_position': 2
    },
    'CRYPTO': {
        'decimals': 8,
        'pip_position': 2 # Varies, usually Satoshi level
    }
}

SYMBOL_OVERRIDE: Dict[str, str] = {
    'USD/JPY': 'JPY_PAIRS',
    'EUR/JPY': 'JPY_PAIRS',
    'GBP/JPY': 'JPY_PAIRS',
    'AUD/JPY': 'JPY_PAIRS',
    'BTC/USD': 'CRYPTO',
    'ETH/USD': 'CRYPTO'
}

def get_precision_config(symbol: str) -> Dict[str, int]:
    """Retrieve decimal config for a specific symbol."""
    category = SYMBOL_OVERRIDE.get(symbol, 'DEFAULT')
    return PRECISION_STANDARDS[category]
