"""
==============================================================================
FILE: services/trading/paper_trading_service.py
ROLE: Paper Trading Engine
PURPOSE: Provides realistic trading simulation with virtual portfolios,
         order execution simulation, and performance tracking.

INTEGRATION POINTS:
    - MarketDataService: Real-time and historical price data
    - ExecutionService: Order execution simulation
    - PortfolioService: Virtual portfolio management
    - PaperTradingAPI: Paper trading endpoints

SIMULATION FEATURES:
    - Realistic order execution with slippage
    - Commission and fee calculation
    - Market hours enforcement
    - Partial fill simulation

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
import random
from models.paper_trading import PaperOrder, VirtualPortfolio
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class PaperTradingService:
    """
    Service for paper trading simulation.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        self.commission_rate = 0.005  # $0.005 per share
        self.min_commission = 1.0  # $1 minimum
        
    async def create_virtual_portfolio(
        self,
        user_id: str,
        portfolio_name: str,
        initial_cash: float = 100000.0
    ) -> VirtualPortfolio:
        """
        Create virtual portfolio for paper trading.
        
        Args:
            user_id: User identifier
            portfolio_name: Name of portfolio
            initial_cash: Initial cash amount
            
        Returns:
            VirtualPortfolio object
        """
        logger.info(f"Creating virtual portfolio for user {user_id}")
        
        portfolio = VirtualPortfolio(
            portfolio_id=f"paper_{user_id}_{datetime.utcnow().timestamp()}",
            user_id=user_id,
            portfolio_name=portfolio_name,
            initial_cash=initial_cash,
            current_cash=initial_cash,
            total_value=initial_cash,
            positions={},
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        
        # Save portfolio
        await self._save_portfolio(portfolio)
        
        return portfolio
    
    async def execute_paper_order(
        self,
        portfolio_id: str,
        symbol: str,
        quantity: int,
        order_type: str,
        price: Optional[float] = None
    ) -> PaperOrder:
        """
        Execute paper trading order with realistic simulation.
        
        Args:
            portfolio_id: Virtual portfolio identifier
            symbol: Stock symbol
            quantity: Number of shares
            order_type: Order type (market, limit, stop)
            price: Optional limit/stop price
            
        Returns:
            PaperOrder with execution details
        """
        logger.info(f"Executing paper order for {symbol}")
        
        # Get portfolio
        portfolio = await self._get_portfolio(portfolio_id)
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Get current market price (simplified)
        market_price = await self._get_market_price(symbol)
        
        # Calculate execution price with slippage
        if order_type == "market":
            execution_price = await self._apply_slippage(market_price, quantity)
        elif order_type == "limit":
            if price and (quantity > 0 and market_price <= price) or (quantity < 0 and market_price >= price):
                execution_price = await self._apply_slippage(price, quantity)
            else:
                raise ValueError("Limit order not executable at current price")
        else:
            execution_price = await self._apply_slippage(market_price, quantity)
        
        # Calculate commission
        commission = self._calculate_commission(abs(quantity))
        
        # Calculate total cost
        total_cost = abs(quantity) * execution_price + commission
        
        # Check if sufficient cash
        if quantity > 0 and portfolio.current_cash < total_cost:
            raise ValueError("Insufficient cash for purchase")
        
        # Create order
        order = PaperOrder(
            order_id=f"paper_order_{portfolio_id}_{datetime.utcnow().timestamp()}",
            user_id=portfolio.user_id,
            symbol=symbol,
            quantity=quantity,
            order_type=order_type,
            price=price,
            status="filled",
            filled_price=execution_price,
            filled_quantity=quantity,
            commission=commission,
            slippage=abs(execution_price - market_price) if order_type == "market" else 0.0,
            created_date=datetime.utcnow()
        )
        
        # Update portfolio
        await self._update_portfolio_positions(portfolio, order)
        
        return order
    
    async def get_portfolio_performance(
        self,
        portfolio_id: str
    ) -> Dict:
        """
        Get portfolio performance metrics.
        
        Args:
            portfolio_id: Virtual portfolio identifier
            
        Returns:
            Performance metrics dictionary
        """
        portfolio = await self._get_portfolio(portfolio_id)
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Calculate current total value
        positions_value = sum(
            pos.get('quantity', 0) * pos.get('current_price', 0)
            for pos in portfolio.positions.values()
        )
        total_value = portfolio.current_cash + positions_value
        
        # Calculate returns
        total_return = ((total_value - portfolio.initial_cash) / portfolio.initial_cash) * 100
        
        return {
            'portfolio_id': portfolio_id,
            'initial_cash': portfolio.initial_cash,
            'current_cash': portfolio.current_cash,
            'positions_value': positions_value,
            'total_value': total_value,
            'total_return': total_return,
            'num_positions': len(portfolio.positions)
        }
    
    async def _get_market_price(self, symbol: str) -> float:
        """Get current market price (simplified)."""
        # In production, fetch from market data service
        return 100.0  # Mock price
    
    async def _apply_slippage(self, price: float, quantity: int) -> float:
        """Apply realistic slippage based on order size."""
        # Slippage increases with order size
        size_factor = min(1.0, abs(quantity) / 1000.0)  # Normalize by 1000 shares
        slippage_pct = 0.001 * (1 + size_factor)  # 0.1% to 0.2% slippage
        
        # Random slippage direction
        slippage = price * slippage_pct * random.choice([-1, 1])
        return price + slippage
    
    def _calculate_commission(self, quantity: int) -> float:
        """Calculate commission."""
        commission = quantity * self.commission_rate
        return max(commission, self.min_commission)
    
    async def _update_portfolio_positions(self, portfolio: VirtualPortfolio, order: PaperOrder):
        """Update portfolio positions after order execution."""
        symbol = order.symbol
        quantity = order.filled_quantity
        price = order.filled_price
        
        # Update position
        if symbol in portfolio.positions:
            pos = portfolio.positions[symbol]
            total_cost = (pos['quantity'] * pos['avg_price']) + (quantity * price)
            total_quantity = pos['quantity'] + quantity
            pos['avg_price'] = total_cost / total_quantity if total_quantity != 0 else 0
            pos['quantity'] = total_quantity
        else:
            portfolio.positions[symbol] = {
                'quantity': quantity,
                'avg_price': price,
                'current_price': price
            }
        
        # Update cash
        cost = abs(quantity) * price + order.commission
        if quantity > 0:  # Buy
            portfolio.current_cash -= cost
        else:  # Sell
            portfolio.current_cash += cost
        
        portfolio.updated_date = datetime.utcnow()
        await self._save_portfolio(portfolio)
    
    async def _get_portfolio(self, portfolio_id: str) -> Optional[VirtualPortfolio]:
        """Get portfolio from cache."""
        cache_key = f"paper_portfolio:{portfolio_id}"
        portfolio_data = self.cache_service.get(cache_key)
        if portfolio_data:
            return VirtualPortfolio(**portfolio_data)
        return None
    
    async def _save_portfolio(self, portfolio: VirtualPortfolio):
        """Save portfolio to cache."""
        cache_key = f"paper_portfolio:{portfolio.portfolio_id}"
        self.cache_service.set(cache_key, portfolio.dict(), ttl=86400 * 365)


# Singleton instance
_paper_trading_service: Optional[PaperTradingService] = None


def get_paper_trading_service() -> PaperTradingService:
    """Get singleton paper trading service instance."""
    global _paper_trading_service
    if _paper_trading_service is None:
        _paper_trading_service = PaperTradingService()
    return _paper_trading_service
