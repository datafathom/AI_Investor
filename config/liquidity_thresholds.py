"""
Liquidity Threshold Configuration.
Defines execution safety standards per asset class.
"""
from typing import Dict

# Min depth (total size in base currency within 10 pips of mid)
# Max spread in pips
# Min 24h volume (simulated/reporting)

LIQUIDITY_STANDARDS = {
    'MAJOR_FX': {
        'min_depth': 5_000_000,
        'max_spread_pips': 2.0,
        'min_volume_24h': 1_000_000_000
    },
    'MINOR_FX': {
        'min_depth': 1_000_000,
        'max_spread_pips': 5.0,
        'min_volume_24h': 100_000_000
    },
    'EXOTIC_FX': {
        'min_depth': 100_000,
        'max_spread_pips': 15.0,
        'min_volume_24h': 10_000_000
    }
}

ASSET_CLASS_MAPPING = {
    'EUR/USD': 'MAJOR_FX',
    'GBP/USD': 'MAJOR_FX',
    'USD/JPY': 'MAJOR_FX',
    'AUD/USD': 'MAJOR_FX',
    'USD/CAD': 'MAJOR_FX',
    'USD/CHF': 'MAJOR_FX',
    'EUR/GBP': 'MINOR_FX',
    'EUR/JPY': 'MINOR_FX',
    # Others default to MINOR or EXOTIC
}

def get_asset_standards(symbol: str) -> Dict[str, float]:
    """Retrieve standards for a specific symbol."""
    asset_class = ASSET_CLASS_MAPPING.get(symbol, 'MINOR_FX')
    return LIQUIDITY_STANDARDS[asset_class]
