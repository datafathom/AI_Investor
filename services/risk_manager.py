"""
Risk Manager Service.
Centralizes risk calculations and enforcement.
"""
from decimal import Decimal
from typing import Dict, Optional

class RiskManager:
    """
    Risk Manager Logic.
    Enforces PD-001 (1% Risk) and PD-002 (3% Portfolio Freeze).
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RiskManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
        self.daily_loss = Decimal("0.00")
        self.max_daily_loss_pct = Decimal("0.03") # 3%
        self.max_position_risk_pct = Decimal("0.01") # 1%
        self.initialized = True

    def check_trade_risk(self, account_balance: float, risk_amount: float) -> bool:
        """
        Check if a single trade violates the 1% rule.
        """
        balance = Decimal(str(account_balance))
        risk = Decimal(str(risk_amount))
        
        max_allowed_risk = balance * self.max_position_risk_pct
        
        if risk > max_allowed_risk:
            return False # Reject
        return True

    def check_portfolio_freeze(self, account_balance: float, current_daily_loss: float) -> bool:
        """
        Check if the portfolio should be frozen due to daily drawdown.
        """
        balance = Decimal(str(account_balance))
        daily_loss = Decimal(str(current_daily_loss))
        
        max_loss = balance * self.max_daily_loss_pct
        
        if daily_loss >= max_loss:
            return True # Freeze
        return False
