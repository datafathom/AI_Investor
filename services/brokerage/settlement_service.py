
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SettlementService:
    """
    Service for managing multi-currency settlements and FX conversions.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettlementService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Default reporting currency
        self._base_currency = "USD"
        
        # Simulated balances
        self._balances = {
            "USD": 50000.00,
            "EUR": 12000.00,
            "JPY": 1500000.00,
            "GBP": 5000.00
        }
        
        # Simulated FX rates (relative to 1 USD)
        self._rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "JPY": 145.0,
            "GBP": 0.78,
            "CAD": 1.35
        }

    def get_rates(self) -> Dict[str, float]:
        """
        Returns live FX conversion rates.
        """
        # In a real app, this would fetch from an API and cache.
        return self._rates

    def convert_currency(self, from_currency: str, to_currency: str, amount: float) -> Dict[str, Any]:
        """
        Executes a simulated currency conversion.
        """
        from_rate = self._rates.get(from_currency)
        to_rate = self._rates.get(to_currency)
        
        if not from_rate or not to_rate:
            return {"status": "ERROR", "message": "Unsupported currency"}
            
        if self._balances.get(from_currency, 0) < amount:
            return {"status": "ERROR", "message": "Insufficient funds"}

        # Calculate conversion
        usd_value = amount / from_rate
        result_amount = usd_value * to_rate
        
        # Perform "Trade"
        self._balances[from_currency] -= amount
        self._balances[to_currency] = self._balances.get(to_currency, 0) + result_amount
        
        logger.info(f"FX Trade: {amount} {from_currency} -> {result_amount:.2f} {to_currency}")
        
        return {
            "status": "SUCCESS",
            "from": from_currency,
            "to": to_currency,
            "amount_sold": amount,
            "amount_bought": round(result_amount, 2),
            "rate": round(to_rate / from_rate, 4),
            "timestamp": datetime.now().isoformat()
        }

    def get_balance_summary(self) -> Dict[str, Any]:
        """
        Returns consolidated balance in reporting currency.
        """
        total_usd = 0
        breakdown = []
        
        for curr, bal in self._balances.items():
            rate = self._rates.get(curr, 1.0)
            usd_val = bal / rate
            total_usd += usd_val
            breakdown.append({
                "currency": curr,
                "balance": round(bal, 2),
                "usd_value": round(usd_val, 2),
                "is_base": curr == self._base_currency
            })
            
        return {
            "base_currency": self._base_currency,
            "total_equity_usd": round(total_usd, 2),
            "balances": breakdown,
            "timestamp": datetime.now().isoformat()
        }

def get_settlement_service():
    return SettlementService()
