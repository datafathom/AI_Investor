import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TradeAggregator:
    """
    Phase 162.2: MFO Block Trade Aggregation.
    Bundles individual family orders into a single block to reduce slippage 
    and ensure fair allocation of fills.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TradeAggregator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("TradeAggregator initialized")

    def aggregate_orders(self, ticker: str, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregates multiple family orders into a single block order.
        """
        if not orders:
            return {}

        total_quantity = sum(order.get('quantity', 0) for order in orders)
        order_ids = [order.get('id', 'unknown') for order in orders]
        
        logger.info(f"MFO_LOG: Aggregated {len(orders)} orders for {ticker} into block of {total_quantity} shares.")
        
        return {
            "block_id": f"BLK-{ticker}-{len(orders)}",
            "ticker": ticker,
            "total_quantity": total_quantity,
            "constituent_orders": order_ids,
            "status": "AGGREGATED"
        }

    def allocate_fill(self, block_id: str, filled_quantity: int, original_orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Pro-rata allocation of a partial fill.
        """
        total_requested = sum(o.get('quantity', 0) for o in original_orders)
        fill_ratio = Decimal(str(filled_quantity)) / Decimal(str(total_requested))
        
        allocations = []
        for order in original_orders:
            allocated = int(Decimal(str(order.get('quantity', 0))) * fill_ratio)
            allocations.append({
                "family_id": order.get('family_id'),
                "allocated_quantity": allocated,
                "residual": order.get('quantity', 0) - allocated
            })
            
        logger.info(f"MFO_LOG: Allocated {filled_quantity} shares for block {block_id} pro-rata.")
        return allocations
