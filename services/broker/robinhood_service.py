"""
==============================================================================
FILE: services/broker/robinhood_service.py
ROLE: Brokerage Interface
PURPOSE: Acts as the "Hands" of the system for Robinhood stock/options trading.
USAGE: Handles Auth, Balance checks, and Order Execution via robin_stocks.
INPUT/OUTPUT:
    - Input: Side/Symbol/Quantity for orders; Credentials for login.
    - Output: Order confirmation JSON or Account/Portfolio summaries.
==============================================================================
"""

import logging
try:
    import robin_stocks.robinhood as r
except ImportError:
    r = None
from typing import Dict, Any, List, Optional
from utils.core.config import get_env

logger = logging.getLogger(__name__)

class RobinhoodService:
    """
    Wrapper for Robinhood API interactions.
    """
    
    def __init__(self, mock: bool = False):
        self.username = get_env("ROBINHOOD_USERNAME")
        self.password = get_env("ROBINHOOD_PASSWORD")
        self.totp = get_env("ROBINHOOD_TOTP") # For 2FA
        self.is_logged_in = False
        self.use_mock = mock
        if self.use_mock:
            logger.info("RobinhoodService initialized in MOCK MODE.")

    def login(self) -> bool:
        """
        Authenticate with Robinhood.
        """
        if self.use_mock:
            self.is_logged_in = True
            return True

        if not self.username or not self.password:
            logger.error("Robinhood credentials missing in environment.")
            return False
            
        try:
            # Login with TOTP if available
            login_data = r.login(
                username=self.username,
                password=self.password,
                mfa_code=self.totp
            )
            self.is_logged_in = True
            logger.info("Successfully logged into Robinhood.")
            return True
        except Exception as e:
            logger.error(f"Failed to login to Robinhood: {e}")
            return False

    def get_account_profile(self) -> Dict[str, Any]:
        """Fetch general account information."""
        if self.use_mock:
            return {
                "account_number": "MOCK12345",
                "buying_power": "25000.00",
                "cash": "10000.00",
                "portfolio_cash": "15000.00"
            }
        if not self.is_logged_in:
            if not self.login(): return {}
        return r.profiles.load_account_profile()

    def get_portfolio_positions(self) -> List[Dict[str, Any]]:
        """Fetch current stock positions."""
        if self.use_mock:
            return [
                {"symbol": "TSLA", "quantity": 10, "average_buy_price": "200.00"},
                {"symbol": "NVDA", "quantity": 5, "average_buy_price": "450.00"}
            ]
        if not self.is_logged_in:
            if not self.login(): return []
        
        positions = r.account.get_all_positions()
        # Enrich with ticker symbols
        enriched_positions = []
        for pos in positions:
            instrument_url = pos.get('instrument')
            ticker = r.account.get_symbol_by_url(instrument_url)
            pos['symbol'] = ticker
            enriched_positions.append(pos)
            
        return enriched_positions

    def get_crypto_positions(self) -> List[Dict[str, Any]]:
        """Fetch current crypto positions."""
        if self.use_mock:
            return [{"symbol": "BTC", "quantity": 0.1, "average_buy_price": "40000.00"}]
        if not self.is_logged_in:
            if not self.login(): return []
        return r.crypto.get_crypto_positions()

    def place_market_order(self, symbol: str, quantity: float, side: str = "buy") -> Dict[str, Any]:
        """
        Place a market order.
        side: 'buy' or 'sell'
        """
        if self.use_mock:
            return {
                "id": "mock_order_id",
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "status": "filled",
                "price": "199.99"
            }
        if not self.is_logged_in:
            if not self.login(): return {"error": "Authentication failed"}
            
        try:
            if side.lower() == "buy":
                return r.orders.order_buy_market(symbol, quantity)
            else:
                return r.orders.order_sell_market(symbol, quantity)
        except Exception as e:
            logger.error(f"Order failed for {symbol}: {e}")
            return {"error": str(e)}

    def logout(self):
        """Terminate the session."""
        r.logout()
        self.is_logged_in = False
        logger.info("Logged out of Robinhood.")
