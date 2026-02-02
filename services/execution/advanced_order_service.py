"""
==============================================================================
FILE: services/execution/advanced_order_service.py
ROLE: Advanced Order Types Service
PURPOSE: Manages advanced order types including trailing stops, bracket orders,
         OCO/OTO orders, and conditional orders.

INTEGRATION POINTS:
    - ExecutionService: Order execution infrastructure
    - BrokerageService: Broker-specific order type support
    - MarketDataService: Real-time price monitoring
    - RiskService: Order validation
    - AdvancedOrderAPI: Order management endpoints

ORDER TYPES:
    - Trailing Stop (trailing amount or percentage)
    - Bracket Orders (entry, profit target, stop loss)
    - OCO (One-Cancels-Other)
    - OTO (One-Triggers-Other)
    - Conditional Orders (price, time, volume conditions)

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from models.orders import (
    TrailingStopOrder, BracketOrder, ConditionalOrder,
    OrderType, OrderStatus
)
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class AdvancedOrderService:
    """
    Service for advanced order types management.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        self.active_orders: Dict[str, Dict] = {}
        
    async def create_trailing_stop(
        self,
        user_id: str,
        symbol: str,
        quantity: int,
        trailing_type: str,
        trailing_value: float,
        initial_stop_price: Optional[float] = None
    ) -> TrailingStopOrder:
        """
        Create trailing stop order.
        
        Args:
            user_id: User identifier
            symbol: Stock symbol
            quantity: Number of shares
            trailing_type: "amount" or "percentage"
            trailing_value: Trailing amount or percentage
            initial_stop_price: Optional initial stop price
            
        Returns:
            TrailingStopOrder object
        """
        logger.info(f"Creating trailing stop for {symbol}")
        
        order = TrailingStopOrder(
            order_id=f"trail_{user_id}_{datetime.now(timezone.utc).timestamp()}",
            symbol=symbol,
            quantity=quantity,
            trailing_type=trailing_type,
            trailing_value=trailing_value,
            initial_stop_price=initial_stop_price,
            current_stop_price=initial_stop_price,
            highest_price=initial_stop_price
        )
        
        # Save order
        await self._save_order(order.order_id, order.model_dump())
        self.active_orders[order.order_id] = order.model_dump()
        
        return order
    
    async def create_bracket_order(
        self,
        user_id: str,
        symbol: str,
        quantity: int,
        entry_price: float,
        profit_target_price: Optional[float] = None,
        stop_loss_price: Optional[float] = None
    ) -> BracketOrder:
        """
        Create bracket order with entry, profit target, and stop loss.
        
        Args:
            user_id: User identifier
            symbol: Stock symbol
            quantity: Number of shares
            entry_price: Entry price
            profit_target_price: Optional profit target price
            stop_loss_price: Optional stop loss price
            
        Returns:
            BracketOrder object
        """
        logger.info(f"Creating bracket order for {symbol}")
        
        entry_order_id = f"entry_{user_id}_{datetime.now(timezone.utc).timestamp()}"
        profit_target_order_id = f"profit_{user_id}_{datetime.now(timezone.utc).timestamp()}" if profit_target_price else None
        stop_loss_order_id = f"stop_{user_id}_{datetime.now(timezone.utc).timestamp()}" if stop_loss_price else None
        
        bracket = BracketOrder(
            bracket_id=f"bracket_{user_id}_{datetime.now(timezone.utc).timestamp()}",
            entry_order_id=entry_order_id,
            profit_target_order_id=profit_target_order_id,
            stop_loss_order_id=stop_loss_order_id,
            profit_target_price=profit_target_price,
            stop_loss_price=stop_loss_price
        )
        
        # Save bracket order
        await self._save_order(bracket.bracket_id, bracket.model_dump())
        
        return bracket
    
    async def create_oco_order(
        self,
        user_id: str,
        symbol: str,
        quantity: int,
        order1: Dict,
        order2: Dict
    ) -> Dict:
        """
        Create One-Cancels-Other (OCO) order.
        
        Args:
            user_id: User identifier
            symbol: Stock symbol
            quantity: Number of shares
            order1: First order definition
            order2: Second order definition
            
        Returns:
            OCO order dictionary
        """
        logger.info(f"Creating OCO order for {symbol}")
        
        oco_id = f"oco_{user_id}_{datetime.now(timezone.utc).timestamp()}"
        
        oco_order = {
            "oco_id": oco_id,
            "symbol": symbol,
            "quantity": quantity,
            "order1": order1,
            "order2": order2,
            "status": "pending",
            "created_date": datetime.now(timezone.utc).isoformat()
        }
        
        # Save OCO order
        await self._save_order(oco_id, oco_order)
        
        return oco_order
    
    async def create_conditional_order(
        self,
        user_id: str,
        symbol: str,
        quantity: int,
        order_type: str,
        condition_type: str,
        condition_value: float
    ) -> ConditionalOrder:
        """
        Create conditional order with trigger.
        
        Args:
            user_id: User identifier
            symbol: Stock symbol
            quantity: Number of shares
            order_type: Order type (market, limit, etc.)
            condition_type: Condition type (price, time, volume)
            condition_value: Condition trigger value
            
        Returns:
            ConditionalOrder object
        """
        logger.info(f"Creating conditional order for {symbol}")
        
        order = ConditionalOrder(
            order_id=f"cond_{user_id}_{datetime.now(timezone.utc).timestamp()}",
            symbol=symbol,
            quantity=quantity,
            order_type=order_type,
            condition_type=condition_type,
            condition_value=condition_value,
            triggered=False
        )
        
        # Save conditional order
        await self._save_order(order.order_id, order.model_dump())
        
        return order
    
    async def update_trailing_stop(
        self,
        order_id: str,
        current_price: float
    ) -> TrailingStopOrder:
        """
        Update trailing stop based on current price.
        
        Args:
            order_id: Trailing stop order ID
            current_price: Current market price
            
        Returns:
            Updated TrailingStopOrder
        """
        order_data = self.active_orders.get(order_id)
        if not order_data:
            raise ValueError(f"Order {order_id} not found")
        
        order = TrailingStopOrder(**order_data)
        
        # Update highest price
        if order.highest_price is None or current_price > order.highest_price:
            order.highest_price = current_price
        
        # Calculate new stop price
        if order.trailing_type == "amount":
            new_stop = order.highest_price - order.trailing_value
        else:  # percentage
            new_stop = order.highest_price * (1 - order.trailing_value / 100.0)
        
        # Only move stop up, never down
        if order.current_stop_price is None or new_stop > order.current_stop_price:
            order.current_stop_price = new_stop
        
        # Update stored order
        self.active_orders[order_id] = order.model_dump()
        await self._save_order(order_id, order.model_dump())
        
        return order
    
    async def _save_order(self, order_id: str, order_data: Dict):
        """Save order to cache."""
        cache_key = f"order:{order_id}"
        self.cache_service.set(cache_key, order_data, ttl=86400 * 7)  # 7 days


# Singleton instance
_advanced_order_service: Optional[AdvancedOrderService] = None


def get_advanced_order_service() -> AdvancedOrderService:
    """Get singleton advanced order service instance."""
    global _advanced_order_service
    if _advanced_order_service is None:
        _advanced_order_service = AdvancedOrderService()
    return _advanced_order_service
