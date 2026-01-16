"""
==============================================================================
FILE: services/execution/paper_exchange.py
ROLE: Simulated Stock Exchange
PURPOSE:
    Execute trades in a virtual environment to validate strategies 
    without risking real capital.
    
    Features:
    - Cash Balance Tracking
    - Portfolio Positions Tracking
    - Order Execution (Market Orders)
    - Slippage Simulation (Optional)
    - Commission Simulation
    
ROADMAP: Phase 23 - Paper Trading Simulator
==============================================================================
"""

import logging
from typing import Dict, Any, List
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class PaperExchange:
    def __init__(self, initial_cash: float = 100000.0):
        self.cash = initial_cash
        self.positions: Dict[str, Dict[str, Any]] = {} # {'AAPL': {'quantity': 10, 'avg_price': 150.0}}
        self.orders: List[Dict[str, Any]] = []
        self.COMMISSION_RATE = 0.0 # $0 simulated commissions for now
        
    def get_account_summary(self) -> Dict[str, Any]:
        """
        Return current account state.
        """
        return {
            "cash": self.cash,
            "positions": self.positions
        }
        
    def submit_market_order(self, 
                          symbol: str, 
                          quantity: int, 
                          side: str, 
                          current_price: float) -> Dict[str, Any]:
        """
        Execute a Market Order immediately at 'current_price'.
        Args:
            side: 'BUY' or 'SELL'
        """
        if quantity <= 0:
            return {"status": "REJECTED", "reason": "Quantity must be > 0"}
            
        cost = quantity * current_price
        
        # BUY Logic
        if side == "BUY":
            if cost > self.cash:
                logger.warning(f"PAPER TRADE REJECTED: Insufficient Funds. Need ${cost}, have ${self.cash}")
                return {"status": "REJECTED", "reason": "Insufficient Funds"}
                
            self.cash -= cost
            
            # Update Position
            if symbol not in self.positions:
                self.positions[symbol] = {'quantity': 0, 'avg_price': 0.0}
                
            pos = self.positions[symbol]
            old_qty = pos['quantity']
            new_qty = old_qty + quantity
            
            # Weighted Average Price
            old_cost = old_qty * pos['avg_price']
            new_cost = old_cost + cost
            pos['avg_price'] = new_cost / new_qty
            pos['quantity'] = new_qty
            
        # SELL Logic
        elif side == "SELL":
            if symbol not in self.positions or self.positions[symbol]['quantity'] < quantity:
                logger.warning(f"PAPER TRADE REJECTED: Insufficient Position. Have {self.positions.get(symbol, {}).get('quantity',0)}, need {quantity}")
                return {"status": "REJECTED", "reason": "Insufficient Position"}
                
            self.cash += cost
            
            # Update Position
            self.positions[symbol]['quantity'] -= quantity
            if self.positions[symbol]['quantity'] == 0:
                del self.positions[symbol]
                
        else:
            return {"status": "REJECTED", "reason": "Invalid Side"}
            
        # Record Order
        order = {
            "id": str(uuid.uuid4()),
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": current_price,
            "timestamp": datetime.now().isoformat(),
            "status": "FILLED"
        }
        self.orders.append(order)
        logger.info(f"PAPER TRADE EXECUTED: {side} {quantity} {symbol} @ ${current_price:.2f}")
        
        return order

# Singleton
_instance = None

def get_paper_exchange() -> PaperExchange:
    global _instance
    if _instance is None:
        _instance = PaperExchange()
    return _instance
