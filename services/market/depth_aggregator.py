"""
Depth Aggregator Service.
Aggregates order book levels to provide liquidity insights and net volume analysis.
"""
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DepthAggregator:
    """
    Calculates aggregate metrics from level 2 order books.
    """

    @staticmethod
    def get_total_volume_at_depth(book: Dict[str, Any], pip_range: float = 0.0005) -> Dict[str, float]:
        """
        Calculate total available volume within a specific price range of the mid-price.
        
        Args:
            book: Normalized book from Level2Parser.
            pip_range: Distance from mid-price to include in volume sum.
            
        Returns:
            Dict: {'bid_volume': float, 'ask_volume': float, 'imbalance': float}
        """
        mid = book.get('mid')
        if mid is None:
            return {'bid_volume': 0.0, 'ask_volume': 0.0, 'imbalance': 0.0}

        low_bound = mid - pip_range
        high_bound = mid + pip_range

        bid_vol = sum(level['size'] for level in book['bids'] if level['price'] >= low_bound)
        ask_vol = sum(level['size'] for level in book['asks'] if level['price'] <= high_bound)

        total = bid_vol + ask_vol
        imbalance = (bid_vol - ask_vol) / total if total > 0 else 0.0

        return {
            'bid_volume': float(bid_vol),
            'ask_volume': float(ask_vol),
            'imbalance': float(imbalance)
        }

    @staticmethod
    def get_vwap_for_size(book: Dict[str, Any], size: float, direction: str) -> Optional[float]:
        """
        Calculate the Volume Weighted Average Price (VWAP) for an order of specific size.
        This provides a more accurate estimate of entry/exit price than the mid.
        """
        levels = book['asks'] if direction.upper() == 'BUY' else book['bids']
        
        accumulated_size = 0.0
        weighted_sum = 0.0
        
        for level in levels:
            remaining_needed = size - accumulated_size
            price = level['price']
            level_size = level['size']
            
            take_from_level = min(remaining_needed, level_size)
            weighted_sum += take_from_level * price
            accumulated_size += take_from_level
            
            if accumulated_size >= size:
                return weighted_sum / size
                
        # Not enough liquidity to fill the entire size
        return None
