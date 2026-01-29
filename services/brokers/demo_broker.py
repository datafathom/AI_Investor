"""
Demo Broker Service.
Mocks a brokerage for paper trading.
"""
from decimal import Decimal
from typing import Dict, Optional, List
import uuid
import datetime

class DemoBrokerService:
    """
    Simulates a broker for demo/paper trading.
    Singleton pattern.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DemoBrokerService, cls).__new__(cls)
            cls._instance.positions = {}
            cls._instance.orders = []
            cls._instance.balance = Decimal("100000.00")
            cls._instance.equity = Decimal("100000.00")
        return cls._instance

    def execute_market_order(self, symbol: str, side: str, quantity: float, current_price: float) -> Dict:
        """
        Execute a simulated market order.
        """
        trade_id = str(uuid.uuid4())
        cost = Decimal(str(quantity)) * Decimal(str(current_price))
        
        # Simplified execution logic
        trade = {
            "id": trade_id,
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": current_price,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "FILLED"
        }
        
        # Update positions
        if symbol not in self.positions:
            self.positions[symbol] = {"quantity": 0.0, "avg_price": 0.0}
            
        pos = self.positions[symbol]
        
        if side.upper() == "BUY":
             new_qty = pos["quantity"] + quantity
             # Average price calculation (simplified)
             total_val = (pos["quantity"] * pos["avg_price"]) + (quantity * current_price)
             if new_qty > 0:
                 pos["avg_price"] = total_val / new_qty
             pos["quantity"] = new_qty
             self.balance -= cost # Subtract cost (cash)
             
        elif side.upper() == "SELL":
            pos["quantity"] -= quantity
            self.balance += cost
            
        return trade

    def get_account_summary(self) -> Dict:
        """
        Return demo account summary.
        """
        return {
            "balance": float(self.balance),
            "equity": float(self.equity), # In real impl, would update with MTM of positions
            "positions": self.positions
        }

    def reset_account(self, amount: float = 100000.00):
        """
        Reset demo account.
        """
        self.balance = Decimal(str(amount))
        self.equity = Decimal(str(amount))
        self.positions = {}
        self.orders = []
        return True
