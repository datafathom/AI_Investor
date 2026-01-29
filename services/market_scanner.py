"""
Market Scanner Service.
Fetches real-time (or simulated) price data for market scanning.
"""
from typing import Dict, List, Optional
import random
from decimal import Decimal
from config.currency_pairs import MAJOR_PAIRS

class MarketScannerService:
    """
    Scans the market for price data.
    Singleton pattern.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MarketScannerService, cls).__new__(cls)
        return cls._instance

    def scan_major_pairs(self) -> Dict[str, Dict]:
        """
        Fetch current price data for all Major Pairs.
        In a real scenario, this would call a data provider.
        Here we return simulated data for the 'Hunter' to analyze.
        """
        market_snapshot = {}
        
        for pair in MAJOR_PAIRS:
            # Simulate subtle price movements
            base_price = 1.0850 if "EUR" in pair else 1.2700 if "GBP" in pair else 149.00
            if "JPY" in pair: # Adjust simulation for JPY
                base_price = 149.00
                
            current_price = base_price + (random.uniform(-0.05, 0.05))
            
            market_snapshot[pair] = {
                "symbol": pair,
                "price": round(current_price, 5),
                "volume": random.randint(1000, 50000),
                "timestamp": "now" # In real app, use datetime
            }
            
        return market_snapshot
