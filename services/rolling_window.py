"""
Rolling Window Service.
Maintains a sliding window of price data for multiple symbols.
"""
from collections import deque
from typing import Dict, List, Optional


class RollingWindowService:
    """
    Manages sliding windows of price data for asset correlation analysis.
    Supports fixed-size buffers per symbol.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RollingWindowService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, window_size: int = 288):
        """
        Initialize the RollingWindowService.
        
        Args:
            window_size: Maximum number of price points to retain per symbol.
        """
        if getattr(self, 'initialized', False):
            return
        self.window_size = window_size
        self.buffers: Dict[str, deque] = {}
        self.initialized = True

    def add_price(self, symbol: str, price: float):
        """
        Add a new price point to the symbol's buffer.
        
        Args:
            symbol: Asset symbol (e.g., 'EUR/USD').
            price: New price data point.
        """
        if symbol not in self.buffers:
            self.buffers[symbol] = deque(maxlen=self.window_size)

        self.buffers[symbol].append(float(price))

    def get_history(self, symbol: str) -> List[float]:
        """Retrieve the historical price buffer for a symbol."""
        if symbol not in self.buffers:
            return []
        return list(self.buffers[symbol])

    def clear(self, symbol: Optional[str] = None):
        """Clear buffers."""
        if symbol:
            if symbol in self.buffers:
                self.buffers[symbol].clear()
        else:
            self.buffers.clear()

# Global Singleton
rolling_window_service = RollingWindowService()
